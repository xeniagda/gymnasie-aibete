import random
import numpy as np
from util import *

def agentInput2n(agentInput):
    exp_2 = 2 ** np.arange(11)

    return int((agentInput[:-2] * exp_2[:-2]).sum())

class Qlearner:
    def __init__(self, random_epsilon):
        # TODO: Implement!
        self.q_table = np.random.normal(0, 0.2, size=[2 ** 9, 3])

        # Hur ofta agenten svarar med en slumpmässig action
        self.random_epsilon = random_epsilon

    def getAction(self, agentInput):
        if random.random() < self.random_epsilon:
            action = random.choice([Actions.LEFT, Actions.RIGHT, Actions.JUMP])
            return action
        else:
            n = agentInput2n(agentInput)
            print(n)

            vals = self.q_table[n]
            max_n = np.argmax(vals)

            return [Actions.LEFT, Actions.RIGHT, Actions.JUMP][max_n]

    def update(self, oldAgentInput, action, newAgentInput, reward):
        # Uppdatera q tabellen
        pass
