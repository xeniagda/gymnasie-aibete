import sys
import os.path
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
from random_action_method import *
from levelGenerator import *

experimentLayouts = [{
        "numLevels": 10,
        "ticksPerLevel": 100,
        "runsPerSet": 4,
        "name": "Premade2-LRvar-FD0.8-RAM0.2,6-dq",
        "levelGenerator": PremadeLevelGenerator(2),
        "parameterSets": [
            {
                "learningRate": lambda t: 0.1,
                "futureDiscount": lambda t: 0.8,
                "randomActionMethod": lambda t: TRandom(0.2, 1 / 6),
                "agentType": "dq"
            }, {
                "learningRate": lambda t: 0.03,
                "futureDiscount": lambda t: 0.8,
                "randomActionMethod": lambda t: TRandom(0.2, 1 / 6),
                "agentType": "ddq"
            }, {
                "learningRate": lambda t: 0.001,
                "futureDiscount": lambda t: 0.8,
                "randomActionMethod": lambda t: TRandom(0.2, 1 / 6),
                "agentType": "dq"
            }
        ]
}]
