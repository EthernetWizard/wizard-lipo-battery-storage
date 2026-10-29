# Wizard Lipo Battery Storage

A compact, 3D-printable storage box for 12 × LP801437 pouch cells (3.7 V, 350 mAh, ~8.5 × 14.5 × 38 mm worst case).
Cells stand on end, tabs up, each in its own pocket so they never touch each other.
Rounded block styling, a thin seam line, a cylindrical spine hinge and a hidden magnetic latch.

## Files

- `stl/wizard_lipo_battery_storage_base.stl`
- `stl/wizard_lipo_battery_storage_lid.stl`
- `scripts/generate.py` – parametric generator (Python + trimesh)

## Specs

- Base: 46.6 × 56.4 × 37.6 mm (about 46.6 × 63.7 × 43.2 mm closed, including hinge spine and lid)
- Pockets: 12 in a 4 × 3 grid, 9.0 × 15.0 mm, 36 mm deep, 1.2 mm dividers
- 6 mm vent/push-out hole in each pocket floor
- Hinge pin: ~30 mm of **1.75 mm filament**
- Latch: **2 × 4 × 2 mm neodymium disc magnets** (one in the base lip, one in the lid, matching positions)

## Assembly

1. Press-fit/glue the magnets into the pockets at the front of the base and lid. Test polarity first so they attract.
2. Hold the lid at ~90° so the centre knuckle sits between the two base knuckles.
3. Push the filament pin in from the open (left) end until it stops, then melt a small blob on the end (or add a drop of glue).
4. If it binds, ream the hinge holes with a 2 mm drill bit.

## Print settings

- Material: PETG (or ABS/ASA). Avoid PLA if the box will sit somewhere warm.
- Layer height 0.08–0.2 mm, 3+ perimeters, 15–20 % infill.
- **Base:** floor-down, no supports (the hinge has a built-in 45° gusset).
- **Lid:** upside-down (rounded top on the bed). Ironing on the top surface gives a smooth finish. A brim or light support under the hinge barrel can help.
- For a premium finish: sand 400 → 800 grit, filler primer, satin/gloss spray.

## Regenerating / customising

```bash
pip install -r requirements.txt
python scripts/generate.py      # writes to stl/
```

Edit the parameters at the top of the script (cell size, clearance, corner radius, magnet size, etc.).

## Battery safety

- Store cells at roughly 3.8 V (40–60 % charge) in a cool, dry place.
- Keep the box on a non-flammable surface.
- Cover exposed tabs/leads with tape. Don't store swollen or damaged cells.
- Printed plastic is not fireproof or a fire containment device.
- Verify your cells' actual dimensions before printing. Cells with wires or protection boards may need larger pockets.

## License

MIT (see `LICENSE`).
