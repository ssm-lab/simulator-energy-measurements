import math
import threading
import time

from util.singletonFlag import Singleton
from DurationBasedMeasurement import DurationBasedMeasurement
from FixedPeriodMeasurement import FixedPeriodMeasurement
def exp1(): # trade off experiment on sim step
    Singleton.get_instance().flag_init() # make sure that when program starts it can run
    measure_model = DurationBasedMeasurement("test", "/home/yimoning/mcmaster/fall2023/sim_energy_measurements/data/")
    for step in range(1, 2):
            out_file = "500*100" + "_" + str(step) + "_stepsize.csv"
            round_needed = math.ceil(100 / step)
            # print(out_file)
            # print(Singleton.get_instance().getFlag())
            def measure_thread_func():
                measure_model.measure()
            Singleton.get_instance().store_time(label="Start")
            measure_thread = threading.Thread(target=measure_thread_func)
            measure_thread.start()
            time.sleep(10)
            Singleton.get_instance().turnOff()
            measure_thread.join()
            Singleton.get_instance().flag_init()

exp1()
def exp2():
    measure_model = FixedPeriodMeasurement("test1", "/home/yimoning/mcmaster/fall2023/sim_energy_measurements/data/").set_duration(1).set_period(10)
    measure_model.measure()
# exp2()