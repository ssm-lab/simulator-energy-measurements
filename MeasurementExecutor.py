import logging
import threading
import time
from abc import ABC, abstractmethod
from util.log_init import log_init
import util.DummySignal as ud
from MeasurementStrategy import MeasurementStrategy

class MeasurementExecutor(ABC):
    def __init__(self):
        self.measure_success = False
        self.measurable_success = False
        log_init()
        self.strategy = None
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

    def set_strategy(self, new_strategy: MeasurementStrategy):
        self.strategy = new_strategy
        return self

    def run_measure_wrapper(self):
        try:
            self.strategy.measure(self.cool_down)
            self.measure_success = True
        except Exception as e:
            logging.error(f"Measure thread error: {e}")
            self.measure_success = False

    def run_measurable_wrapper(self):
        try:
            self.run_measuareable()
            self.measurable_success = True
        except Exception as e:
            logging.error(f"Measurable thread error: {e}")
            self.measurable_success = False
    @abstractmethod
    def run_measuareable(self):
        pass


    def run_model(self):
        try:
            logging.info("Process start")
            self.measure_success = False
            self.measurable_success = False
            measure_thread = threading.Thread(target=self.run_measure_wrapper)
            measure_thread.start()
            ud.DummySignal.get_instance().acquire_lock()
            time.sleep(self.heat_up)
            measurable_thread = threading.Thread(target=self.run_measurable_wrapper)
            logging.info("Measurable start, processing...")
            measurable_thread.start()
            measurable_thread.join()
            logging.info("Measurable finished, cooling down ...")
            ud.DummySignal.get_instance().release_lock(self.cool_down)
            measure_thread.join()
            if self.measurable_success and self.measure_success:
                logging.info("Process finished, success!")
            else:
                logging.error("Process finished with errors")
        except Exception as e:
            logging.error(f"An error occurred: {e}")

