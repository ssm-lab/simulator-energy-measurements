import os

# import experiment_loop_run as el
from experiment_loop_run import run

# from exp_tk import run
os.environ['RDMAV_FORK_SAFE'] = '1'
import multiprocessing
from queue import Queue

if multiprocessing.get_start_method() is None:
    multiprocessing.set_start_method('spawn')

queue = Queue()
pool = multiprocessing.Pool(processes=16)
for _ in range(16):
    ret = pool.apply_async(run, args=(500,))
    queue.put(ret)

while not queue.empty():
    queue.get()

pool.close()
pool.join()

