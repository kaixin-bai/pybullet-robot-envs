#add parent dir to find package. Only needed for source code build, pip install doesn't need it.
import os, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
print(currentdir)
parentdir = os.path.dirname(os.path.dirname(currentdir))
os.sys.path.insert(0, parentdir)


from pybullet_robot_envs.envs.icub_envs.icub_reach_gym_env import iCubReachGymEnv
from pybullet_robot_envs import robot_data

import math as m

from baselines import logger
from baselines import deepq

log_dir = '../pybullet_logs/icubreach_deepq'

def callback(lcl, glb):
    is_solved = lcl['t'] > 100 and sum(lcl['episode_rewards'][-101:-1]) / 100 >= 199
    if is_solved:
        print("is solved!")
    return is_solved

def main():

  use_IK = 1
  discreteAction = 1
  use_IK = 1 if discreteAction else use_IK

  icubenv = iCubReachGymEnv(urdfRoot=robot_data.getDataPath(), renders=False, useIK=use_IK, isDiscrete=discreteAction) #gym.make("iCubPush-v0")

  logger.configure(dir=log_dir, format_strs=['stdout','log','csv','tensorboard'])

  act = deepq.learn(env=icubenv,
                    network='mlp',
                    lr=1e-3,
                    total_timesteps=100000,
                    buffer_size=50000,
                    exploration_fraction=0.1,
                    exploration_final_eps=0.02,
                    print_freq=10,
                    callback=callback
                    )

  print("Saving model.pkl to ",log_dir)
  act.save(log_dir+"/model.pkl")

if __name__ == '__main__':
  main()
