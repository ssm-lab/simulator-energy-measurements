import time

from src.MeasurementExecutor import MeasurementExecutor
from pypdevs.simulator import Simulator
import threading

from util.singletonFlag import Singleton


class ModelExecutor:
    def __init__(self):
        self.measure_executor = None
        self.sim = None
        self.heat_up = 10
        self.cool_down = 10

    def set_heat_up(self, heat_up: int):
        self.heat_up = heat_up
        return self

    def set_cool_down(self, cool_down: int):
        self.cool_down = cool_down
        return self

    def set_sim(self, sim: Simulator):
        self.sim = sim
        return self

    def set_executor(self, measure_executor):
        self.measure_executor = measure_executor
        return self

    def run_sim(self):
        pass

    def run_model(self):
        Singleton.get_instance().flag_init()
        Singleton.get_instance().store_time(label="Start")
        measure_thread = threading.Thread(target=self.measure_executor.execute)
        measure_thread.start()
        time.sleep(self.heat_up)
        sim_thread = threading.Thread(target=self.run_sim)
        sim_thread.start()
        measure_thread.join()
        sim_thread.join()
        Singleton.get_instance().flag_init()

