# F-150 Lightning Auxiliary Marker-Lamp Controller

This project is a controller for aftermarket amber marker lamps on a 2023
Ford F-150 Lightning. The intended behavior is for the auxiliary lamps to
follow the factory parking lamps without connecting to the vehicle CAN bus or
the trailer-lighting connector.

Current project files:

- [`docs/rear-parking-wire-test.md`](docs/rear-parking-wire-test.md) — field
  procedure for identifying and verifying the rear parking-lamp output.
- [`hardware/controller-design.md`](hardware/controller-design.md) —
  preliminary protected solid-state controller circuit.
- [`enclosure/controller_enclosure.scad`](enclosure/controller_enclosure.scad)
  — parametric two-piece enclosure concept.
- [`enclosure/README.md`](enclosure/README.md) — enclosure generation and
  measurement notes.

## Design status

This is a preliminary design. Do not permanently connect the controller until
the rear-lamp waveform, aftermarket lamp current, supply location, connectors,
and mounting environment have been verified.
