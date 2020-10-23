#! /usr/bin/env python

import rospy
from geometry_msgs.msg import Twist 

rospy.init_node('topic_publisher')
pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
rate = rospy.Rate(2)
count = Twist()
count.angular.z = 0

while not rospy.is_shutdown(): 
  pub.publish(count)
  count.angular.z += 1
  rate.sleep()