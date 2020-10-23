#! /usr/bin/env python

import rospy
import rospkg
import sys
from services_quiz.srv import BB8CustomServiceMessage, BB8CustomServiceMessageRequest


rospy.init_node('service_client')
rospy.wait_for_service('/move_bb8_in_square_custom')

start_bb8_service           = rospy.ServiceProxy('/move_bb8_in_square_custom', BB8CustomServiceMessage)
start_bb8_object            = BB8CustomServiceMessageRequest()
start_bb8_object.side       = 2
start_bb8_object.repetitions  = 2

result = start_bb8_service(start_bb8_object)
# Print the result given by the service called
print result