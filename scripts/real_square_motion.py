#!/usr/bin/env python
"""Drive a JetAuto robot around a rounded square using timed velocity commands.

Each lap is four straight sides joined by four smooth left turns. The lap is
repeated twice, then the robot is stopped. Speeds and durations are ROS
parameters, so they can be re-tuned for a different robot or floor without
editing code.
"""
import rospy
from geometry_msgs.msg import Twist

try:
    input = raw_input  # Python 2 (ROS Melodic)
except NameError:
    pass  # Python 3 (ROS Noetic)


class JetAutoPatternController(object):
    def __init__(self):
        rospy.init_node("jetauto_pattern_controller", anonymous=False)

        cmd_topic = rospy.get_param("~cmd_topic", "jetauto_controller/cmd_vel")
        self.pub = rospy.Publisher(cmd_topic, Twist, queue_size=10)

        # Calibrated on the physical robot by tuning durations at fixed speeds
        self.side_speed = rospy.get_param("~side_speed", 0.5)  # m/s
        self.side_time = rospy.get_param("~side_time", 4.0)  # s per straight side
        self.turn_speed = rospy.get_param("~turn_speed", 0.5)  # m/s while turning
        self.turn_rate = rospy.get_param("~turn_rate", 0.7)  # rad/s, positive = left
        self.turn_time = rospy.get_param("~turn_time", 2.2)  # s per corner
        self.laps = rospy.get_param("~laps", 2)

        self.rate = rospy.Rate(20)

    def publish_for_duration(self, linear_x=0.0, linear_y=0.0, angular_z=0.0, duration=1.0):
        """Publish one velocity command at 20 Hz for `duration` seconds."""
        msg = Twist()
        msg.linear.x = linear_x
        msg.linear.y = linear_y
        msg.angular.z = angular_z

        t_end = rospy.Time.now() + rospy.Duration(duration)
        while rospy.Time.now() < t_end and not rospy.is_shutdown():
            self.pub.publish(msg)
            self.rate.sleep()

    def stop_robot(self):
        self.pub.publish(Twist())
        rospy.sleep(0.3)

    def run_once(self):
        """One lap: four straight sides, each followed by a smooth turn."""
        for side in range(1, 5):
            rospy.loginfo("Side %d: straight", side)
            self.publish_for_duration(linear_x=self.side_speed, duration=self.side_time)

            rospy.loginfo("Side %d: smooth turn", side)
            self.publish_for_duration(
                linear_x=self.turn_speed, angular_z=self.turn_rate, duration=self.turn_time
            )

    def wait_for_start(self):
        input("Place robot at start pose, then press Enter to begin...")

    def run(self):
        self.wait_for_start()
        for lap in range(1, self.laps + 1):
            rospy.loginfo("Starting lap %d / %d", lap, self.laps)
            self.run_once()

        rospy.loginfo("Pattern complete.")
        self.stop_robot()


if __name__ == "__main__":
    try:
        controller = JetAutoPatternController()
        controller.run()
    except rospy.ROSInterruptException:
        pass
