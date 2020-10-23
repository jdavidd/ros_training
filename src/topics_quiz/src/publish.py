#! /usr/bin/env python

import rospy
from geometry_msgs.msg import Twist 
from sensor_msgs.msg import LaserScan 

pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)

last_data   = ""
started     = False
move        = Twist()     

def callback(data):  
    print("new message")
    global started, last_data
    last_data = data.ranges
    if (not started):
        started = True

def processing_data(data):
    global move
    length = len(data)
    middle = length/2 + length%2 if length != 0 else 0
    value_middle    = data[middle]
    value_left      = data[length-1]
    value_right     = data[0]

    if value_middle > 1:
        move.linear.x   = 1
        move.angular.z  = 0
    else:
        move.linear.x   = 0
        move.angular.z  = 1.57
    
    if value_right < 1:
        move.linear.x   = 0.5
        move.angular.z  = 1.57

    if value_left < 1:
        move.linear.x   = 0.5
        move.angular.z  = -1.57

    print(value_middle, value_left, value_right)
    print("Move: ", move)
        
def listener():
    rospy.init_node('topics_quiz_node')
    sub = rospy.Subscriber('/kobuki/laser/scan', LaserScan, callback)
    
    global started, pub, last_data, move
    print rospy.is_shutdown() == True
    while not rospy.is_shutdown():
        print(started)
        if (started):
            processing_data(last_data)
            pub.publish(move)
        rospy.sleep(0.5)

listener()
        