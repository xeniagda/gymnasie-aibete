import random

class LevelGenerator:
    def __init__(self):
        pass

    def generateRandom(self,length=20):
        level = []
        x = 1
        for i in range(length):
            delta_x = int(round(random.gauss(0, 2)))
            delta_x = min(2, delta_x)
            if x + delta_x >= 1:
                x += delta_x
            level.append(x)

        return level
    
    def generateFlat(self,length=20):
        return [1]*length
