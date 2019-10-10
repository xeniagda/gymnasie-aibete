import random
from gameEngine import *
from graphics import UI 
import threading
from agents.deepqlearner import *
from agents.doubledeepqlearner import *
from levelGenerator import *
import time,sys
from gamePlayer import *
import matplotlib.pyplot as plt
import json
from functools import reduce
from operator import add
from random_action_method import *

RENDER = False
DESIRED_DATA_POINTS = 20
GAME_LENGTH = 100

ui = UI(RENDER,0.0)

evalLevelGenerator = PremadeLevelGenerator(2)
evalLevels = []
for i in range(4000):
    evalLevels.append(evalLevelGenerator.generate(100))

def evaluate(numGames,random_epsilon, learning_rate, future_discount):
    levelGenerator = PremadeLevelGenerator(2)
    agent = DoubleDeepQlearner(random_epsilon(0),future_discount(0),learning_rate(0),False)

    results = {
        "loss": [],
        "reward":[],
        "random_epsilon":str(random_epsilon(0))+"->"+str(random_epsilon(1)),
        "learning_rate":str(learning_rate(0))+"->"+str(learning_rate(1)),
        "future_discount":str(future_discount(0))+"->"+str(future_discount(1)),
    }

    for i in range(numGames):
        agent.random_action_method = random_epsilon(i/(numGames-1))
        agent.learning_rate = learning_rate(i/(numGames-1))
        agent.future_discount = future_discount(i/(numGames-1))
        playTime,avgReward = playGame(levelGenerator.generate(100),agent,GAME_LENGTH,RENDER,ui)

        agent.random_action_method = NoRandomness()
        playTime,avgReward = playGame(evalLevels[0],agent,GAME_LENGTH,RENDER,ui)

       # print(agent.latestLoss.numpy(),avgReward)

        results["loss"].append(agent.latestLoss.numpy().item())
        results["reward"].append(avgReward)
        print(str(i) + "/"+str(numGames))

    return results

def averageLists(lists):
    avg = list(reduce(lambda results1,results2: map(add,results1,results2),lists))
    avg = [s/len(lists) for s in avg]
    return avg

def strParameterLambda(f):
    s1 = str(f(0))
    s2 = str(f(1))
    if s1==s2:
        return s1
    else:
        return s1+"->"+s2

def evaluateManyTimes(numTimes,numGames,random_epsilon, learning_rate, future_discount):
    totResults = {
        "loss": [],
        "reward":[],
        "random_epsilon":strParameterLambda(random_epsilon),
        "learning_rate":strParameterLambda(learning_rate),
        "future_discount":strParameterLambda(future_discount),
    }
    startTime = time.time()
    for i in range(numTimes):
        print(str(i+1)+": ")
        print("Learning rate: ", strParameterLambda(learning_rate))
        print("Future discount: ", strParameterLambda(future_discount))
        print("Randomness: ", strParameterLambda(random_epsilon))
        partialResult = evaluate(numGames,random_epsilon,learning_rate,future_discount)
        totResults["loss"].append(partialResult["loss"])
        totResults["reward"].append(partialResult["reward"])
        secondsLeft = (time.time()-startTime)/(i+1)*numTimes-(time.time()-startTime)
        minutesLeft = math.floor(secondsLeft//60)
        hoursLeft = math.floor(minutesLeft/60)
        print("Time left: ",hoursLeft,"h",minutesLeft%60,"m");
    
    #totResults["loss"] = averageLists(totResults["loss"])
    #totResults["reward"] = averageLists(totResults["reward"])
    return totResults

def averageChunks(vals,chunkSize):
    res = []
    for i in range(0, len(vals), chunkSize):
        res.append(sum(vals[i:i+chunkSize])/chunkSize)
    return res

def saveResults(resultsList,saveName):
    jsonData = json.dumps(resultsList)

    f = open(saveName,"w")
    f.write(jsonData)
    f.close()

def loadResults(saveName):
    with open(saveName,"r") as f:
        return json.loads(f.read())


def showResult(resultsList):
    chunkSize = int(math.ceil(len(resultsList[0]["loss"][0])/DESIRED_DATA_POINTS))

    plt.subplot(1,2,1)
    for results in resultsList:
        plt.plot(averageChunks(averageLists(results["loss"]),chunkSize),label=(str(results["random_epsilon"])))

    plt.title('Loss')
    plt.yscale('log')
    plt.legend(loc='upper left')

    plt.subplot(1,2,2)
    for results in resultsList:
        plt.plot(averageChunks(averageLists(results["reward"]),chunkSize),label=(str(results["random_epsilon"])))

    plt.title('Reward')
    plt.legend(loc='upper left')
    plt.show()

def main():
    saveName = "results/premade2longTraining.json"

    resultsList = []

    """resultsList.append(evaluateManyTimes(1,20000,lambda t:TRandom(0.2, 1 / 6),lambda t: t*0.0001+(1-t)*0.0005,lambda t: 0.8))
    saveResults(resultsList,saveName)
    resultsList.append(evaluateManyTimes(1,20000,lambda t:TRandom(0.05, 1 / 6),lambda t: t*0.0001+(1-t)*0.0005,lambda t: 0.8))
    saveResults(resultsList,saveName)
    resultsList.append(evaluateManyTimes(1,20000,lambda t:SingleFrame(0.05),lambda t: t*0.0001+(1-t)*0.0005,lambda t: 0.8))
    saveResults(resultsList,saveName)"""
    resultsList.append(evaluateManyTimes(1,20000,lambda t:SingleFrame(0.2),lambda t: 0.001,lambda t: 0.8))
    saveResults(resultsList,saveName)

    showResult(resultsList)

if RENDER:
    threading.Thread(target=main, daemon=True).start()
    ui.main_loop()
else:
    main()
