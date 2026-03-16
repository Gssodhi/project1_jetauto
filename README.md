# JetAuto Motion Pattern Controller

## Project Overview

This project implements a ROS node that controls a mobile robot using velocity commands.  
The robot performs a sequence of calibrated motions including forward movement, lateral motion, rotation, and a combined motion to approximately return toward the starting position.

The motion pattern is executed using the `geometry_msgs/Twist` message published to the robot's velocity command topic.

The project was tested using ROS and the Turtlesim simulator to validate motion behavior before deploying on the physical robot.

---

# Project Structure
project1_jetauto/
├── scripts/
│ └── real_square_motion.py
├── README.md
└── answers.txt

- `real_square_motion.py` – main ROS node that publishes velocity commands
- `README.md` – project documentation
- `answers.txt` – reflection answers

---

# Robot Setup and Communication

Communication with the robot was established using ROS topics.

The ROS master was started using:

- `real_square_motion.py` – main ROS node that publishes velocity commands
- `README.md` – project documentation
- `answers.txt` – reflection answers

---

# Robot Setup and Communication

Communication with the robot was established using ROS topics.

The ROS master was started using:
roscore

Available ROS nodes and topics were verified using:
rosnode list
rostopic list


To identify the robot velocity command topic:


rostopic list | grep cmd_vel


The command topic was inspected using:


rostopic info /cmd_vel
rosmsg show geometry_msgs/Twist


The `geometry_msgs/Twist` message allows control of:

- `linear.x` → forward/backward motion
- `linear.y` → sideways motion
- `angular.z` → rotational motion

---

# How to Run the Project

## 1 Start ROS master


roscore


## 2 Launch simulation (for testing)


rosrun turtlesim turtlesim_node


## 3 Run the motion controller


rosrun project1_jetauto real_square_motion.py


## 4 Reset simulation if needed


rosservice call /reset

---

# Motion Pattern

The robot performs the following sequence:

1. Move forward
2. Move left sideways
3. Rotate 90° clockwise
4. Move right sideways
5. Move forward while turning to approximately return toward the starting position

---

# Calibration Procedure

Motion calibration was performed by adjusting the duration of each command while keeping velocity constant until the desired displacement or rotation was achieved.

Each segment was tested independently before executing the full pattern.

---

# Calibration Table

| Motion | Velocity command | Target | Initial time estimate | Measured result | Final tuned time |
|---|---|---|---|---|---|
| Forward | `linear.x = 0.5` | ~1 m | 4.0 s | slightly short | 5.0 s |
| Left sideways | `linear.y = 0.5` | ~1 m | 4.0 s | small drift | 5.0 s |
| Clockwise turn | `angular.z = -0.71` | 90° | 2.0 s | under-rotation | 2.2 s |
| Right sideways | `linear.y = -0.5` | ~1 m | 4.0 s | close | 5.0 s |
| Forward + turn | `linear.x = 1.0`, `angular.z = 0.35` | return toward start | 4.5 s | overshoot | 5.6 s |

---

# Notes

- Motion control is implemented using **open-loop time-based velocity commands**.
- Small errors accumulate due to timing differences and simulator behavior.
- In real robots additional factors such as friction, wheel slip, and sensor noise may affect motion accuracy.

---

# Author

Group 1:  
Project: JetAuto Motion Control Pattern