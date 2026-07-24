# Preliminary Auxiliary Marker-Lamp Controller

Status: design concept updated with initial vehicle and load measurements.

## Confirmed measurements

- C4483 cavity 10, violet/green, follows the desired parking-lamp behavior.
- Multimeter indication with parking lamps active:
  - approximately 6 V with the truck off;
  - approximately 8 V with the truck on.
- Total aftermarket marker-lamp current: 0.25 A while supplied by the truck's
  energized accessory circuit.
- The input waveform has not yet been observed with an oscilloscope.

The most likely explanation for the reduced multimeter readings is
battery-amplitude PWM. The input circuit must therefore accumulate valid PWM
pulses while rejecting isolated diagnostic pulses.

## Requirements

- Detect the factory rear parking-lamp output without CAN or trailer wiring.
- Add no more than approximately 6 mA peak to the BCM parking-lamp output.
- Power the aftermarket lamps from a separate fused 12 V feed.
- Prevent off-state diagnostic pulses from flashing the aftermarket lamps.
- Default to auxiliary lamps off after an open circuit or loss of controller
  power.
- Tolerate reverse polarity and common automotive electrical transients.

## Proposed architecture

```text
 C4483-10
 VT-GN
    |
  F1 100 mA
    |
 reverse/transient protection
    |
 PWM-compatible optocoupler input
    |
 Schmitt-trigger pulse filter
    |
 automotive smart high-side switch

 Separate fused 12 V ---- smart switch ---- amber marker lamps
 Vehicle ground ----------------------------- marker-lamp ground
```

The optocoupler separates the BCM sense circuit from the load controller. A
protected automotive high-side switch supplies the 0.25 A lamp load and
eliminates relay-coil power, audible clicking, and contact wear.

## Candidate circuit

### Factory-lamp sense input

| Ref | Candidate value/part | Purpose |
|---|---|---|
| F1 | 100 mA inline fuse or fusible lead | Protect sense lead |
| D1 | SMAJ33A automotive-qualified equivalent | Positive transient clamp |
| D2 | 1N4148W, anti-parallel with optocoupler LED | Reverse-voltage protection |
| R1, R2 | 1.0 kΩ, 0.25 W each, series | Set LED current and share dissipation |
| U1 | LTV-817S, PC817-class optocoupler, or automotive-qualified equivalent | Isolated detection |

If the suspected PWM waveform rises to 14.8 V, two 1.0 kΩ resistors produce
approximately:

```text
(14.8 V - 1.2 V) / 2.0 kΩ = 6.8 mA peak
```

If the signal is actually steady DC, input current is approximately 2.4 mA at
6 V and 3.4 mA at 8 V. These values provide substantially more optocoupler
margin than the original 5.4 kΩ proposal while remaining a small additional
BCM load. Final resistor values remain subject to waveform and temperature
testing.

Do not add a large capacitor directly to the BCM output. PWM accumulation and
diagnostic-pulse rejection are performed on the isolated, low-voltage side.

### Isolated pulse filter and high-side-switch control

| Ref | Candidate value/part | Purpose |
|---|---|---|
| U2 | Protected 5 V automotive regulator, LM2931-5.0 class | Logic supply |
| U3 | SN74HC14-Q1 Schmitt-trigger inverter | Clean switching threshold |
| R3 | 10 kΩ provisional | U1 collector path; lets successive PWM pulses discharge C1 |
| R4 | 100 kΩ provisional | Slowly restores the filtered node when pulses stop |
| C1 | 10 µF provisional, low-leakage | Integrates PWM and rejects isolated pulses |
| U4 | TPS1H200A-Q1 | Protected 40 V automotive high-side lamp switch |
| R5 | Per U4 data-sheet stand-alone application | U4 current-limit programming |
| R6 | 100 kΩ | Defined U4 input-off state |
| C2 | Per U4 data-sheet application | Fault-delay/behavior configuration |

The optocoupler transistor discharges the filtered node through R3 when the
parking-lamp PWM is active. R4 charges the node to 5 V after valid pulses stop.
A Schmitt inverter converts the slow RC edge into a clean control signal for
U4. R3 is intentionally much smaller than R4 so repeated PWM pulses accumulate
quickly while isolated pulses have limited effect.

The timing values are provisional. Real switching behavior depends on PWM
frequency and duty cycle, U3 thresholds, optocoupler current-transfer ratio,
temperature, and capacitor tolerance. Select R3, R4, and C1 after a scope
capture or by conservative pulse-generator bench testing. Tie unused
Schmitt-trigger inputs to a defined logic level.

The TPS1H200A-Q1 is an AEC-Q100, 40 V, 200 mΩ smart high-side switch with
short-circuit, overload, and thermal protection. At 0.25 A its nominal
conduction loss is only:

```text
P = I²R = 0.25² × 0.2 = 0.0125 W
```

Configure its current limit above normal lamp startup current. A provisional
target is 0.75–1.0 A, subject to measuring startup inrush and applying the
device data-sheet equations and tolerances.

### Lamp-power path

```text
12 V source -- F2 -- U4 supply
U4 output -- auxiliary marker lamp positive
auxiliary marker lamp negative -- chassis ground
```

F2 must be located close to the power source. Use a 2 A automotive branch fuse
with 18 AWG automotive primary wire from the fuse-box tap to the controller.
The 2 A fuse provides ample margin over the measured 0.25 A operating current,
while U4 provides the tighter downstream overload and short-circuit
protection:

```text
1.25 × 0.25 A = 0.3125 A
```

The fuse must protect every conductor between the fuse-box tap and U4. The
smaller grille pigtail is protected by U4's programmed current limit. A 5 A
upstream fuse is also compatible with 18 AWG feed wiring, but 2 A provides
better protection and adequate operating margin for this load.

## Installation interfaces

Provisional four-circuit arrangement:

1. `SENSE` — fused high-impedance connection to C4483-10, violet/green.
2. `BATT+` — separately fused controller/load supply.
3. `GND` — chassis ground.
4. `LAMP+` — switched output to the marker lamps.

A fifth terminal can provide a dedicated lamp return if relying on local
chassis grounding is undesirable.

Use sealed automotive connectors, strain relief, abrasion-resistant loom, and
drip loops. The enclosure should not be the primary environmental seal for
unsealed wire penetrations.

## Bench validation before vehicle installation

1. Sweep the sense input from 0 to 16 V and record output thresholds.
2. Apply short 12–15 V pulses and verify pulses shorter than the measured BCM
   diagnostic pulse do not enable the output.
3. Hold the input at 14.8 V for at least one hour and check component
   temperatures.
4. Test input reverse polarity through a current-limited supply.
5. Test power interruption and brownout; output oscillation is unacceptable.
6. Test at the maximum expected lamp current with the actual harness and fuse.
7. Confirm the output switches off when the sense conductor is disconnected.

## Open inputs needed to finalize the design

- Desired behavior during approach lighting and remote start
- Actual parking-lamp PWM amplitude, frequency, and duty cycle
- Measured off-state diagnostic-pulse width and interval, if any
- Controller mounting location and temperature/water exposure
- Preferred connector family and wire exit directions
- Maximum acceptable enclosure dimensions
