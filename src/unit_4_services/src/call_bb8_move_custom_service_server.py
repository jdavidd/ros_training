#! /usr/bin/env python

import rospy
import rospkg
import sys
from my_custom_srv_msg_pkg.srv import MyCustomServiceMessage, MyCustomServiceMessageRequest

rospy.init_node('service_client')
rospy.wait_for_service('/move_bb8_in_circle_custom')

start_bb8_service           = rospy.ServiceProxy('/move_bb8_in_circle_custom', MyCustomServiceMessage)
start_bb8_object            = MyCustomServiceMessageRequest()
start_bb8_object.duration   = 5

result = start_bb8_service(start_bb8_object)
# Print the result given by the service called
print result