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
        return "SingleFramf(ε={})".format(self.random_epsilon)
