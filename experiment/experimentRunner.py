import random
import sys
import os.path
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

import gamePlayer
from random_action_method import *

from agents.deepqlearner import DeepQlearner
from agents.doubledeepqlearner import DoubleDeepQlearner


def run(parameterSet,levelGenerator,ticksPerLevel,numLevels,agentType):
    random.seed(0)

    agent = None

    if agentType == "dq":
        agent = DeepQlearner(parameterSet.randomEpsilon(0),parameterSet.futureDiscount(0),parameterSet.learningRate(0),False)
    if agentType == "ddq":
        agent = DoubleDeepQlearner(parameterSet.randomEpsilon(0),parameterSet.futureDiscount(0),parameterSet.learningRate(0),False)
    
    loss = []
    reward = []

    for i in range(numLevels):
        agent.random_action_method = parameterSet.randomEpsilon(i/(numLevels-1))
        agent.learning_rate = parameterSet.learningRate(i/(numLevels-1))
        agent.future_discount = parameterSet.futureDiscount(i/(numLevels-1))

        playTime,avgReward = gamePlayer.playGame(levelGenerator.generate(ticksPerLevel),agent,ticksPerLevel,False,None)

        if i%100:
            agent.random_action_method = NoRandomness()
            playTime,avgReward = gamePlayer.playGame(levelGenerator.generate(ticksPerLevel),agent,ticksPerLevel,False,None)

        loss.append(agent.latestLoss.numpy().item())
        reward.append(avgReward)

    parameterSet.addResult(loss,reward)

