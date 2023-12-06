import time
from datetime import datetime

from MeasurementStrategy import MeasurementStrategy

import util.singletonFlag as us


class FixedPeriodMeasurementStrategy(MeasurementStrategy):
    def __init__(self, outfile_name, data_folder):
        super().__init__(outfile_name, data_folder)
        self.duration = 1
        self.period = 10
        self.measure_func = self.measure_energy_decorator(self.csv_handler)(self._measure_func)

    def set_duration(self, seconds):
        self.duration = seconds
        return self

    def set_period(self, period):
        self.period = period
        return self

    def _measure_func(self):
        time.sleep(self.duration)

    def measure(self):
        print("Measure starts")
        print(datetime.now().strftime('%H:%M:%S'))
        while self.period > 0:
            self.measure_func()
            self.period -= self.duration
        print("Measure done")
        print(datetime.now().strftime('%H:%M:%S'))
        self.csv_handler.save_data()
