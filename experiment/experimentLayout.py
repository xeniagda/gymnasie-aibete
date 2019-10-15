import sys
import os.path
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
from random_action_method import *

experimentLayouts = {
    "testExperiment": {
        "numLevels": 1,
        "ticksPerLevel": 12412343,
        "runsPerSet": 4,
        "ticks": 100,
        
        "parameterSets": [
            {
                "parameters": {
                    "learningRate": lambda t: 0,
                    "futureDiscount": lambda t: 0,
                    "randomActionMethod": lambda t: TRandom(0.6*t,1/6),
                }
            }
        ],
    }

}

