

from parameterSet import ParameterSet

import sys
import os.path
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

import levelGenerator
import json
import experimentRunner
from tqdm import tqdm

class Experiment:

        
    def __init__(self, **kwargs):
        self.setup(**kwargs)
        self.settings = kwargs


    def setup(
            self,
            parameterSets, 
            name="experiment", 
            runsPerSet=2, 
            numLevels=10, 
            ticksPerLevel=100, 
            levelGenerator = levelGenerator.FlatLevelGenerator(), 
            **kwargs):

        self.parameterSets = [ParameterSet.loadFromDict(paramSet) for paramSet in parameterSets]
        self.runsPerSet = runsPerSet
        self.ticksPerLevel = ticksPerLevel
        self.numLevels = numLevels
        self.levelGenerator = levelGenerator
        self.name = name
        


    @staticmethod
    def loadFromDict(data):
        return Experiment(**data)

    def saveToFile(self):
        path = "results/data/"+self.name+".json"
        with open(path, "w") as f:            
            f.write(json.dumps({
                **self.settings, "levelGenerator":str(self.levelGenerator), 
                "parameterSets": [paramSet.dictify() for paramSet in self.parameterSets]
            }))
        


    def run(self):
        print("Running experiment " + self.name)
        for paramSet in tqdm(self.parameterSets):
            for i in tqdm(range(self.runsPerSet)):
                experimentRunner.run(paramSet, self.levelGenerator, self.ticksPerLevel, self.numLevels) 
            self.saveToFile()

    def plot(self, plt):
        self.parameterSets
