#! /usr/bin/env python

import rospy
# Import the service message used by the service /trajectory_by_name
from iri_wam_reproduce_trajectory.srv import ExecTraj, ExecTrajRequest
import sys
import rospkg


# Initialise a ROS node with the name service_client
rospy.init_node('service_client')
# Wait for the service client /trajectory_by_name to be running
rospy.wait_for_service('/execute_trajectory')
# Create the connection to the service
traj_by_name_service = rospy.ServiceProxy('/execute_trajectory', ExecTraj)
# Create an object of type TrajByNameRequest
traj_by_name_object = ExecTrajRequest()
# Fill the variable traj_name of this object with the desired value
rospack = rospkg.RosPack()
# This rospack.get_path() works in the same way as $(find name_of_package) in the launch files.
traj = rospack.get_path('iri_wam_reproduce_trajectory') + "/config/get_food.txt"
traj_by_name_object = ExecTrajRequest()
traj_by_name_object.file = traj
# Send through the connection the name of the trajectory to be executed by the robot
result = traj_by_name_service(traj_by_name_object)
# Print the result given by the service called
print result