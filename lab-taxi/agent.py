import numpy as np
import random
from collections import defaultdict

class Agent:

    def __init__(self, nA=6, alpha=0.1):
        """ Initialize agent.

        Params
        ======
        - nA: number of actions available to the agent
        """
        self.nA = nA
        self.Q = defaultdict(lambda: np.zeros(self.nA))
        self.epsilon = 0.005
        self.gamma = 1.0
        self.alpha = alpha

    def select_action(self, state):
        """ Given the state, select an action.

        Params
        ======
        - state: the current state of the environment

        Returns
        =======
        - action: an integer, compatible with the task's action space
        """
        if random.random() > self.epsilon:
            # select greedy action with probability epsilon
            return np.argmax(self.Q[state])
        else:
            # otherwise, select an action randomly
            return np.random.choice(self.nA)
        
    def step(self, state, action, reward, next_state, done):
        """ Update the agent's knowledge, using the most recently sampled tuple.

        Params
        ======
        - state: the previous state of the environment
        - action: the agent's previous choice of action
        - reward: last reward received
        - next_state: the current state of the environment
        - done: whether the episode is complete (True or False)
        """

        # estimate in Q-table (for current state, action pair)
        current_Q_estimate = self.Q[state][action]
        # current policy (for next state S')
        policy_s = np.ones(self.nA) * self.epsilon / self.nA
         # greedy action
        policy_s[np.argmax(self.Q[next_state])] = 1 - self.epsilon + (self.epsilon / self.nA)
        # get value of state at next time step
        Q_next = np.dot(self.Q[next_state], policy_s)
        # construct target
        alternative_Q_estimate = reward + (self.gamma * Q_next)
        
        updated_Q = current_Q_estimate + (self.alpha * (alternative_Q_estimate - current_Q_estimate))
        self.Q[state][action] = updated_Q
