#! /usr/bin/env python

import rospy
from std_srvs.srv import Empty, EmptyResponse # you import the service message python classes generated from Empty.srv.
from geometry_msgs.msg import Twist

def my_callback(request):
    move        = Twist()     
    move.linear.x   = 0.2
    move.angular.z  = 0.2

    pub.publish(move)
    return EmptyResponse() # the service Response class, in this case EmptyResponse
    #return MyServiceResponse(len(request.words.split())) 

rospy.init_node('service_server') 
my_service = rospy.Service('/move_bb8_in_circle', Empty , my_callback) # create the Service called my_service with the defined callback
pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)

rospy.spin() # maintain the service open.