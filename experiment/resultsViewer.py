import os,json
from plotter import *

def getExperimentNames():
    return list(map(lambda name: name[:-5],os.listdir("results/data")))

def loadResults(saveName):
    with open("results/data/" + saveName + ".json","r") as f:
        return json.loads(f.read())

def main():

    experimentNames = getExperimentNames()
    while True:
        for i,experimentName in enumerate(experimentNames):
            print(str(i)+": "+experimentName)
        print(str(len(experimentNames))+": exit")

        choice = int(input("Your choice:"))

        if choice==len(experimentNames):
            return

        Plotter.plotExperiment(loadResults(experimentNames[choice]))

main()