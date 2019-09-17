import numpy as np
import graphics
from util import * 
import random
import math

# random.seed(1)

AROUND_RAD = 2

class GameEngine:
    def __init__(self,level=[1,1,1,2,1,1]):
        self.level = level
        self.bad_blocks = np.random.uniform(0, 1, size=(len(level), )) < 0.1
        self.player = Player(0,level[0],0,0)

    def performTick(self, action, draw=False, timeStep=0.01):
        last_x = self.player.x
        self.player.applyAction(action)
        self.player.move(timeStep)
        self.resolveCollisions()

        delta_x = self.player.x - last_x
        reward = delta_x
        if 0 <= int(self.player.x) < len(self.bad_blocks):
            if self.bad_blocks[int(self.player.x)] and self.player.isOnGround:
                reward -= 0.02
        if draw:
            graphics.drawGame(self, reward)
        
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
                rx = int(self.player.x + dx) % len(self.level)

                is_solid = ry > self.level[rx]

                if is_solid:
                    res[iy * (AROUND_RAD * 2 + 1) + ix] = 1

        res[-2] = self.player.x % 1
        res[-1] = self.player.y % 1

        return res
    
    def resolveCollisions(self):
        self.player.isOnGround = False
        for i in range(int(self.player.x)-1,int(self.player.x)+2):
            if i>=0 and i<len(self.level):
                self.player.isOnGround |= self.player.resolveCollisionWithBlock(i,0,1,self.level[i])
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

        self.groundSpeed = 1
        self.airSpeed = 0.5
        self.gravity = -3
        self.jump = 4

        self.isOnGround = False
    
    def applyAction(self,action):
        currentSpeed = self.groundSpeed
        if not self.isOnGround:
            currentSpeed = self.airSpeed
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
            if distUp == minDist:
                self.y = by+bh
                self.vy = 0
                return True
            if distLeft == minDist:
                self.x = bx-self.width
                self.vx = 0
            if distRight == minDist:
                self.x = bx+bw
                self.vx = 0
            if distDown == minDist:
                self.y = by-self.height
                self.vy = 0
        return False
