import time
from abc import ABC, abstractmethod

from src.MeasurementExecutor import MeasurementExecutor
from pypdevs.simulator import Simulator
import threading

from util.singletonFlag import Singleton

# put a measuareable
class ModelExecutor(ABC):
    def __init__(self):
        self.measure_executor = None
        self.measuareable = None
        self.heat_up = 10
        self.cool_down = 10

    def set_heat_up(self, heat_up: int):
        self.heat_up = heat_up
        return self

    def set_cool_down(self, cool_down: int):
        self.cool_down = cool_down
        return self

    def set_measuareable(self, measuareable):
        self.measuareable = measuareable
        return self

    def set_executor(self, measure_executor):
        self.measure_executor = measure_executor
        return self

    @abstractmethod
    def run_measuareable(self):
        pass

    def measurable_end(self):
        Singleton.get_instance().turnOff()

    def run_model(self):
        Singleton.get_instance().flag_init()
        Singleton.get_instance().store_time(label="Start")
        measure_thread = threading.Thread(target=self.measure_executor.execute)
        measure_thread.start()
        time.sleep(self.heat_up)
        measuareable_thread = threading.Thread(target=self.run_measuareable)
        measuareable_thread.start()
        measure_thread.join()
        measuareable_thread.join()
        Singleton.get_instance().flag_init()

