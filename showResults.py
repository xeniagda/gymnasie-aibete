import os,json
from plotter import *

plotter = Plotter()

def getResultsNames():
    return list(map(lambda name: name[:-5],os.listdir("results/data")))

def saveResults(resultsList,saveName):
    jsonData = json.dumps(resultsList)

    f = open("results/data/" + saveName + ".json","w")
    f.write(jsonData)
    f.close()

def loadResults(saveName):
    with open("results/data/" + saveName + ".json","r") as f:
        return json.loads(f.read())

def main():

    resultsNames = getResultsNames()
    while True:
        for i,resultsName in enumerate(resultsNames):
            print(str(i)+": "+resultsName)
        print(str(len(resultsNames))+": exit")

        choice = int(input("Your choice:"))

        if choice==len(resultsNames):
            return
        plotter.plot(loadResults(resultsNames[choice]),plotAll=True)

main()