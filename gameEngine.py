import numpy as np
#from graphics import UI
from util import * 
import random
import math

ACCELERATION = True
SECONDS_PER_TICK = 0.3

AROUND_RAD = 3
VISION_SIZE = AROUND_RAD * 2 + 1
AGENT_INPUT_SIZE = VISION_SIZE ** 2
INTERPOLATE_AGENT_INPUT = False

if not INTERPOLATE_AGENT_INPUT:
    AGENT_INPUT_SIZE += 2

AGENT_INPUT_SIZE += 2


# random.seed(1)

class GameEngine:
    def __init__(self,ui,level):
        self.ui = ui
        self.level = level
        
        self.player = Player(0,level[0][0],0,0)

    def performTick(self, action, draw=False, timeStep=SECONDS_PER_TICK):
        last_x = self.player.x
        self.player.applyAction(action,timeStep)

        for i in range(20):
            self.player.move(timeStep/20)
            self.resolveCollisions()

        delta_x = self.player.x - last_x
        #print(delta_x)
        reward = delta_x
        if 0 <= int(self.player.x) < len(self.level):
            if self.level[int(self.player.x)][1] and self.player.isOnGround:
                reward -= SECONDS_PER_TICK
        
        self.ui.setReward(reward)
        
        agentInput = self.getAgentInput()

        terminate = (self.player.x>=len(self.level) or action == Actions.RESTART)

        return (agentInput,reward,terminate)
    
    def getAgentInput(self):
        if not INTERPOLATE_AGENT_INPUT:
            res = np.zeros((AGENT_INPUT_SIZE, ))

            for dx in range(-AROUND_RAD, AROUND_RAD + 1):
                for dy in range(-AROUND_RAD, AROUND_RAD + 1):
                    ix =  dx + AROUND_RAD
                    iy =  dy + AROUND_RAD

                    ry = self.player.y + dy + 0.5
                    rx = math.floor(self.player.x +self.player.width/2 + dx)

                    if 0 <= rx < len(self.level):
                        is_solid = ry < self.level[rx][0]
                        is_bad = self.level[rx][1]

                        if is_solid:
                            res[iy * VISION_SIZE + ix] = 1
                            if is_bad:
                                res[iy * VISION_SIZE + ix] = -1

            res[-4] = self.player.vx
            res[-3] = self.player.vy

            res[-2] = self.player.x - round(self.player.x)
            res[-1] = self.player.y - round(self.player.y)

            return res
        else:
            agent_vision = np.zeros((AGENT_INPUT_SIZE, ))

            for dx in range(-AROUND_RAD, AROUND_RAD + 1):
                for dy in range(-AROUND_RAD, AROUND_RAD + 1):
                    atX = self.player.x + self.player.width / 2 - 0.5 + dx
                    atY = self.player.y + dy

                    solid_value = 0
                    for xCorner in [0, 1]:
                        for yCorner in [0, 1]:
                            xCoord = int(atX + xCorner)
                            yCoord = int(atY + yCorner)

                            if xCorner:
                                xMul = atX % 1
                            else:
                                xMul = 1 - (atX % 1)

                            if yCorner:
                                yMul = atY % 1
                            else:
                                yMul = 1 - (atY % 1)

                            if 0 <= xCoord < len(self.level):
                                value_here = self.level[xCoord][0] > yCoord
                            else:
                                value_here = 0
                            solid_value += value_here * xMul * yMul

                    ix = dx + AROUND_RAD
                    iy = dy + AROUND_RAD

                    agent_vision[int(iy) * VISION_SIZE + int(ix)] = solid_value

            agent_vision[-2] = self.player.vx
            agent_vision[-1] = self.player.vy

            return agent_vision
    
    def resolveCollisions(self):
        self.player.isOnGround = False
        for i in range(int(self.player.x)-1,int(self.player.x)+2):
            if i>=0 and i<len(self.level):
                self.player.isOnGround |= self.player.resolveCollisionWithBlock(i,-100,1,self.level[i][0]+100)
            if i < 0:
                self.player.isOnGround |= self.player.resolveCollisionWithBlock(i,-100,1,1e10)


class Player:
    def __init__(self,x,y,vx,vy):
        #lower right corner
        self.x = x
        self.y = y

        self.vx = vx
        self.vy = vy

        self.width = 0.2
        self.height = 1

        self.groundSpeed = 2.0
        self.airSpeed = 1.2
        self.gravity = -3
        self.jump = 4

        self.isOnGround = False
    
    def applyAction(self,action,timeStep):
        currentSpeed = self.groundSpeed
        if not self.isOnGround:
            currentSpeed = self.airSpeed
        
        if not ACCELERATION:
            self.vx = 0
        if action == Actions.LEFT:
            if ACCELERATION:
                self.vx -= 0.2*timeStep
                self.vx = max(self.vx,-currentSpeed)
            else:
                self.vx = -currentSpeed
        if action == Actions.RIGHT:
            if ACCELERATION:
                self.vx += 0.2*timeStep
                self.vx = min(self.vx,currentSpeed)
            else:
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
