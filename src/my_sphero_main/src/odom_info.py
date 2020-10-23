#!/usr/bin/env python

import rospy
from nav_msgs.msg import Odometry

class OdomSphero():
    
    def __init__(self):
        self.sphero_odom    = rospy.Subscriber('/odom', Odometry, self.callback)
        self.data           = Odometry()
    
    def callback(self, msg):                                    # Define a function called 'callback' that receives a parameter 
        self.data = msg
    
    def get_odomdata(self):
        return self.data
    
if __name__ == '__main__':
    rospy.init_node('odom_sphero_subscriber', anonymous=True)
    odom_sphero_object = OdomSphero()
    rospy.loginfo(odom_sphero_object.get_odomdata())
    rate = rospy.Rate(0.5)
    ctrl_c = False
    
    def shutdownhook():
        # works better than the rospy.is_shut_down()
        global ctrl_c
        rospy.loginfo("shutdown time!")
        ctrl_c = True
    
    rospy.on_shutdown(shutdownhook)
    
    while not ctrl_c:
        data = odom_sphero_object.get_odomdata()
        rate.sleep()
        rospy.loginfo(data)
