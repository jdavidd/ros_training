#! /usr/bin/env python

import rospy
from sensor_msgs.msg import LaserScan

class LaserTopicReader(object):
    def __init__(self):
        self.sub = rospy.Subscriber('/kobuki/laser/scan', LaserScan, self.topic_callback)
        self.laser_data = LaserScan()
        self._front     = 0
        self._left      = 0
        self._right     = 0
    
    def topic_callback(self, msg):
        self.laser_data = msg
        rospy.logdebug(self.laser_data)
    
    def get_laserdata(self):
        return self.laser_data

    def crash_detector(self):
    
        if (len(self.laser_data.ranges)>0):
            self._front = self.laser_data.ranges[360]
            self._right = self.laser_data.ranges[0]
            self._left = self.laser_data.ranges[719]
            rospy.loginfo("Front Distance == "+str(self._front))
            rospy.loginfo("Left Distance == "+str(self._left))
            rospy.loginfo("Right Distance == "+str(self._right))

    
        return self.convert_to_dict()
        
        
    def convert_to_dict(self):
        """
        Converts the fiven message to a dictionary telling in which direction there is a detection
        """
        detect_dict = {}
        # We consider that when there is a big Z axis component there has been a very big front crash
        detection_dict = {"front":self._front,
                          "left":self._left,
                          "right":self._right}
        return detection_dict
        
if __name__ == "__main__":
    rospy.init_node('laser_topic_subscriber', log_level=rospy.INFO)
    laser_reader_object = LaserTopicReader()
    rospy.loginfo(laser_reader_object.get_laserdata())
    rate = rospy.Rate(1)
    
    ctrl_c = False
    def shutdownhook():
        # works better than the rospy.is_shut_down()
        global ctrl_c
        print "shutdown time!"
        ctrl_c = True

    rospy.on_shutdown(shutdownhook)
    
    while not ctrl_c:
        data = laser_reader_object.get_laserdata()
        laser_reader_object.crash_detector()
        rate.sleep()