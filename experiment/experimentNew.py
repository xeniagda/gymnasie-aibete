

from ParameterSet import ParameterSet
sys.path.insert(0, "..")
import levelGenerator
import json

class Experiment:

        
    def __init__(self, **kwargs):
        self.setup(kwargs)
        self.settings = kwargs


    def setup(
            self,
            *parameterSets, 
            name="experiment", 
            runsPerSet=1, 
            numLevels=1, 
            ticksPerLevel=12313, 
            levelGenerator = None, 
            agentType="dq", 
            **kwargs):
        self.parameterSets = [ParameterSet.loadFromDict(paramSet) for paramSet in parameterSets]
        self.runsPerSet = runsPerSet
        self.ticksPerLevel = ticksPerLevel
        self.numLevels = numLevels
        self.levelGenerator = levelGenerator
        self.agentType = agentType
        


    @staticmethod
    def loadFromDict(data):
        return Experiment(**data)

    def saveToFile(self, path):
        with open(path, "w") as f:            
            f.write(json.dumps({
                "settings": self.settings, 
                "parameterSets": [paramSet.dictify() for paramSet in self.parameterSets]
            }))
        


    def run(self):
        for paramSet in self.parameterSets:
            run(paramSet, self.levelGenerator, self.ticksPerLevel, self.numLevels, self.agentType) 

    def plot(self, plt):
        self.parameterSets
