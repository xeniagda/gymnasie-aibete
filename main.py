from gameEngine import *
from graphics import init_screen, draw_loop
import threading
from agents.qlearner import Qlearner

class Driver:
    def __init__(self,level,agent):
        self.engine = GameEngine(level)
        self.agent = agent
        self.playGame()

    def playGame(self):
        agentInput = self.engine.getAgentInput()
        while True:
            action = self.agent.getAction(agentInput)
            newAgentInput,reward,terminate = self.engine.performTick(action,True)

            self.agent.update(agentInput,action,newAgentInput,reward)
            if terminate:
                break


def main():
    agent = Qlearner(0.1)
    driver = Driver([1,3,2,4,4,3,1,1,1,1],agent)

threading.Thread(target=main, daemon=True).start()
init_screen()
draw_loop()
