import random
from graphics import UI 
import threading
from agents.deepqlearner import *
from agents.humanAgent import *
import levelGenerator
import time,sys
from gamePlayer import *

RANDOM_EPSILON = 0.05
RENDER = True
LOG_TIME = False
WORLD_TYPE = levelGenerator.PremadeLevelGenerator(0)
WORLD_SIZE = 30

MAX_TIME = 2000

class Driver:
    def __init__(self,level_size,agent):
        self.level_size = level_size
        self.agent = agent
        self.rewards = []

        self.startTime = time.time()
        self.numTicks = 0

    def play(self):
        while True:
            playGame(WORLD_TYPE.generate(self.level_size),self.agent,MAX_TIME,RENDER,ui)


ui = UI(RENDER,0.0)

def main():
    agent = HumanAgent(ui)#DeepQlearner(RANDOM_EPSILON)

    driver = Driver(WORLD_SIZE, agent)
    
    driver.play()


if RENDER:
    threading.Thread(target=main, daemon=True).start()
    ui.main_loop()

main()
