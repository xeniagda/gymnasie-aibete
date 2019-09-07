
class AgentBase:
    def __init__(self):
        pass

    def getAction(self, agentInput):
        raise NotImplementedError("Implement me!")

    def update(self, oldAgentInput, action, newAgentInput, reward):
        raise NotImplementedError("Implement me!")
