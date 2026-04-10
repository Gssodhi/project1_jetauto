#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist

class JetAutoPatternController:
    def __init__(self):
        rospy.init_node("jetauto_pattern_controller", anonymous=False)

        # Change this topic if your robot uses a different velocity command topic
        cmd_topic = rospy.get_param("~cmd_topic", "/cmd_vel")
        self.pub = rospy.Publisher(cmd_topic, Twist, queue_size=10)

        # Safe engineering defaults (must be tuned on the real robot)
        self.forward_speed = rospy.get_param("~forward_speed", 0.5)
        self.lateral_speed = rospy.get_param("~lateral_speed", 0.50)
        self.turn_speed = rospy.get_param("~turn_speed", -0.71)   # negative => clockwise
        self.combo_forward_speed = rospy.get_param("~combo_forward_speed", 1.3)
        self.combo_turn_speed = rospy.get_param("~combo_turn_speed", 0.5)

        # Timing constants to be calibrated experimentally
        self.forward_time = rospy.get_param("~forward_time", 5.0)
        self.left_time = rospy.get_param("~left_time", 5.0)
        self.turn_time = rospy.get_param("~turn_time", 2.2)
        self.right_time = rospy.get_param("~right_time", 5.0)
        self.combo_time = rospy.get_param("~combo_time", 3.6)

        self.rate = rospy.Rate(20)

    def publish_for_duration(self, linear_x=0.0, linear_y=0.0, angular_z=0.0, duration=1.0):
        msg = Twist()
        msg.linear.x = linear_x
        msg.linear.y = linear_y
        msg.angular.z = angular_z

        t_end = rospy.Time.now() + rospy.Duration(duration)
        while rospy.Time.now() < t_end and not rospy.is_shutdown():
            self.pub.publish(msg)
            self.rate.sleep()

        #self.stop_robot()

    def stop_robot(self):
        msg = Twist()
        self.pub.publish(msg)
        rospy.sleep(0.3)

    def run_once(self):

    # ---- Side 1 (straight) ----
       rospy.loginfo("Step 1: straight")
       self.publish_for_duration(
         linear_x=0.5,
        angular_z=0.0,
        duration=4.0
    )

    # ---- Turn 1 (anticlockwise curve) ----
       rospy.loginfo("Step 2: smooth turn")
       self.publish_for_duration(
        linear_x=0.5,
        angular_z=0.7,
        duration=2.2
    )

    # ---- Side 2 ----
       rospy.loginfo("Step 3: straight")
       self.publish_for_duration(
        linear_x=0.5,
        angular_z=0.0,
        duration=4.0
    )

    # ---- Turn 2 ----
       rospy.loginfo("Step 4: smooth turn")
       self.publish_for_duration(
        linear_x=0.5,
        angular_z=0.7,
        duration=2.2
    )

    # ---- Side 3 ----
       rospy.loginfo("Step 5: straight")
       self.publish_for_duration(
        linear_x=0.5,
        angular_z=0.0,
        duration=4.0
    )

    # ---- Turn 3 ----
       rospy.loginfo("Step 6: smooth turn")
       self.publish_for_duration(
        linear_x=0.5,
        angular_z=0.7,
        duration=2.2
    )

    # ---- Side 4 ----
       rospy.loginfo("Step 7: straight")
       self.publish_for_duration(
        linear_x=0.5,
        angular_z=0.0,
        duration=4.0
    )

    # ---- Final Turn (return to start) ----
       rospy.loginfo("Step 8: final smooth turn")
       self.publish_for_duration(
        linear_x=0.5,
        angular_z=0.7,
        duration=2.2
    )


    def wait_for_start(self):
        raw_input("Place robot at start pose, then press Enter to begin...")

    def run(self):
        self.wait_for_start()
        for i in range(2):
            rospy.loginfo("Starting pattern repetition %d / 2")
            self.run_once()

        rospy.loginfo("Pattern complete.")
        self.stop_robot()

if __name__ == "__main__":
    try:
        controller = JetAutoPatternController()
        controller.run()
    except rospy.ROSInterruptException:
        pass

