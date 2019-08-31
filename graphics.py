import math
import time

def drawGame(level,player):
    #level is a list of heights of pillars
    #player is a Player object

    x = round(player.x)
    y = round(player.y)

    for i in range(5):
        line = ""
        for j in range(len(level)):
            if 5-i==y and j==x:
                line += "*"
            elif 5-i<=level[j]:
                line += "#"
            else:
                line += " "
        print(line)
    
    time.sleep(1)