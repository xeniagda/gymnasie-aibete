import random
from graphics import UI 
import threading
from agents.doubledeepqlearner import *
from agents.humanAgent import *
from random_action_method import *
import levelGenerator
import time,sys
from gamePlayer import *


RANDOM_EPSILON = 0.2
RENDER = True
LOG_TIME = False
WORLD_TYPE = levelGenerator.PremadeLevelGenerator(2)
WORLD_SIZE = 30

MAX_TIME = 100

totalTicks = 0

class Driver:
    def __init__(self,level_size,agent):
        self.level_size = level_size
        self.agent = agent
        self.rewards = []

        self.startTime = time.time()
        self.numTicks = 0

    def play(self):
        global totalTicks
        while True:
            gamelen,reward = playGame(WORLD_TYPE.generate(self.level_size),self.agent,MAX_TIME,RENDER,ui)
            totalTicks += gamelen
            if totalTicks%1000==0:
                print(totalTicks,round(reward))

ui = UI(RENDER,0.01)

def main():
    agent = DoubleDeepQlearner(SingleFrame(RANDOM_EPSILON), future_discount=0.8, learning_rate=0.001,fromSave=False)

    driver = Driver(WORLD_SIZE, agent)
    
    driver.play()


if RENDER:
    threading.Thread(target=main, daemon=True).start()
    ui.main_loop()

main()
