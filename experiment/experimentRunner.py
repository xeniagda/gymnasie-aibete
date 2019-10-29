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

def run(parameterSet,levelGenerator,ticksPerLevel,numLevels):
    #print("Running on parameters:")
    #print(parameterSet)
    random.seed(0)

    agent = None

    if parameterSet.agentType == "dq":
        agent = DeepQlearner(parameterSet.randomActionMethod(0),parameterSet.futureDiscount(0),parameterSet.learningRate(0),False)
    if parameterSet.agentType == "ddq":
        agent = DoubleDeepQlearner(parameterSet.randomActionMethod(0),parameterSet.futureDiscount(0),parameterSet.learningRate(0),False)
    if parameterSet.agentType == "dueldq":
        agent = DuelingDQL(parameterSet.randomActionMethod(0),parameterSet.futureDiscount(0),parameterSet.learningRate(0),False)
    
    loss = []
    reward = []

    for i in range(numLevels // NUM_LEVELS_PARALLEL):
        agent.random_action_method = parameterSet.randomActionMethod(i/(numLevels))
        agent.learning_rate = parameterSet.learningRate(i/(numLevels))
        agent.future_discount = parameterSet.futureDiscount(i/(numLevels))

        levels = [levelGenerator.generate(ticksPerLevel) for _ in range(NUM_LEVELS_PARALLEL)]

        gamePlayer.playGames(levels,agent,ticksPerLevel,False,None)
        

        if i%((numLevels//NUM_LEVELS_PARALLEL)//100+1)==0:
            agent.random_action_method = NoRandomness()
            levels = [levelGenerator.generate(ticksPerLevel) for _ in range(NUM_LEVELS_PARALLEL)]
            playTime,avgReward = gamePlayer.playGames(levels,agent,ticksPerLevel,False,None)
            loss.append(agent.latestLoss.numpy().item())
            reward.append(avgReward)

    parameterSet.addResult(loss,reward)

