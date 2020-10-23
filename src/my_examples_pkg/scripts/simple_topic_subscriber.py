#! /usr/bin/env python

import rospy
from nav_msgs.msg import Odometry
import time

def callback(msg): 
  print msg.pose.pose.position
  print(' ')
  print msg.pose.pose.orientation
  time.sleep(5)
  print('=======')

rospy.init_node('topic_subscriber')
sub = rospy.Subscriber('odom', Odometry, callback)
rospy.spin()