import math
import time

counter = 0
def drawGame(level,player):
    #level is a list of heights of pillars
    #player is a Player object
    asciiArtGraphics(level,player)


def asciiArtGraphics(level,player):
    global counter
    counter+=1
    if counter<10:
        return
    counter = 0
    x = int(player.x*3)
    y = int(player.y)

    print("\033[2J")
    for i in range(10):
        line = ""
        for j in range(len(level)*3):
            if 9-i==y and j==x:
                line += "*"
            elif 9-i<level[int(j/3)]:
                line += "#"
            else:
                line += " "
        print(line)
    
    time.sleep(0.02)
