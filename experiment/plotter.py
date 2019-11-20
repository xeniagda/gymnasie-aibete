import matplotlib.pyplot as plt
from functools import reduce
from operator import add
import math,time
import numpy as np

DESIRED_DATA_POINTS = 20

def averageLists(lists):
    return lists.mean(axis=0)

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
    """chunkSize = 1#len(vals)//15
    res = []
    for i in range(0, len(vals), chunkSize):
        res.append(sum(vals[i:min(i+chunkSize,len(vals))])/(min(i+chunkSize,len(vals))-i))
    return res
    """
    return vals

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
                },color,plotOnlyAverage,experimentData["numLevels"]*experimentData["ticksPerLevel"]/1000)
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
                },color,plotOnlyAverage,experimentData["numLevels"]*experimentData["ticksPerLevel"]/1000)
                color+=1

        rewardSubplot.legend(loc='upper left')
        fig.show()

    
    def plotForPaper(experiments,verticalZoom,plotOnlyAverage=False):

        fig, rewardSubplot = plt.subplots(1,1)
        fig.set_size_inches(5, 5)

        rewardSubplot.set_xlabel('Thousands of ticks played [kt]')
        rewardSubplot.set_ylabel('Reward')

        parameterValueLists = {
            "learningRate":set(),
            "futureDiscount": set(),
            "randomActionMethod": set(),
            "agentType": set(),
        }
        for experimentData in experiments:
            for parameterSetData in experimentData["parameterSets"]:
                for key,val in parameterSetData.items():
                    if key=="results":
                        continue
                    parameterValueLists[key].add(val)

        notInLabel = []

        for key,val in parameterValueLists.items():
            if len(val)==1:
                notInLabel.append(key)


        color = 0
        for experimentData in experiments:
            for parameterSetData in experimentData["parameterSets"]:
                Plotter.addParemterSetToSubplots(parameterSetData,{
                    "reward":rewardSubplot
                },color,plotOnlyAverage,experimentData["numLevels"]*experimentData["ticksPerLevel"]/1000,verticalZoom,notInLabel=notInLabel)
                color+=1

        fig.show()

        rewardSubplot.legend(loc='lower right')

        box = rewardSubplot.get_position()
        rewardSubplot.set_position([box.x0, box.y0, box.width, box.height*0.8])

        # Put a legend to the right of the current axis
        rewardSubplot.legend(loc='lower center', bbox_to_anchor=(0.5, 1))
        fig.savefig("paper/"+experiments[0]["name"]+".png", bbox_inches='tight')


    def addParemterSetToSubplots(parameterSetData,subplots,colorIndex,plotOnlyAverage,ticksPlayed,verticalZoom,haveLabel=True,notInLabel=[]):
        label = []
        if "learningRate" not in notInLabel:
            label.append("LR=" + parameterSetData["learningRate"])
        if "futureDiscount" not in notInLabel:
            label.append("FD=" + parameterSetData["futureDiscount"])
        if "randomActionMethod" not in notInLabel:
            label.append(parameterSetData["randomActionMethod"])
        if "agentType" not in notInLabel:
            label.append(parameterSetData["agentType"])
            
        label = ", ".join(label)

        zippedResults = zipDicts(parameterSetData["results"])
        for key,value in subplots.items():
            if key not in zippedResults:
                continue
            data = np.array(zippedResults[key])

            if not plotOnlyAverage:
                Plotter.addCurvesToSubplot(subplots[key],data[:,:int(data.shape[1]*verticalZoom)],ticksPlayed*verticalZoom,colorIndex)
            
            Plotter.addAverageToSubplot(subplots[key],data[:,:int(data.shape[1]*verticalZoom)],label,colorIndex,ticksPlayed*verticalZoom,haveLabel)

    def addCurvesToSubplot(subplot,dataLists,colorIndex,ticksPlayed):
        for d in dataLists:
            yVals = averageChunks(d)
            xVals = np.linspace(0,ticksPlayed,len(yVals))
            subplot.plot(xVals,yVals,color=("C"+str(colorIndex%10)),alpha=0.2)

    def addAverageToSubplot(subplot,dataLists,label,colorIndex,ticksPlayed,haveLabel):
        yVals = averageChunks(averageLists(dataLists))
        xVals = np.linspace(0,ticksPlayed,len(yVals))
        print(len(yVals))
        if not haveLabel:
            subplot.plot(xVals,yVals,color=("C"+str(colorIndex%10)))
        else:
            subplot.plot(xVals,yVals,color=("C"+str(colorIndex%10)),label=label)

    def getFluctuation(dataList):
        fluct = []
        for i in range(len(dataList)-1):
            if abs(dataList[i+1])+abs(dataList[i])==0:
                fluct.append(1)
            else:
                fluct.append(abs(dataList[i+1]-dataList[i])/(abs(dataList[i+1])+abs(dataList[i])))
        return fluct