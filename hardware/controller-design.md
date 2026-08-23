# Auxiliary Marker-Lamp Controller

Status: Revision B assembled, bench tested, installed, and verified working in
the vehicle.

## Confirmed measurements

- C4483 cavity 10, violet/green, follows the desired parking-lamp behavior.
- Multimeter indication with parking lamps active:
  - approximately 6 V with the truck off;
  - approximately 8 V with the truck on.
- Total aftermarket marker-lamp current: 0.25 A while supplied by the truck's
  energized accessory circuit.
- The input waveform has not yet been characterized with an oscilloscope. The
  assembled circuit nevertheless responds correctly to the selected signal in
  the vehicle.

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
 PWM-compatible optocoupler input
    |
 asymmetric RC pulse filter
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
| D3 | 1N4148WS, anti-parallel with optocoupler LED | Reverse-voltage protection |
| R1, R2 | 1.0 kΩ, 0.25 W each, series | Set LED current and share dissipation |
| U2 | VO617A-4X017T | Isolated detection with specified high CTR |

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
| Q1 | SBC807-40LT1G | PNP level shifter driven by the optocoupler |
| R3 | 10 kΩ | Limits optocoupler/base current |
| R4 | 100 kΩ | Holds Q1 off without a sense signal |
| R5 | 10 kΩ | Charges the filtered control node |
| R6 | 100 kΩ | Discharges the filtered node after pulses stop |
| C1 | 10 µF | Accumulates parking-lamp PWM pulses |
| D4 | BZT52-C5V1-QX | Clamps the switch input near 5.1 V |
| U1 | BSP762TXUMA1 | Protected automotive high-side lamp switch in SO-8 |

The optocoupler turns on Q1 during each parking-lamp pulse. Q1 charges C1
through R5; R6 discharges it when pulses stop. D4 limits the resulting control
voltage for U1. The nominal charge time constant is 0.10 seconds and the
nominal discharge time constant is 1.0 second, providing persistence through
normal lamp PWM without placing a capacitor on the BCM output.

The timing values remain subject to characterization. Real switching behavior depends on PWM
frequency and duty cycle, U3 thresholds, optocoupler current-transfer ratio,
temperature, and capacitor tolerance. Select R3, R4, and C1 after a scope
capture or by conservative pulse-generator bench testing. Tie unused
Schmitt-trigger inputs to a defined logic level.

The BSP762TXUMA1 is an automotive smart high-side switch in a hand-solderable SO-8
package with short-circuit, overload, overvoltage, and thermal protection. At
0.25 A and its typical 70 mΩ on-resistance, nominal conduction loss is:

```text
P = I²R = 0.25² × 0.07 = 0.0044 W
```

Its protection threshold is fixed internally. The external 2 A branch fuse
protects the feed wiring and provides a second level of fault protection.

### Lamp-power path

```text
12 V source -- F2 -- U4 supply
U4 output -- auxiliary marker lamp positive
auxiliary marker lamp negative -- chassis ground
```

F2 must be located close to the power source. Use a 2 A automotive branch fuse
with 18 AWG automotive primary wire from the fuse-box tap to the controller.
The 2 A fuse provides ample margin over the measured 0.25 A operating current,
while U1 provides downstream overload and short-circuit
protection:

```text
1.25 × 0.25 A = 0.3125 A
```

The fuse must protect every conductor between the fuse-box tap and U1. The
smaller grille pigtail also benefits from U1's fixed internal current limiting.
A 5 A
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

## Future characterization

- Actual parking-lamp PWM amplitude, frequency, and duty cycle
- Measured off-state diagnostic-pulse width and interval, if any
- Turn-on and turn-off thresholds across automotive temperature extremes
- Vehicle sleep-current contribution over an extended parked interval
- Transient-immunity testing beyond normal bench and in-vehicle operation
