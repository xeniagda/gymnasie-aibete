import numpy as np
from graphics import UI
from util import * 
import random
import math

# random.seed(1)

AROUND_RAD = 2

class GameEngine:
    def __init__(self,ui,level):
        self.ui = ui
        self.level = level
        
        self.player = Player(0,level[0][0],0,0)

    def performTick(self, action, draw=False, timeStep=0.01):
        last_x = self.player.x
        self.player.applyAction(action)
        self.player.move(timeStep)
        self.resolveCollisions()

        delta_x = self.player.x - last_x
        reward = delta_x
        if 0 <= int(self.player.x) < len(self.level):
            if self.level[int(self.player.x)][1] and self.player.isOnGround:
                reward -= 0.2
        
        self.ui.setReward(reward)
        
        agentInput = self.getAgentInput()

        terminate = self.player.x>=len(self.level)

        return (agentInput,reward,terminate)
    
    def getAgentInput(self):
        res = np.zeros(((AROUND_RAD * 2 + 1) ** 2 + 2, ))

        for dx in range(-AROUND_RAD, AROUND_RAD + 1):
            for dy in range(-AROUND_RAD, AROUND_RAD + 1):
                ix =  dx + AROUND_RAD
                iy =  dy + AROUND_RAD

                ry = self.player.y + dy + 0.5
                rx = round(self.player.x + dx)

                if 0 <= rx < len(self.level):
                    is_solid = ry < self.level[rx][0]
                    is_bad = self.level[rx][1]

                    if is_solid:
                        res[iy * (AROUND_RAD * 2 + 1) + ix] = 1
                        if is_bad:
                            res[iy * (AROUND_RAD * 2 + 1) + ix] = -1

        res[-2] = self.player.x - round(self.player.x)
        res[-1] = self.player.y - round(self.player.y)

        return res
    
    def resolveCollisions(self):
        self.player.isOnGround = False
        for i in range(int(self.player.x)-1,int(self.player.x)+2):
            if i>=0 and i<len(self.level):
                self.player.isOnGround |= self.player.resolveCollisionWithBlock(i,0,1,self.level[i][0])
            if i < 0:
                self.player.isOnGround |= self.player.resolveCollisionWithBlock(i,0,1,1e10)


class Player:
    def __init__(self,x,y,vx,vy):
        #lower right corner
        self.x = x
        self.y = y

        self.vx = vx
        self.vy = vy

        self.width = 0.2
        self.height = 1

        self.groundSpeed = 1.5
        self.airSpeed = 0.8
        self.gravity = -3
        self.jump = 4

        self.isOnGround = False
    
    def applyAction(self,action):
        currentSpeed = self.groundSpeed
        if not self.isOnGround:
            currentSpeed = self.airSpeed
        self.vx = 0
        if action == Actions.LEFT:
            self.vx = -currentSpeed
        if action == Actions.RIGHT:
            self.vx = currentSpeed
        if action == Actions.JUMP and self.isOnGround:
            self.vy = self.jump
        
    def move(self,timeStep):
        self.vy += self.gravity * timeStep
        self.x += self.vx * timeStep
        self.y += self.vy * timeStep
    
    def resolveCollisionWithBlock(self,bx,by,bw,bh):
        if(max(bx,self.x)<min(bx+bw,self.x+self.width)
            and max(by,self.y)<min(by+bh,self.y+self.height)):
            distLeft = self.x+self.width-bx
            distRight = bx+bw-self.x
            distDown = self.y+self.height-by
            distUp = by+bh-self.y
            minDist = min(distLeft,distRight,distUp,distDown)
            if distUp == minDist and self.vy<0:
                self.y = by+bh
                self.vy = 0
                return True
            if distLeft == minDist and self.vx>0:
                self.x = bx-self.width
                self.vx = 0
            if distRight == minDist and self.vx<0:
                self.x = bx+bw
                self.vx = 0
            if distDown == minDist and self.vy>0:
                self.y = by-self.height
                self.vy = 0
        return False
