# Quadruped Stair-Climbing Robot

A 12-DOF (4 legs × 3 DOF) quadruped designed to climb stairs. Status: **mechanical design phase**, simulation-first, with a physical build planned.

> Demo video, CAD renders and write-up: _coming soon_

## Goals
- Design a leg and body able to handle standard stair geometry
- Validate the design in MuJoCo before buying or printing parts
- Build a physical copy (one leg first, then the full robot)

## Repo layout
| Path | Contents |
|---|---|
| `cad/` | STEP/STL exports and renders |
| `docs/` | Design rationale, decision log, stair/torque calculations |
| `hardware/` | Parts list (BOM), power budget |
| `sim/mujoco/` | Simulation model and gait/stair experiments |
| `firmware/` | Controller code for the physical robot |
| `media/` | Photos, GIFs, demo video links |

## Status
See [ROADMAP.md](ROADMAP.md).

## License
MIT (code) — see [LICENSE](LICENSE). CAD/docs: CC BY 4.0 unless noted.
