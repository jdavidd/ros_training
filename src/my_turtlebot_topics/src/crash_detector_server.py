#! /usr/bin/env python

import rospy
from std_srvs.srv import Trigger, TriggerResponse
from kobuki_laser_subscriber import LaserTopicReader
import time


class CrashDirectionService(object):
    
    def __init__(self, srv_name='/crash_direction_service_laser'):
        self._srv_name = srv_name
        self._laser_reader_object = LaserTopicReader()
        self.detection_dict = {"front":0, "left":0, "right":0}
        self._my_service = rospy.Service(self._srv_name, Trigger , self.srv_callback)

    def srv_callback(self, request):
        self.detection_dict = self._laser_reader_object.crash_detector()
        
        message = self.direction_to_move()
        
        rospy.logdebug("DIRECTION ==>"+message)
        
        response = TriggerResponse()
        """
        ---                                                                                                 
        bool success   # indicate if crashed                                       
        string message # Direction
        """
        response.success = self.has_crashed()
        response.message = message
        
        rospy.loginfo('here: ' + str(response.success))
        return response
    
    def has_crashed(self):
        if self.detection_dict["front"] < 0.8:
            return True 
        else:
            return False
    
    def direction_to_move(self):

        if self.detection_dict["left"] > self.detection_dict["right"]:
            message = "left"
        else:
            message = "right"
        
        return message

if __name__ == "__main__":
    rospy.init_node('crash_direction_service_server', log_level=rospy.INFO) 
    dir_serv_object = CrashDirectionService()
    rospy.spin() # mantain the service open.