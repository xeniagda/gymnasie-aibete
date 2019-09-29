import numpy as np
import math
import time
import pygame
from gameEngine import VISION_SIZE, AROUND_RAD, SECONDS_PER_TICK

width, height = size = 720, 600

TIME_PER_FRAME = 0.002

SCALE = 50
# Game units

REWARD_CHANGE_SPEED = 0.5
PLAYER_FOLLOW_MARGINS = 7

AGENT_INPUT_SCALE = 20

class Graphics():
    def __init__(self,screen):
        self.screen = screen
        self.game_engine = None
        self.agent = None
        self.reward = 0

        self.font = pygame.font.SysFont("comicsansms", 72)

        self.delta_x = 0
        self.delta_y = 0

    def setGameEngine(self,game_engine):
        self.game_engine = game_engine

    def setReward(self,reward):
        reward = reward / SECONDS_PER_TICK
        self.reward = self.reward * REWARD_CHANGE_SPEED ** SECONDS_PER_TICK + (1 - REWARD_CHANGE_SPEED ** SECONDS_PER_TICK) * reward

    def set_offset(self):
        player = self.game_engine.player

        if player.x - self.delta_x < PLAYER_FOLLOW_MARGINS:
            self.delta_x = player.x - PLAYER_FOLLOW_MARGINS

        if player.x - self.delta_x > (width - PLAYER_FOLLOW_MARGINS * SCALE) / SCALE:
            self.delta_x = player.x - (width - PLAYER_FOLLOW_MARGINS * SCALE) / SCALE

        if player.y - self.delta_y < PLAYER_FOLLOW_MARGINS:
            self.delta_y = player.y - PLAYER_FOLLOW_MARGINS

        if player.y - self.delta_y > (height - PLAYER_FOLLOW_MARGINS * SCALE) / SCALE:
            self.delta_y = player.y - (height - PLAYER_FOLLOW_MARGINS * SCALE) / SCALE

    def draw(self):
        if self.game_engine == None:
            return

        self.set_offset()

        player = self.game_engine.player

        if self.reward > 0:
            v = min(int(self.reward * 255), 255)
            self.screen.fill((255 - v, 255, 255 - v))
        elif self.reward < 0:
            v = min(int(-self.reward * 255), 255)
            self.screen.fill((255, 255 - v, 255 - v))
        else:
            self.screen.fill((255, 255, 255))

        rec = self.getRect(player.x - self.delta_x, player.y - self.delta_y,
                      player.width, player.height)

        pygame.draw.rect(self.screen, (138, 36, 55), rec)
        pygame.draw.rect(self.screen, (204, 90, 112), rec.inflate(-2, -2))
        pygame.draw.rect(self.screen, (186, 84, 162), rec.inflate(-4, -4))

        for x, (wallHeight,isBad) in enumerate(self.game_engine.level):
            rec = self.getRect(x - self.delta_x, 0, 1, wallHeight - self.delta_y)
            col_outer = (38, 95, 133)
            col_inner = (107, 164, 201)
            if isBad:
                col_outer = (133, 50, 10)
                col_inner = (201, 80, 47)

            if self.screen.get_bounding_rect().colliderect(rec):
                pygame.draw.rect(self.screen, col_outer, rec)
                pygame.draw.rect(self.screen, col_inner, rec.inflate(-2, -2))

        ### Rita agentInput

        rec = pygame.Rect(AGENT_INPUT_SCALE*(VISION_SIZE-1)/2, AGENT_INPUT_SCALE*(VISION_SIZE-1)/2, AGENT_INPUT_SCALE, AGENT_INPUT_SCALE)
                
        pygame.draw.rect(self.screen, (0,0,255), rec)

        agentInput = self.game_engine.getAgentInput()

        for y in range(VISION_SIZE):
            for x in range(VISION_SIZE):

                rec = pygame.Rect(x * AGENT_INPUT_SCALE, (VISION_SIZE-1)*AGENT_INPUT_SCALE-y * AGENT_INPUT_SCALE, AGENT_INPUT_SCALE, AGENT_INPUT_SCALE)
                # Visa bakgrunden igenom
                inp = agentInput[y * VISION_SIZE + x]

                # RGB, 0..1
                col = np.zeros((3, ))
                if inp > 0:
                    col = np.array([1 - inp, 1 - inp, 1 - inp])
                else:
                    col = np.array([1, 1 + inp, 1 + inp])

                col_back = (col + np.array([0.5, 0.5, 0.5])) / 2
                if x == y == AROUND_RAD:
                    col_back = (col + np.array([0, 0, 1])) / 2
                    rec = rec.inflate(-2, -2)

                pygame.draw.rect(self.screen, (int(col_back [0] * 255), int(col_back [1] * 255), int(col_back [2] * 255)), rec)
                pygame.draw.rect(self.screen, (int(col[0] * 255), int(col[1] * 255), int(col[2] * 255)), rec.inflate(-2, -2))
        

        #Rita text
        if self.agent != None:
            self.screen.blit(self.font.render(str(self.agent.random_epsilon), True, (0, 128, 0)),(0,0))

        #if agent!=None:
            #print(agent.random_epsilon)

        pygame.display.flip()

    def getRect(self,x,y,w,h):
        return pygame.Rect(int(x*SCALE),int(height-(y+h)*SCALE),math.ceil(w*SCALE+1),math.ceil(h*SCALE+1))
    

class UI():
    def __init__(self,RENDER,sleepTime):
        self.screen = None
        self.game_engine = None
        self.agent = None
        self.done = False
        self.RENDER = RENDER
        if RENDER:
            pygame.init()
            pygame.display.set_caption("Title")

            self.screen = pygame.display.set_mode(size)

            self.graphics = Graphics(self.screen)

        self.sleepTime = sleepTime

        self.pressedKeys = set()

    def setGameEngine(self,ge):
        if not self.RENDER:
            return
        self.game_engine = ge
        self.graphics.setGameEngine(ge)

    def setAgent(self,ag):
        if not self.RENDER:
            return
        self.agent = ag

    def setReward(self,reward):
        if not self.RENDER:
            return
        self.graphics.setReward(reward)

    def handleInput(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                self.pressedKeys.add(event.key)
                #print(event.key)
                if event.key == 97: # A, slow down
                    self.sleepTime = (self.sleepTime+0.001)*1.4-0.001
                if event.key == 100: # D, speed up
                    self.sleepTime = (self.sleepTime+0.001)/1.4-0.001
                    self.sleepTime = max(0,self.sleepTime)
                if event.key == 119: # W, more random
                    self.agent.random_epsilon += 0.01
                if event.key == 115: # S, less random
                    self.agent.random_epsilon -= 0.01
                    self.agent.random_epsilon = max(0,self.agent.random_epsilon)
                
                if hasattr(self.agent,'random_epsilon'):
                    print("eps: ",round(self.agent.random_epsilon,3))
                print("sleep: ", round(self.sleepTime,3))
                print(event.key)
            if event.type == pygame.KEYUP:
                self.pressedKeys.remove(event.key)


    def main_loop(self):
        last_time = time.time()

        while not self.done:
            self.handleInput()

            self.graphics.draw()                                                                                                                                     

            time.sleep(0.02)
