#! /usr/bin/env python

import rospy
import rospkg
from iri_wam_reproduce_trajectory.srv import ExecTraj, ExecTrajRequest
import sys

rospy.init_node('service_client')
rospy.wait_for_service('/execute_trajectory')

exec_traj_service = rospy.ServiceProxy('/execute_trajectory', ExecTraj)
exec_traj_object = ExecTrajRequest()

rospack = rospkg.RosPack()
traj_path = rospack.get_path('iri_wam_reproduce_trajectory') + "/config/get_food.txt"
exec_traj_object.file = traj_path

result = exec_traj_service(exec_traj_object)
# Print the result given by the service called
print result