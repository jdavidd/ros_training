#! /usr/bin/env python

import rospy
import rospkg
import sys
from std_srvs.srv import Empty, EmptyRequest

rospy.init_node('service_client')
rospy.wait_for_service('/move_bb8_in_circle')

start_bb8_service = rospy.ServiceProxy('/move_bb8_in_circle', Empty)
result = start_bb8_service()
# Print the result given by the service called
print result