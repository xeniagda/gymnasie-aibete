
from experiment import Experiment
from experimentLayout import experimentLayout

def main():
    a = Experiment.loadFromDict(experimentLayout)
    a.run()

main()