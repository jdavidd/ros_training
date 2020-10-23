#! /usr/bin/env python

import rospy
from nav_msgs.msg import Odometry

class OdomTopicReader(object):
    def __init__(self):
        self._sub = rospy.Subscriber('/odom', Odometry, self.topic_callback)
        self.odom_data = Odometry()
    
    def topic_callback(self, msg):
        self.odom_data = msg
        rospy.logdebug(self.odom_data)
    
    def get_odomdata(self):
        return self.odom_data
    
if __name__ == "__main__":
    rospy.init_node('odom_topic_subscriber', log_level=rospy.INFO)
    odom_reader_object = OdomTopicReader()
    rospy.loginfo(odom_reader_object.get_odomdata())
    rate = rospy.Rate(1)
    
    ctrl_c = False
    def shutdownhook():
        # works better than the rospy.is_shut_down()
        global ctrl_c
        print "shutdown time!"
        ctrl_c = True

    rospy.on_shutdown(shutdownhook)
    
    while not ctrl_c:
        data = odom_reader_object.get_odomdata()
        rospy.loginfo(data)
        rate.sleep()