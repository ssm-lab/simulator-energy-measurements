import time
from datetime import datetime

from src.MeasureStrategy import MeasurementStrategy

import util.singletonFlag as us


class DurationBasedMeasurementStrategy(MeasurementStrategy):
    def __init__(self, outfile_name, data_folder):
        super().__init__(outfile_name, data_folder)
        self.duration = 1
        self.measure_func = self.measure_energy_decorator(self.csv_handler)(self._measure_func)


    def set_duration(self, seconds):
        self.duration = seconds
        return self

    def _measure_func(self):
        time.sleep(self.duration)

    def measure(self):
        print("Measure starts")
        print(datetime.now().strftime('%H:%M:%S'))
        while not us.Singleton.get_instance().getFlag():
            self.measure_func()
        print("Measure done")
        print(datetime.now().strftime('%H:%M:%S'))
        self.csv_handler.save_data()
