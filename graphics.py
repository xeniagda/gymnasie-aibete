import math
import time
import threading
import pygame

width, height = size = 1080, 800

SCALE = 50

pygame.init()

screen = pygame.display.set_mode(size)

pygame.display.set_caption("Title")

pg_level = None
pg_player = None

def draw_loop():
    global screen, pg_level, pg_player,height 

    while True:
        level = pg_level
        player = pg_player
        if player == None or level == None:
            continue

        #level is a list of heights of pillars
        #player is a Player object
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        
        screen.fill((255, 255, 255))
        rec = getRect(player.x, player.y, player.width, player.height)
        pygame.draw.rect(screen, (0, 0, 0), rec)

        for x, wall_height in enumerate(level):
            rec = getRect(x, 0, 1, wall_height)
            pygame.draw.rect(screen, (0, 0, 0), rec)
            
        

        pygame.display.flip()

def getRect(x,y,w,h):
    return pygame.Rect(int(x*SCALE),int(height-(y+h)*SCALE),int(w*SCALE),int(h*SCALE))

def drawGame(level, player):
    global pg_level, pg_player

    pg_level = level
    pg_player = player
    time.sleep(0.005)

thread = threading.Thread(target=draw_loop, daemon=True)
thread.start()
