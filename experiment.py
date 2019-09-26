import random
from gameEngine import *
from graphics import UI 
import threading
from agents.deepqlearner import *
from levelGenerator import *
import time,sys
from gamePlayer import *
import matplotlib.pyplot as plt

RENDER = False

ui = UI(RENDER,0.0)

levelGenerator = IntegerLevelGenerator(0.5,0.0)
evalLevels = []
for i in range(100):
    evalLevels.append(levelGenerator.generate(100))

def evaluate(games,random_epsilon, learning_rate, future_discount):
    levelGenerator = IntegerLevelGenerator(0.5,0.0)
    agent = DeepQlearner(random_epsilon,future_discount,learning_rate,False)

    results = {
        "loss": [],
       "reward":[]
    }

    for i in range(games):
        agent.random_epsilon = random_epsilon
        playTime,avgReward = playGame(levelGenerator.generate(100),agent,2000,RENDER,ui)

        agent.random_epsilon = 0
        playTime,avgReward = playGame(evalLevels[i],agent,2000,RENDER,ui)

       # print(agent.latestLoss.numpy(),avgReward)

        results["loss"].append(agent.latestLoss.numpy())
        results["reward"].append(avgReward)
        print(str(i) + "/"+str(games))

    return results

def averageChunks(vals,chunkSize):
    res = []
    for i in range(0, len(vals), chunkSize):
        res.append(sum(vals[i:i+chunkSize])/chunkSize)
    return res

def main():
    
    allResults = []

    allResults.append(evaluate(100,0.05,0.0025,0.8))
    allResults.append(evaluate(100,0.05,0.005,0.8))
    allResults.append(evaluate(100,0.05,0.01,0.8))
    
    for results in allResults:
        print(results["loss"])
        print(results["reward"])

        
    plt.subplot(1,2,1)
    for i in range(len(allResults)):
        plt.plot(averageChunks(allResults[i]["loss"],10),label=str(i))

    plt.title('Loss')
    plt.legend(loc='upper left')

    plt.subplot(1,2,2)
    for i in range(len(allResults)):
        plt.plot(averageChunks(allResults[i]["reward"],10),label=str(i))

    plt.title('Reward')
    plt.legend(loc='upper left')
    plt.show()

if RENDER:
    threading.Thread(target=main, daemon=True).start()
    ui.main_loop()
else:
    main()
