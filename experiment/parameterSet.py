import sys
import os.path
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))


from random_action_method import TRandom

def parameterToString(par):
    strFrom = str(par(0))
    strTo = str(par(1))
    if strFrom == strTo:
        return strFrom
    else:
        return strFrom + "->" + strTo

class ParameterSet:
    def __init__(self,randomActionMethod=TRandom(0.2,1/6),learningRate=0.03,futureDiscount=0.8):
        self.learningRate = learningRate
        self.futureDiscount = futureDiscount
        self.randomActionMethod = randomActionMethod

        self.results = []
    @staticmethod
    def loadFromDict(data):
        res = ParameterSet(**data["parameters"])
        return res
    
    def addResult(self,loss,reward):
        self.results.append({
            "loss":loss,
            "reward":reward
        })

    def getPlotTitle(self):
        return ("LR=" + parameterToString(self.learningRate) + 
        "FD=" + parameterToString(self.futureDiscount) + 
        "RAM=" + parameterToString(self.randomActionMethod))

    def plot(self, pltCtx,plotAllResults=True):
        pltCtx.addData()

    def dictify(self):
        return {
            "learningRate": parameterToString(self.learningRate),
            "futureDiscount": parameterToString(self.futureDiscount),
            "randomActionMethod": parameterToString(self.randomActionMethod),
            "results": self.results
        }
    
    def __str__(self):
        return ("learningRate: " + parameterToString(self.learningRate)+"\n"
        + "futureDiscount: " + parameterToString(self.futureDiscount)+"\n"
        + "randomActionMethod: " + parameterToString(self.randomActionMethod))+"\n"