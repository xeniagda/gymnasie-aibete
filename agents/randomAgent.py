from util import *
import random

class RandomAgent:
    def __init__(self):
        pass

    def getAction(self, agentInput):
        if random.randint(1,10)==1:
            return Actions.RIGHT
        else:
            return Actions.JUMP

    def update(self, oldAgentInput, action, newAgentInput, reward):
        pass
