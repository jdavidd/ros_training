#! /usr/bin/env python

import rospy
from geometry_msgs.msg import Twist

rospy.init_node('topic_publisher')
pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
rate = rospy.Rate(0.5)
velocity = Twist()
velocity.linear.x = 0
velocity.angular.z = 0

while not rospy.is_shutdown(): 
  pub.publish(velocity)
  velocity.linear.x = min(velocity.linear.x + 0.05, 1)
  velocity.angular.z = min(velocity.angular.z + 0.05, 1)
  rate.sleep()
