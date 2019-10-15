

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

