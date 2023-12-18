import logging
import time

from MeasurementStrategy import MeasurementStrategy


class FixedPeriodMeasurementStrategy(MeasurementStrategy):
    def __init__(self, path):
        super().__init__(path)
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

    def measure(self, cooldown_second):
        logging.info("Measurement start, waiting for measurable")
        while self.period + cooldown_second > 0:
            self.measure_func()
            self.period -= self.duration
        logging.info("Measure done")
        self.csv_handler.save_data()
        logging.info("Data successfully saved into" + self.file_loc)
