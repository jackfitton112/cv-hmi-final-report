#Pybullet simulation of a Assistive Robotic Arm for feeding a person with disabilities

import pybullet as p
import time
import pybullet_data

# Connect to the PyBullet simulator
physicsClient = p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())

# Load the URDF file for the Kuka LBR iiwa robot
robot = p.loadURDF("robot.urdf", [0, 0, 0], useFixedBase=True)

# start the simulation
p.setGravity(0, 0, -9.81)
p.setRealTimeSimulation(1)

# get number of joints in the robot
num_joints = p.getNumJoints(robot)
print("Number of joints in the robot:", num_joints) #5


while True:
    time.sleep(1)

