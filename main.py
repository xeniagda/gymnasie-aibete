import random
from graphics import UI 
import threading
from agents.doubledeepqlearner import *
from agents.humanAgent import *
from random_action_method import TRandom
import levelGenerator
import time,sys
from gamePlayer import *


RANDOM_EPSILON = 0.2
RENDER = True
LOG_TIME = False
WORLD_TYPE = levelGenerator.PremadeLevelGenerator(2)
WORLD_SIZE = 30

MAX_TIME = 100

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


ui = UI(RENDER,0.01)

def main():
    agent = DoubleDeepQlearner(TRandom(RANDOM_EPSILON, 1 / 6), future_discount=0.95, learning_rate=0.01)

    driver = Driver(WORLD_SIZE, agent)
    
    driver.play()


if RENDER:
    threading.Thread(target=main, daemon=True).start()
    ui.main_loop()

main()
