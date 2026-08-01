# Revision B (V2) Notes

These items were discovered while assembling and bench-testing Revision A.
They must be resolved before generating or ordering another PCB revision.

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
and cross-wired. Correct the generated footprint and verify the physical pad
numbers against the manufacturer package drawing before releasing Revision B.

## 2. Resolve the J1/mounting-hole interference

J1 mechanically overlaps the upper-left mounting-hole area. Reposition J1,
the mounting hole, or both so the complete connector body, mating-plug access,
wire-entry space, and tool-access envelope clear the mounting hardware.

Add explicit connector and mounting-hardware courtyards and check their
clearance rather than checking copper pads alone.

## 3. Enlarge the C3 footprint

The Revision A C3 footprint is too narrow for the actual Panasonic
`EEE-FK1H470P` capacitor. Replace the custom footprint dimensions with the
manufacturer-recommended land pattern and body/courtyard dimensions.

Before releasing Revision B, measure the received component and verify:

- Pad width, length, and center spacing
- 8 mm-class can body clearance
- Polarity marking and silkscreen visibility
- Hand-soldering access around both terminals
- Clearance to adjacent components and traces

## Revision B release gate

Print the component-side fabrication drawing at 1:1 scale and physically place
Q1, C3, J1, the mating plug, and representative M3 mounting hardware on it.
Do not order Revision B until all three corrections pass this fit check and a
fresh KiCad DRC reports no violations or unconnected pads.
