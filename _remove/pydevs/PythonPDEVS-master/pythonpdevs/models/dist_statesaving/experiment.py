import sys

sys.setrecursionlimit(20000)
import random

sys.path.append("../../src/")
from model import DEVStone
from simulator import Simulator

model = DEVStone(3, int(sys.argv[1]), False)
sim = Simulator(model)
sim.setMessageCopy('custom')
sim.setStateSaving(str(sys.argv[2]))
sim.setTerminationTime(1000)
sim.setSchedulerMinimalList()
sim.simulate()
