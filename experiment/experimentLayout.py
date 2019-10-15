import sys
import os.path
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
from random_action_method import *
from levelGenerator import *

experimentLayouts = {
    "testExperiment": {
        "numLevels": 10,
        "ticksPerLevel": 100,
        "runsPerSet": 4,
        "name": "Premade2-LR0-FD0-RAM0.6,6-dq",
        "levelGenerator": PremadeLevelGenerator(2),
        "agentType":"dq",
        "parameterSets": [
            {
                "parameters": {
                    "learningRate": lambda t: 0.1,
                    "futureDiscount": lambda t: 0.8,
                    "randomActionMethod": lambda t: TRandom(0.2,1/6),
                }
            }
        ],
    }

}

