import random

class LevelGenerator:
    def __init__(self):
        pass

    def generate(self, length):
        raise NotImplementedError("Imprement me!")

class RandomLevelGenerator(LevelGenerator):
    def __init__(self, std_dev):
        super(RandomLevelGenerator, self).__init__()
        self.std_dev = std_dev

    def generate(self,length):
        level = []
        y = 1
        for i in range(length):
            delta_y = int(round(random.gauss(0, 2)))
            delta_y = min(2, delta_y)
            if y + delta_y >= 1:
                y += delta_y
            level.append(y)

        return level

class FlatLevelGenerator(LevelGenerator):
    def __init__(self):
        super(FlatLevelGenerator, self).__init__()

    def generateFlat(self, length):
        return [1] * length
