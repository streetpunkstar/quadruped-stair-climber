# Roadmap

## Mechanical
- [x] Leg geometry locked (9" segments, 5-bar knee)
- [x] Hip cluster architecture (ab/ad shaft, near/far bushings, A/B plate)
- [ ] Single test leg built and moving
- [ ] Ab/ad + hip bracket design and waterjet quotes
- [ ] Rubber foot with force sensor
- [ ] Chassis (two aluminum rails + tie panel) validated
- [ ] Full four-leg build

## Control
- [ ] Servo bus comms from Teensy (RS-485 + TTL buses)
- [ ] Closed-form IK + 5-bar calibration table
- [ ] Creep gait on flat ground (with weight shift)
- [ ] Uneven terrain
- [ ] Stairs (depth-camera stair detection + foot placement)

## Software / perception
- [ ] IMU complementary/Kalman filter (hand-rolled)
- [ ] ROS 2 on Jetson Nano, robot_localization
- [ ] Simulation model (MuJoCo) for gait and stair experiments

## Later
- Dynamic trot, 6-bar knee, BLDC actuators, residual RL on top of classical gait
