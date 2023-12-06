from abc import ABC, abstractmethod

from pyJoules.energy_meter import measure_energy
from pyJoules.handler.csv_handler import CSVHandler


class MeasurementStrategy(ABC):

    def __init__(self, outfile_name, data_folder):
        self.DATA_FOLDER = data_folder
        self.csv_handler = CSVHandler(self.DATA_FOLDER + outfile_name)

    @abstractmethod
    def measure(self):
        pass

    @staticmethod
    def measure_energy_decorator(csv_handler):
        def decorator(func):
            @measure_energy(handler=csv_handler)
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)
            return wrapper
        return decorator