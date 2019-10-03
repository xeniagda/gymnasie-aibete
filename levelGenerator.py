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

class IntegerLevelGenerator(LevelGenerator):
    def __init__(self, std_dev,badRatio):
        super(IntegerLevelGenerator, self).__init__()
        self.std_dev = std_dev
        self.badRatio = badRatio

    def generate(self,length):
        level = []
        y = 1
        for i in range(length):
            delta_y = int(round(random.gauss(0, self.std_dev)))
            delta_y = min(2, delta_y)
            if y + delta_y >= 1:
                y += delta_y
            level.append((y,np.random.uniform(0,1)<self.badRatio))

        return level

class FlatLevelGenerator(LevelGenerator):
    def __init__(self):
        super(FlatLevelGenerator, self).__init__()

    def generate(self, length):
        return [(1,0)] * length

class PremadeLevelGenerator(LevelGenerator):
    def __init__(self,index):
        super(PremadeLevelGenerator, self).__init__()
        self.index = index

    def generate(self,length):
        if self.index == 0:
            return list(zip([2,2,2,2,3,2,3,4,3,3,3,4,3,3,3,0,3,3,0,3,3,3,2,5,3,2,2,2,2],[0]*30))
        if self.index == 1:
            return list(zip([3,3,3,3,3,0,0,3,0,3,0,0,3,3,3,3,4,3,3,3,5,3,3,2,5,3,3,3,3,3,3,3,3,0,3,0,0,3,0,3,0,0,3,3,3,3,4,3,3,3,5,3,3,2,5,3,3,3,3,3],[0]*60))
        if self.index == 2:
            return list(zip([3,3,3,3,3,3,0,0,3,3,3,3,3,3,0,0,3,3,3,3,3,3,0,0,3,3,3,3,3,3,0,0,3,3,3,3,3,3,0,0,3,3,3,3,3,3,0,0,3,3,3,3,3,3,0,0,3,3,3,3],
                            [0,0,0,0,0,0,1,1,0,0,0,0,0,0,1,1,0,0,0,0,0,0,1,1,0,0,0,0,0,0,1,1,0,0,0,0,0,0,1,1,0,0,0,0,0,0,1,1,0,0,0,0,0,0,1,1,0,0,0,0]))