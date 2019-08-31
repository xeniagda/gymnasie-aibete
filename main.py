from gameEngine import GameEngine


class Driver:
    def __init__(self,level,agent):
        self.engine = GameEngine(level)
        self.agent = agent
    def playGame():
        agentState = self.engine.getAgentState()
        while True:
            action = self.agent.getAction(agentState)
            newAgentState,reward,terminate = self.engine.getNextState(action)

            self.agent.update(agentState,action,newAgentState,reward)
            if terminate:
                break

