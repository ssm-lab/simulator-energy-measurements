import sys
import time

from pyJoules.energy_meter import measure_energy
from pyJoules.handler.csv_handler import CSVHandler

sys.path.append("/home/yimoning/research/util/")
import constants as uc
import singletonFlag as us


class EnergyMeasurement:
    def __init__(self):
        self.DATA_FOLDER = '/home/yimoning/research/data/'
        self.csv_handler = CSVHandler(self.DATA_FOLDER + uc.FILE_NAME)
        self.measure_energy_for_one_second = self.measure_energy_decorator(self.csv_handler)(self._measure_energy_for_one_second)

    @staticmethod
    def measure_energy_decorator(csv_handler):
        def decorator(func):
            @measure_energy(handler=csv_handler)
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)
            return wrapper
        return decorator

    def _measure_energy_for_one_second(self):
        time.sleep(1)  # Sleep for one second

    def run(self):
        while not us.Singleton.get_instance().getFlag():
            # print(us.Singleton.get_instance().getFlag())
            self.measure_energy_for_one_second()
        self.csv_handler.save_data()
        # us.Singleton.get_instance().turnOff()

# if __name__ == '__main__':
#     energy_measurement = EnergyMeasurement()
#     energy_measurement.run()
