#! /usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
from math import pi
from services_quiz.srv import BB8CustomServiceMessage, BB8CustomServiceMessageResponse
import time

def make_a_move(side):
    move.angular.z      = 0.0
    move.linear.x       = 0.5
    pub.publish(move)
    time.sleep(2*side)

    move.angular.z      = 0.0
    move.linear.x       = 0.0
    pub.publish(move)
    time.sleep(4)

    move.linear.x       = 0
    move.angular.z      = 0.2
    pub.publish(move)
    time.sleep(4)

    move.angular.z      = 0.0
    move.linear.x       = 0.0
    pub.publish(move)
    time.sleep(1)



def move_like_square(side):
    make_a_move(side)
    make_a_move(side)
    make_a_move(side)
    make_a_move(side)

def my_callback(request):
    
    print "Request Data==> repetitions="+str(request.repetitions)
    my_response     = BB8CustomServiceMessageResponse()
    i               = 0

    while i < request.repetitions:
        move_like_square(request.side)
        rate.sleep()
        i = i + 1

    my_response.success = True
    move.angular.z  = 0
    move.linear.x   = 0
    pub.publish(move)
    
    return my_response

rospy.init_node('service_server') 
my_service  = rospy.Service('/move_bb8_in_square_custom', BB8CustomServiceMessage , my_callback) # create the Service called my_service with the defined callback
pub         = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
move        = Twist()  
rate        = rospy.Rate(5)
rospy.spin() # maintain the service open.