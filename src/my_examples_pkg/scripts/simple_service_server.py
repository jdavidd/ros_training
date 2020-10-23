#! /usr/bin/env python

import rospy
from std_srvs.srv import Empty, EmptyResponse # you import the service message python classes generated from Empty.srv.
from geometry_msgs.msg import Twist

def my_callback(request):
    rospy.loginfo("The Service move_bb8_in_circle has been called")
    rospy.loginfo('ceva')
    move_circle = Twist()
    move_circle.linear.x = 0.2
    move_circle.angular.z = 0.2
    my_pub.publish(move_circle)
    return EmptyResponse() # the service Response class, in this case EmptyResponse
    #return MyServiceResponse(len(request.words.split())) 

rospy.init_node('service_server')
my_service = rospy.Service('/move_bb8_in_circle', Empty , my_callback) # create the Service called my_service with the defined callback
my_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
rospy.spin() # maintain the service open.