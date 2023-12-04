from GridModel import *
from pypdevs.simulator import Simulator
from src.DurationBasedMeasurement import DurationBasedMeasurement
from src.MeasurementExecutor import MeasurementExecutor
from src.ModelExecutor import ModelExecutor

from util.singletonFlag import Singleton


class Demo(ModelExecutor):
    def __init__(self):
        super().__init__()
        measure_model = DurationBasedMeasurement("test",
                                                 "/home/yimoning/mcmaster/fall2023/sim_energy_measurements/data/")
        measure_executor = MeasurementExecutor(measure_model)
        sirGrid = SIRGrid(100)
        sim = Simulator(sirGrid)
        self.set_executor(measure_executor).set_sim(sim)

    def run_sim(self):
        self.sim.setTerminationTime(100)
        total_sim = 100
        self.sim.setVerbose(None)
        current = 0
        while current < total_sim:
            self.sim.setTerminationTime(current + 1)
            self.sim.simulate()
            current += 1
        # print(str(end-start))
        Singleton.get_instance().store_time(label="sim_end")
        Singleton.get_instance().turnOff()

if __name__ == '__main__':
    demo = Demo()
    demo.run_model()