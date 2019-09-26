import random
from gameEngine import *
from graphics import UI 
import threading
from agents.deepqlearner import *
from levelGenerator import *
import time,sys
from gamePlayer import *
import matplotlib.pyplot as plt
import json
from functools import reduce
from operator import add

RENDER = False

ui = UI(RENDER,0.0)

levelGenerator = IntegerLevelGenerator(0.5,0.0)
evalLevels = []
for i in range(100):
    evalLevels.append(levelGenerator.generate(100))

def evaluate(numGames,random_epsilon, learning_rate, future_discount):
    levelGenerator = IntegerLevelGenerator(0.5,0.0)
    agent = DeepQlearner(random_epsilon,future_discount,learning_rate,False)

    results = {
        "loss": [],
        "reward":[],
        "random_epsilon":random_epsilon,
        "learning_rate":learning_rate,
        "future_discount":future_discount
    }

    for i in range(numGames):
        agent.random_epsilon = random_epsilon
        playTime,avgReward = playGame(levelGenerator.generate(100),agent,2000,RENDER,ui)

        agent.random_epsilon = 0
        playTime,avgReward = playGame(evalLevels[i],agent,2000,RENDER,ui)

       # print(agent.latestLoss.numpy(),avgReward)

        results["loss"].append(agent.latestLoss.numpy().item())
        results["reward"].append(avgReward)
       # print(str(i) + "/"+str(numGames))

    return results

def averageLists(lists):
    avg = list(reduce(lambda results1,results2: map(add,results1,results2),lists))
    avg = [s/len(lists) for s in avg]
    return avg


def evaluateManyTimes(numTimes,numGames,random_epsilon, learning_rate, future_discount):
    totResults = {
        "loss": [],
        "reward":[],
        "random_epsilon":random_epsilon,
        "learning_rate":learning_rate,
        "future_discount":future_discount
    }
    for i in range(numTimes):
        partialResult = evaluate(numGames,random_epsilon,learning_rate,future_discount)
        totResults["loss"].append(partialResult["loss"])
        totResults["reward"].append(partialResult["reward"])
        print(i+1,random_epsilon)
    
    totResults["loss"] = averageLists(totResults["loss"])
    totResults["reward"] = averageLists(totResults["reward"])
    return totResults

def averageChunks(vals,chunkSize):
    res = []
    for i in range(0, len(vals), chunkSize):
        res.append(sum(vals[i:i+chunkSize])/chunkSize)
    return res

def saveResults(resultsList):
    jsonData = json.dumps(resultsList)

    f = open("latestResults.jsonData","w")
    f.write(jsonData)
    f.close()


def showResult(resultsList):
    saveResults(resultsList)

    plt.subplot(1,2,1)
    for results in resultsList:
        plt.plot(averageChunks(results["loss"],10),label=("η="+str(results["learning_rate"])))

    plt.title('Loss')
    plt.yscale('log')
    plt.legend(loc='upper left')

    plt.subplot(1,2,2)
    for results in resultsList:
        plt.plot(averageChunks(results["reward"],10),label=("η="+str(results["learning_rate"])))

    plt.title('Reward')
    plt.legend(loc='upper left')
    plt.show()

def main():
    
    resultsList = []

    resultsList.append(evaluateManyTimes(20,200,0.05,0.0025,0.8))
    resultsList.append(evaluateManyTimes(20,200,0.05,0.005,0.8))
    resultsList.append(evaluateManyTimes(20,200,0.05,0.01,0.8))

    showResult(resultsList)

if RENDER:
    threading.Thread(target=main, daemon=True).start()
    ui.main_loop()
else:
    main()
