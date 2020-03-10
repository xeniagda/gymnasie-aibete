import sys
import os.path
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
from random_action_method import *
from levelGenerator import *
import math

experimentLayouts = [{
        "numLevels": 40000,
        "ticksPerLevel": 100,
        "runsPerSet": 1,
        "name": "Nena3-LR0.003-FD0.8-RAMsingle0.2-ATdq-SER",
        "levelGenerator": NenaGenerator(3),
        "parameterSets": [
            {
                "learningRate": lambda t: 0.01,
                "futureDiscount": lambda t: 0.8,
                "randomActionMethod": lambda t: SinSingleFrame(0.2),
                "agentType": "dq"
            }
        ],
        "saveEveryRun": True,
},{
        "numLevels": 40000,
        "ticksPerLevel": 100,
        "runsPerSet": 100,
        "name": "Nena3-LR0.003-FD0var-RAMsingle0.2-ATdq",
        "levelGenerator": NenaGenerator(3),
        "parameterSets": [
            {
                "learningRate": lambda t: 0.003,
                "futureDiscount": lambda t: 0.99,
                "randomActionMethod": lambda t: SingleFrame(0.2),
                "agentType": "dq"
            }, {
                "learningRate": lambda t: 0.003,
                "futureDiscount": lambda t: 0.95,
                "randomActionMethod": lambda t: SingleFrame(0.2),
                "agentType": "dq"
            }, {
                "learningRate": lambda t: 0.003,
                "futureDiscount": lambda t: 0.9,
                "randomActionMethod": lambda t: SingleFrame(0.2),
                "agentType": "dq"
            }, {
                "learningRate": lambda t: 0.003,
                "futureDiscount": lambda t: 0.8,
                "randomActionMethod": lambda t: SingleFrame(0.2),
                "agentType": "dq"
            }, {
                "learningRate": lambda t: 0.003,
                "futureDiscount": lambda t: 0.5,
                "randomActionMethod": lambda t: SingleFrame(0.2),
                "agentType": "dq"
            }, {
                "learningRate": lambda t: 0.003,
                "futureDiscount": lambda t: 0.2,
                "randomActionMethod": lambda t: SingleFrame(0.2),
                "agentType": "dq"
            }, {
                "learningRate": lambda t: 0.003,
                "futureDiscount": lambda t: 0.0,
                "randomActionMethod": lambda t: SingleFrame(0.2),
                "agentType": "dq"
            }
        ]
},{
        "numLevels": 40000,
        "ticksPerLevel": 100,
        "runsPerSet": 100,
        "name": "Nena3-LR0.003-FD0.8-RAMepsvar-ATdq",
        "levelGenerator": NenaGenerator(3),
        "parameterSets": [
            {
                "learningRate": lambda t: 0.003,
                "futureDiscount": lambda t: 0.8,
                "randomActionMethod": lambda t: SingleFrame(0),
                "agentType": "dq"
            }, {
                "learningRate": lambda t: 0.003,
                "futureDiscount": lambda t: 0.8,
                "randomActionMethod": lambda t: SingleFrame(0.05),
                "agentType": "dq"
            }, {
                "learningRate": lambda t: 0.003,
                "futureDiscount": lambda t: 0.8,
                "randomActionMethod": lambda t: SingleFrame(0.2),
                "agentType": "dq"
            }, {
                "learningRate": lambda t: 0.003,
                "futureDiscount": lambda t: 0.8,
                "randomActionMethod": lambda t: SingleFrame(0.5),
                "agentType": "dq"
            }, {
                "learningRate": lambda t: 0.003,
                "futureDiscount": lambda t: 0.8,
                "randomActionMethod": lambda t: SingleFrame(1.0),
                "agentType": "dq"
            }
        ]
},{
        "numLevels": 40000,
        "ticksPerLevel": 100,
        "runsPerSet": 100,
        "name": "Nena3-LR0.003-FD0.8-RAMblendVar2-ATdq",
        "levelGenerator": NenaGenerator(3),
        "parameterSets": [
            {
                "learningRate": lambda t: 0.003,
                "futureDiscount": lambda t: 0.8,
                "randomActionMethod": lambda t: NoRandomness(),
                "agentType": "dq"
            },
            {
                "learningRate": lambda t: 0.003,
                "futureDiscount": lambda t: 0.8,
                "randomActionMethod": lambda t: Blend(MultiFrame(0.05,6), NoRandomness(), 20, 20),
                "agentType": "dq"
            }, {
                "learningRate": lambda t: 0.003,
                "futureDiscount": lambda t: 0.8,
                "randomActionMethod": lambda t: Blend(MultiFrame(0.1,6), NoRandomness(), 20, 20),
                "agentType": "dq"
            }, {
                "learningRate": lambda t: 0.003,
                "futureDiscount": lambda t: 0.8,
                "randomActionMethod": lambda t: Blend(MultiFrame(0.2,6), NoRandomness(), 20, 20),
                "agentType": "dq"
            }, {
                "learningRate": lambda t: 0.003,
                "futureDiscount": lambda t: 0.8,
                "randomActionMethod": lambda t: Blend(MultiFrame(0.5,6), NoRandomness(), 20, 20),
                "agentType": "dq"
            }, {
                "learningRate": lambda t: 0.003,
                "futureDiscount": lambda t: 0.8,
                "randomActionMethod": lambda t: Blend(MultiFrame(1,6), NoRandomness(), 20, 20),
                "agentType": "dq"
            }
        ]
},{
        "numLevels": 40000,
        "ticksPerLevel": 100,
        "runsPerSet": 100,
        "name": "Nena3-LR0.003-FD0.8-RAMvar-ATdq",
        "levelGenerator": NenaGenerator(3),
        "parameterSets": [
            {
                "learningRate": lambda t: 0.003,
                "futureDiscount": lambda t: 0.8,
                "randomActionMethod": lambda t: SingleFrame(0.2),
                "agentType": "dq"
            }, {
                "learningRate": lambda t: 0.003,
                "futureDiscount": lambda t: 0.8,
                "randomActionMethod": lambda t: SingleFrame((1-t)*0.95+0.05),
                "agentType": "dq"
            }, {
                "learningRate": lambda t: 0.003,
                "futureDiscount": lambda t: 0.8,
                "randomActionMethod": lambda t: MultiFrame(0.2,6),
                "agentType": "dq"
            }, {
                "learningRate": lambda t: 0.003,
                "futureDiscount": lambda t: 0.8,
                "randomActionMethod": lambda t: Blend(MultiFrame(0.2,6), NoRandomness(), 20, 20),
                "agentType": "dq"
            }, {
                "learningRate": lambda t: 0.003,
                "futureDiscount": lambda t: 0.8,
                "randomActionMethod": lambda t: Blend(SingleFrame(0.2), NoRandomness(), 20, 20),
                "agentType": "dq"
            }, {
                "learningRate": lambda t: 0.003,
                "futureDiscount": lambda t: 0.8,
                "randomActionMethod": lambda t: SingleFrame(1),
                "agentType": "dq"
            },
        ]
},{
        "numLevels": 40000,
        "ticksPerLevel": 100,
        "runsPerSet": 100,
        "name": "Nena3-LR0.003-FD0.8-RAMsingle0.2-ATdq",
        "levelGenerator": NenaGenerator(3),
        "parameterSets": [{
                "learningRate": lambda t: 0.003,
                "futureDiscount": lambda t: 0.8,
                "randomActionMethod": lambda t: SingleFrame(0.2),
                "agentType": "dq"
            }, {
                "learningRate": lambda t: 0.003,
                "futureDiscount": lambda t: 0.8,
                "randomActionMethod": lambda t: SingleFrame(0.2),
                "agentType": "dq"
            }, {
                "learningRate": lambda t: 0.003,
                "futureDiscount": lambda t: 0.8,
                "randomActionMethod": lambda t: SingleFrame(0.2),
                "agentType": "dq"
            }, {
                "learningRate": lambda t: 0.003,
                "futureDiscount": lambda t: 0.8,
                "randomActionMethod": lambda t: SingleFrame(0.2),
                "agentType": "dq"
            }, {
                "learningRate": lambda t: 0.003,
                "futureDiscount": lambda t: 0.8,
                "randomActionMethod": lambda t: SingleFrame(0.2),
                "agentType": "dq"
            }
        ]
},{
        "numLevels": 80000,
        "ticksPerLevel": 100,
        "runsPerSet": 100,
        "name": "Premade2-LRvar-FD0.8-RAMsingle0.2-ATdq",
        "levelGenerator": PremadeLevelGenerator(2),
        "parameterSets": [
            {
                "learningRate": lambda t: 0.03,
                "futureDiscount": lambda t: 0.8,
                "randomActionMethod": lambda t: SingleFrame(0.2),
                "agentType": "dq"
            }, {
                "learningRate": lambda t: 0.01,
                "futureDiscount": lambda t: 0.8,
                "randomActionMethod": lambda t: SingleFrame(0.2),
                "agentType": "dq"
            }, {
                "learningRate": lambda t: 0.003,
                "futureDiscount": lambda t: 0.8,
                "randomActionMethod": lambda t: SingleFrame(0.2),
                "agentType": "dq"
            }, {
                "learningRate": lambda t: 0.001,
                "futureDiscount": lambda t: 0.8,
                "randomActionMethod": lambda t: SingleFrame(0.2),
                "agentType": "dq"
            }
        ]
},{
        "numLevels": 40000,
        "ticksPerLevel": 100,
        "runsPerSet": 100,
        "name": "Premade2-LR0.003-FD0var-RAMsingle0.2-ATdq",
        "levelGenerator": PremadeLevelGenerator(2),
        "parameterSets": [
            {
                "learningRate": lambda t: 0.003,
                "futureDiscount": lambda t: 0.99,
                "randomActionMethod": lambda t: SingleFrame(0.2),
                "agentType": "dq"
            }, {
                "learningRate": lambda t: 0.003,
                "futureDiscount": lambda t: 0.95,
                "randomActionMethod": lambda t: SingleFrame(0.2),
                "agentType": "dq"
            }, {
                "learningRate": lambda t: 0.003,
                "futureDiscount": lambda t: 0.9,
                "randomActionMethod": lambda t: SingleFrame(0.2),
                "agentType": "dq"
            }, {
                "learningRate": lambda t: 0.003,
                "futureDiscount": lambda t: 0.8,
                "randomActionMethod": lambda t: SingleFrame(0.2),
                "agentType": "dq"
            }, {
                "learningRate": lambda t: 0.003,
                "futureDiscount": lambda t: 0.5,
                "randomActionMethod": lambda t: SingleFrame(0.2),
                "agentType": "dq"
            }, {
                "learningRate": lambda t: 0.003,
                "futureDiscount": lambda t: 0.2,
                "randomActionMethod": lambda t: SingleFrame(0.2),
                "agentType": "dq"
            }, {
                "learningRate": lambda t: 0.003,
                "futureDiscount": lambda t: 0.0,
                "randomActionMethod": lambda t: SingleFrame(0.2),
                "agentType": "dq"
            }
        ]
},{
        "numLevels": 40000,
        "ticksPerLevel": 100,
        "runsPerSet": 100,
        "name": "Premade2-LR0.003-FD0.8-RAMepsvar-ATdq",
        "levelGenerator": PremadeLevelGenerator(2),
        "parameterSets": [
            {
                "learningRate": lambda t: 0.003,
                "futureDiscount": lambda t: 0.8,
                "randomActionMethod": lambda t: SingleFrame(0),
                "agentType": "dq"
            }, {
                "learningRate": lambda t: 0.003,
                "futureDiscount": lambda t: 0.8,
                "randomActionMethod": lambda t: SingleFrame(0.05),
                "agentType": "dq"
            }, {
                "learningRate": lambda t: 0.003,
                "futureDiscount": lambda t: 0.8,
                "randomActionMethod": lambda t: SingleFrame(0.2),
                "agentType": "dq"
            }, {
                "learningRate": lambda t: 0.003,
                "futureDiscount": lambda t: 0.8,
                "randomActionMethod": lambda t: SingleFrame(0.5),
                "agentType": "dq"
            }, {
                "learningRate": lambda t: 0.003,
                "futureDiscount": lambda t: 0.8,
                "randomActionMethod": lambda t: SingleFrame(1.0),
                "agentType": "dq"
            }
        ]
},{
        "numLevels": 40000,
        "ticksPerLevel": 100,
        "runsPerSet": 100,
        "name": "Premade2-LR0.003-FD0.8-RAMblendVar2-ATdq",
        "levelGenerator": PremadeLevelGenerator(2),
        "parameterSets": [
            {
                "learningRate": lambda t: 0.003,
                "futureDiscount": lambda t: 0.8,
                "randomActionMethod": lambda t: NoRandomness(),
                "agentType": "dq"
            },
            {
                "learningRate": lambda t: 0.003,
                "futureDiscount": lambda t: 0.8,
                "randomActionMethod": lambda t: Blend(MultiFrame(0.05,6), NoRandomness(), 20, 20),
                "agentType": "dq"
            }, {
                "learningRate": lambda t: 0.003,
                "futureDiscount": lambda t: 0.8,
                "randomActionMethod": lambda t: Blend(MultiFrame(0.1,6), NoRandomness(), 20, 20),
                "agentType": "dq"
            }, {
                "learningRate": lambda t: 0.003,
                "futureDiscount": lambda t: 0.8,
                "randomActionMethod": lambda t: Blend(MultiFrame(0.2,6), NoRandomness(), 20, 20),
                "agentType": "dq"
            }, {
                "learningRate": lambda t: 0.003,
                "futureDiscount": lambda t: 0.8,
                "randomActionMethod": lambda t: Blend(MultiFrame(0.5,6), NoRandomness(), 20, 20),
                "agentType": "dq"
            }, {
                "learningRate": lambda t: 0.003,
                "futureDiscount": lambda t: 0.8,
                "randomActionMethod": lambda t: Blend(MultiFrame(1,6), NoRandomness(), 20, 20),
                "agentType": "dq"
            }
        ]
},{
        "numLevels": 40000,
        "ticksPerLevel": 100,
        "runsPerSet": 100,
        "name": "Premade2-LR0.003-FD0.8-RAMvar-ATdq",
        "levelGenerator": PremadeLevelGenerator(2),
        "parameterSets": [
            {
                "learningRate": lambda t: 0.003,
                "futureDiscount": lambda t: 0.8,
                "randomActionMethod": lambda t: SingleFrame(0.2),
                "agentType": "dq"
            }, {
                "learningRate": lambda t: 0.003,
                "futureDiscount": lambda t: 0.8,
                "randomActionMethod": lambda t: SingleFrame((1-t)*0.95+0.05),
                "agentType": "dq"
            }, {
                "learningRate": lambda t: 0.003,
                "futureDiscount": lambda t: 0.8,
                "randomActionMethod": lambda t: MultiFrame(0.2,6),
                "agentType": "dq"
            }, {
                "learningRate": lambda t: 0.003,
                "futureDiscount": lambda t: 0.8,
                "randomActionMethod": lambda t: Blend(MultiFrame(0.2,6), NoRandomness(), 20, 20),
                "agentType": "dq"
            }, {
                "learningRate": lambda t: 0.003,
                "futureDiscount": lambda t: 0.8,
                "randomActionMethod": lambda t: Blend(SingleFrame(0.2), NoRandomness(), 20, 20),
                "agentType": "dq"
            }, {
                "learningRate": lambda t: 0.003,
                "futureDiscount": lambda t: 0.8,
                "randomActionMethod": lambda t: SingleFrame(1),
                "agentType": "dq"
            },
        ]
},{
        "numLevels": 40000,
        "ticksPerLevel": 100,
        "runsPerSet": 100,
        "name": "Premade2-LR0.003-FD0.8-RAMsingle0.2-ATdq",
        "levelGenerator": PremadeLevelGenerator(2),
        "parameterSets": [{
                "learningRate": lambda t: 0.003,
                "futureDiscount": lambda t: 0.8,
                "randomActionMethod": lambda t: SingleFrame(0.2),
                "agentType": "dq"
            }, {
                "learningRate": lambda t: 0.003,
                "futureDiscount": lambda t: 0.8,
                "randomActionMethod": lambda t: SingleFrame(0.2),
                "agentType": "dq"
            }, {
                "learningRate": lambda t: 0.003,
                "futureDiscount": lambda t: 0.8,
                "randomActionMethod": lambda t: SingleFrame(0.2),
                "agentType": "dq"
            }, {
                "learningRate": lambda t: 0.003,
                "futureDiscount": lambda t: 0.8,
                "randomActionMethod": lambda t: SingleFrame(0.2),
                "agentType": "dq"
            }, {
                "learningRate": lambda t: 0.003,
                "futureDiscount": lambda t: 0.8,
                "randomActionMethod": lambda t: SingleFrame(0.2),
                "agentType": "dq"
            }
        ]
},{
        "numLevels": 40000,
        "ticksPerLevel": 100,
        "runsPerSet": 100,
        "name": "Nena3-LR0.003-FD0.8-RAMepsdec-ATdq",
        "levelGenerator": NenaGenerator(3),
        "parameterSets": [
            {
                "learningRate": lambda t: 0.003,
                "futureDiscount": lambda t: 0.8,
                "randomActionMethod": lambda t: SingleFrame((1-t)*0.95+0.05),
                "agentType": "dq"
            }
        ]
},{
        "numLevels": 40000,
        "ticksPerLevel": 100,
        "runsPerSet": 100,
        "name": "Premade2-LR0.003-FD0.8-RAMepsdec-ATdq",
        "levelGenerator": PremadeLevelGenerator(2),
        "parameterSets": [
            {
                "learningRate": lambda t: 0.003,
                "futureDiscount": lambda t: 0.8,
                "randomActionMethod": lambda t: SingleFrame((1-t)*0.95+0.05),
                "agentType": "dq"
            }
        ]
}]
