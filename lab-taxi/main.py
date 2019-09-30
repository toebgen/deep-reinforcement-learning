from agent import Agent
from monitor import interact
import gym
import numpy as np
import sys

best_alpha, best_reward = 0., float("-inf")

for i in range(19):
    alpha = 0.05 * i
    print("\ni={}, alpha={}, best_reward={}".format(i, alpha, best_reward))

    env = gym.make('Taxi-v2')
    agent = Agent(alpha=alpha)
    num_episodes = 20000
    avg_rewards, best_avg_reward = interact(env, agent, num_episodes)
    
    if best_avg_reward > best_reward:
        print("Updated best_reward with {}, alpha={}".format(best_avg_reward, alpha))
        best_reward = best_avg_reward
        best_alpha = alpha

print('\n')
print("Result:\nbest_alpha={}, best_reward={}".format(best_alpha, best_reward))