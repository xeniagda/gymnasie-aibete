import os

import tensorflow as tf
import tensorflow.keras as kr

import random
import numpy as np
from util import *

from gameEngine import AGENT_INPUT_SIZE

SAVE_PATH = "deep-q-learner-save.h5"

# Tillåts att gå 10% över denna
SOFT_REPLAY_LIMIT = 50000

TRAIN_RATE = 500
BATCH_SIZE = 10240

ACTIONS = [Actions.LEFT, Actions.RIGHT, Actions.JUMP]

def elu(x, alpha):
    return np.where(x > 0, x, alpha * (np.exp(x) - 1))

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

    def call_fast(self, x):
        # Om vi bara kör på ett spel, så tar det mer tid att använda tensorflow
        l1k, l1b = self.layer1.kernel.numpy(), self.layer1.bias.numpy()
        # Anta alpha == 1
        x = elu(l1b + np.dot(x, l1k), 1)

        l2k, l2b = self.layer2.kernel.numpy(), self.layer2.bias.numpy()
        x = l2b + np.dot(x, l2k)

        return x


class DeepQlearner:
    def __init__(self, random_epsilon,future_discount=0.75,learning_rate=0.001, fromSave=True):
        self.model = RLModel()
        self.model.build((None, AGENT_INPUT_SIZE))

        if os.path.isfile(SAVE_PATH) and fromSave:
            print("Loading")
            self.model.load_weights(SAVE_PATH)
        else:
            print("Creating new model")

        # Står om detta i Atari-pappret
        # Basically en pool av alla saker som har hänt i alla spel
        # Varje gång träning händer så dras en slumpmässig batch härifrån
        # Består av: (agent_input, action, agent_input_after, reward)
        self.experience_replay = [
            np.zeros(shape=(SOFT_REPLAY_LIMIT, AGENT_INPUT_SIZE)),  # Input
            np.zeros(shape=(SOFT_REPLAY_LIMIT)),  # Action
            np.zeros(shape=(SOFT_REPLAY_LIMIT, AGENT_INPUT_SIZE)),  # Input after
            np.zeros(shape=(SOFT_REPLAY_LIMIT)),  # Reward
        ]
        self.experience_replay_index = 0

        self.random_epsilon = random_epsilon
        self.learning_rate = learning_rate
        self.future_discount = future_discount

        self.loss_measure = tf.losses.MeanSquaredError()
        self.opt = tf.optimizers.Adam(lr=self.learning_rate)

        self.n_since_last_train = 0

        self.t_random = [0, None]  # (time, action)

    def getAction(self, agentInput):
        if random.random() < self.random_epsilon:
            return random.choice(ACTIONS)
            #if self.t_random[0] > 0:
            #    return self.t_random[1]
        else:
            pred = self.model.call_fast(agentInput)
            return ACTIONS[np.argmax(pred)]

    def update(self, oldAgentInput, action, newAgentInput, reward):
        if random.random() < self.random_epsilon:
            self.t_random = [random.random(), random.choice([Actions.LEFT, Actions.RIGHT])]

        self.t_random[0] -= 0.01

        # Lägg till i experience_replay
        self.experience_replay[0][self.experience_replay_index] = oldAgentInput
        self.experience_replay[1][self.experience_replay_index] = ACTIONS.index(action)
        self.experience_replay[2][self.experience_replay_index] = newAgentInput
        self.experience_replay[3][self.experience_replay_index] = reward
        self.experience_replay_index = (self.experience_replay_index+1)%SOFT_REPLAY_LIMIT

        self.n_since_last_train += 1

        if self.n_since_last_train > TRAIN_RATE:
            #print("Training")
            loss = self.train_on_random_minibatch()
            print("Loss =", loss)
            self.model.save_weights(SAVE_PATH)

            self.n_since_last_train = 0

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
        q_after = self.model(agent_input_after)
        wanted_q = reward + self.future_discount * tf.reduce_max(q_after, axis=1)
        #wanted_q = reward

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
