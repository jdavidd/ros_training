#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
from std_srvs.srv import Empty, EmptyResponse


class MoveBB8():
    
    def __init__(self):
        self.bb8_vel_publisher = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
        self.cmd = Twist()
        self.ctrl_c = False
        self.rate = rospy.Rate(10) # 10hz
        rospy.on_shutdown(self.shutdownhook)
        
    def publish_once_in_cmd_vel(self):
        """
        This is because publishing in topics sometimes fails the first time you publish.
        In continuous publishing systems, this is no big deal, but in systems that publish only
        once, it IS very important.
        """
        while not self.ctrl_c:
            connections = self.bb8_vel_publisher.get_num_connections()
            if connections > 0:
                self.bb8_vel_publisher.publish(self.cmd)
                rospy.loginfo("Cmd Published")
                break
            else:
                self.rate.sleep()
        
    def shutdownhook(self):
        # works better than the rospy.is_shutdown()
        self.stop_bb8()
        self.ctrl_c = True

    def stop_bb8(self):
        rospy.loginfo("shutdown time! Stop the robot")
        self.cmd.linear.x = 0.0
        self.cmd.angular.z = 0.0
        self.publish_once_in_cmd_vel()

    def move_bb8(self, linear_speed=0.2, angular_speed=0.2):
        
        self.cmd.linear.x = linear_speed
        self.cmd.angular.z = angular_speed
        
        rospy.loginfo("Moving BB8!")
        self.publish_once_in_cmd_vel()

def my_callback(request):
    movebb8_object = MoveBB8()
    while not movebb8_object.ctrl_c:
        try:
            movebb8_object.move_bb8()
        except rospy.ROSInterruptException:
            movebb8_object.stop_bb8()

    return EmptyResponse()
if __name__ == '__main__':
    rospy.init_node('move_bb8_test', anonymous=True)
    my_service = rospy.Service('/my_service', Empty , my_callback) # create the Service called my_service with the defined callback
    rospy.spin() # maintain the service open.