# JetAuto Motion Pattern Controller

## Demo Video
Watch the demo here: https://youtube.com/shorts/lGA7h6az9sY

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

# ROS Communication Setup

The robot is controlled using ROS topics.

## 1. Connect to the robot

SSH into the JetAuto robot computer:


ssh jetauto@<robot_ip>


Example:


ssh jetauto@192.168.1.102


---

## 2. Start ROS master (if not already running)

On the robot:


roscore


---

## 3. Verify ROS communication

Check ROS environment variables:


echo $ROS_MASTER_URI
echo $ROS_IP


Expected output:


ROS_MASTER_URI=http://192.168.1.102:11311


---

## 4. Verify ROS nodes and topics

List ROS nodes:


rosnode list


List ROS topics:


rostopic list


---

# Identify Robot Command Topic

The JetAuto robot accepts velocity commands through a `cmd_vel` topic.

Find available command topics:


rostopic list | grep cmd_vel


Typical output:


/cmd_vel
/jetauto_controller/cmd_vel


Inspect the topic:


rostopic info /cmd_vel


Check the message type:


rostopic type /cmd_vel


Display message structure:


rosmsg show geometry_msgs/Twist


---

# Running the Motion Controller

Navigate to the project directory:


cd ~/catkin_ws/src/project1_jetauto


Make the script executable (first time only):


chmod +x scripts/real_square_motion.py


Run the ROS node:


rosrun project1_jetauto real_square_motion.py _cmd_topic:=/cmd_vel


If your robot uses a different topic:


rosrun project1_jetauto real_square_motion.py _cmd_topic:=/jetauto_controller/cmd_vel

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