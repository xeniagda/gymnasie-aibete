import random
import sys
import os.path
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

import gamePlayer
from random_action_method import *

from agents.deepqlearner import DeepQlearner
from agents.doubledeepqlearner import DoubleDeepQlearner
from agents.duelingdql import DuelingDQL

NUM_LEVELS_PARALLEL = 500
RESULT_RESOLUTION = 0.001


def run(parameterSet,levelGenerator,ticksPerLevel,numLevels,serPath):
    #print("Running on parameters:")
    #print(parameterSet)

    agent = None

    if parameterSet.agentType == "dq":
        agent = DeepQlearner(parameterSet.randomActionMethod(0),parameterSet.futureDiscount(0),parameterSet.learningRate(0),False)
    if parameterSet.agentType == "ddq":
        agent = DoubleDeepQlearner(parameterSet.randomActionMethod(0),parameterSet.futureDiscount(0),parameterSet.learningRate(0),False)
    if parameterSet.agentType == "dueldq":
        agent = DuelingDQL(parameterSet.randomActionMethod(0),parameterSet.futureDiscount(0),parameterSet.learningRate(0),False)
    
    random.seed(0)
    loss = []
    reward = []

    save_n = 0

    for i in range(numLevels // NUM_LEVELS_PARALLEL):
        agent.random_action_method = parameterSet.randomActionMethod(float(i)/(numLevels // NUM_LEVELS_PARALLEL))
        agent.learning_rate = parameterSet.learningRate(float(i)/(numLevels // NUM_LEVELS_PARALLEL))
        agent.future_discount = parameterSet.futureDiscount(float(i)/(numLevels // NUM_LEVELS_PARALLEL))

        levels = [levelGenerator.generate(ticksPerLevel) for _ in range(NUM_LEVELS_PARALLEL)]

        gamePlayer.playGames(levels,agent,ticksPerLevel,False,None)
        

        if i % max(1, int(numLevels / NUM_LEVELS_PARALLEL * RESULT_RESOLUTION)) == 0:
            agent.random_action_method = NoRandomness()
            levels = [levelGenerator.generate(ticksPerLevel) for _ in range(NUM_LEVELS_PARALLEL)]
            playTime,avgReward = gamePlayer.playGames(levels,agent,ticksPerLevel,False,None,train=False)
            loss.append(agent.latestLoss.numpy().item())
            reward.append(avgReward)

            if serPath is not None:
                serSavePath = os.path.join(serPath, "save-" + str(save_n) + ".h5")
                agent.save(serSavePath)

                save_n += 1

    parameterSet.addResult(loss,reward)

    return agent, reward[-1]
