import random
from gameEngine import *
from graphics import UI 
import threading
from agents.deepqlearner import *
import levelGenerator
import time,sys

RANDOM_EPSILON = 0.05
RENDER = True
LOG_TIME = False
WORLD_TYPE = levelGenerator.IntegerLevelGenerator(1.5,0.0)
WORLD_SIZE = 30

MAX_TIME = 9000

def playGame(engine,agent):
    if RENDER:
        ui.setGameEngine(engine)
        ui.setAgent(agent)
    agentInput = engine.getAgentInput()

    play_time = 0
    startTime = time.time()

    while True:
        action = agent.getAction(agentInput)
        newAgentInput,reward,terminate = engine.performTick(action, RENDER)

        agent.update(agentInput,action,newAgentInput,reward)
        agentInput = newAgentInput
        if terminate or play_time > MAX_TIME:
            return play_time

        play_time += 1

        if LOG_TIME:
            if play_time%1000==0:
                print("Time: ",round(time.time()-startTime,3))
                startTime = time.time()

        time.sleep(ui.sleepTime)


class Driver:
    def __init__(self,level_size,agent):
        self.level_size = level_size
        self.agent = agent
        self.rewards = []

        self.startTime = time.time()
        self.numTicks = 0

    def play(self):
        while True:
            playGame(GameEngine(ui,WORLD_TYPE.generate(self.level_size)),self.agent)


ui = UI(RENDER)

def main():
    agent = DeepQlearner(RANDOM_EPSILON)

    driver = Driver(WORLD_SIZE, agent)
    
    driver.play()


if RENDER:
    threading.Thread(target=main, daemon=True).start()
    ui.main_loop()

main()
