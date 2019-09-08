import math
import time
import pygame

width, height = size = 1080, 800

TIME_PER_FRAME = 0.002

SCALE = 50

screen = None

game_engine = None
done = False

# Game units
PLAYER_FOLLOW_X = 7
REWARD = 0

def init_screen():
    global screen
    pygame.init()
    screen = pygame.display.set_mode(size)

    pygame.display.set_caption("Title")



def draw_loop():
    global screen, game_engine, pg_player,height, done, REWARD, TIME_PER_FRAME

    last_time = time.time()

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == 275: # Right
                    TIME_PER_FRAME = 0
                if event.key == 276: # Left
                    TIME_PER_FRAME = 0.002

        if game_engine == None:
            continue

        delta_x = 0
        if game_engine.player.x > PLAYER_FOLLOW_X:
            delta_x = game_engine.player.x - PLAYER_FOLLOW_X

        if REWARD > 0:
            v = min(int(REWARD * 7000), 255)
            screen.fill((255 - v, 255, 255 - v))
        elif REWARD < 0:
            v = min(int(-REWARD * 7000), 255)
            screen.fill((255, 255 - v, 255 - v))
        else:
            screen.fill((255, 255, 255))

        rec = getRect(game_engine.player.x - delta_x, game_engine.player.y,
                      game_engine.player.width, game_engine.player.height)

        pygame.draw.rect(screen, (0, 0, 0), rec)
        pygame.draw.rect(screen, (0, 0, 255), rec.inflate(-2, -2))

        for x, wall_height in enumerate(game_engine.level):
            rec = getRect(x - delta_x, 0, 1, wall_height)
            if screen.get_bounding_rect().colliderect(rec):
                pygame.draw.rect(screen, (0, 0, 0), rec)

        pygame.display.flip()

        time.sleep(0.02)

def getRect(x,y,w,h):
    return pygame.Rect(int(x*SCALE),int(height-(y+h)*SCALE),int(w*SCALE),int(h*SCALE))

def drawGame(ge, reward):
    global game_engine, REWARD, TIME_PER_FRAME

    game_engine = ge
    time.sleep(TIME_PER_FRAME)

    REWARD = REWARD * 0.9 + 0.1 * reward
