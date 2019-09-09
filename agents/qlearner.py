import random
import os
import time
import numpy as np
from util import *

SAVE_PATH = "q-table-learner.npz"
SAVE_INTERVAL = 10

FUTURE_DISCOUNT = 0.8 ** 0.01

NR_STATES_PER_BLOCK = 2

def agentInput2n(agentInput):
    exp = NR_STATES_PER_BLOCK ** np.arange(3*3+2)

    y = agentInput[-1]
    x = agentInput[-2]
    if NR_STATES_PER_BLOCK == 2:
        if y < 0.5:
            agentInput[-1] = 0
        else:
            agentInput[-1] = 1

        if x < 0.5:
            agentInput[-2] = 0
        else:
            agentInput[-2] = 1

    elif NR_STATES_PER_BLOCK == 3:
        if y < 0.3:
            agentInput[-1] = 0
        elif y < 0.7:
            agentInput[-1] = 1
        else:
            agentInput[-1] = 2

        if x < 0.3:
            agentInput[-2] = 0
        elif x < 0.7:
            agentInput[-2] = 1
        else:
            agentInput[-2] = 2

    return int((agentInput * exp).sum())

class Qlearner:
    def __init__(self, random_epsilon):
        if os.path.isfile(SAVE_PATH):
            print("Reading old q table")
            arch = np.load(SAVE_PATH)
            print(arch.files)
            self.q_table = arch["qtable"]
            print(self.q_table)
        else:
            print("Creating new q table")
            self.q_table = np.random.normal(0, 0.2, size=[NR_STATES_PER_BLOCK ** (3 * 3 + 2), 3])

        # Hur ofta agenten svarar med en slumpmässig action
        self.random_epsilon = random_epsilon

        self.learning_rate = 0.1
        self.t_random = [0, None] # (time, action)

        self.last_save = time.time()

    def getAction(self, agentInput):
        if random.random() < self.random_epsilon:
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

        if time.time() - self.last_save > SAVE_INTERVAL:
            print("Saving q table")
            np.savez_compressed(SAVE_PATH, qtable=self.q_table)
            self.last_save = time.time()
