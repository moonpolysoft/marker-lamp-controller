# Controller Enclosure Concept

`controller_enclosure.scad` is a preliminary parametric enclosure consisting
of a base and lid. It is intentionally larger than the expected circuit so
terminal blocks, an automotive relay, and strain relief can be evaluated.

Default external dimensions are approximately 100 × 72 × 38 mm, excluding
mounting tabs. This is deliberately generous; the switch to a solid-state
power stage should permit a substantially smaller final enclosure.

## Generate models

Open the file in OpenSCAD and change `part`:

```scad
part = "base";
part = "lid";
part = "assembly";
```

Export the base and lid separately as STL.

Command-line examples:

```sh
openscad -D 'part="base"' -o controller_base.stl controller_enclosure.scad
openscad -D 'part="lid"' -o controller_lid.stl controller_enclosure.scad
```

## Printing assumptions

- Material: ASA preferred for heat and UV resistance; PETG is suitable for
  an interior dry prototype. PLA is not recommended in a vehicle.
- Layer height: 0.20 mm
- Walls: at least 4 perimeters
- Top/bottom layers: at least 5
- Infill: 30% or greater around mounting tabs
- Print both pieces with their large flat exterior faces on the build plate.

The current lid uses screws, not printed snap fits. The model includes an
O-ring/gasket channel concept, but sealing has not been validated. Use sealed
cable glands or sealed bulkhead connectors for an exterior/underbody mounting
location.

## Measurements required before finalization

- Finished PCB length, width, and component height
- Final PCB dimensions and tallest component
- Connector or cable-gland diameters
- Cable exit direction
- Available mounting footprint and bolt spacing
- Required ingress protection
