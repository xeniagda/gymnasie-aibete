import time
from gameEngine import GameEngine

def playGame(level,agent,maxTime,render,ui,logTime=False):
    engine = GameEngine(ui,level)

    if render:
        ui.setGameEngine(engine)
        ui.setAgent(agent)
    agentInput = engine.getAgentInput()

    play_time = 0
    startTime = time.time()

    rewardSum = 0

    while True:
        action = agent.getAction(agentInput)
        newAgentInput,reward,terminate = engine.performTick(action, render)
        rewardSum += reward
        agent.update(agentInput,action,newAgentInput,reward)
        agentInput = newAgentInput
        if terminate or play_time >= maxTime:
            return (play_time,rewardSum/play_time*1000)

        play_time += 1

        if logTime:
            if play_time%1000==0:
                print("Time: ",round(time.time()-startTime,3))
                startTime = time.time()

        time.sleep(ui.sleepTime)