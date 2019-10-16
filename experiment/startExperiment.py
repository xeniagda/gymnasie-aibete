
from experiment import Experiment
from experimentLayout import experimentLayouts

def main():
    a = Experiment.loadFromDict(experimentLayouts[0])
    a.run()

main()