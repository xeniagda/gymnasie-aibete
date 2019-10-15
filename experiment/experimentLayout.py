

{
    "testExperiment": {
        "levelGenerator": "randomGenerator(4)",
        
        "runsPerSet": 4,
        "ticks": 100,
        "parameterSets": [
            {
                "parameters": {
                    "learningRate": 0,
                    "futureDiscount": 0,
                    "randomActionMethod": Trandom(0.6,1/6),
                    "runs": 4,
                },
                "results": [
                    {
                        "loss":[],
                        "reward":[]
                    }
                ]
            }
        ],
    }

}