#! /usr/bin/env python

import rospy
from my_examples_pkg_armand.msg import Age

rospy.init_node('age_topic_publisher')
pub = rospy.Publisher('/age', Age, queue_size=1)
rate = rospy.Rate(0.5)
age = Age()
age.years = 0
age.months = 0
age.days = 1

while not rospy.is_shutdown(): 
  pub.publish(age)
  rate.sleep()
