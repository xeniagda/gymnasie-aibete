import tensorflow as tf
import tensorflow.keras as kr

import random
import numpy as np
from util import *

FUTURE_DISCOUNT = 0.8**0.01
LEARNING_RATE = 0.01

# Tillåts att gå 10% över denna
SOFT_REPLAY_LIMIT = 1000

TRAIN_RATE = 1000
BATCH_SIZE = 256

ACTIONS = [Actions.LEFT, Actions.RIGHT, Actions.JUMP]


class RLModel(kr.models.Model):
    def __init__(self):
        super(RLModel, self).__init__()
        self.layer1 = kr.layers.Dense(8,
                                      bias_initializer=None,
                                      activation=kr.activations.elu)
        self.layer2 = kr.layers.Dense(3,
                                      bias_initializer=None,
                                      activation=kr.activations.linear)

    def call(self, x):
        x = self.layer1(x)
        x = self.layer2(x)
        return x

class DeepQlearner:
    def __init__(self, random_epsilon):
        self.model = RLModel()
        self.model.build((None, 11))

        # Står om detta i Atari-pappret
        # Basically en pool av alla saker som har hänt i alla spel
        # Varje gång träning händer så dras en slumpmässig batch härifrån
        # Består av: (agent_input, action, agent_input_after, reward)
        self.experience_replay = [
            np.zeros(shape=(0, 3 * 3 + 2)),  # Input
            np.zeros(shape=(0)),  # Action
            np.zeros(shape=(0, 3 * 3 + 2)),  # Input after
            np.zeros(shape=(0)),  # Reward
        ]

        # Hur ofta agenten svarar med en slumpmässig action
        self.random_epsilon = random_epsilon

        self.loss_measure = tf.losses.MeanSquaredError()
        self.opt = tf.optimizers.Adam(lr=LEARNING_RATE)

        self.n_since_last_train = 0

    def getAction(self, agentInput):
        if random.random() < self.random_epsilon:
            action = random.choice(ACTIONS)
            return action
        else:
            pred = self.model(agentInput.reshape(1, 11))
            return ACTIONS[np.argmax(pred[0])]

    def update(self, oldAgentInput, action, newAgentInput, reward):
        # Lägg till i experience_replay
        self.experience_replay[0] = np.concatenate(
            [self.experience_replay[0], [oldAgentInput]], axis=0)
        self.experience_replay[1] = np.concatenate(
            [self.experience_replay[1], [ACTIONS.index(action)]], axis=0)
        self.experience_replay[2] = np.concatenate(
            [self.experience_replay[2], [newAgentInput]], axis=0)
        self.experience_replay[3] = np.concatenate(
            [self.experience_replay[3], [reward]], axis=0)

        # Tillåt 10% över SOFT_REPLAY_LIMIT för att inte göra clean_er varje tick
        # Borde hjälpa performaance, då att ta bort saker i början inte är så billigt
        if len(self.experience_replay[0]) > SOFT_REPLAY_LIMIT * 1.1:
            self.clean_er()

        self.n_since_last_train += 1

        if self.n_since_last_train > TRAIN_RATE:
            print("Training")
            loss = self.train_on_random_minibatch()
            print("Loss =", loss)

            self.n_since_last_train = 0

    def clean_er(self):
        # Begränsa self.experience_replay till de nr_er sista elementen

        self.experience_replay[0] = self.experience_replay[0][
            -SOFT_REPLAY_LIMIT:]
        self.experience_replay[1] = self.experience_replay[1][
            -SOFT_REPLAY_LIMIT:]
        self.experience_replay[2] = self.experience_replay[2][
            -SOFT_REPLAY_LIMIT:]
        self.experience_replay[3] = self.experience_replay[3][
            -SOFT_REPLAY_LIMIT:]

    def train_on_random_minibatch(self):
        idxs = np.random.randint(self.experience_replay[0].shape[0],
                                 size=(BATCH_SIZE, ))

        loss = self.train_on_batch(
            self.experience_replay[0][idxs],
            self.experience_replay[1][idxs],
            self.experience_replay[2][idxs],
            self.experience_replay[3][idxs],
        )
        return loss.numpy()

    def train_on_batch(self, agent_input_before, action, agent_input_after,
                       reward):
        q_after = self.model(agent_input_before)
        wanted_q = reward + FUTURE_DISCOUNT * tf.reduce_max(q_after, axis=1)

        tvars = self.model.trainable_variables

        with tf.GradientTape() as tape:
            pred_q_for_all_actions = self.model(agent_input_before)

            # Indexera med rätt actions
            action_ind = tf.transpose(
                [tf.range(agent_input_before.shape[0]), action])
            pred_q_for_action = tf.gather_nd(pred_q_for_all_actions,
                                             action_ind)

            loss = self.loss_measure(wanted_q, pred_q_for_action)

            gradients = tape.gradient(loss, tvars)
        self.opt.apply_gradients(zip(gradients, tvars))

        return loss
