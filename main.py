import random
from gameEngine import *
from graphics import UI 
import threading
from agents.deepqlearner import *
import levelGenerator
import time,sys

RANDOM_EPSILON = 0.05
RENDER = True
LOG_TIME = True
WORLD_TYPE = levelGenerator.IntegerLevelGenerator(1,0.0)
WORLD_SIZE = 30

MAX_TIME = 9000

class Driver:
    def __init__(self,level_size,agent):
        self.level_size = level_size
        self.reset_engine()
        self.agent = agent
        self.rewards = []

        self.startTime = time.time()
        self.numTicks = 0

    def reset_engine(self):
        self.engine = GameEngine(ui,WORLD_TYPE.generate(self.level_size))
        ui.setGameEngine(self.engine)

    def playGame(self):
        agentInput = self.engine.getAgentInput()

        play_time = 0
        while True:
            action = self.agent.getAction(agentInput)
            newAgentInput,reward,terminate = self.engine.performTick(action, RENDER)

            self.agent.update(agentInput,action,newAgentInput,reward)
            agentInput = newAgentInput
            if terminate or play_time > MAX_TIME:
                self.reset_engine()
                play_time = 0

            play_time += 1

            self.logReward(reward)
            
            if LOG_TIME:
                self.numTicks += 1
                if self.numTicks==1000:
                    print("Time: ",round(time.time()-self.startTime,3))
                    self.startTime = time.time()
                    self.numTicks = 0

            time.sleep(ui.sleepTime)

    def logReward(self,reward):
        self.rewards.append(reward)
        if len(self.rewards)==1000:
            #print("Avg reward = ",int(sum(self.rewards)*100))
            self.rewards = []


ui = UI(RENDER)

def main():
    agent = DeepQlearner(RANDOM_EPSILON)

    driver = Driver(WORLD_SIZE, agent)
    if RENDER:
        ui.setGameEngine(driver.engine)
        ui.setAgent(agent)
    
    driver.playGame()


if RENDER:
    threading.Thread(target=main, daemon=True).start()
    ui.main_loop()

main()
