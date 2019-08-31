import graphics
from util import * 

class GameEngine:
    def __init__(self,level=[1,1,1,2,1,1]):
        self.level = level
        self.player = Player(0,level[0],0,0)

    def getNextState(self,action,draw=False,timeStep=0.1):
        self.player.applyAction(action)
        self.player.move(timeStep)
        self.resolveCollision()

        if draw:
            graphics.drawGame(self.level,self.player)
        
        agentState = self.getAgentState()
        reward = 1
        terminate = False 
        return (agentState,reward,terminate)
    
    def getAgentState(self):
        return [self.player.x,self.player.y]
    
    def resolveCollision(self):
        pass    

class Player:
    def __init__(self,x,y,vx,vy):
        #lower right corner
        self.x = x
        self.y = y

        self.vx = vx
        self.vy = vy

        self.width = 0.2
        self.height = 1

        self.speed = 1
        self.gravity = -0.2
        self.jump = 1
    
    def applyAction(self,action):
        if action == Actions.LEFT:
            self.vx = -self.speed
        if action == Actions.RIGHT:
            self.vx = self.speed
        if action == Actions.JUMP and self.isOnGround():
            self.vy = self.jump
        
    def move(self,timeStep):
        self.vy += self.gravity * timeStep
        self.x += self.vx * timeStep
        self.y += self.vy * timeStep

