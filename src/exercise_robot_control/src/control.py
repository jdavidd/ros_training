#! /usr/bin/env python
import rospy                               # Import the Python library for ROS
from geometry_msgs.msg import Twist

rospy.init_node('topic_publisher')         # Initiate a Node named 'topic_publisher'
pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1) 

rate = rospy.Rate(2)                       # Set a publish rate of 2 Hz
var = Twist()                              # Create a var of type Int32
var.linear.x = 0.5
var.angular.z = 0.45

while not rospy.is_shutdown():           # Create a loop that will go until someone stops the program execution
  pub.publish(var)                       # Publish the message within the 'count' variable
  rate.sleep()         