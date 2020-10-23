#! /usr/bin/env python


import rospy
from bb8_move_circle_custom_class import MoveBB8Custom
import sys
sys.path.append('../')
from .my_custom_srv_msg_pkg.srv import MyCustomServiceMessage, MyCustomServiceMessageResponse

def my_callback(request):
    rospy.loginfo("The Service move_bb8_in_circle has been called")
    movebb8_object = MoveBB8Custom(request.duration)
    movebb8_object.move_bb8()
    rospy.loginfo("Finished service move_bb8_in_circle")
    my_response = MyCustomServiceMessageResponse()
    my_response.succes = True

    return my_response 

rospy.init_node('service_move_bb8_in_circle_custom_server') 
my_service = rospy.Service('/move_bb8_in_circle_custom', MyCustomServiceMessage , my_callback)
rospy.loginfo("Service /move_bb8_in_circle Ready")
rospy.spin() # mantain the service open.