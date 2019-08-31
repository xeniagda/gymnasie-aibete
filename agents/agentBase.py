
class AgentBase:
    def __init__(self):
        pass

    def getAction(self,agentState):
        raise NotImplementedError("Implement me!")

    def update(self,oldAgentState,action,newAgentState,reward):
        raise NotImplementedError("Implement me!")