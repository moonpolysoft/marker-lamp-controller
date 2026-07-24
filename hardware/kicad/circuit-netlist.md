# Revision A Circuit Connectivity

This is the authoritative human-readable netlist for the PCB. Pin numbers
refer to component package pins, not schematic-symbol ordering.

| Net | Connections |
|---|---|
| `SENSE` | J1-1, R1-1 |
| `SENSE_LED` | R1-2, R2-1 |
| `OPTO_A` | R2-2, U2-1, D3 cathode |
| `GND` | J1-4, U2-2, U2-3, D3 anode, D2 anode, C2-2, C3-2, U1-1, R6-2, C1-2, D4 anode |
| `VPRE` (`BATT_RAW`) | J1-2, D1 anode |
| `VPWR` | D1 cathode, D2 cathode, C2-1, C3-1, R4-1, Q1-2 emitter, U1 pins 5–8 |
| `QBASE` | U2-4 collector, R3-1 |
| `QBASE_BIAS` | R3-2, R4-2, Q1-1 base |
| `QCOL` | Q1-3 collector, R5-1 |
| `CTRL` | R5-2, R6-1, C1-1, D4 cathode, U1-2 |
| `LAMP_OUT` | U1-3, J1-3 |
| `NC` | U1-4 only |

## Package pin checks

- U1 `BSP762TXUMA1`: 1 GND, 2 IN, 3 OUT, 4 NC, 5–8 Vbb.
- U2 `VO617A-4X017T`: 1 LED anode, 2 LED cathode, 3 transistor emitter,
  4 transistor collector.
- Q1 `SBC807-40LT1G`: 1 base, 2 emitter, 3 collector.
- D1 is the series reverse-polarity diode.
- D2 is the supply TVS.
- D3 is antiparallel to the optocoupler LED.
- D4 is the 5.1 V control-node clamp.

## Installation connector

1. `SENSE` — C4483 cavity 10, violet/green.
2. `BATT_RAW` — 12 V feed with an external 2 A fuse at the source.
3. `LAMP_OUT` — positive feed to the grille lamps.
4. `GND` — chassis ground and lamp return.
