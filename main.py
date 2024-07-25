from runner import Runner
from plotter import Plotter
import sys

if __name__ == "__main__":
    if sys.argv[1:]:
        runner = Runner(sys.argv[1])
    else:
        runner = Runner("configuration.yaml")
    runner.run()
        
    plotter = Plotter(runner.output_file_path)
    
    plotter.plot()