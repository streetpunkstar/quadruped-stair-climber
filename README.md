# Quadruped Stair-Climbing Robot

A custom ≤10 lb (4.5 kg) quadruped built from scratch as a hands-on project in embedded systems, robot mechanics, firmware and actuator selection. Target: climb a real residential staircase (8.75" rise / 9.75" tread, 11 steps).

**Status:** single test leg in hardware build; full-leg CAD in progress.

## Design at a glance
- 4 legs x 4 actuators (ab/ad, hip pitch, knee drive, ankle) = 16 servos
- 9" thigh + 9" shin (carbon-fiber tube), knee driven remotely from the hip through a 5-bar linkage
- Stair reach margin: 12.1% over the target staircase (CAD/numerical estimate)
- Teensy 4.1 for real-time control (~100 Hz IK loop); Jetson Nano + Intel RealSense for perception (ROS 2)
- Per-foot force sensing (SingleTact) under a cast silicone tread
- Classical gait control first (creep gait), then stairs; learned locomotion is a later track

## Repo layout
| Path | Contents |
|---|---|
| `cad/` | STEP/STL exports and renders |
| `docs/` | Design rationale, decisions, calculations |
| `hardware/` | Bill of materials, power budget |
| `sim/` | Simulation (MuJoCo) |
| `firmware/` | Teensy controller code |
| `media/` | Photos, GIFs, demo video links |

See [docs/design-rationale.md](docs/design-rationale.md) and [ROADMAP.md](ROADMAP.md).

## License
MIT (code) — see [LICENSE](LICENSE). CAD and docs: CC BY 4.0 unless noted.
