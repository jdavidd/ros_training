#!/usr/bin/env python

import rospy
from sensor_msgs.msg import Imu

class ImuSphero():
    
    def __init__(self):
        self.sphero_imu    = rospy.Subscriber('/sphero/imu/data3', Imu, self.callback)
        self.data          = Imu()
        self._threshhold   = 0.1
    
    def callback(self, msg):
        self.data = msg
    
    def get_imudata(self):
        return self.data
    
    def four_sector_detection(self):
        """
        Detects in which four directions there is an obstacle that made the robot crash
        Based on the imu data
        Axis:
         ^y
         |
        zO-->x
        
        """
        print(self.data)
        x_accel = self.data.linear_acceleration.x
        y_accel = self.data.linear_acceleration.y
        z_accel = self.data.linear_acceleration.z
        
        
        axis_list = [x_accel, y_accel, z_accel]
        
        max_axis_index = axis_list.index(max(axis_list))
        positive = axis_list[max_axis_index] >= 0
        significative_value = abs(axis_list[max_axis_index]) > self._threshhold
        
        
        if significative_value:
            if max_axis_index == 0:
                # Winner is in the x axis, therefore its a side crash left/right
                rospy.logwarn("[X="+str(x_accel))
                rospy.loginfo("Y="+str(y_accel)+", Z="+str(z_accel)+"]")
                if positive:
                    message = "right"
                else:
                    message = "left"
            
            elif max_axis_index == 1:
                # Winner is the Y axis, therefore its a forn/back crash
                rospy.logwarn("[Y="+str(y_accel))
                rospy.loginfo("X="+str(x_accel)+", Z="+str(z_accel)+"]")
                if positive:
                    message = "front"
                else:
                    message = "back"
            elif max_axis_index == 2:
                # Z Axixs is the winner, therefore its a crash that made it jump
                rospy.logwarn("[Z="+str(z_accel))
                rospy.loginfo("X="+str(x_accel)+", Y="+str(y_accel)+"]")
                
                if positive:
                    message = "up"
                else:
                    message = "down"
            else:
                message = "unknown_direction"
        else:
            rospy.loginfo("X="+str(x_accel)+"Y="+str(y_accel)+", Z="+str(z_accel)+"]")
            message = "nothing"
        
        return self.convert_to_dict(message)
        
    def convert_to_dict(self, message):
        """
        Converts the fiven message to a dictionary telling in which direction there is a detection
        """
        detect_dict = {}
        # We consider that when there is a big Z axis component there has been a very big front crash
        detection_dict = {"front":(message=="front" or message=="up" or message=="down"),
                          "left":message=="left",
                          "right":message=="right",
                          "back":message=="back"}
        return detection_dict

if __name__ == '__main__':
    rospy.init_node('imu_sphero_subscriber', anonymous=True)
    imu_sphero_object = ImuSphero()
    rospy.loginfo(imu_sphero_object.get_imudata())
    rate = rospy.Rate(0.5)
    ctrl_c = False
    
    def shutdownhook():
        # works better than the rospy.is_shut_down()
        global ctrl_c
        rospy.loginfo("shutdown time!")
        ctrl_c = True
    
    rospy.on_shutdown(shutdownhook)
    
    while not ctrl_c:
        data = imu_sphero_object.four_sector_detection()
        rate.sleep()
        rospy.loginfo(data)
