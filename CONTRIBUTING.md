# Contributing

Thank you for helping improve the marker-lamp controller. Contributions may be
submitted through the issue and pull-request facilities of the repository host.

## Before reporting a problem

Include enough context to distinguish a design issue from a vehicle, assembly,
or installation difference:

- PCB revision and source commit
- Vehicle model year, trim, and relevant lighting options
- Lamp part or measured steady-state current
- Supply voltage, fuse size, and bench-supply current limit
- Exact test points and reference ground used
- Measurements, scope captures, photographs, and reproduction steps

Remove VINs, registration details, addresses, keys, and other identifying data
from photographs and diagnostic exports.

## Design changes

Keep editable source files and regenerated outputs in the same change. For PCB
changes, update the generator/netlist, Revision B KiCad board as applicable,
BOM, DRC report, preview, and fabrication archive. For enclosure changes,
update the OpenSCAD source, exported STL files, and enclosure documentation.

Please document:

- The problem being solved and any assumptions
- Component manufacturer part numbers and footprints
- Automotive voltage, temperature, and transient ratings where relevant
- Hand-assembly and enclosure-clearance effects
- Tests performed and any validation still outstanding

Do not silently replace safety-critical parts or increase fuse ratings. Avoid
committing KiCad history, editor lock files, slicer profiles, distributor carts,
or generated files that contain personal information.

## Validation

For PCB changes, run KiCad DRC and confirm zero violations and unconnected
pads. Inspect Gerbers and drill files independently before fabrication. Bench
test new assemblies using a current-limited supply before connecting them to a
vehicle.

For enclosure changes, render both parts in OpenSCAD, check that each is a
valid solid, and verify connector access, PCB clearances, screw engagement,
and print orientation.

## Licensing contributions

By contributing, you agree that your contribution is licensed under the
repository's CERN Open Hardware Licence Version 2—Strongly Reciprocal
(`CERN-OHL-S-2.0`). Do not contribute material you do not have the right to
license. Clearly identify third-party material and its licence.
