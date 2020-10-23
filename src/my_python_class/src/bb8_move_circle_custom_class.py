#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
import time

class MoveBB8Custom():
    
    def __init__(self, duration):
        self.bb8_vel_publisher = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
        self.cmd = Twist()
        self.ctrl_c = False
        self.rate = rospy.Rate(10) # 10hz
        self.duration = duration
        rospy.on_shutdown(self.shutdownhook)
        
    def publish_once_in_cmd_vel(self):
        """
        This is because publishing in topics sometimes fails the first time you publish.
        In continuous publishing systems, this is no big deal, but in systems that publish only
        once, it IS very important.
        """
        while not self.ctrl_c:
            connections = self.bb8_vel_publisher.get_num_connections()
            if connections > 0:
                self.bb8_vel_publisher.publish(self.cmd)
                rospy.loginfo("Cmd Published")
                break
            else:
                self.rate.sleep()
        
    def shutdownhook(self):
        # works better than the rospy.is_shutdown()
        self.ctrl_c = True

    def move_bb8(self, linear_speed=0.2, angular_speed=0.2):
        
        self.cmd.linear.x   = linear_speed
        self.cmd.angular.z  = angular_speed
        
        rospy.loginfo("Moving BB8!")
        self.publish_once_in_cmd_vel()

        i = 0
        while i < self.duration:
            i = i + 1
            time.sleep(1)

        self.cmd.linear.x   = 0
        self.cmd.angular.z  = 0
        
        rospy.loginfo("Stoping BB8!")
        self.publish_once_in_cmd_vel()

if __name__ == '__main__':
    rospy.init_node('move_bb8_test', anonymous=True)
    Custom_object = MoveBB8Custom()
    try:
        movebb8_object.move_bb8()
    except rospy.ROSInterruptException:
        pass