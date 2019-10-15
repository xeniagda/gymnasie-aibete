
from experimentNew import Experiment
from experimentLayout import experimentLayouts

def main():

    a = Experiment(**experimentLayouts["testExperiment"])
    a.run()
    a.saveToFile("testResults.json")

main()