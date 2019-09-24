import random
import numpy as np

class LevelGenerator:
    def __init__(self):
        pass

    def generate(self, length):
        raise NotImplementedError("Imprement me!")

class RandomLevelGenerator(LevelGenerator):
    def __init__(self, std_dev,badRatio):
        super(RandomLevelGenerator, self).__init__()
        self.std_dev = std_dev
        self.badRatio = badRatio

    def generate(self,length):
        level = []
        y = 1
        for i in range(length):
            delta_y = random.gauss(0, 2)
            delta_y = min(2, delta_y)
            if y + delta_y >= 1:
                y += delta_y

            if random.random() < 0.2 and len(level) >= 2 and y - level[-2][0] < 2:
                y += 1

            level.append((y,np.random.uniform(0,1)<0.1))

        return level

class FlatLevelGenerator(LevelGenerator):
    def __init__(self):
        super(FlatLevelGenerator, self).__init__()

    def generate(self, length):
        return [(1,0)] * length
