import math
import time

counter = 0
def drawGame(level,player):
    global counter
    #level is a list of heights of pillars
    #player is a Player object
    counter+=1
    if counter<10:
        return
    counter = 0
    x = int(player.x*3)
    y = int(player.y)

    for i in range(6):
        line = ""
        for j in range(len(level)*3):
            if 5-i==y and j==x:
                line += "*"
            elif 5-i<level[int(j/3)]:
                line += "#"
            else:
                line += " "
        print(line)
    
    time.sleep(0.05)