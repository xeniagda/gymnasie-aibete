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

            level.append((y,np.random.uniform(0,1)<self.badRatio))

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
        if self.index == 3:
            return list(zip([3,3,3,3,3,3,0,0,3,3,3,3,3,3,0,0,3,3,3,3,3,3,0,0,3,3,3,3,3,3,0,0,3,3,3,3,3,3,0,0,3,3,3,3,3,3,0,0,3,3,3,3,3,3,0,0,3,3,3,3],
                            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]))
    def __str__(self):
        return f"PremadeLevelGenerator({self.index})"

class NenaGenerator(LevelGenerator):
    def __init__(self, difficulty):
        super(NenaGenerator, self).__init__()
        self.modules = []
        if (difficulty > 0): 
            self.modules.extend([
                [[10, 10, 10, 10], [0]*4],
                [[3,4,4,5,5,6,6,7], [0]*8],
                [[7,6,6,5,5,4,4,3], [0]*8], 
                [[0,2,2,4,4,6], [0]*6],
                [[3,4,5,4,2], [0]*5],
                [[6,4,4,2,2,0], [0]*6],
            ])
        if (difficulty > 1): 
            self.modules.extend([
                [[3,3,3,3,0,0,3,3,3,3], [0,0,0,0,1,1,0,0,0,0]],   
                [[7,6,5,6,7], [0,0,1,0,0]],
            ])
        if (difficulty > 2): 
            self.modules.extend([
                [[2, 0, 3, 1, 4, 2, 5], [0, 1, 0, 1, 0, 1, 0]],
                [[4, 0, 0, 3, -1, -1, 2, -2, -2, 1], [0,1, 1, 0, 1, 1, 0, 1, 1, 0]],
                [[0, 2, 0, 0, 0, 2, 0], [0, 1, 0, 0, 0, 1, 0]],
                [[3, 0, 0, 0, 3, 5], [0, 1, 1, 1, 0, 0]],
                [[1, 0, 1, 0, 1, 0, 1], [0, 1, 0, 1, 0, 1, 0]],
            ])
        if (difficulty > 3): 
            self.modules.extend([
                [[3,3,3,1,0,3,1,3,1,0,3], [0,0,0,1,1,0,1,0,1,1,0]]
            ])
    
    def generate(self, length): 
        level = []
        badBlocks = []
        lastModule = [0, 0, 0, 0, 0, 0, 0, 0]

        while len(level) < length:
            module = random.choice(self.modules)
            dif = lastModule[len(lastModule)-1]-module[0][0]
            for j in module[0]: 
                level.append(j+dif)
            for j in module[1]: 
                badBlocks.append(j)
            lastModule = [x+dif for x in module[0]] 

        return list(zip(level, badBlocks))[:length]


class HoleGenerator(LevelGenerator):
    def __init__(self, difficulty):
        super(HoleGenerator, self).__init__()
        self.modules = []
        if (difficulty > 0): 
            self.modules.extend([
                [[3,3,0,0,3,3], [0,0,1,1,0,0]],   
                [[7,6,5,7], [0,0,1,0]],
            ])
        if (difficulty > 1): 
            self.modules.extend([
                [[3,0,0,3,0,3], [0,1,1,0,1,0]],  
                [[3,0,3,0,0,3], [0,1,0,1,1,0]], 
                [[3,0,3,0,0,3], [0,1,0,1,1,0]], 
            ])
        if (difficulty > 2): 
            self.modules.extend([
                [[3,3,3,1,0,3,1,3,1,0,3], [0,0,0,1,1,0,1,0,1,1,0]],
                [[3,0,4,4,0,0,5], [0,1,0,0,1,1,0]], 
                [[3,0,0,2,0,3,3], [0,1,1,0,1,0,0]], 
            ])
    
    def generate(self, length): 
        level = [0] * 5
        badBlocks = [0] * 5
        lastModule = [0, 0, 0, 0, 0, 0, 0, 0]

        while len(level) < length:
            module = random.choice(self.modules)
            dif = lastModule[len(lastModule)-1]-module[0][0]
            for j in module[0]: 
                level.append(j+dif)
            for j in module[1]: 
                badBlocks.append(j)
            lastModule = [x+dif for x in module[0]] 

        return list(zip(level, badBlocks))[:length]
