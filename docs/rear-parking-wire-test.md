# Rear Parking-Lamp Wire Field Test

Vehicle: 2023 Ford F-150 Lightning

Purpose: identify a conventional rear parking-lamp voltage that can be used
only as a high-impedance control signal for an auxiliary marker-lamp
controller.

## Test results — initial multimeter measurements

The driver-side candidate passed the functional test: its signaling follows
the desired parking-lamp behavior.

With the parking lamps active, a multimeter measured approximately:

| Vehicle state | Measurement from C4483-10 to body ground |
|---|---:|
| Truck off | 6 V DC indicated |
| Truck on | 8 V DC indicated |

The aftermarket marker-lamp assembly draws 0.25 A while operating from the
truck's energized accessory circuit. This is the relevant normal operating
current at the vehicle's active low-voltage-system voltage.

The 6 V and 8 V readings are likely averaged measurements of a
battery-amplitude PWM waveform used to dim the factory LED lamp. This is an
engineering inference, not yet a confirmed waveform measurement. The revised
controller input is therefore designed to detect and integrate a pulsed input
rather than requiring a steady 12 V level.

## Candidate conductors

Start with the driver-side rear lamp:

| Side | Connector | Cavity | Ford circuit | Wire color | Function |
|---|---|---:|---|---|---|
| Driver/left | C4483, black, 12 cavities | 10 | CLS08 | Violet/green (`VT-GN`) | Park rear left |
| Passenger/right | C4484, black, 12 cavities | 10 | CLS09 | White/orange (`WH-OG`) | Park rear right |

The driver-side violet/green conductor at C4483 cavity 10 is the preferred
first candidate.

## Equipment

- Digital multimeter with insulated probes
- Fine back-probe pin or automotive back-probe adapter
- Plastic trim tool
- Suitable socket/driver for the rear-lamp fasteners
- Optional oscilloscope with an automotive-rated input or appropriately rated
  probe

Do not use an incandescent test lamp. Do not jumper connector cavities.

## Access

1. Park securely, select Park, and switch the vehicle off.
2. Open the tailgate.
3. Remove the fasteners exposed along the inside edge of the driver-side rear
   lamp.
4. Pull the lamp assembly straight rearward to release its locating pins. Do
   not lever against painted panels.
5. Locate the black 12-cavity connector plugged into the lamp assembly.
6. On the truck-harness side, locate the violet wire with a green stripe.
7. Verify the molded cavity number is `10`. Do not identify the conductor by
   counting cavities alone; connector drawings can show different viewing
   faces.

Pins 6 and 12 at this connector are associated with the rear-corner-radar
CAN-FD network. Do not probe them.

## Voltage test

Keep the connector attached so the factory lamp remains operational.

1. Set the multimeter to DC volts, using a range suitable for at least 20 V.
2. Connect the black lead to a verified clean chassis ground.
3. Carefully back-probe C4483 cavity 10 with the red lead. Do not spread or
   damage the terminal.
4. Record the voltage for each state below.

| Vehicle state | Expected result | Measured |
|---|---|---|
| Vehicle asleep, lamps off | Near 0 V | |
| Vehicle awake, lamps off | Near 0 V; brief diagnostic pulses are possible | |
| Parking lamps selected, truck off | PWM suspected; meter indicated about 6 V | 6 V |
| Parking/headlamps selected, truck on | PWM suspected; meter indicated about 8 V | 8 V |
| Brake applied, parking lamps off | Near 0 V | |
| Left turn signal, parking lamps off | Near 0 V | |
| Hazard lamps, parking lamps off | Near 0 V | |
| Reverse selected, parking lamps off | Near 0 V | |
| Unlock/approach lighting | Record whether output activates | |
| Remote start | Record whether output activates | |
| Vehicle charging, otherwise asleep | Record voltage and pulses | |

Use an assistant for control operation. Do not place yourself behind or under
a vehicle that can move. Reverse testing should be performed only with the
vehicle secured and the tester clear of its path.

## Diagnostic-pulse check

A multimeter may average short BCM diagnostic pulses and display a small or
unstable voltage while the lamp is visibly off. If possible, inspect the
conductor with an oscilloscope:

1. Use a common-ground, automotive-safe measurement setup.
2. Observe the line for at least 60 seconds while the lamps are off and the
   vehicle transitions from awake to asleep.
3. Record pulse amplitude, width, and repetition interval.
4. Repeat while charging and shortly after unlocking the vehicle.

Do not connect a grounded bench oscilloscope directly unless its grounding
arrangement is known to be safe for vehicle use.

## Acceptance criteria

The conductor is suitable as a controller input if:

- it remains asserted whenever the desired factory parking lamps are on;
- brake, turn, hazard, and reverse operation do not assert it independently;
- any off-state diagnostic pulses are short enough to reject with input
  filtering; and
- the factory lamp continues to work normally with no warnings or diagnostic
  messages.

The eventual controller input must draw only a few milliamps. The auxiliary
lamps must be powered from a separate fused circuit.

The functional conductor test is complete. An oscilloscope capture remains
useful for finalizing the controller's input threshold and pulse filter, but
is not required before beginning bench prototypes.

## Reference connector records

- C4483 left rear lamp: <https://www.f150lightningforum.com/forum/attachments/rear-lamp-assembly-lh-c4483-pdf.104247/>
- C4484 right rear lamp: <https://www.f150lightningforum.com/forum/attachments/rear-lamp-assembly-rh-c4484-pdf.104245/>
