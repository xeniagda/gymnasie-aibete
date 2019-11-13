import os,json
from plotter import *
from datetime import datetime

def getExperimentFiles():
    fileNames = list(map(lambda name: name[:-5],os.listdir("results/data")))
    return sorted([(os.path.getmtime("results/data/"+name+".json"),name) for name in fileNames])

def loadResults(saveName):
    with open("results/data/" + saveName + ".json","r") as f:
        return json.loads(f.read())

def main():
    experimentNames = getExperimentFiles()
    while True:
        for i,(modifiedTimestamp, experimentName) in enumerate(experimentNames):
            print(str(i)+": "+experimentName, "("+datetime.utcfromtimestamp(modifiedTimestamp).strftime('%Y-%m-%d %H:%M')+")")
        print(str(len(experimentNames))+": exit")

        choices = list(map(int,input("Your choice:").split(",")))

        if choices[0]==len(experimentNames):
            return

        #Plotter.plotExperiments([loadResults(experimentNames[choice][1]) for choice in choices],plotOnlyAverage=True)

        Plotter.plotForPaper([loadResults(experimentNames[choice][1]) for choice in choices],plotOnlyAverage=True)

main()
