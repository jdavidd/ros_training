#! /usr/bin/env python

import rospy

import actionlib
import time
from actionlib.msg import TestFeedback, TestResult, TestAction
from geometry_msgs.msg import Twist 
from std_msgs.msg import Empty

class MoveDroneSquare(object):
    
  # create messages that are used to publish feedback/result
  _feedback = TestFeedback()
  _result   = TestResult()

  def __init__(self):
    # creates the action server
    self._as = actionlib.SimpleActionServer("move_drone_square_as", TestAction, self.goal_callback, False)
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
    
    #take of drone
    self.take_off_drone()
    
    side_square = goal.goal
    turn        = 1.8

    for i in xrange(0, 4):
    
      if self._as.is_preempt_requested():
        rospy.loginfo('The goal has been cancelled/preempted')
        self._as.set_preempted()
        success = False
        break
      self.make_a_move(side_square, turn)
      # builds the next feedback msg to be sent
      self._feedback.feedback = i
      # publish the feedback
      self._as.publish_feedback(self._feedback)
      # the sequence is computed at 1 Hz frequency
      r.sleep()
    
    if success:
      self._result.result = side_square*4 + turn*4
      rospy.loginfo('Succeeded moving drone')
      self._as.set_succeeded(self._result)

      self.stop_drone()
      self.land_drone()

if __name__ == '__main__':
  rospy.init_node('move_square')
  MoveDroneSquare()
  rospy.spin()