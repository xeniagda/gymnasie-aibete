import random
from gameEngine import *
from graphics import UI 
import threading
from agents.deepqlearner import *
from agents.doubledeepqlearner import *
from levelGenerator import *
import time,sys
from gamePlayer import *
import json
from random_action_method import *
from plotter import Plotter

RENDER = False
GAME_LENGTH = 100
LOG_EVALUATION = False
CONTINOUS_PLOTTING = False

ui = UI(RENDER,0.0)
plotter = Plotter()

evalLevelGenerator = PremadeLevelGenerator(2)
evalLevels = []
for i in range(4000):
    evalLevels.append(evalLevelGenerator.generate(100))


def strParameterLambda(f):
    s1 = str(f(0))
    s2 = str(f(1))
    if s1==s2:
        return s1
    else:
        return s1+"->"+s2

def evaluate(numGames,random_epsilon, learning_rate, future_discount):
    levelGenerator = PremadeLevelGenerator(2)
    agent = DoubleDeepQlearner(random_epsilon(0),future_discount(0),learning_rate(0),False)

    results = {
        "loss": [],
        "reward":[],
        "random_epsilon":strParameterLambda(random_epsilon),
        "learning_rate":strParameterLambda(learning_rate),
        "future_discount":strParameterLambda(future_discount),
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
        if LOG_EVALUATION and i%100==0:
            print(str(i) + "/"+str(numGames))
        if CONTINOUS_PLOTTING and i%100==0:
            plotter.updateData([results])
        

    return results


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

def saveResults(resultsList,saveName):
    jsonData = json.dumps(resultsList)

    f = open("results/data/" + saveName + ".json","w")
    f.write(jsonData)
    f.close()

def loadResults(saveName):
    with open("results/data/" + saveName + ".json","r") as f:
        return json.loads(f.read())

def mergeResults(resultsListA,resultsListB):
    for results in resultsListB:
        found = False
        for i in range(len(resultsListA)):
            if results["random_epsilon"]==resultsListA[i]["random_epsilon"]:
                found = True
                resultsListA[i]["loss"] += results["loss"]
                resultsListA[i]["reward"] += results["reward"]
                break
        if not found:
            resultsListA.append(results)
    return resultsListA
def main():
    saveName = "premade2-REvar-LR0.001-FD0.8"
    
    resultsList = []#loadResults(saveName)

    resultsList.append(evaluateManyTimes(4,20000,lambda t:TRandom(0.2, 1 / 6),lambda t: 0.001,lambda t: 0.8))
    saveResults(resultsList,saveName)
    resultsList.append(evaluateManyTimes(4,20000,lambda t:TRandom(0.05, 1 / 6),lambda t: 0.001,lambda t: 0.8))
    saveResults(resultsList,saveName)
    resultsList.append(evaluateManyTimes(4,20000,lambda t:SingleFrame(0.05),lambda t: 0.001,lambda t: 0.8))
    saveResults(resultsList,saveName)
    resultsList.append(evaluateManyTimes(4,20000,lambda t:SingleFrame(0.2),lambda t: 0.001,lambda t: 0.8))
    saveResults(resultsList,saveName)
    plotter.saveImage(resultsList,saveName,plotAll=True)

    plotter.plot(resultsList)

if CONTINOUS_PLOTTING:
    threading.Thread(target=main, daemon=True).start()
    plotter.startContiniousPlotting()
else:
    main()
