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

random.seed(11)

RANDOM_EPSILON = 0.2
RENDER = True
LOG_TIME = False
TRAIN = False
WORLD_TYPE = levelGenerator.NenaGenerator(2)
WORLD_SIZE = 60

MAX_TIME = 200

totalTicks = 0

N_GAMES = 1

class Driver:
    def __init__(self,level_size,agent):
        self.level_size = level_size
        self.agent = agent
        self.rewards = []

        self.startTime = time.time()
        self.numTicks = 0

    def play(self):
        global totalTicks

        i = 0
        while True:
            levels = [WORLD_TYPE.generate(self.level_size) for _ in range(N_GAMES)]
            gamelen,reward = playGames(levels,self.agent,MAX_TIME,RENDER,ui,LOG_TIME, TRAIN, i)
            totalTicks += gamelen
            if totalTicks%1000==0:
                print(totalTicks,round(reward))
            i += 1

ui = UI(RENDER,0.06)

def main():
    path = "results/networks/Nena3-LRvar-FD0.8-RAMsingle0.2-ATdq-SER/every_run/paramset-1-run-0/save-80.h5"
    agent = DeepQlearner(NoRandomness(), future_discount=0.8, learning_rate=0.00,load_path=path)
    # agent = HumanAgent(ui)

    driver = Driver(WORLD_SIZE, agent)
    
    driver.play()


if RENDER:
    threading.Thread(target=main, daemon=True).start()
    ui.main_loop()

main()
