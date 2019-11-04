import sys
import os.path
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
from random_action_method import *
from levelGenerator import *
import math

experimentLayouts = [{
        "numLevels": 80000,
        "ticksPerLevel": 100,
        "runsPerSet": 20,
        "name": "Premade2-LR0.003-FD0.8-RAMblend-ATdq",
        "levelGenerator": PremadeLevelGenerator(2),
        "parameterSets": [
            {
                "learningRate": lambda t: 0.003,
                "futureDiscount": lambda t: 0.8,
                "randomActionMethod": lambda t: Blend(SingleFrame(0.2), NoRandomness(), 20, 20),
                "agentType": "dq"
            }, {
                "learningRate": lambda t: 0.003,
                "futureDiscount": lambda t: 0.8,
                "randomActionMethod": lambda t: Blend(SingleFrame(0.2), NoRandomness(), 20, 20),
                "agentType": "dq"
            }, {
                "learningRate": lambda t: 0.003,
                "futureDiscount": lambda t: 0.8,
                "randomActionMethod": lambda t: Blend(SingleFrame(0.2), NoRandomness(), 20, 20),
                "agentType": "dq"
            }, {
                "learningRate": lambda t: 0.003,
                "futureDiscount": lambda t: 0.8,
                "randomActionMethod": lambda t: Blend(SingleFrame(0.2), NoRandomness(), 20, 20),
                "agentType": "dq"
            }, {
                "learningRate": lambda t: 0.003,
                "futureDiscount": lambda t: 0.8,
                "randomActionMethod": lambda t: Blend(SingleFrame(0.2), NoRandomness(), 20, 20),
                "agentType": "dq"
            }
        ]
},{
        "numLevels": 80000,
        "ticksPerLevel": 100,
        "runsPerSet": 20,
        "name": "Premade2-LRvar-FD0.8-RAMBlend-ATdq",
        "levelGenerator": PremadeLevelGenerator(2),
        "parameterSets": [
            {
                "learningRate": lambda t: 0.03,
                "futureDiscount": lambda t: 0.8,
                "randomActionMethod": lambda t: Blend(SingleFrame(0.2), NoRandomness(), 20, 20),
                "agentType": "dq"
            },
            {
                "learningRate": lambda t: 0.01,
                "futureDiscount": lambda t: 0.8,
                "randomActionMethod": lambda t: Blend(SingleFrame(0.2), NoRandomness(), 20, 20),
                "agentType": "dq"
            }, {
                "learningRate": lambda t: 0.0055,
                "futureDiscount": lambda t: 0.8,
                "randomActionMethod": lambda t: Blend(SingleFrame(0.2), NoRandomness(), 20, 20),
                "agentType": "dq"
            }, {
                "learningRate": lambda t: 0.003,
                "futureDiscount": lambda t: 0.8,
                "randomActionMethod": lambda t: Blend(SingleFrame(0.2), NoRandomness(), 20, 20),
                "agentType": "dq"
            }, {
                "learningRate": lambda t: 0.001,
                "futureDiscount": lambda t: 0.8,
                "randomActionMethod": lambda t: Blend(SingleFrame(0.2), NoRandomness(), 20, 20),
                "agentType": "dq"
            }
        ]
},{
        "numLevels": 80000,
        "ticksPerLevel": 100,
        "runsPerSet": 20,
        "name": "Premade2-LRvar-FD0.9-RAMBlend-ATdq",
        "levelGenerator": PremadeLevelGenerator(2),
        "parameterSets": [{
                "learningRate": lambda t: 0.3,
                "futureDiscount": lambda t: 0.9,
                "randomActionMethod": lambda t: Blend(SingleFrame(0.2), NoRandomness(), 20, 20),
                "agentType": "dq"
            }, {
                "learningRate": lambda t: 0.1,
                "futureDiscount": lambda t: 0.9,
                "randomActionMethod": lambda t: Blend(SingleFrame(0.2), NoRandomness(), 20, 20),
                "agentType": "dq"
            },
            {
                "learningRate": lambda t: 0.03,
                "futureDiscount": lambda t: 0.9,
                "randomActionMethod": lambda t: Blend(SingleFrame(0.2), NoRandomness(), 20, 20),
                "agentType": "dq"
            },
            {
                "learningRate": lambda t: 0.01,
                "futureDiscount": lambda t: 0.9,
                "randomActionMethod": lambda t: Blend(SingleFrame(0.2), NoRandomness(), 20, 20),
                "agentType": "dq"
            }, {
                "learningRate": lambda t: 0.003,
                "futureDiscount": lambda t: 0.9,
                "randomActionMethod": lambda t: Blend(SingleFrame(0.2), NoRandomness(), 20, 20),
                "agentType": "dq"
            }
        ]
},{
        "numLevels": 80000,
        "ticksPerLevel": 100,
        "runsPerSet": 20,
        "name": "Premade2-LR0.003-FDvar-RAMBlend-ATdq",
        "levelGenerator": PremadeLevelGenerator(2),
        "parameterSets": [
            {
                "learningRate": lambda t: 0.003,
                "futureDiscount": lambda t: 0.99,
                "randomActionMethod": lambda t: Blend(SingleFrame(0.2), NoRandomness(), 20, 20),
                "agentType": "dq"
            }, {
                "learningRate": lambda t: 0.003,
                "futureDiscount": lambda t: 0.95,
                "randomActionMethod": lambda t: Blend(SingleFrame(0.2), NoRandomness(), 20, 20),
                "agentType": "dq"
            }, {
                "learningRate": lambda t: 0.003,
                "futureDiscount": lambda t: 0.9,
                "randomActionMethod": lambda t: Blend(SingleFrame(0.2), NoRandomness(), 20, 20),
                "agentType": "dq"
            }, {
                "learningRate": lambda t: 0.003,
                "futureDiscount": lambda t: 0.8,
                "randomActionMethod": lambda t: Blend(SingleFrame(0.2), NoRandomness(), 20, 20),
                "agentType": "dq"
            }, {
                "learningRate": lambda t: 0.003,
                "futureDiscount": lambda t: 0.5,
                "randomActionMethod": lambda t: Blend(SingleFrame(0.2), NoRandomness(), 20, 20),
                "agentType": "dq"
            }, {
                "learningRate": lambda t: 0.003,
                "futureDiscount": lambda t: 0.2,
                "randomActionMethod": lambda t: Blend(SingleFrame(0.2), NoRandomness(), 20, 20),
                "agentType": "dq"
            }
        ]
},{
        "numLevels": 80000,
        "ticksPerLevel": 100,
        "runsPerSet": 20,
        "name": "Premade2-LRvar2-FD0.8-RAMBlend-ATdq",
        "levelGenerator": PremadeLevelGenerator(2),
        "parameterSets": [
            {
                "learningRate": lambda t: 0.03 if t<0.35 else 0.001,
                "futureDiscount": lambda t: 0.8,
                "randomActionMethod": lambda t: Blend(SingleFrame(0.2), NoRandomness(), 20, 20),
                "agentType": "dq"
            },
            {
                "learningRate": lambda t: 0.03*(1-t)+t*0.001,
                "futureDiscount": lambda t: 0.8,
                "randomActionMethod": lambda t: Blend(SingleFrame(0.2), NoRandomness(), 20, 20),
                "agentType": "dq"
            }, {
                "learningRate": lambda t: math.exp(math.log(0.03)*(1-t)+t*math.log(0.001)),
                "futureDiscount": lambda t: 0.8,
                "randomActionMethod": lambda t: Blend(SingleFrame(0.2), NoRandomness(), 20, 20),
                "agentType": "dq"
            }
        ]
},{
        "numLevels": 20000,
        "ticksPerLevel": 100,
        "runsPerSet": 10,
        "name": "Nena3-LRvar-FD0.8-RAM0.2,6-ATdq",
        "levelGenerator": NenaGenerator(3),
        "parameterSets": [
            {
                "learningRate": lambda t: 0.03,
                "futureDiscount": lambda t: 0.8,
                "randomActionMethod": lambda t: TRandom(0.2, 1 / 6),
                "agentType": "dq"
            }, {
                "learningRate": lambda t: 0.01,
                "futureDiscount": lambda t: 0.8,
                "randomActionMethod": lambda t: TRandom(0.2, 1 / 6),
                "agentType": "dq"
            }, {
                "learningRate": lambda t: 0.0055,
                "futureDiscount": lambda t: 0.8,
                "randomActionMethod": lambda t: TRandom(0.2, 1 / 6),
                "agentType": "dq"
            }, {
                "learningRate": lambda t: 0.003,
                "futureDiscount": lambda t: 0.8,
                "randomActionMethod": lambda t: TRandom(0.2, 1 / 6),
                "agentType": "dq"
            }
        ]
},{
        "numLevels": 20000,
        "ticksPerLevel": 100,
        "runsPerSet": 20,
        "name": "Premade2-LRvar-FD0.8-RAMblend0.15,0.03-ATdueldq",
        "levelGenerator": PremadeLevelGenerator(2),
        "parameterSets": [
            {
                "learningRate": lambda t: 0.001,
                "futureDiscount": lambda t: 0.8,
                "randomActionMethod": lambda t: Blend(SingleFrame(1), NoRandomness(), 0.15, 0.03),
                "agentType": "dueldq"
            }, {
                "learningRate": lambda t: 0.005,
                "futureDiscount": lambda t: 0.8,
                "randomActionMethod": lambda t: Blend(SingleFrame(1), NoRandomness(), 0.15, 0.03),
                "agentType": "dueldq"
            }
        ]
},{
        "numLevels": 20000,
        "ticksPerLevel": 100,
        "runsPerSet": 20,
        "name": "Premade2-RL0.03-FD0.8-RAMvar-dq",
        "levelGenerator": PremadeLevelGenerator(2),
        "parameterSets": [
            {
                "learningRate": lambda t: 0.03,
                "futureDiscount": lambda t: 0.8,
                "randomActionMethod": lambda t: TRandom(0.2, 1 / 6),
                "agentType": "dq"
            }, {
                "learningRate": lambda t: 0.03,
                "futureDiscount": lambda t: 0.8,
                "randomActionMethod": lambda t: Blend(SingleFrame(0.2), NoRandomness(), 20, 20),
                "agentType": "dq"
            }
        ]
}, {
        "numLevels": 20000,
        "ticksPerLevel": 100,
        "runsPerSet": 20,
        "name": "Premade2-LR0.003-FD0.8-RAMBlendvar,6-ATdq",
        "levelGenerator": PremadeLevelGenerator(2),
        "parameterSets": [
            {
                "learningRate": lambda t: 0.003,
                "futureDiscount": lambda t: 0.8,
                "randomActionMethod": lambda t: Blend(SingleFrame(0.2), NoRandomness(), 100, 100),
                "agentType": "dq"
            }, {
                "learningRate": lambda t: 0.003,
                "futureDiscount": lambda t: 0.8,
                "randomActionMethod": lambda t: Blend(SingleFrame(0.2), NoRandomness(), 35, 100),
                "agentType": "dq"
            }, {
                "learningRate": lambda t: 0.003,
                "futureDiscount": lambda t: 0.8,
                "randomActionMethod": lambda t: Blend(SingleFrame(0.2), NoRandomness(), 100, 35),
                "agentType": "dq"
            }
        ]
}, {
        "numLevels": 20000,
        "ticksPerLevel": 100,
        "runsPerSet": 20,
        "name": "Premade2-LR0.003-FD0.8-RAMBlend,epsvar-ATdq",
        "levelGenerator": PremadeLevelGenerator(2),
        "parameterSets": [
            {
                "learningRate": lambda t: 0.003,
                "futureDiscount": lambda t: 0.8,
                "randomActionMethod": lambda t: Blend(SingleFrame(0.2), NoRandomness(), 20, 20),
                "agentType": "dq"
            }, {
                "learningRate": lambda t: 0.003,
                "futureDiscount": lambda t: 0.8,
                "randomActionMethod": lambda t: Blend(SingleFrame(0.4), NoRandomness(), 20, 20),
                "agentType": "dq"
            }, {
                "learningRate": lambda t: 0.003,
                "futureDiscount": lambda t: 0.8,
                "randomActionMethod": lambda t: Blend(SingleFrame(0.6), NoRandomness(), 20, 20),
                "agentType": "dq"
            }, {
                "learningRate": lambda t: 0.003,
                "futureDiscount": lambda t: 0.8,
                "randomActionMethod": lambda t: Blend(SingleFrame(0.8), NoRandomness(), 20, 20),
                "agentType": "dq"
            }, {
                "learningRate": lambda t: 0.003,
                "futureDiscount": lambda t: 0.8,
                "randomActionMethod": lambda t: Blend(SingleFrame(1), NoRandomness(), 20, 20),
                "agentType": "dq"
            }
        ]
}, {
        "numLevels": 80000,
        "ticksPerLevel": 100,
        "runsPerSet": 20,
        "name": "Hole2-LR0.001-FD0.8-RAMvar-ATdq",
        "levelGenerator": HoleGenerator(2),
        "parameterSets": [
            {
                "learningRate": lambda t: 0.001,
                "futureDiscount": lambda t: 0.8,
                "randomActionMethod": lambda t: Blend(SingleFrame(0.2), NoRandomness(), 20, 20),
                "agentType": "dq"
            }, {
                "learningRate": lambda t: 0.001,
                "futureDiscount": lambda t: 0.8,
                "randomActionMethod": lambda t: Blend(SingleFrame(0.05), NoRandomness(), 20, 20),
                "agentType": "dq"
            }, {
                "learningRate": lambda t: 0.001,
                "futureDiscount": lambda t: 0.8,
                "randomActionMethod": lambda t: Blend(MultiFrame(0.05,6), NoRandomness(), 20, 20),
                "agentType": "dq"
            }, {
                "learningRate": lambda t: 0.001,
                "futureDiscount": lambda t: 0.8,
                "randomActionMethod": lambda t: Blend(MultiFrame(0.2,6), NoRandomness(), 20, 20),
                "agentType": "dq"
            }
        ]
}]
