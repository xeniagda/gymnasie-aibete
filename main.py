import random
from gameEngine import *
from graphics import init_screen, draw_loop
import threading
from agents.qlearner import Qlearner

class Driver:
    def __init__(self,level_size,agent):
        self.level_size = level_size
        self.reset_engine()
        self.agent = agent
        self.playGame()

    def reset_engine(self):
        self.engine = GameEngine(generate_level(self.level_size))

    def playGame(self):
        agentInput = self.engine.getAgentInput()
        while True:
            action = self.agent.getAction(agentInput)
            newAgentInput,reward,terminate = self.engine.performTick(action,True)

            self.agent.update(agentInput,action,newAgentInput,reward)
            agentInput = newAgentInput
            if terminate:
                self.reset_engine()

def generate_level(length=20):
    level = []
    x = 1
    for i in range(length):
        delta_x = int(round(random.gauss(0, 2)))
        delta_x = min(2, delta_x)
        if x + delta_x >= 1:
            x += delta_x
        level.append(x)

    return level

def main():
    agent = Qlearner(0.01)
    driver = Driver(30, agent)

threading.Thread(target=main, daemon=True).start()
init_screen()
draw_loop()
