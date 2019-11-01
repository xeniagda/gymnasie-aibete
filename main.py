import random
from graphics import UI 
import threading
from agents.deepqlearner import *
from agents.duelingdql import *
from agents.humanAgent import *
from random_action_method import *
import levelGenerator
import time,sys
from gamePlayer import *


RANDOM_EPSILON = 0.2
RENDER = True
LOG_TIME = False
TRAIN = False
WORLD_TYPE = levelGenerator.PremadeLevelGenerator(1)
WORLD_SIZE = 30

MAX_TIME = 100

totalTicks = 0

N_GAMES = 100

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
            levels = [WORLD_TYPE.generate(self.level_size) for _ in range(N_GAMES)]
            gamelen,reward = playGames(levels,self.agent,MAX_TIME,RENDER,ui,LOG_TIME, TRAIN)
            totalTicks += gamelen
            if totalTicks%1000==0:
                print(totalTicks,round(reward))

ui = UI(RENDER,0.01)

def main():
    path = "results/networks/Premade1-LR0.003-FD0.8-RAM0.2,6-ATdq/paramset_0.h5"
    agent = DeepQlearner(NoRandomness(), future_discount=0.8, learning_rate=0.04,load_path=path)
    # agent = HumanAgent(ui)

    driver = Driver(WORLD_SIZE, agent)
    
    driver.play()


if RENDER:
    threading.Thread(target=main, daemon=True).start()
    ui.main_loop()

main()
