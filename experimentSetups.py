experimentSetups = {
    "premade2-RE0.2,6-LR0.001-FDvar": {
        "numberOfParameterSets": 4,
        "agentsPerParameterSet": 10,
        "gamesPerEvaluation": 20000,
        "parameterSets": [{
            "random_action_method": lambda t: TRandom(0.2, 1 / 6),
            "learning_rate": lambda t: 0.003,
            "future_discount": lambda t: 0.8
        }, {
            "random_action_method": lambda t: TRandom(0.2, 1 / 6),
            "learning_rate": lambda t: 0.001,
            "future_discount": lambda t: 0.8
        }, {
            "random_action_method": lambda t: TRandom(0.2, 1 / 6),
            "learning_rate": lambda t: 0.0003,
            "future_discount": lambda t: 0.8
        }, {
            "random_action_method": lambda t: TRandom(0.2, 1 / 6),
            "learning_rate": lambda t: 0.0001,
            "future_discount": lambda t: 0.8
        }]
    }
}