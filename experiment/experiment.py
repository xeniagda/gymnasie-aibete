

from parameterSet import ParameterSet

import sys
import os
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
            saveEveryRun = False,
            **kwargs):

        self.parameterSets = [ParameterSet.loadFromDict(paramSet) for paramSet in parameterSets]
        self.runsPerSet = runsPerSet
        self.ticksPerLevel = ticksPerLevel
        self.numLevels = numLevels
        self.levelGenerator = levelGenerator
        self.name = name
        self.saveEveryRun = saveEveryRun


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

        network_path = os.path.join("results", "networks", self.name)
        if not os.path.isdir(network_path):
            os.makedirs(network_path)

        for idx, paramSet in tqdm(enumerate(self.parameterSets)):
            save_name = os.path.join(network_path, "best_paramset_" + str(idx) + ".h5")

            best_reward_so_far = 0
            for i in tqdm(range(self.runsPerSet)):
                if self.saveEveryRun:
                    serPath = os.path.join(network_path, "every_run", "paramset-" + str(idx) + "-run-" + str(i))
                    if not os.path.isdir(serPath):
                        os.makedirs(serPath)
                else:
                    serPath = None

                agent, last_reward = experimentRunner.run(
                    paramSet,
                    self.levelGenerator,
                    self.ticksPerLevel,
                    self.numLevels,
                    serPath,
                )

                if last_reward > best_reward_so_far:
                    best_reward_so_far = last_reward
                    agent.save(save_name)

            self.saveToFile()

    def plot(self, plt):
        self.parameterSets
