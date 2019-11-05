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
    chunkSize = len(vals)//10
    res = []
    for i in range(0, len(vals), chunkSize):
        res.append(sum(vals[i:i+chunkSize])/chunkSize)
    return res

class Plotter():
    def __init__(self):
        pass
    
    def plotExperiments(experiments,plotOnlyAverage=False):

        fig, (lossSubplot,rewardSubplot) = plt.subplots(1,2)
        fig.set_size_inches(18.5, 10.5)

        lossSubplot.set_title('Loss')
        lossSubplot.set_yscale('log')
        rewardSubplot.set_title('Reward')

        color = 0
        for experimentData in experiments:
            for parameterSetData in experimentData["parameterSets"]:
                Plotter.addParemterSetToSubplots(parameterSetData,{
                    "loss":lossSubplot,
                    "reward":rewardSubplot
                },color,plotOnlyAverage)
                color+=1

        lossSubplot.legend(loc='upper left')
        fig.show()
    
    def plotExperimentsWithFluctuation(experiments,plotOnlyAverage=False):

        fig, ((rewardSubplot),(fluctuationSubplot)) = plt.subplots(2,1)
        fig.set_size_inches(18.5, 10.5)

        rewardSubplot.set_title('Reward')
        fluctuationSubplot.set_title('Fluctuation')

        color = 0
        for experimentData in experiments:
            for parameterSetData in experimentData["parameterSets"]:
                for res in parameterSetData["results"]:
                    res["fluctuation"] = Plotter.getFluctuation(res["reward"])

                Plotter.addParemterSetToSubplots(parameterSetData,{
                    "reward":rewardSubplot,
                    "fluctuation":fluctuationSubplot
                },color,plotOnlyAverage)
                color+=1

        rewardSubplot.legend(loc='upper left')
        fig.show()


    def addParemterSetToSubplots(parameterSetData,subplots,colorIndex,plotOnlyAverage):
        label = "LR=" + parameterSetData["learningRate"]
        label += ", FD=" + parameterSetData["futureDiscount"]
        label += ", " + parameterSetData["randomActionMethod"]
        label += ", " + parameterSetData["agentType"]

        zippedResults = zipDicts(parameterSetData["results"])
        for key,value in subplots.items():
            if not plotOnlyAverage:
                Plotter.addCurvesToSubplot(subplots[key],zippedResults[key],colorIndex)
            
            Plotter.addAverageToSubplot(subplots[key],zippedResults[key],label,colorIndex)

    def addCurvesToSubplot(subplot,dataLists,colorIndex):
        for d in dataLists:
            subplot.plot(averageChunks(d),color=("C"+str(colorIndex%10)),alpha=0.2)

    def addAverageToSubplot(subplot,dataLists,label,colorIndex):
        subplot.plot(averageChunks(averageLists(dataLists)),color=("C"+str(colorIndex%10)),label=label)

    def getFluctuation(dataList):
        fluct = []
        for i in range(len(dataList)-1):
            if abs(dataList[i+1])+abs(dataList[i])==0:
                fluct.append(1)
            else:
                fluct.append(abs(dataList[i+1]-dataList[i])/(abs(dataList[i+1])+abs(dataList[i])))
        return fluct