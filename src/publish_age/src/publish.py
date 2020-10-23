#! /usr/bin/env python

import rospy
from Age.msg import Age 

rospy.init_node('age_publisher')
pub = rospy.Publisher('/sub', Age, queue_size=1)
rate = rospy.Rate(2)
age = Age()
age.years   = 1
age.months  = 6
age.days    = 21

while not rospy.is_shutdown(): 
  pub.publish(age)
  rate.sleep()