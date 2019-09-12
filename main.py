import random
from gameEngine import *
import graphics
import threading
from agents.deepqlearner import *
import levelGenerator

RANDOM_EPSILON = 0.005
RENDER = True
WORLD_TYPE = levelGenerator.RandomLevelGenerator(3)
WORLD_SIZE = 30

MAX_TIME = 9000

class Driver:
    def __init__(self,level_size,agent):
        self.level_size = level_size
        self.reset_engine()
        self.agent = agent
        self.rewards = []

        self.playGame()

    def reset_engine(self):
        self.engine = GameEngine(WORLD_TYPE.generate(self.level_size))

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

    def logReward(self,reward):
        self.rewards.append(reward)
        if len(self.rewards)==1000:
            print("Avg reward = ",int(sum(self.rewards)*100))
            self.rewards = []



def main():
    agent = DeepQlearner(RANDOM_EPSILON)
    driver = Driver(WORLD_SIZE, agent)

    if RENDER:
        graphics.drawGame(driver.engine, 0)

if RENDER:
    threading.Thread(target=main, daemon=True).start()
    graphics.init_screen()
    graphics.draw_loop()

main()
