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

class MultiFrame(RandomActionMethod):
    def __init__(self, random_epsilon, average_time):
        super(MultiFrame, self).__init__(random_epsilon)
        self.current_action = None
        self.time_lambda = 1 / average_time
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
        return "MultiFrame({},{})".format(self.random_epsilon,int(1/self.time_lambda))

# Backwards compatability!
TRandom = lambda random_epsilon, time_lambda: MultiFrame(random_epsilon, 1 / time_lambda)


class Blend(RandomActionMethod):
    def __init__(self, ram_a, ram_b, average_time_a, average_time_b):
        # random_epsilon does not apply here
        super(Blend, self).__init__(-1)

        self.ram_a = ram_a
        self.ram_b = ram_b

        self.average_time_a = average_time_a
        self.average_time_b = average_time_b

        self.at_a = True
        self.time = 0

    def get_random_action(self):
        self.random_epsilon = -1

        if self.time <= 0:
            # Switch to other
            self.at_a ^= True

            if self.at_a:
                self.time = random.expovariate(1 / self.average_time_a)
            else:
                self.time = random.expovariate(1 / self.average_time_b)

        self.time -= 1

        if self.at_a:
            return self.ram_a.get_random_action()
        else:
            return self.ram_b.get_random_action()

    def __str__(self):
        return "Blend(a={},b={},t_a={},t_b={})".format(
            self.ram_a,
            self.ram_b,
            self.average_time_a,
            self.average_time_b
        )
