import time
from datetime import datetime

from pyJoules.energy_meter import measure_energy
from pyJoules.handler.csv_handler import CSVHandler
import sys
import util.singletonFlag as us
import util.constants as uc

class EnergyMeasurement:

    def __init__(self, outfile_name) -> None:
        self.DATA_FOLDER = '/home/yimoning/research/exp_data/trade_off_on_sim_step1/'
        self.csv_handler = CSVHandler(self.DATA_FOLDER + outfile_name)
        self.measure_energy_for_one_second = self.measure_energy_decorator(self.csv_handler)(self._measure_energy_for_one_second)
        self.duration = 1

    def set_duration(self, seconds):
        self.duration = seconds
        return self

    @staticmethod
    def measure_energy_decorator(csv_handler):
        def decorator(func):
            @measure_energy(handler=csv_handler)
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)
            return wrapper
        return decorator

    def _measure_energy_for_one_second(self):
        time.sleep(self.duration)  # Sleep for one second


    def run(self):
        print("Measure starts")
        print(datetime.now().strftime('%H:%M:%S'))
        while not us.Singleton.get_instance().getFlag():
            self.measure_energy_for_one_second()
        print("Measure done")
        print(datetime.now().strftime('%H:%M:%S'))
        self.csv_handler.save_data()
        time.sleep(3)


if __name__ == '__main__':
    energy_measurement = EnergyMeasurement("TEST")
    energy_measurement.run()
