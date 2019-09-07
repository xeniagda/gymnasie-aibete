import graphics
from util import * 
import random

random.seed(1)

class GameEngine:
    def __init__(self,level=[1,1,1,2,1,1]):
        self.level = level
        self.player = Player(0,level[0],0,0)

    def performTick(self, action, draw=False, timeStep=0.01):
        self.player.applyAction(action)
        self.player.move(timeStep)
        self.resolveCollisions()

        if draw:
            graphics.drawGame(self.level,self.player)
        
        agentInput = self.getAgentInput()
        reward = 1
        terminate = self.player.x>=len(self.level)
        return (agentInput,reward,terminate)
    
    def getAgentInput(self):
        return [self.player.x,self.player.y]
    
    def resolveCollisions(self):
        self.player.isOnGround = False
        for i in range(int(self.player.x)-1,int(self.player.x)+2):
            if i>=0 and i<len(self.level):
                self.player.isOnGround |= self.resolveCollisionWithBlock(i,0,1,self.level[i])

    def resolveCollisionWithBlock(self,bx,by,bw,bh):
        if(max(bx,self.player.x)<min(bx+bw,self.player.x+self.player.width)
            and max(by,self.player.y)<min(by+bh,self.player.y+self.player.height)):
            distLeft = self.player.x+self.player.width-bx
            distRight = bx+bw-self.player.x
            distDown = self.player.y+self.player.height-by
            distUp = by+bh-self.player.y
            minDist = min(distLeft,distRight,distUp,distDown)
            if distUp == minDist:
                self.player.y = by+bh
                self.player.vy = 0
                return True
            if distLeft == minDist:
                self.player.x = bx-self.player.width
                self.player.vx = 0
            if distRight == minDist:
                self.player.x = bx+bw
                self.player.vx = 0
            if distDown == minDist:
                self.player.y = by-self.player.height
                self.player.vy = 0
        return False

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

