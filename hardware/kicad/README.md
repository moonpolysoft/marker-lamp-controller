# Fabrication Design

This directory contains Revision A of the two-layer marker-lamp controller.

## Files

- `marker-lamp-controller.kicad_pcb` — generated KiCad 10 PCB.
- `generate_pcb.py` — deterministic PCB generator using KiCad's `pcbnew`
  Python module.
- `circuit-netlist.md` — readable authoritative circuit connectivity.
- `revision-b-notes.md` — corrections found while assembling Revision A that
  must be incorporated before the next board order.
- `BOM.csv` — orderable manufacturer and DigiKey part numbers.
- `drc-report.txt` — KiCad board DRC result.
- `fabrication/` — OSH Park Gerbers and separate plated/non-plated drills.
- `board-render.png` — top-side board preview (custom hand-solder footprints
  do not carry 3D body models).

The PCB generator and `circuit-netlist.md` are authoritative for Revision A.

## Connector

Board header:

- Same Sky `TBP01R1-508-04BE`

Mating pluggable terminal connector:

- Same Sky `TBP01P1-508-04BE`

Pinout:

1. `SENSE` — driver-side rear parking output, C4483 cavity 10,
   violet/green.
2. `BATT+` — separately fused 12 V feed; use a 2 A fuse.
3. `LAMP+` — switched positive output to the 0.25 A grille LEDs.
4. `GND` — chassis ground and grille LED return.

## Board construction

- 80 × 45 mm
- Two copper layers
- 1 oz copper
- Minimum designed trace/space: 0.20 mm / 0.20 mm
- Signal traces: 0.35–0.60 mm
- Power/load traces: 1.2 mm
- Vias: 0.8 mm finished pad, 0.4 mm drill
- Four 3.2 mm non-plated mounting holes
- Mounting-hole centers: 72 × 37 mm
- Components on the top side

These values exceed the OSH Park two-layer minima of 0.1524 mm
trace/spacing, 0.127 mm annular ring, and 0.254 mm minimum drill.

## DigiKey availability review

The BOM was checked against DigiKey stock on 2026-07-24. Stock changes
continuously, so verify it again before ordering.

- BSP762TXUMA1: stocked, cut tape available.
- VO617A-4X017T: stocked, cut tape available.
- TBP01R1-508-04BE header: stocked.
- TBP01P1-508-04BE mating plug: stocked.
- STPS2H100A and SMBJ22A: stocked, cut tape available.
- SBC807-40LT1G: stocked, automotive-qualified.
- 1N4148WS: stocked alternate selected.
- BZT52-C5V1-QX: stocked, automotive-qualified.
- CGA6P1X7R1E106K250AC: stocked, automotive-qualified.
- C0805C104K5RAC7210: stocked, active replacement for an obsolete Murata
  bypass capacitor considered during selection.
- EEE-FK1H470P and all three Yageo resistor values: stocked.

## Regenerate

```sh
python3 generate_pcb.py
```

Run from this directory or from the project root using the full relative path.

## Status

Revision A is an engineering prototype. Bench test the sense waveform,
turn-on/off delays, reverse polarity, output short protection, thermal
behavior, and vehicle sleep current before permanent installation.

KiCad 10 DRC reports zero violations, zero unconnected pads, and zero footprint
errors. This verifies the artwork rules and connectivity, not the behavior of
the untested vehicle signal.
