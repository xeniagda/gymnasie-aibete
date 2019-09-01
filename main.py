from gameEngine import * 
from agents.randomAgent import *

class Driver:
    def __init__(self,level,agent):
        self.engine = GameEngine(level)
        self.agent = agent
        self.playGame()

    def playGame(self):
        agentState = self.engine.getAgentState()
        while True:
            action = self.agent.getAction(agentState)
            newAgentState,reward,terminate = self.engine.getNextState(action,True)

            self.agent.update(agentState,action,newAgentState,reward)
            if terminate:
                break


def main():
    agent = RandomAgent()
    driver = Driver([1,3,2,4,4,3,1,1,1,1],agent)

main()