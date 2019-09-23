import math
import time
import pygame

width, height = size = 720, 600

TIME_PER_FRAME = 0.002

SCALE = 50
# Game units
REWARD = 0
REWARD_CHANGE_SPEED = 0.2
PLAYER_FOLLOW_MARGINS = 7

class Graphics():
    def __init__(self,screen):
        self.screen = screen
        self.game_engine = None
        self.agent = None

        self.font = pygame.font.SysFont("comicsansms", 72)

        self.delta_x = 0
        self.delta_y = 0

    def setGameEngine(self,game_engine):
        self.game_engine = game_engine

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

        if REWARD > 0:
            v = min(int(REWARD * 7000), 255)
            self.screen.fill((255 - v, 255, 255 - v))
        elif REWARD < 0:
            v = min(int(-REWARD * 7000), 255)
            self.screen.fill((255, 255 - v, 255 - v))
        else:
            self.screen.fill((255, 255, 255))

        rec = self.getRect(player.x - self.delta_x, player.y - self.delta_y,
                      player.width, player.height)

        pygame.draw.rect(self.screen, (138, 36, 55), rec)
        pygame.draw.rect(self.screen, (204, 90, 112), rec.inflate(-2, -2))
        pygame.draw.rect(self.screen, (186, 84, 162), rec.inflate(-4, -4))

        for x, wall_height in enumerate(self.game_engine.level):
            rec = self.getRect(x - self.delta_x, 0, 1, wall_height - self.delta_y)
            col_outer = (38, 95, 133)
            col_inner = (107, 164, 201)
            if self.game_engine.bad_blocks[x]:
                col_outer = (133, 50, 10)
                col_inner = (201, 80, 47)

            if self.screen.get_bounding_rect().colliderect(rec):
                pygame.draw.rect(self.screen, col_outer, rec)
                pygame.draw.rect(self.screen, col_inner, rec.inflate(-2, -2))

        # Rita agentInput
        agentInput = self.game_engine.getAgentInput()
        for y in range(5):
            for x in range(5):
                rec = pygame.Rect(x * 5,y * 5, 5, 5)
                if agentInput[y * 5 + x] == 1:
                    pygame.draw.rect(self.screen, (0, 0, 0), rec)
                elif agentInput[y * 5 + x] == 0:
                    pygame.draw.rect(self.screen, (255, 255, 255), rec)
                else:
                    pygame.draw.rect(self.screen, (255, 0, 0), rec)

        #Rita text
        if self.agent != None:
            self.screen.blit(self.font.render(str(self.agent.random_epsilon), True, (0, 128, 0)),(0,0))

        #if agent!=None:
            #print(agent.random_epsilon)

        pygame.display.flip()

    def getRect(self,x,y,w,h):
        return pygame.Rect(int(x*SCALE),int(height-(y+h)*SCALE),math.ceil(w*SCALE+1),math.ceil(h*SCALE+1))
    

class UI():
    def __init__(self):
        self.screen = None
        self.game_engine = None
        self.agent = None
        self.done = False

        pygame.init()
        pygame.display.set_caption("Title")

        self.screen = pygame.display.set_mode(size)

        self.graphics = Graphics(self.screen)

    def setGameEngine(self,ge):
        self.game_engine = ge
        self.graphics.setGameEngine(ge)

    def setAgent(self,ag):
        self.agent = ag

    def setReward(self,reward):
        REWARD = REWARD * REWARD_CHANGE_SPEED ** 0.01 + (1 - REWARD_CHANGE_SPEED ** 0.01) * reward

    def handleInput(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                print(event.key)
                if event.key == 275: # Right
                    TIME_PER_FRAME = 0
                if event.key == 276: # Left
                    TIME_PER_FRAME = 0.002
                if event.key == 114: # R
                    if agent.random_epsilon>0:
                        agent.random_epsilon = 0
                    else:
                        agent.random_epsilon = 0.005
                    print("new eps: ",agent.random_epsilon)
                print(event.key)

    def main_loop(self):
        last_time = time.time()

        while not self.done:
            self.handleInput()

            self.graphics.draw()                                                                                                                                     

            time.sleep(0.02)
