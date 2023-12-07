from GridModel import *
from pypdevs.simulator import Simulator
from DurationBasedMeasurementStrategy import DurationBasedMeasurementStrategy
from MeasurementExecutor import MeasurementExecutor

from util.singletonFlag import Singleton


class Demo(MeasurementExecutor):
    def __init__(self):
        super().__init__()
        measure_model = DurationBasedMeasurementStrategy("test", "data/")
        # measure_executor = MeasurementExecutor(measure_model)
        sirGrid = SIRGrid(10)
        sim = Simulator(sirGrid)
        self.set_strategy(measure_model).set_measuareable(sim)

    def run_measuareable(self):
        self.measuareable.setTerminationTime(10)
        total_sim = 100
        self.measuareable.setVerbose(None)
        current = 0
        while current < total_sim:
            self.measuareable.setTerminationTime(current + 1)
            self.measuareable.simulate()
            current += 1
        # print(str(end-start))
        Singleton.get_instance().store_time(label="sim_end")
        Singleton.get_instance().turnOff()

if __name__ == '__main__':
    demo = Demo()
    demo.run_model()
