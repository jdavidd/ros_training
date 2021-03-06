#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist

class MoveSphero():
    
    def __init__(self):
        self.sphero_vel_publisher   = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
        self.cmd                    = Twist()
        self.rate                   = rospy.Rate(10) # 10hz
        self.linearspeed            = 0.2
        self.angularspeed           = 0.5

    def move_sphero(self, direction):
        
        if direction == 'forward':
            self.cmd.linear.x   = self.linearspeed
            self.cmd.angular.z  = 0.0
        elif direction == 'right':  
            self.cmd.linear.x   = 0.0
            self.cmd.angular.z  = self.angularspeed
        elif direction == 'left':
            self.cmd.linear.x   = 0.0
            self.cmd.angular.z  = -self.angularspeed
        elif direction == 'backward':
            self.cmd.linear.x   = -self.linearspeed
            self.cmd.angular.z  = 0.0
        elif direction == 'stop':
            self.cmd.linear.x   = 0.0
            self.cmd.angular.z  = 0.0
        else:
            pass

        rospy.loginfo("Moving " + direction + " !")
        self.sphero_vel_publisher.publish(self.cmd)
            
if __name__ == '__main__':
    rospy.init_node('move_sphero_test', anonymous=True)
    move_sphero_object = MoveSphero()

    rate = rospy.Rate(1)
    ctrl_c = False
    
    def shutdownhook():
        # works better than the rospy.is_shut_down()
        global ctrl_c
        global twist_object
        global pub
        
        rospy.loginfo("shutdown time!")
        
        ctrl_c = True
        move_sphero_object.move_sphero(direction="stop")
    
    rospy.on_shutdown(shutdownhook)
    
    while not ctrl_c:
        move_sphero_object.move_sphero(direction="forward")
        rate.sleep()