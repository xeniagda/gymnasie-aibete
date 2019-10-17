import matplotlib.pyplot as plt
from functools import reduce
from operator import add
import math,time

DESIRED_DATA_POINTS = 20

def averageLists(lists):
    if type(lists[0])!=list:
        return lists
    avg = list(reduce(lambda results1,results2: map(add,results1,results2),lists))
    avg = [s/len(lists) for s in avg]
    return avg

def zipDicts(d):
    ret = {}

    for res in d:
        for key, value in res.items():
            if key in ret:
                ret[key].append(value)
            else:
                ret[key] = [value]
    
    return ret

def averageChunks(vals):
    chunkSize = len(vals)//20
    res = []
    for i in range(0, len(vals), chunkSize):
        res.append(sum(vals[i:i+chunkSize])/chunkSize)
    return res

class Plotter():
    def __init__(self):
        pass
    
    def plotExperiment(experimentData,plotOnlyAverage=False):

        fig, (lossSubplot,rewardSubplot) = plt.subplots(1,2)
        fig.set_size_inches(18.5, 10.5)

        lossSubplot.set_title('Loss')
        lossSubplot.set_yscale('log')
        rewardSubplot.set_title('Reward')

        for i,parameterSetData in enumerate(experimentData["parameterSets"]):
            Plotter.addParemterSetToSubplots(parameterSetData,{
                "loss":lossSubplot,
                "reward":rewardSubplot
            },i,plotOnlyAverage)

        lossSubplot.legend(loc='upper left')
        rewardSubplot.legend(loc='upper left')
        fig.show()


    def addParemterSetToSubplots(parameterSetData,subplots,colorIndex,plotOnlyAverage):
        label = "LR=" + parameterSetData["learningRate"]
        label += ", FD=" + parameterSetData["futureDiscount"]
        label += ", " + parameterSetData["randomActionMethod"]
        label += ", " + parameterSetData["agentType"]

        zippedResults = zipDicts(parameterSetData["results"])
        for key,value in zippedResults.items():
            if not plotOnlyAverage:
                Plotter.addCurvesToSubplot(subplots[key],value,colorIndex)
            
            Plotter.addAverageToSubplot(subplots[key],value,label,colorIndex)

    def addCurvesToSubplot(subplot,dataLists,colorIndex):
        for d in dataLists:
            subplot.plot(averageChunks(d),color=("C"+str(colorIndex)),alpha=0.2)

    def addAverageToSubplot(subplot,dataLists,label,colorIndex):
        subplot.plot(averageChunks(averageLists(dataLists)),color=("C"+str(colorIndex)),label=label)