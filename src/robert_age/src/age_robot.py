#! /usr/bin/env python

import rospy
from AgeR.msg import AgeR #Import Age message from the exercise_33 package

rospy.init_node('age_robot')
pub = rospy.Publisher('/age_info', AgeR, queue_size=1) #Create a Publisher that will publish in the /age_info topic
rate = rospy.Rate(2)
age = Age() #Create an Age message object
age.years = 5 #Fill the values of the message
age.months = 10 #Fill the values of the message
age.days = 21 #Fill the values of the message

while not rospy.is_shutdown(): 
  pub.publish(age) #Publish the message into the defined topic /age_info
  rate.sleep()