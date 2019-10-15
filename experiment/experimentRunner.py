import sys,random
sys.path.insert(0,'..')
import gamePlayer
from random_action_method import *

def run(parameterSet,levelGenerator,ticksPerLevel,numLevels,agentType):
    random.seed(0)

    agent = None

    if agentType = "dq":
        agent = DeepQlearner(parameterSet.randomEpsilon(0),parameterSet.futureDiscount(0),parameterSet.learningRate(0),False)
    if agentType = "ddq"
        agent = DoubleDeepQlearner(parameterSet.randomEpsilon(0),parameterSet.futureDiscount(0),parameterSet.learningRate(0),False)
    
    loss = []
    reward = []

    for i in range(numLevels):
        agent.random_action_method = parameterSet.randomEpsilon(i/(numGames-1))
        agent.learning_rate = parameterSet.learningRate(i/(numGames-1))
        agent.future_discount = parameterSet.futureDiscount(i/(numGames-1))

        playTime,avgReward = playGame(levelGenerator.generate(ticksPerLevel),agent,GAME_LENGTH,RENDER,ui)

        if i%100:
            agent.random_action_method = NoRandomness()
            playTime,avgReward = playGame(evalLevels[0],agent,GAME_LENGTH,RENDER,ui)

        loss.append(agent.latestLoss.numpy().item())
        reward.append(avgReward)

    parameterSet.addResult(loss,reward)

