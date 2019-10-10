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

    def plot(self,data):
        if len(data)==0:
            return
        
        plt.clf()
        chunkSize = 0
        if type(data[0]["loss"][0])==list:
            chunkSize = int(math.ceil(len(data[0]["loss"][0])/DESIRED_DATA_POINTS))
        else:
            chunkSize = int(math.ceil(len(data[0]["loss"])/DESIRED_DATA_POINTS))

        plt.subplot(1,2,1)
        for results in data:
            plt.plot(averageChunks(averageLists(results["loss"]),chunkSize),label=(str(results["random_epsilon"])))

        plt.title('Loss')
        plt.yscale('log')
        plt.legend(loc='upper left')

        plt.subplot(1,2,2)
        for results in data:
            plt.plot(averageChunks(averageLists(results["reward"]),chunkSize),label=(str(results["random_epsilon"])))

        plt.title('Reward')
        plt.legend(loc='upper left')
        plt.show()

    def updateData(self, data):
        self.data = data