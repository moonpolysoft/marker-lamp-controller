# Revision B (V2) Notes

These items were discovered while assembling and bench-testing Revision A.
They are implemented in the generated Revision B PCB. Keep this file as the
design rationale and fabrication checklist.

## 1. Correct the Q1 footprint pin mapping

Revision A swaps Q1 pins 1 and 2 at the physical SOT-23 pads. The specified
onsemi `SBC807-40LT1G` uses:

- Pin 1: base
- Pin 2: emitter
- Pin 3: collector

With the SOT-23 mounted component-side up and its single lead on the right,
the physical leads are:

- Upper-left: pin 1, base -- connect to `QBASE`
- Lower-left: pin 2, emitter -- connect to `VPWR`
- Right: pin 3, collector -- connect to `QCOL`

Revision A instead connects the upper-left pad to `VPWR` and the lower-left
pad to `QBASE`. The assembled prototype required both left leads to be lifted
and cross-wired. Revision B connects upper-left pin 1 to `QBASE`, lower-left
pin 2 to `VPWR`, and right-side pin 3 to `QCOL`.

## 2. Resolve the J1/mounting-hole interference

J1 mechanically overlaps the upper-left mounting-hole area. Reposition J1,
the mounting hole, or both so the complete connector body, mating-plug access,
wire-entry space, and tool-access envelope clear the mounting hardware.

Revision B moves J1 7 mm toward the lower-left mounting hole. Its body now
occupies Y=14.2–35.1 mm, between the two left mounting holes at Y=5 and
Y=42 mm. The matching enclosure opening moves by the same 7 mm.

## 3. Enlarge the C3 footprint

The Revision A C3 footprint is too narrow for the actual Panasonic
`EEE-FK1H470P` capacitor. Revision B uses the standard 8 × 6.2 mm SMD-can
geometry: 6.1 mm pad-center spacing, 4.0 × 2.5 mm pads, and an 8.3 × 8.3 mm
body envelope.

Before releasing Revision B, measure the received component and verify:

- Pad width, length, and center spacing
- 8 mm-class can body clearance
- Polarity marking and silkscreen visibility
- Hand-soldering access around both terminals
- Clearance to adjacent components and traces

## Revision B release record

Revision B implements all three corrections and passed a fresh KiCad DRC with
no violations or unconnected pads before submission to OSH Park. The enclosure
was updated for the relocated J1 and confirmed by prototype printing. The
fabricated Revision B assembly still requires bench and in-vehicle validation.
