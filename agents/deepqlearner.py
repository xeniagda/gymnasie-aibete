import os

import tensorflow as tf
import tensorflow.keras as kr

import random
import numpy as np
from util import *

from gameEngine import AGENT_INPUT_SIZE
from experience_replay import ExperienceReplay

SAVE_PATH = "deep-q-learner-save.h5"

ER_SIZE = 50000

TRAIN_RATE = 500
BATCH_SIZE = 10240

ACTIONS = [Actions.LEFT, Actions.RIGHT, Actions.JUMP, Actions.NONE]

def elu(x, alpha):
    return np.where(x > 0, x, alpha * (np.exp(x) - 1))

class RLModel(kr.models.Model):
    def __init__(self):
        super(RLModel, self).__init__()
        self.layer1 = kr.layers.Dense(8,
                                      bias_initializer=None,
                                      activation=kr.activations.elu)
        self.layer2 = kr.layers.Dense(4,
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
    def __init__(self, random_action_method,future_discount=0.75,learning_rate=0.001,load_path=None):
        learning_rate = learning_rate*(1-future_discount)/(1-0.8)

        self.model = RLModel()
        self.model.build((None, AGENT_INPUT_SIZE))
        self.load_path = load_path
        if load_path is not None and os.path.isfile(load_path):
            print("Loading")
            self.model.load_weights(load_path)

        self.exp_rep = ExperienceReplay(ER_SIZE, AGENT_INPUT_SIZE)

        self.random_action_method = random_action_method

        self.learning_rate = learning_rate
        self.future_discount = future_discount

        self.loss_measure = tf.losses.MeanSquaredError()
        self.opt = tf.optimizers.Adam(lr=self.learning_rate)

        self.n_since_last_train = 0

        self.latestLoss = tf.add(0,0)

    def getActions(self, agentInputs):
        rand_action = self.random_action_method.get_random_action()
        if rand_action is not None:
            return [rand_action] * agentInputs.shape[0]
        else:
            pred = self.model.call(agentInputs)
            print(pred[0])
            return [ACTIONS[x] for x in np.argmax(pred, axis=1)]

    def update(self, oldAgentInputs, actions, newAgentInputs, rewards):
        # Lägg till i experience_replay

        actions = np.array([ACTIONS.index(action) for action in actions])
        #print(["LEFT","RIGHT","JUMP","NONE"][actions[0]],rewards[0])
        self.exp_rep.add_experinces(oldAgentInputs, actions, newAgentInputs, rewards)

        self.n_since_last_train += oldAgentInputs.shape[0]

        if self.n_since_last_train > TRAIN_RATE:
            loss = self.train_on_random_minibatch()

            self.n_since_last_train = 0

    def train_on_random_minibatch(self):
        input, action, new_input, reward = self.exp_rep.get_random_minibatch(BATCH_SIZE)

        loss = self.train_on_batch(input, action, new_input, reward)
        
        #if self.load_path is not None:
        #    self.save(self.load_path)

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

        self.latestLoss = loss
        return loss

    def save(self, path=SAVE_PATH):
        self.model.save_weights(path)
