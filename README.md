# JetAuto ROS Motion Controller

A ROS node that drives a physical **JetAuto** mobile robot around a rounded-square path using timed velocity commands (`geometry_msgs/Twist` on `cmd_vel`). The pattern was prototyped in Turtlesim, then calibrated on the real robot.

▶️ **Demo video:** https://youtube.com/shorts/lGA7h6az9sY

![ROS](https://img.shields.io/badge/ROS-1%20(catkin)-22314E?logo=ros&logoColor=white)
![Python](https://img.shields.io/badge/Python-rospy-3776AB?logo=python&logoColor=white)

Group project (Group 1), Seneca Polytechnic.

## What it does

1. Waits for you to place the robot at its start pose and press Enter
2. Drives one lap of the pattern:
   - **straight side**: forward at 0.5 m/s for 4.0 s
   - **smooth corner**: forward at 0.5 m/s while turning left at 0.7 rad/s for 2.2 s
   - repeats the side and the corner four times
3. Runs the lap twice, then publishes a zero-velocity command to stop the robot

Every speed and duration is a ROS parameter, so the pattern can be re-tuned without editing code.

## Run it

On the robot (or a machine sharing its ROS master):

```bash
cd ~/catkin_ws/src
git clone https://github.com/Gssodhi/project1_jetauto.git
cd ~/catkin_ws && catkin_make && source devel/setup.bash

roscore   # if a ROS master isn't already running

rosrun project1_jetauto real_square_motion.py _cmd_topic:=/jetauto_controller/cmd_vel
```

To find the right command topic on your robot:

```bash
rostopic list | grep cmd_vel   # e.g. /cmd_vel, /jetauto_controller/cmd_vel
rostopic info /cmd_vel
rosmsg show geometry_msgs/Twist
```

### Parameters

| Parameter | Default | Meaning |
|---|---|---|
| `~cmd_topic` | `jetauto_controller/cmd_vel` | Velocity command topic |
| `~side_speed` | `0.5` | Forward speed on straight sides (m/s) |
| `~side_time` | `4.0` | Duration of each straight side (s) |
| `~turn_speed` | `0.5` | Forward speed through corners (m/s) |
| `~turn_rate` | `0.7` | Turn rate through corners (rad/s, positive = left) |
| `~turn_time` | `2.2` | Duration of each corner (s) |
| `~laps` | `2` | Number of laps |

Example: `rosrun project1_jetauto real_square_motion.py _side_time:=4.5 _turn_time:=2.0`

## How it was calibrated

Control is **open-loop**: there's no odometry or sensor feedback, just a velocity held for a set time. To get roughly 1 m sides and clean corners, we kept each velocity fixed and tuned only the duration. Each segment was tested on its own on the real floor, adjusted until the measured distance or angle was close, and only then combined into the full pattern.

## What we learned

- **Simulation isn't reality.** Turtlesim is deterministic. On the real robot, wheel slip, friction, uneven floors and command latency all change the result, so timings that were perfect in simulation needed re-tuning.
- **Errors add up.** Small timing or speed errors on each segment accumulate over a lap. Turns are the most sensitive, since a slightly wrong angle sends every later side off course.
- **Next step:** close the loop with odometry or IMU feedback, so the robot stops on measured distance and heading instead of elapsed time.

## Project structure

```
scripts/real_square_motion.py   ROS node (rospy)
package.xml, CMakeLists.txt     catkin package definition
```
