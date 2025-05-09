import numpy as np
import random
from collections import defaultdict


class QLearningAgent:
    def __init__(self, actions, alpha=0.1, gamma=0.99, epsilon=0.1):
        self.q_table = defaultdict(lambda: np.zeros(len(actions)))
        self.actions = actions
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon

    def choose_action(self, state):
        if random.random() < self.epsilon:
            return random.choice(self.actions)
        return self.actions[np.argmax(self.q_table[state])]

    def update(self, state, action, reward, next_state):
        a_idx = self.actions.index(action)
        next_max = np.max(self.q_table[next_state])
        self.q_table[state][a_idx] += self.alpha * (reward + self.gamma * next_max - self.q_table[state][a_idx])
