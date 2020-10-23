#! /usr/bin/env python

import rospy
import time
import actionlib
from ardrone_as.msg import ArdroneAction, ArdroneGoal, ArdroneResult, ArdroneFeedback
from geometry_msgs.msg import Twist 
from std_msgs.msg import Empty

"""
class SimpleGoalState:
    PENDING = 0
    ACTIVE = 1
    DONE = 2
    WARN = 3
    ERROR = 4

"""
# We create some constants with the corresponing vaules from the SimpleGoalState class
PENDING = 0
ACTIVE = 1
DONE = 2
WARN = 3
ERROR = 4

nImage = 1

# definition of the feedback callback. This will be called when feedback
# is received from the action server
# it just prints a message indicating a new message has been received
def feedback_callback(feedback):
    """
    Error that might jump
    
    self._feedback.lastImage = 
AttributeError: 'ArdroneAS' obj
    
    """
    global nImage
    print('[Feedback] image n.%d received'%nImage)
    nImage += 1

# initializes the action client node
rospy.init_node('drone_action_client')

#move drone
move_topic          = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
move                = Twist()

#take off

take_off_topic      = rospy.Publisher( '/drone/takeoff', Empty, queue_size = 1)
land_topic          = rospy.Publisher( '/drone/land', Empty, queue_size = 1)

action_server_name  = '/ardrone_action_server'
client              = actionlib.SimpleActionClient(action_server_name, ArdroneAction)

# waits until the action server is up and running
rospy.loginfo('Waiting for action Server '+action_server_name)
client.wait_for_server()
rospy.loginfo('Action Server Found...'+action_server_name)

# creates a goal to send to the action server
goal = ArdroneGoal()
goal.nseconds = 10 # indicates, take pictures along 10 seconds

client.send_goal(goal, feedback_cb=feedback_callback)


# You can access the SimpleAction Variable "simple_state", that will be 1 if active, and 2 when finished.
#Its a variable, better use a function like get_state.
#state = client.simple_state
# state_result will give the FINAL STATE. Will be 1 when Active, and 2 if NO ERROR, 3 If Any Warning, and 3 if ERROR
state_result = client.get_state()

rate = rospy.Rate(1)

rospy.loginfo("state_result: "+str(state_result))

i = 0
while i < 3:
    take_off_topic.publish(Empty())
    rospy.loginfo('Taking off...')
    time.sleep(1)
    i += 1

while state_result < DONE:
    rospy.loginfo("move drone")

    move.linear.x = 1
    move.angular.z = 1

    move_topic.publish(move)

    rate.sleep()
    state_result = client.get_state()
    rospy.loginfo("Moving around. State : "+str(state_result))
    
i = 0
while i < 3:
    land_topic.publish(Empty())
    rospy.loginfo('Land drone...')
    time.sleep(1)
    i += 1
rospy.loginfo("[Result] State: "+str(state_result))
if state_result == ERROR:
    rospy.logerr("Something went wrong in the Server Side")
if state_result == WARN:
    rospy.logwarn("There is a warning in the Server Side")

#rospy.loginfo("[Result] State: "+str(client.get_result()))