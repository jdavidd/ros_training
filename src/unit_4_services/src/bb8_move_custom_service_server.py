#! /usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
from my_custom_srv_msg_pkg.srv import MyCustomServiceMessage, MyCustomServiceMessageResponse

def my_callback(request):
    
    print "Request Data==> duration="+str(request.duration)
    my_response     = MyCustomServiceMessageResponse()
    move            = Twist()  
    move.linear.x   = 0.2
    move.angular.z  = 0.2
    i               = 0

    while i <= request.duration:
        pub.publish(move)
        rate.sleep()
        i = i + 1

    my_response.success = True
    move.angular.z  = 0
    move.linear.x   = 0
    pub.publish(move)
    
    return my_response

rospy.init_node('service_server') 
my_service = rospy.Service('/move_bb8_in_circle_custom', MyCustomServiceMessage , my_callback) # create the Service called my_service with the defined callback
pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)

rate = rospy.Rate(1)
rospy.spin() # maintain the service open.