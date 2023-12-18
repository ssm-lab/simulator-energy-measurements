import time
from abc import ABC, abstractmethod
from pyJoules.energy_meter import measure_energy
from pyJoules.handler.csv_handler import CSVHandler
import os

class MeasurementStrategy(ABC):

    def __init__(self, path):
        self.csv_handler = CSVHandler(path)

    @abstractmethod
    def measure(self, cooldown_second: int):
        pass


    def cool_down(self, seconds):
        time.sleep(seconds)

    @staticmethod
    def measure_energy_decorator(csv_handler):
        def decorator(func):
            @measure_energy(handler=csv_handler)
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)
            return wrapper
        return decorator