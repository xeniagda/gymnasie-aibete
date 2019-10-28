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
        self.add_experinces(
            np.array([input]),
            np.array([action]),
            np.array([input_after]),
            np.array([reward]),
        )

    def add_experinces(self, inputs, actions, inputs_after, rewards):
        number = inputs.shape[0]

        for (write, data) in [
            (self.inputs, inputs),
            (self.actions, actions),
            (self.inputs_after, inputs_after),
            (self.rewards, rewards),
        ]:
            assert data.shape[0] == number

            if number + self.current_index <= self.size:
                write[self.current_index : self.current_index + number] = data
            else:
                write[self.current_index : ] = data[:self.size - self.current_index]
                if number + self.current_index > 2 * self.size:
                    print("You're adding too much stuff to the ER!")
                else:
                    write[:number - self.size + self.current_index] = data[self.size - self.current_index:]

        self.current_index = (self.current_index + number) % self.size
        self.highest = max(self.highest, self.current_index)

    def get_random_minibatch(self, minibatch_size):
        idxs = np.random.randint(self.highest, size=(minibatch_size, ))

        return (
            self.inputs[idxs],
            self.actions[idxs],
            self.inputs_after[idxs],
            self.rewards[idxs],
        )
