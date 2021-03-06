#! /usr/bin/env python

import rospy

import actionlib
import time
from my_sphero_main.msg import exam_action_rec_odomFeedback, exam_action_rec_odomResult, exam_action_rec_odomAction
from nav_msgs.msg import Odometry 
from odom_info import OdomSphero
from odometry_analysis import check_if_out_maze

class RecordOdom(object):

    def __init__(self, goal_distance):
        # creates the action server
        self._as = actionlib.SimpleActionServer("/record_odom", exam_action_rec_odomAction, self.goal_callback, False)
        self._as.start()
        self.odom_subs = OdomSphero()
        self._result   = exam_action_rec_odomResult()
        self._seconds_recording = 120
        self._goal_distance = goal_distance


    def goal_callback(self, goal):
        # helper variables
        r = rospy.Rate(1)
        success = True
        for i in xrange(self._seconds_recording):
            rospy.loginfo("Recording Odom index="+str(i))
            if self._as.is_preempt_requested():
                rospy.loginfo('The goal has been cancelled/preempted')
                self._as.set_preempted()
                success = False
                break
            else:
                if not self.reached_distance_goal():
                    self._result.result_odom_array.append(self.odom_subs.get_odomdata())
            r.sleep()

        if success:
            self._as.set_succeeded(self._result)
        self._result   = exam_action_rec_odomResult()

    def reached_distance_goal(self):
        return check_if_out_maze(self._goal_distance, self._result.result_odom_array)
    
if __name__ == '__main__':
    rospy.init_node('record_odom_action_server_node')
    RecordOdom(goal_distance=2.0)
    rospy.spin()