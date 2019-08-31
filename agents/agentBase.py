from enum import Enum

class Action(Enum):
    LEFT=0
    RIGHT=1
    JUMP=2

class AgentBase:
    def __init__(self):
        pass

    def getAction(self,agentState):
        raise NotImplementedError("Implement me!")

    def update(self,oldAgentState,action,newAgentState):
        raise NotImplementedError("Implement me!")