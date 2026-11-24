# Bill of Materials

Status: Owned / Ordered / Planned. Prices are approximate list prices. Quantities are for the full four-leg robot unless noted.

## Actuators
| Part | Role | Qty | Unit | Status |
|---|---|---|---|---|
| Feetech SM8512BL | Hip pitch + ab/ad | 8 | ~$212 | 2 owned (test leg) |
| Feetech HL-3955 | Knee drive | 4 | ~$90 | 1 owned |
| Feetech STS3215 (12 V) | Ankle | 4 | ~$15–25 | 1 owned |
| URT-2 debug board | Servo setup/debug | 1 | | Owned |

Servo total: about $2,136.

## Electronics
| Part | Role | Qty | Status |
|---|---|---|---|
| Teensy 4.1 | Real-time controller | 1 | Owned |
| SP3485 RS-485 transceiver breakout | SM8512BL bus | 2 | Owned |
| Jetson Nano | Companion computer (ROS 2) | 1 | Owned |
| Intel RealSense D400-series | Depth camera | 1 | Owned |
| 9-DOF IMU | Orientation | 1 | Owned |
| SingleTact 15 mm / 45 N | Foot force sensor | 4 | Test unit owned |

SM8512BL servos are RS-485; HL-3955 and STS3215 are TTL half-duplex, so they need separate buses from the Teensy (verify against the datasheets when wiring).

## Power
| Part | Qty | Status |
|---|---|---|
| 3S5P pack, LG M50LT 21700 cells (~273 Wh, ~1.04 kg) | 1 | Planned |
| 3S BMS + fuse sized for ~24–30 A sustained | 1 | Planned |
| 12 V servo rail + isolated 5 V rail for the Jetson | 1 | Planned |
| 12 V bench supply | 1 | Planned |

Power wiring must be a heavier path than the signal connectors (JST-XH is rated about 3 A per contact).

## Structure
| Part | Role | Qty | Status |
|---|---|---|---|
| Carbon-fiber tube, 20 mm OD / 18 mm ID | Thigh and shin | 2 x 1 m | Owned |
| 20x20 mm T-slot rail (8020.net) | Chassis side rails | 2 x 500 mm | 1 ordered |
| Slotted inside corner brackets + M5 T-nuts | Rail mounting | 25 / 50 | Ordered |
| 6 mm 1045 steel shaft | Ab/ad shaft | 4 | Planned |
| 6061 aluminum hub and boss (PCBWay) | Shaft coupling | per leg | Ordered (test leg) |
| 5–6 mm aluminum, waterjet | A/B plates, brackets, hub disc | per leg | Planned |
| igus igubal EFSM-06 bushings | Ab/ad shaft support | 2 per leg | Ordered |
| 2.5 x 24 mm slotted spring pins | Shaft cross pins | per leg | Ordered |
| M4 shoulder screws, nylon nuts | Pivot joints | | Ordered |
| 625ZZ / 626ZZ / MR85 bearings | Knee and linkage pivots | | Owned / planned |
| Metalset A4 epoxy | Tube-to-plug bonding | | Owned |

## Foot
| Part | Qty | Status |
|---|---|---|
| Smooth-Sil 945/950 silicone (Shore ~45–50A), Ease Release 200 | | Trial kit owned |
| PETG pressure puck | 4 | Planned (printed) |

## Fabrication
Bambu Lab X2D (PLA for mockups, PETG, CF/glass composites for structure). Vendors: PCBWay (CNC), SendCutSend / OSH Cut (waterjet), 8020.net (extrusion), McMaster-Carr (fasteners, tooling).

## Still needed
Small bushings and springs, M2/M3 hardware and heat-set inserts, M5 socket-head screws (length after bracket stack-up), ab/ad + hip aluminum brackets (long lead), second chassis rail.
