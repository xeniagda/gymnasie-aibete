import tensorflow as tf
import tensorflow.keras as kr

import random
import numpy as np
from util import *

# Tillåts att gå 10% över denna
SOFT_REPLAY_LIMIT = 10000

class RLModel(kr.models.Model):
    def __init__(self):
        super(RLModel, self).__init__()
        self.layer1 = kr.layers.Dense(8, bias_initializer=None, activation=kr.activations.elu)
        self.layer2 = kr.layers.Dense(3, bias_initializer=None, activation=kr.activations.linear)

    def call(self, x):
        x = self.layer1(x)
        x = self.layer2(x)
        return x

class DeepQlearner:
    def __init__(self, random_epsilon):
        # TODO: Implement!
        self.model = RLModel()
        self.model.build((None, 11))

        # Står om detta i Atari-pappret
        # Basically en pool av alla saker som har hänt i alla spel
        # Varje gång träning händer så dras en slumpmässig batch härifrån
        # Består av: (agent_input, action, agent_input_after, reward)
        self.experience_replay = [
            np.zeros(shape=(0, 3 * 3 + 2)), # Input
            np.zeros(shape=(0)), # Action
            np.zeros(shape=(0, 3 * 3 + 2)), # Input after
            np.zeros(shape=(0)), # Reward
        ]

        # Hur ofta agenten svarar med en slumpmässig action
        self.random_epsilon = random_epsilon

    def getAction(self, agentInput):
        if random.random() < self.random_epsilon:
            action = random.choice([Actions.LEFT, Actions.RIGHT, Actions.JUMP])
            return action
        else:
            # TODO: Ask the model!
            pred = self.model(agentInput.reshape(1, 11))
            return [Actions.LEFT, Actions.RIGHT, Actions.JUMP][np.argmax(pred[0])]

    def update(self, oldAgentInput, action, newAgentInput, reward):
        # Lägg till i experience_replay
        self.experience_replay[0] = np.concatenate(
            [self.experience_replay[0], [oldAgentInput]],
            axis=0
        )
        self.experience_replay[1] = np.concatenate(
            [self.experience_replay[1], [action]],
            axis=0
        )
        self.experience_replay[2] = np.concatenate(
            [self.experience_replay[2], [newAgentInput]],
            axis=0
        )
        self.experience_replay[3] = np.concatenate(
            [self.experience_replay[3], [reward]],
            axis=0
        )

        # Tillåt 10% över SOFT_REPLAY_LIMIT för att inte göra clean_er varje tick
        # Borde hjälpa performaance, då att ta bort saker i början inte är så billigt
        if len(self.experience_replay[0]) > SOFT_REPLAY_LIMIT * 1.1:
            self.clean_er()


    def clean_er(self):
        # Begränsa self.experience_replay till de nr_er sista elementen

        self.experience_replay[0] = self.experience_replay[0][-SOFT_REPLAY_LIMIT:]
        self.experience_replay[1] = self.experience_replay[1][-SOFT_REPLAY_LIMIT:]
        self.experience_replay[2] = self.experience_replay[2][-SOFT_REPLAY_LIMIT:]
        self.experience_replay[3] = self.experience_replay[3][-SOFT_REPLAY_LIMIT:]
