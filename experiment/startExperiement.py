
from experiment import Experiment
from experimentLayout import experimentLayouts

def main():

    a = Experiment(**experimentLayouts["testExperiment"])
    a.run()

main()