import math

from GridModel import *
from pypdevs.simulator import Simulator
import time
from pyJoules.energy_meter import measure_energy
from pyJoules.handler.csv_handler import CSVHandler
DATA_FOLDER = '/home/yimoning/research/exp_data/trade_off_on_sim_step1/'
import Measure
# given size and sim step, run simulation
from util.singletonFlag import Singleton
import timeit
def run_sim(size, numSteps):
    Singleton.get_instance().store_time(label="sim_start")
    sirGrid = SIRGrid(size)
    sim = Simulator(sirGrid)
    sim.setTerminationTime(numSteps)
    total_sim = numSteps
    sim.setVerbose(None)
    start = timeit.default_timer()
    current = 0
    while current < total_sim:
        sim.setTerminationTime(current + 1)
        sim.simulate()
        current += 1
    end = timeit.default_timer()
    # print(str(end-start))
    Singleton.get_instance().store_time(label="sim_end")
    Singleton.get_instance().turnOff()
def run_sim(size, numSteps, step):
    Singleton.get_instance().store_time(label="sim_start")
    sirGrid = SIRGrid(size, step)
    sim = Simulator(sirGrid)
    sim.setTerminationTime(numSteps)
    total_sim = numSteps
    sim.setVerbose(None)
    start = timeit.default_timer()
    current = 0
    while current < total_sim:
        sim.setTerminationTime(current + 1)
        sim.simulate()
        current += 1
    end = timeit.default_timer()
    # print(str(end-start))
    Singleton.get_instance().store_time(label="sim_end")
    Singleton.get_instance().turnOff()
#     energy_measurement = EnergyMeasurement()
#     energy_measurement.run()
import threading

def exp():
    Singleton.get_instance().flag_init() # make sure that when program starts it can run
    for size in range(50, 52):
        for step in range(50, 52):
            out_file = str(size) + "*" + str(size) + "_" + str(step) + "_times.csv"
            # print(out_file)
            measure_model = Measure.EnergyMeasurement(out_file)
            # print(Singleton.get_instance().getFlag())
            def measure_thread_func():
                measure_model.run()
            Singleton.get_instance().store_time(label="Start")
            measure_thread = threading.Thread(target=measure_thread_func)
            measure_thread.start()
            time.sleep(10)
            def sim_thread_func():
                run_sim(size, step)
            sim_thread = threading.Thread(target=sim_thread_func)
            sim_thread.start()

            measure_thread.join()
            sim_thread.join()

            Singleton.get_instance().flag_init()
# exp()


def exp1(): # trade off experiment on sim step
    Singleton.get_instance().flag_init() # make sure that when program starts it can run
    for step in range(1, 101):
            out_file = "500*100" + "_" + str(step) + "_stepsize.csv"
            round_needed = math.ceil(100 / step)
            # print(out_file)
            measure_model = Measure.EnergyMeasurement(out_file)
            # print(Singleton.get_instance().getFlag())
            def measure_thread_func():
                measure_model.run()
            Singleton.get_instance().store_time(label="Start")
            measure_thread = threading.Thread(target=measure_thread_func)
            measure_thread.start()
            time.sleep(10)
            def sim_thread_func():
                run_sim(500, round_needed, step)
            sim_thread = threading.Thread(target=sim_thread_func)
            sim_thread.start()

            measure_thread.join()
            sim_thread.join()

            Singleton.get_instance().flag_init()


if __name__ == "__main__":
    exp1()
