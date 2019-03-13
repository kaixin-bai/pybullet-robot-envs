import os,  inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(os.path.dirname(currentdir))
os.sys.path.insert(0,parentdir)

import pybullet as p
import numpy as np
import copy
import math
import pybullet_data
from math import pi

class iCub:

    def __init__(self, urdfRootPath=currentdir+'/icub_with_hands_pybullet.sdf', timeStep=0.01):
        self.urdfRootPath = urdfRootPath
        self.timeStep = timeStep

        ## CHECK VALUE
        self.maxVelocity = .35
        self.maxForce = 200.
        self.useInverseKinematics = 1
        self.useSimulation = 1
        self.indices_torso = [16,17,18]
        self.indices_left_arm = [19, 20, 21, 22, 24, 25, 26]
        self.indices_right_arm = [30, 31, 32, 34, 35, 36, 37]
        self.indices_head = range(27,30)

        self.home_pos_torso = [0.0, 0.0, 0.0]
        self.home_pos_head = [0.0, 0.0, 0.0]
        ## BUG First two joints seem inverted w.r.t robot
        ## BUG Dirrent elbow sign w.r.t robot
        ## BUG Different sign for second joint for left

        self.home_left_arm = [0.0, pi/3.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        ## BUG First two joints seem inverted w.r.t robot
        self.home_right_arm = [0.0, -pi/4.0, -pi/3.0, pi/2.0, 0.0, 0.0, 0.0]

        self.motorNames = []
        self.motorIndices = []

        self.right_hand_Id = 37

        self.reset()

    def reset(self):
        self.icubId = p.loadSDF(currentdir+"/icub_with_hands_pybullet.sdf")
        self.icubId = self.icubId[0]
        self.numJoints = p.getNumJoints(self.icubId)

        # count = 0;
        # for jointIndex in self.indices_torso:
        #     jointInfo = p.getJointInfo(self.icubId, jointIndex)
        #     qIndex = jointInfo[0]
        #     if qIndex > -1:
        #         self.motorNames.append(str(jointInfo[1]))
        #         self.motorIndices.append(jointIndex)
        #     p.resetJointState(self.icubId, jointIndex, self.home_pos_torso[count])
        #     p.setJointMotorControl2(self.icubId, jointIndex, p.POSITION_CONTROL, targetPosition=self.home_pos_torso[count], force=self.maxForce)
        #     count = count + 1
        #
        # count = 0;
        # for jointIndex in self.indices_left_arm:
        #     jointInfo = p.getJointInfo(self.icubId, jointIndex)
        #     qIndex = jointInfo[0]
        #
        #     if qIndex > -1:
        #         self.motorNames.append(str(jointInfo[1]))
        #         self.motorIndices.append(jointIndex)
        #     p.resetJointState(self.icubId, jointIndex, self.home_left_arm[count])
        #     p.setJointMotorControl2(self.icubId, jointIndex, p.POSITION_CONTROL, targetPosition=self.home_left_arm[count], force=self.maxForce)
        #     print(p.getJointState(self.icubId, jointIndex))
        #     count = count + 1
        # count = 0;
        #
        # for jointIndex in self.indices_right_arm:
        #     jointInfo = p.getJointInfo(self.icubId, jointIndex)
        #     qIndex = jointInfo[0]
        #     if qIndex > -1:
        #         self.motorNames.append(str(jointInfo[1]))
        #         self.motorIndices.append(jointIndex)
        #     p.resetJointState(self.icubId, jointIndex, self.home_right_arm[count])
        #     p.setJointMotorControl2(self.icubId, jointIndex, p.POSITION_CONTROL, targetPosition=self.home_right_arm[count], force=self.maxForce)
        #     count = count + 1
        # count = 0;
        #
        # for jointIndex in self.indices_head:
        #     jointInfo = p.getJointInfo(self.icubId, jointIndex)
        #     qIndex = jointInfo[0]
        #     if qIndex > -1:
        #         self.motorNames.append(str(jointInfo[1]))
        #         self.motorIndices.append(jointIndex)
        #     p.resetJointState(self.icubId, jointIndex, self.home_pos_head[count])
        #     p.setJointMotorControl2(self.icubId, jointIndex, p.POSITION_CONTROL, targetPosition=self.home_pos_head[count], force=self.maxForce)
        #     count = count + 1

    def getActionDimension(self):
         if (self.useInverseKinematics):
             return len(self.motorIndices)
         return 6
    def getObservationDimension(self):
        return len(self.getObservation())

    # def getObservation(self):
    #     observation = []
    #     state = p.getLinkState(self.icubId, self.right_hand_Id)
    #     pos = state[0]
    #     orn = state[1]
    #     euler = p.getEulerFromQuaternion(orn)
    #
    #     print(pos)
    #     print(euler)
    #     observation.extend(list(pos))
    #     observation.extend(list(euler))
    #
    #     return observation
