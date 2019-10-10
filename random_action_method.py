import random

from util import Actions

ACTIONS = [Actions.LEFT, Actions.RIGHT, Actions.JUMP, Actions.NONE]

class RandomActionMethod:
    def __init__(self, random_random_epsilon):
        self.random_epsilon = random_random_epsilon

    # Give None if no random action should be chosen
    def get_random_action(self):
        raise NotImplementedError("Implement me!")


class SingleFrame(RandomActionMethod):
    def __init__(self, random_epsilon):
        super(SingleFrame, self).__init__(random_epsilon)

    # Give None if no random action should be chosen
    def get_random_action(self):
        if random.random() < self.random_epsilon:
            return random.choice(ACTIONS)
        else:
            return None

    def __str__(self):
        return "SingleFrame(eps={})".format(self.random_epsilon)

class NoRandomness(RandomActionMethod):
    def __init__(self):
        super(NoRandomness, self).__init__(0)

    # Give None if no random action should be chosen
    def get_random_action(self):
        return None

    def __str__(self):
        return "NoRandomness"

class TRandom(RandomActionMethod):
    def __init__(self, random_epsilon, time_lambda):
        super(TRandom, self).__init__(random_epsilon)
        self.current_action = None
        self.time_lambda = time_lambda
        self.time = 0 # ~ Exp(time_lambda)

    # Give None if no random action should be chosen
    def get_random_action(self):
        if self.time > 0:
            self.time -= 1
            return self.current_action

        if random.random() < self.random_epsilon:
            self.current_action = random.choice(ACTIONS)
            self.time = random.expovariate(self.time_lambda)

        return None

    def __str__(self):
        return "TRandom(eps={})".format(self.random_epsilon)
