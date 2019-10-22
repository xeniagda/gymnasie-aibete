
from experiment import Experiment
from experimentLayout import experimentLayouts

def main():
    for i,e in enumerate(experimentLayouts):
        print(str(i) +": "+e["name"])
    
    choice = input("Choose experiment to start: ")

    a = Experiment.loadFromDict(experimentLayouts[int(choice)])
    a.run()

main()