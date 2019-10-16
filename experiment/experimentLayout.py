import sys
import os.path
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
from random_action_method import *
from levelGenerator import *

experimentLayout = [{
        "numLevels": 100,
        "ticksPerLevel": 100,
        "runsPerSet": 4,
        "name": "Premade2-LRvar-FD0.8-RAM0.2,6-dq",
        "levelGenerator": PremadeLevelGenerator(2),
        "agentType": "dq",
        "parameterSets": [
            {
                "learningRate": lambda t: 0.1,
                "futureDiscount": lambda t: 0.8,
                "randomActionMethod": lambda t: TRandom(0.2, 1 / 6),
            }, {
                "learningRate": lambda t: 0.03,
                "futureDiscount": lambda t: 0.8,
                "randomActionMethod": lambda t: TRandom(0.2, 1 / 6),
            }, {
                "learningRate": lambda t: 0.001,
                "futureDiscount": lambda t: 0.8,
                "randomActionMethod": lambda t: TRandom(0.2, 1 / 6),
            }
        ],
    }
}]
