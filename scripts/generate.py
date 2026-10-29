import os
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "stl")
os.makedirs(OUT, exist_ok=True)
import trimesh, numpy as np
from trimesh.creation import box, cylinder, icosphere
from trimesh.convex import convex_hull

# ---------------- parameters (mm) ----------------
cell_t, cell_w = 8.5, 14.5
pt, pw = cell_t+0.5, cell_w+0.5            # pocket 9.0 x 15.0
div, floor_t, depth = 1.2, 1.6, 36.0
nx, ny = 4, 3
side, back, front = 3.5, 3.0, 6.0          # outer margins around the pocket grid
RC = 7.0                                   # vertical corner radius
GX, GY = nx*pt+(nx-1)*div, ny*pw+(ny-1)*div
X, Y = GX+2*side, GY+front+back
H = floor_t+depth                          # seam height
headroom, skin = 3.0, 2.6
LH = headroom+skin                         # lid height
RB, RT, CH = 2.5, 3.0, 0.5                 # bottom fillet, lid top fillet, seam chamfer
R = 3.5                                    # hinge barrel radius
ay, az = Y+R+0.3, H                        # hinge axis sits on the seam
mag_d, mag_h = 4.2, 2.1                    # 4 x 2 mm neodymium disc magnets
pin_d = 1.75

def b(x0,y0,z0,x1,y1,z1):
    m = box(extents=[x1-x0,y1-y0,z1-z0]); m.apply_translation([(x0+x1)/2,(y0+y1)/2,(z0+z1)/2]); return m
def rrect(d, z, n=24):
    w,h = X-2*d, Y-2*d; r = max(RC-d,0.05); pts=[]
    for cx_,cy_,a0 in ((r,r,180),(w-r,r,270),(w-r,h-r,0),(r,h-r,90)):
        for a in np.linspace(a0,a0+90,n):
            pts.append((d+cx_+r*np.cos(np.radians(a)), d+cy_+r*np.sin(np.radians(a)), z))
    return pts
def hull_stack(secs): return convex_hull(np.array([p for d,z in secs for p in rrect(d,z)]))
def vcyl(x,y,z0,z1,r):
    c = cylinder(radius=r,height=z1-z0,sections=48); c.apply_translation([x,y,(z0+z1)/2]); return c
def xcyl(x0,x1,r,y,z,s=48):
    c = cylinder(radius=r,height=x1-x0,sections=s)
    c.apply_transform(trimesh.transformations.rotation_matrix(np.pi/2,[0,1,0]))
    c.apply_translation([(x0+x1)/2,y,z]); return c
def barrel(x0,x1,ch=0.35):                 # chamfered-end barrel segment
    pts=[]
    for xx,rr in ((x0,R-ch),(x0+ch,R),(x1-ch,R),(x1,R-ch)):
        for a in np.linspace(0,2*np.pi,48,endpoint=False):
            pts.append((xx, ay+rr*np.cos(a), az+rr*np.sin(a)))
    return convex_hull(np.array(pts))
def wedge(x0,x1,prof):
    return convex_hull(np.array([(x,y,z) for x in (x0,x1) for y,z in prof]))

# ================= BOX =================
secs=[]
for a in np.linspace(0,90,14):             # bottom fillet
    secs.append((RB-RB*np.sin(np.radians(a)), RB-RB*np.cos(np.radians(a))))
secs += [(0,H-CH),(CH,H)]                  # seam chamfer
body = hull_stack(secs)

cuts=[]
for i in range(nx):
    for j in range(ny):
        x = side+i*(pt+div); y = front+j*(pw+div)
        cuts.append(b(x,y,floor_t,x+pt,y+pw,H+1))
        cuts.append(vcyl(x+pt/2,y+pw/2,-1,floor_t+1,3.0))       # vent / push-out holes
for i in range(nx):                         # fingertip slots across row dividers
    xc = side+i*(pt+div)+pt/2
    cuts.append(b(xc-2.5,front,H-4,xc+2.5,front+GY,H+1))
for sx in (-12,12):                         # magnet pockets
    cuts.append(vcyl(X/2+sx,3.0,H-mag_h,H+1,mag_d/2))
sc = icosphere(subdivisions=4,radius=9.0); sc.apply_translation([X/2,-4.0,H+4.0]); cuts.append(sc)  # thumb scoop
body = body.difference(cuts, engine='manifold')

xs = RC; xe = X-RC; gap=0.4
lbox = 9.0; llid = (xe-xs)-2*lbox-2*gap
seg_box = [(xs,xs+lbox),(xe-lbox,xe)]
seg_lid = [(xs+lbox+gap, xe-lbox-gap)]
kn=[]
for x0,x1 in seg_box:
    kn += [barrel(x0,x1), b(x0,Y-0.6,H-R,x1,ay,H+0.0),
           wedge(x0,x1,[(Y-0.6,H-R),(ay,H-R),(Y-0.6,H-R-(ay-Y)-0.6)])]
body = body.union(kn, engine='manifold')
body = body.difference(xcyl(xs-1,xe-1.5,(pin_d+0.15)/2,ay,az,32), engine='manifold')

# ================= LID =================
secs=[(CH,H),(0,H+CH),(0,H+LH-RT)]
for a in np.linspace(0,90,14):
    secs.append((RT-RT*np.cos(np.radians(a)), H+LH-RT+RT*np.sin(np.radians(a))))
lid = hull_stack(secs)
lid = lid.difference([b(side,front,H-0.01,X-side,Y-back,H+headroom)] +
                     [vcyl(X/2+sx,3.0,H-1,H+mag_h,mag_d/2) for sx in (-12,12)], engine='manifold')
kn=[]
for x0,x1 in seg_lid:
    kn += [barrel(x0,x1), b(x0,Y-1.0,H,x1,ay,H+R)]
lid = lid.union(kn, engine='manifold')
lid = lid.difference(xcyl(xs-1,xe+1,(pin_d+0.45)/2,ay,az,32), engine='manifold')

# ---------------- checks / export ----------------
print('closed overlap vol:', round(body.intersection(lid,engine='manifold').volume,3))
for ang in (10,30,60,90,110):
    l = lid.copy(); l.apply_transform(trimesh.transformations.rotation_matrix(np.radians(-ang),[1,0,0],point=[0,ay,az]))
    print(ang,'deg overlap:', round(body.intersection(l,engine='manifold').volume,3))
body.export(OUT+'/wizard_lipo_battery_storage_base.stl')
lid.export(OUT+'/wizard_lipo_battery_storage_lid.stl')
for n,m in (('base',body),('lid',lid)): print(n,m.is_watertight,np.round(m.bounds[1]-m.bounds[0],1))
print('pin: %.1f mm of 1.75 mm filament'%(xe-xs-2.5))
