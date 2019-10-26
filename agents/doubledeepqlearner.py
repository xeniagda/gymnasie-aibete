# Modifierad version av deepqlearner.py, använder double q learing
# Se https://towardsdatascience.com/double-deep-q-networks-905dd8325412, första formuleringen
import os

import tensorflow as tf
import tensorflow.keras as kr

import random
import numpy as np
from util import *

from gameEngine import AGENT_INPUT_SIZE
from experience_replay import ExperienceReplay

SAVE_PATH_A = "deep-q-learner-save-a.h5"
SAVE_PATH_B = "deep-q-learner-save-b.h5"

ER_SIZE = 50000

TRAIN_RATE = 500
BATCH_SIZE = 10240

ACTIONS = [Actions.LEFT, Actions.RIGHT, Actions.JUMP, Actions.NONE]

def elu(x, alpha):
    return np.where(x > 0, x, alpha * (np.exp(x) - 1))

class RLModel(kr.models.Model):
    def __init__(self):
        super(RLModel, self).__init__()
        self.layer1 = kr.layers.Dense(4,
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


class DoubleDeepQlearner:
    def __init__(self, random_action_method,future_discount=0.75,learning_rate=0.001, saveAndLoad=True):
        learning_rate = learning_rate*(1-future_discount)/(1-0.8)

        self.model_a = RLModel()
        self.model_a.build((None, AGENT_INPUT_SIZE))

        self.model_b = RLModel()
        self.model_b.build((None, AGENT_INPUT_SIZE))

        self.saveAndLoad = saveAndLoad

        if os.path.isfile(SAVE_PATH_A) and os.path.isfile(SAVE_PATH_B) and saveAndLoad:
            print("Loading")
            self.model_a.load_weights(SAVE_PATH_A)
            self.model_b.load_weights(SAVE_PATH_B)

        self.exp_rep_a = ExperienceReplay(ER_SIZE, AGENT_INPUT_SIZE)
        self.exp_rep_b = ExperienceReplay(ER_SIZE, AGENT_INPUT_SIZE)

        self.random_action_method = random_action_method

        self.learning_rate = learning_rate
        self.future_discount = future_discount

        self.loss_measure = tf.losses.MeanSquaredError()
        self.opt = tf.optimizers.Adam(lr=self.learning_rate)

        self.n_since_last_train = 0

        self.latestLoss = tf.add(0,0)

    def getAction(self, agentInput):
        rand_action = self.random_action_method.get_random_action()
        if rand_action is not None:
            return rand_action
        else:
            model = random.choice([self.model_a, self.model_b])

            pred = model.call_fast(agentInput)
            return ACTIONS[np.argmax(pred)]

    def update(self, oldAgentInput, action, newAgentInput, reward):
        if random.random() < 0.5:
            self.exp_rep_a.add_experince(oldAgentInput, ACTIONS.index(action), newAgentInput, reward)
        else:
            self.exp_rep_b.add_experince(oldAgentInput, ACTIONS.index(action), newAgentInput, reward)

        self.n_since_last_train += 1

        if self.n_since_last_train > TRAIN_RATE:
            # print("Training")
            loss = self.train_on_random_minibatch()
            #print("Loss =", loss)
            if self.saveAndLoad:
                self.model_a.save_weights(SAVE_PATH_A)
                self.model_b.save_weights(SAVE_PATH_B)

            self.n_since_last_train = 0

    def train_on_random_minibatch(self):
        train_a = random.random() < 0.5

        if train_a:
            input, action, new_input, reward = self.exp_rep_a.get_random_minibatch(BATCH_SIZE)
        else:
            input, action, new_input, reward = self.exp_rep_b.get_random_minibatch(BATCH_SIZE)

        loss = self.train_on_batch(input, action, new_input, reward, train_a)
        return loss.numpy()

    def train_on_batch(self, agent_input_before, action, agent_input_after,
                       reward, train_a):

        if train_a:
            model_t = self.model_a
            model_p = self.model_b
        else:
            model_t = self.model_b
            model_p = self.model_a

        t_best_action = tf.math.argmax(model_t(agent_input_after), axis=1)
        tba_ind = tf.transpose(
            [tf.range(agent_input_before.shape[0]), tf.cast(t_best_action, "int32")])

        q_after = model_p(agent_input_after)

        q_after_max = tf.gather_nd(q_after, tba_ind)
        wanted_q = reward + self.future_discount * q_after_max
        #wanted_q = reward

        tvars = model_t.trainable_variables

        with tf.GradientTape() as tape:
            pred_q_for_all_actions = model_t(agent_input_before)

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
