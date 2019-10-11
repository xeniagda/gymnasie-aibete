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

def averageChunks(vals,chunkSize):
    res = []
    for i in range(0, len(vals), chunkSize):
        res.append(sum(vals[i:i+chunkSize])/chunkSize)
    return res

class Plotter():
    def __init__(self):
        pass

    def startContiniousPlotting(self):
        plt.ion()
        plt.show()
        self.data = []

        while True:
            self.plot(self.data)
            plt.pause(20)
        
    def saveImage(self,data,saveName,plotAll=False):
        plt.figure(figsize=(20,10))
        self.setupPlot(data,plotAll)
        plt.savefig("results/img/"+saveName+".svg",dpi=500)

    def plot(self,data,plotAll=False):
        self.setupPlot(data,plotAll)
        plt.show()

    def setupPlot(self,data,plotAll=False):
        if len(data)==0:
            return
        
        plt.clf()
        chunkSize = 0
        if type(data[0]["loss"][0])==list:
            chunkSize = int(math.ceil(len(data[0]["loss"][0])/DESIRED_DATA_POINTS))
        else:
            chunkSize = int(math.ceil(len(data[0]["loss"])/DESIRED_DATA_POINTS))

        plt.subplot(1,2,1)
        for i,results in enumerate(data):
            if plotAll:
                for j,l in enumerate(results["loss"]):
                    #if j==0:
                    #    plt.plot(averageChunks(l,chunkSize),color=("C"+str(i)), alpha=.5,label=(str(results["random_epsilon"])))
                    #else:
                    plt.plot(averageChunks(l,chunkSize),color=("C"+str(i)), alpha=.2)
            
            plt.plot(averageChunks(averageLists(results["loss"]),chunkSize),color=("C"+str(i)),label=(results["random_epsilon"]+",lr="+results["learning_rate"]))

        plt.title('Loss')
        plt.yscale('log')
        plt.legend(loc='upper left')

        plt.subplot(1,2,2)
        for i,results in enumerate(data):
            if plotAll:
                for j,l in enumerate(results["reward"]):
                    #if j==0:
                    #    plt.plot(averageChunks(l,chunkSize),color=("C"+str(i)), alpha=.5,label=(str(results["random_epsilon"])))
                    #else:
                    plt.plot(averageChunks(l,chunkSize),color=("C"+str(i)), alpha=.2)
            
            plt.plot(averageChunks(averageLists(results["reward"]),chunkSize),color=("C"+str(i)),label=(results["random_epsilon"]+",lr="+results["learning_rate"]))

        plt.title('Reward')
        plt.legend(loc='upper left')


    def updateData(self, data):
        self.data = data