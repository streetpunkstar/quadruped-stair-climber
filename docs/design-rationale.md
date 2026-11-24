# Design Rationale

## Goal
Climb a real residential staircase (8.75" rise / 9.75" tread, 11 steps) with a robot weighing no more than 10 lb (4.5 kg). The project is learning-first, so decisions favor understanding and low cost over peak performance. Bipedal locomotion and full RL locomotion are explicitly not immediate goals.

## Architecture summary
| Item | Choice |
|---|---|
| Actuators per leg | 4: ab/ad, hip pitch (motor A), knee drive (motor B), ankle |
| Leg | 9" thigh + 9" shin, 20 mm OD carbon-fiber tube (18" total) |
| Knee | Passive pin joint driven from the hip via a 5-bar linkage |
| Chassis | Two fore-aft 20x20 mm aluminum T-slot rails, ~360–380 mm track, tie panel between |
| Hip spacing (front/rear) | ~340 mm (placeholder, can slide to ~360 mm) |
| Control | Teensy 4.1, ~100 Hz loop, closed-form IK |
| Perception | Jetson Nano + Intel RealSense D400 (ROS 2) |

## Key decisions
| Decision | Alternatives considered | Why |
|---|---|---|
| 5-bar knee linkage | 4-bar, 6-bar | 6-bar gained only ~0.8° tuck and ~3.5 points of stair margin; not worth the complexity. Moves knee actuation to the hip to avoid heavy distal mass. |
| 9" segments (up from 8") | 8" segments | Stair reach margin up to 12.1% without raising hip-pitch torque, which depends on stride offset rather than segment length. |
| Feetech servos (SM8512BL, HL-3955, STS3215 12 V) | Dynamixel XM430, Hiwonder HTD-45H, ODrive/BLDC | Dynamixel too expensive per unit; Hiwonder has a proprietary protocol and limited range; BLDC deferred as a separate learning track. 12 V STS3215 chosen over 7.4 V for torque margin. |
| Waterjet flat parts, 5–6 mm aluminum | Laser cut, CNC | No heat-affected zone around cyclically loaded bolt holes; one thickness simplifies quoting. |
| Continuous 6 mm steel shaft in the ab/ad axis | Plate-carried loads | Shaft takes the bending and torsion, so the A/B plate can stay thin and flat. |
| Two-bearing spaced support at ab/ad (igus igubal bushings) | Rely on servo's internal bearing | The servo's radial load rating is undocumented; the ab/ad joint has the highest cantilever moment in the robot. |
| SingleTact 15 mm / 45 N foot sensor | FSR | A force-sensing resistor saturates below real per-leg stance loads. |
| Cast silicone tread (Shore ~45–50A) | PLA foot | PLA does not grip wood floors. |
| Classical control first, learned control later | RL from the start | RL needs a sim model and sim-to-real work, which is a project of its own. Sequence: classical, then residual RL, then full learned locomotion. |
| Skeleton + thin-panel chassis | Heavy extrusion or solid plate | Both exceeded the mass budget. |

## Actuators
| Joint | Servo | Stall (12 V) | Continuous | Qty |
|---|---|---|---|---|
| Hip pitch (motor A) | Feetech SM8512BL | 85 kg·cm | 28 kg·cm | 4 |
| Ab/ad | Feetech SM8512BL | 85 kg·cm | 28 kg·cm | 4 |
| Knee drive (motor B) | Feetech HL-3955 | 55 kg·cm | 13.5 kg·cm | 4 |
| Ankle | Feetech STS3215 (12 V) | 30 kg·cm | 10 kg·cm | 4 |

Motor B torque check (HL-3955): 12.5 kg·cm at a moderate stride and 24.9 kg·cm at an aggressive one, against 13.5 continuous and 55 stall. SM8512BL and HL-3955 have no torque/current control mode, which limits compliant impact absorption. The baseline design is quasi-static (creep gait) only; a dynamic trot is not budgeted in the torque margins.

## Gait and speed
- Creep gait needs a software weight shift of about 1.4" toward the support-triangle centroid before each leg lift.
- Estimated speed: ~0.22–0.32 mph baseline, ~0.6–0.7 mph with software tuning. An 11-step climb is estimated at 1.1–1.8 minutes.

## Knee lessons so far
- At full tuck the rocker and coupler were nearly collinear, so slack let the shin swing ~30°. Fixed by re-clocking the rocker pivot 45° about the knee axis; the shin now droops only a couple of degrees.
- Open: the knee bolt head contacts the coupler linkage past ~90° thigh/shin angle.

## Fabrication gate
PLA mockup, then fit and clearance check, then waterjet order. Cross-pin holes are drilled last, in place, with the shaft assembled.

## Open questions
- Final front/rear hip spacing and chassis length
- Ab/ad + hip bracket design and quotes
- Chassis tie-panel material (3 mm aluminum vs. carbon fiber)
- Re-validate creep-gait weight-shift math with real CAD mass properties
