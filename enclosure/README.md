# Controller Enclosure Concept

`controller_enclosure.scad` is a parametric enclosure consisting of a base and
lid sized for the current Revision B controller PCB. Its fit has been confirmed
with a printed prototype.

Default external dimensions are approximately 96 × 80 × 23.2 mm, excluding
mounting tabs. The lid roof is 4.2 mm thick so recessed screw heads retain a
1.2 mm supporting floor.

The left wall has a support-free, top-open notch sized to admit the Same Sky
`TBP01P1-508-04BE` four-position mating plug from outside. The lid lip is
relieved over the same opening. The nominal 22.5 mm opening width provides
approximately 2.2 mm total clearance around the plug's 20.32 mm length.

The PCB is shifted toward the J1 wall, leaving 0.5 mm nominal clearance
between that PCB edge and the inside wall. The wider enclosure provides more
than 2 mm nominal radial clearance between the populated PCB corners and the
nearest lid bosses. The lid bosses are also inset far enough to leave 1.6 mm
nominal clearance from the inside edge of the lid lip.

The base notch and lid relief deliberately use mirrored source coordinates:
the lid is printed exterior-face down and flipped for assembly. This makes the
two openings align when the enclosure is closed.

Revision B moves J1 by 7 mm along the PCB edge to clear its mounting hole.
The enclosure opening center follows the new connector position.

The base is 19 mm tall, including its 3 mm floor. The solid wall beneath the
J1 notch is 9.5 mm tall.

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
- Lid: use a 5 mm brim to prevent the edges from peeling up from the print
  bed.

## Hardware assumptions

- Lid: four M3 machine screws into heat-set inserts.
- Lid screw recesses: 5.8 mm diameter × 3.0 mm deep, sized for nominal
  5.5 mm-diameter, 3.0 mm-tall heads. Verify the actual screw heads before
  the final print.
- Insert pocket: 4.2 mm diameter × 5.5 mm deep; adjust these two parameters to
  the actual insert manufacturer's recommended hole dimensions.
- Lid insert bosses finish 0.75 mm below the base rim to keep heat-set-insert
  squeeze-out from interfering with lid fit.
- PCB: four M3 screws driven into 2.7 mm pilot holes in printed standoffs.
- PCB mounting pattern: 72 × 37 mm.
- The two PCB standoffs opposite J1 include a 0.5 mm outward print-fit
  adjustment, producing 72.5 mm modeled spacing in that axis.
- No environmental gasket is required for the dry installation location; the
  existing shallow channel may be left unused.

The current lid uses screws, not printed snap fits. The model includes an
O-ring/gasket channel concept, but sealing has not been validated. Use sealed
cable glands or sealed bulkhead connectors for an exterior/underbody mounting
location.

## Checks before vehicle installation

- Confirm the selected heat-set insert diameter and length before printing.
- Confirm that the installed lid screws remain long enough for full insert
  engagement with the recessed 4.2 mm lid roof.
- Verify that the populated PCB, Q1 rework, C3, header, and mating plug clear
  the lid and screw bosses.
- Verify that the connector can be inserted and removed with the lid fitted.
- Confirm the enclosure mounting-tab hole locations against the vehicle.
