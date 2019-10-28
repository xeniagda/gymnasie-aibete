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
from multiGameEngine import MultiGameEngine
from time import sleep

RANDOM_EPSILON = 0.2
RENDER = True
LOG_TIME = False
WORLD_TYPE = levelGenerator.NenaGenerator(1)
WORLD_SIZE = 30

MAX_TIME = 400

totalTicks = 0

# class Driver:
#     def __init__(self,level_size,agent):
#         self.level_size = level_size
#         self.agent = agent
#         self.rewards = []

#         self.startTime = time.time()
#         self.numTicks = 0

#     def play(self):
#         global totalTicks
#         while True:
#             gamelen,reward = playGame(WORLD_TYPE.generate(self.level_size),self.agent,MAX_TIME,RENDER,ui)
#             totalTicks += gamelen
#             if totalTicks%1000==0:
#                 print(totalTicks,round(reward))

ui = UI(RENDER,0.01)

def main():
    # agent = DuelingDQL(TRandom(RANDOM_EPSILON, 1/6), future_discount=0.8, learning_rate=0.04,saveAndLoad=True)
    agent = HumanAgent(ui)

    # driver = Driver(WORLD_SIZE, agent)
    
    # driver.play()

    level = WORLD_TYPE.generate(100)
    ges = MultiGameEngine([level])
    ui.setAgent(agent)

    while True:
        agentInput = None
        action = agent.getAction(agentInput)

        ai, rew = ges.performTick([action])

        ui.setAgentInput(ai[0])
        ui.setReward(rew)
        ge = ges.into_regular_engine(0, ui)
        ui.setGameEngine(ge)

        sleep(ui.sleepTime)


if RENDER:
    threading.Thread(target=main, daemon=True).start()
    ui.main_loop()

main()
