import csv
import os
import time
from datetime import datetime


class Singleton:
    _instance = None
    _filepath = "/home/yimoning/mcmaster/fall2023/new_simMeasure/_remove/data/singleton_flag.txt"
    _time_filepath = "/home/yimoning/mcmaster/fall2023/new_simMeasure/_remove/data/timestamps.csv"

    def __init__(self):
        self.test = 0
        if not os.path.exists(self._filepath):
            with open(self._filepath, 'w') as f:
                f.write("False")
        # Ensure the timestamp CSV file exists.
        if not os.path.exists(self._time_filepath):
            with open(self._time_filepath, 'w', newline='') as f:
                writer = csv.writer(f)
                # writer.writerow(["Timestamp"])

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
    # if flag is false: measurement will continue, otherwise keep running
    def turnOff(self):
        self.test += 1
        print(datetime.now().strftime('%H:%M:%S'))
        time.sleep(10)
        self.store_time(label="End")
        with open(self._filepath, 'w') as f:
            f.write("True")

    def flag_init(self):
        with open(self._filepath, 'w') as f:
            f.write("False")
    def getFlag(self):
        with open(self._filepath, 'r') as f:
            flag_str = f.read().strip()
        return flag_str == "True"

    def store_time(self, label=None):
        """
        Store the current timestamp in a CSV file.
        """
        current_time = datetime.now().strftime('%H:%M:%S')
        # Format the data to be written based on the presence of the label
        data_to_write = [label + ": " + current_time] if label else [current_time]

        with open(self._time_filepath, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(data_to_write)


