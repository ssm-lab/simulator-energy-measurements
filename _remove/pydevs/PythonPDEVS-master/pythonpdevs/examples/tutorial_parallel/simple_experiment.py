from mymodel import MyModel
from pypdevs.simulator import Simulator

model = MyModel()
simulator = Simulator(model)

simulator.setVerbose()

simulator.simulate()