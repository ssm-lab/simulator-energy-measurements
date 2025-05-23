import logging
import time
from MeasurementStrategy import MeasurementStrategy
import util.lock as ud

class DurationBasedMeasurementStrategy(MeasurementStrategy):
    def __init__(self, path=None):
        super().__init__(path)
        self.duration = 1
        self.measure_func = self.measure_energy_decorator(self.csv_handler)(self._measure_func)


    def set_duration(self, seconds):
        self.duration = seconds
        return self

    def _measure_func(self):
        time.sleep(self.duration)

    def measure(self, cooldown_second):
        logging.info("Measurement start, waiting for measurable starts")
        while not ud.DummySignal.get_instance().getFlag():
            self.measure_func()

        logging.info("Measure done")
        self.csv_handler.save_data()
        logging.info("Data successfully saved into" + self.file_loc)
