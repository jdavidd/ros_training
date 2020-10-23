#! /usr/bin/env python

import rospy
import actionlib
import time
from actions_quiz.msg import CustomActionMsgFeedback, CustomActionMsgAction
from geometry_msgs.msg import Twist
from std_msgs.msg import Empty

class LandOrTakeoff(object):

  # create messages that are used to publish feedback/result
  _feedback = CustomActionMsgFeedback()

  def __init__(self):
    print('Initi')
    # creates the action server
    self._as = actionlib.SimpleActionServer("action_custom_msg_as", CustomActionMsgAction, self.goal_callback, False)
    self._as.start()
    self.move_drone = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
    self.take_off   = rospy.Publisher('/drone/takeoff', Empty, queue_size=1)
    self.land       = rospy.Publisher('/drone/land', Empty, queue_size=1)


  def take_off_drone(self):
    i = 0
    while i < 3:
        self.take_off.publish(Empty())
        rospy.loginfo('Taking off...')
        time.sleep(1)
        i += 1
  def land_drone(self):
    i = 0
    while i < 3:
        self.land.publish(Empty())
        rospy.loginfo('Land off...')
        time.sleep(1)
        i += 1
  def make_a_move(self, side, turn_seconds):
    move = Twist()
    move.angular.z      = 0.0
    move.linear.x       = 1
    self.move_drone.publish(move)
    time.sleep(side)

    move.linear.x       = 0.0
    move.angular.z      = 1
    self.move_drone.publish(move)
    time.sleep(turn_seconds)
  def stop_drone(self):
    move = Twist()
    move.linear.x       = 0.0
    move.angular.z      = 0.0
    self.move_drone.publish(move)

  def goal_callback(self, goal):
    # helper variables
    r = rospy.Rate(1)
    success = True

    if self._as.is_preempt_requested():
        rospy.loginfo('The goal has been cancelled/preempted')
        self._as.set_preempted()
        success = False
    else:
        if goal.goal == "TAKEOFF":
            self.take_off_drone()
            self._feedback.feedback = "TAKEOFF"
        else:
            self.land_drone()
            self._feedback.feedback = "LAND"

        # publish the feedback
        self._as.publish_feedback(self._feedback)
        # the sequence is computed at 1 Hz frequency
        r.sleep()
    self.stop_drone()

    # if success:
    #   self._result.result = side_square*4 + turn*4
    #   rospy.loginfo('Succeeded moving drone')
    #   self._as.set_succeeded(self._result)

if __name__ == '__main__':
  rospy.init_node("land_or_takeoff")
  LandOrTakeoff()
  rospy.spin()
