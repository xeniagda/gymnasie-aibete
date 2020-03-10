import time
from multiGameEngine import MultiGameEngine

def playGames(levels,agent,maxTime,render,ui,logTime=False, train=True, i=0):
    engine = MultiGameEngine(levels)
    engine.level_n = i

    if render:
        ui.setGameEngine(engine.into_regular_engine(0, ui))
        ui.setAgent(agent)

    agentInputs = engine.getAgentInputs()

    play_time = 0
    startTime = time.time()

    rewardSum = 0

    while True:
        actions = agent.getActions(agentInputs)
        newAgentInputs, rewards = engine.performTick(actions)

        if train:
            agent.update(agentInputs,actions,newAgentInputs,rewards)

        rewardSum += rewards.mean()
        agentInputs = newAgentInputs
        play_time += 1

        if play_time >= maxTime:
            return (play_time,rewardSum/play_time*1000)

        if logTime:
            if play_time%1000==0:
                print("Time: ",round(time.time()-startTime,3))
                startTime = time.time()

        if ui != None:
            time.sleep(ui.sleepTime)

        if render:
            ui.setGameEngine(engine.into_regular_engine(0, ui))
            ui.setAgentInput(newAgentInputs[0])
            ui.setReward(rewards[0])
