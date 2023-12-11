from GridModel import *
from pypdevs.simulator import Simulator
from DurationBasedMeasurementStrategy import DurationBasedMeasurementStrategy
from MeasurementExecutor import MeasurementExecutor

class Demo(MeasurementExecutor):
    def __init__(self):
        super().__init__()
        
        sirGrid = SIRGrid(10)
        
        measuareable = Simulator(sirGrid)
        measurement_strategy = DurationBasedMeasurementStrategy("test", "data_folder")
        
        self.set_strategy(measurement_strategy).set_measuareable(measuareable)

    def run_measuareable(self):
        self.measuareable.setTerminationTime(10)
        total_sim = 100
        self.measuareable.setVerbose(None)
        current = 0
        while current < total_sim:
            self.measuareable.setTerminationTime(current + 1)
            self.measuareable.simulate()
            current += 1

if __name__ == '__main__':
    demo = Demo()
    demo.run_model()
