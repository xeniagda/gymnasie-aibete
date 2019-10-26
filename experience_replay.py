import numpy as np


class ExperienceReplay:
    def __init__(self, size, input_size):
        self.size = size
        self.inputs = np.zeros(shape=(size, input_size))
        self.actions = np.zeros(shape=(size, ))
        self.inputs_after = np.zeros(shape=(size, input_size))
        self.rewards = np.zeros(shape=(size, ))

        self.current_index = 0

        self.highest = 0

    def add_experince(self, input, action, input_after, reward):
        self.inputs[self.current_index] = input
        self.actions[self.current_index] = action
        self.inputs_after[self.current_index] = input_after
        self.rewards[self.current_index] = reward

        self.current_index = (self.current_index + 1) % self.size
        self.highest = max(self.highest, self.current_index)

    def get_random_minibatch(self, minibatch_size):
        idxs = np.random.randint(self.highest, size=(minibatch_size, ))

        return (
            self.inputs[idxs],
            self.actions[idxs],
            self.inputs_after[idxs],
            self.rewards[idxs],
        )
