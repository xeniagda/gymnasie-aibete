import graphics

class gameEngine:
    def __init__(self,level=[1,1,1,2,1,1]):
        self.level = level
        self.player = Player(0,level[0],0,0)

    def getNextState(self,action,draw=False,timeStep=0.1):
        #Transition to next state
        
        if draw:
            graphics.drawGame(self.level,playerState)
        
        agentState = self.getAgentState()
        reward = 1
        isTerminal = False 
        return (agentState,reward,isTerminal)
    
    def getAgentState():
        return [self.player.x,self.player.y]

class Player:
    def __init__(self,x,y,vx,vy):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy