import random
import numpy as np
from util import *

FUTURE_DISCOUNT = 0.8 ** 0.01

def agentInput2n(agentInput):
    exp_2 = 2 ** np.arange(3*3+2)
    agentInput[-1] = agentInput[-1] > 0.5
    agentInput[-2] = agentInput[-2] > 0.5

    return int((agentInput * exp_2).sum())

class Qlearner:
    def __init__(self, random_epsilon):
        # TODO: Implement!
        self.q_table = np.random.normal(0, 0.2, size=[2 ** (3 * 3 + 2), 3])

        # Hur ofta agenten svarar med en slumpmässig action
        self.random_epsilon = random_epsilon

        self.learning_rate = 0.1
        self.t_random = [0, None] # (time, action)

    def getAction(self, agentInput):
        if random.random() < 0.01:
            return Actions.JUMP
        if self.t_random[0] > 0:
            return self.t_random[1]
        else:
            n = agentInput2n(agentInput)
            vals = self.q_table[n]
            max_n = np.argmax(vals)

            return [Actions.LEFT, Actions.RIGHT, Actions.JUMP][max_n]

    def update(self, oldAgentInput, action, newAgentInput, reward):
        if random.random() < self.random_epsilon:
            self.t_random = [0.1, random.choice([Actions.LEFT, Actions.RIGHT])]

        self.t_random[0] -= 0.01

        # Uppdatera q tabellen

        next_vals = self.q_table[agentInput2n(newAgentInput)]
        max_q = next_vals.max()
        q = reward + FUTURE_DISCOUNT * max_q

        old_i = agentInput2n(oldAgentInput)
        self.q_table[old_i][action.value] = \
            self.learning_rate * q + (1 - self.learning_rate) * self.q_table[old_i][action.value]
