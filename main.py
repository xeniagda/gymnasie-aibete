import random
from gameEngine import *
import graphics
import threading
from agents.deepqlearner import *
from levelGenerator import LevelGenerator

levelGenerator = LevelGenerator()

class Driver:
    def __init__(self,level_size,agent):
        self.level_size = level_size
        self.reset_engine()
        self.agent = agent
        self.playGame()

    def reset_engine(self):
        self.engine = GameEngine(levelGenerator.generateFlat(self.level_size))

    def playGame(self):
        agentInput = self.engine.getAgentInput()
        while True:
            action = self.agent.getAction(agentInput)
            newAgentInput,reward,terminate = self.engine.performTick(action,False)

            self.agent.update(agentInput,action,newAgentInput,reward)
            agentInput = newAgentInput
            if terminate:
                self.reset_engine()



def main():
    agent = DeepQlearner(0.01)
    driver = Driver(30, agent)
    
    graphics.drawGame(driver.engine, 0)

main()

#threading.Thread(target=main, daemon=True).start()
#graphics.init_screen()
#graphics.draw_loop()
