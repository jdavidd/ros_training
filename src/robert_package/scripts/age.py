#! /usr/bin/env python

import rospy
from publish_age.msg import Age 

def callback(msg): 
  print msg.

rospy.init_node('topic_publisher')
sub = rospy.Subscriber('/Age', Age, callback)
rospy.spin()