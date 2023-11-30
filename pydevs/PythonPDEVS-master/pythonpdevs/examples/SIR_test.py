from pypdevs.DEVS import AtomicDEVS, CoupledDEVS
from pypdevs.simulator import Simulator
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import time
import sys
sys.path.append("/home/yimoning/research/util/")
import singletonFlag as us
import constants as uc
class SIRCell(AtomicDEVS):
    def __init__(self, name, initial_state, neighbors):
        AtomicDEVS.__init__(self, name)
        self.state = initial_state
        self.ta = 1.0
        self.beta = 0.3
        self.gamma = 0.1
        self.inport = self.addInPort("inport")
        self.outport = self.addOutPort("outport")
        self.neighbors = neighbors

    def intTransition(self):
        S, I, R = self.state
        if I > 0:  # If the cell is infectious
            new_S = S - self.beta * S * I
            new_I = I + self.beta * S * I - self.gamma * I
            new_R = R + self.gamma * I
            self.state = (new_S, new_I, new_R)
        return self.state

    def timeAdvance(self):
        return self.ta

    def outputFnc(self):
        return {self.outport: ("INFECT", self.neighbors)} if self.state[1] > 0 else {}



    def extTransition(self, inputs):
        if "INFECT" in inputs[self.inport]:
            S, I, R = self.state
            if I == 0:  # If the cell is susceptible
                self.state = (0.999, 0.001, 0.0)
        return self.state


class SIRGrid(CoupledDEVS):
    def __init__(self, size):
        CoupledDEVS.__init__(self, "SIRGrid")
        self.size = size
        self.cells = {}

        for i in range(size):
            for j in range(size):
                name = f"cell_{i}_{j}"
                initial_state = (0.99, 0.01, 0.0) if i == size // 2 and j == size // 2 else (1.0, 0.0, 0.0)
                possible_neighbors = [(i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)]
                neighbors = [(x, y) for x, y in possible_neighbors if 0 <= x < size and 0 <= y < size]
                cell = SIRCell(name, initial_state, neighbors)
                self.cells[(i, j)] = cell
                self.addSubModel(cell)

        # Coupling
        for (i, j), cell in self.cells.items():
            for x, y in cell.neighbors:
                neighbor = self.cells[(x, y)]
                self.connectPorts(cell.outport, neighbor.inport)

import timeit
if __name__ == "__main__":
    # size = int(100000 ** 0.5)
    size = 50  # specify size here
    sirGrid = SIRGrid(size)
    sim = Simulator(sirGrid)
    sim.setTerminationTime(uc.SIMROUND)
    sim.setVerbose(None)
    total_sim = 50
    current = 0
    cmap = sns.light_palette("black", as_cmap=True)
    start = timeit.default_timer()
    while current < total_sim:
        sim.setTerminationTime(current + 1)
        sim.simulate()
        # infected_df = pd.DataFrame(0.0, index=range(size), columns=range(size))
        # for i in range(size):
        #     for j in range(size):
        #         cell_state = sirGrid.cells[(i, j)].state
        #         infected_df.iloc[i, j] = cell_state[1]  # Store the infected percentage in the DataFrame
        #         # print(f"Cell ({i}, {j}) state: {cell_state}")
        #
        # if current % 10 == 0: # generate the plot only once per 10 simulation round
        #     plt.figure(figsize=(8, 6))  # Set a consistent figure size
        #     sns.heatmap(infected_df, cbar=True, cmap=cmap, vmin=0, vmax=1)
        #     plt.show(block=False)
        #     plt.clf()
        current += 1
    end = timeit.default_timer()
    print(str(end-start))
    time.sleep(10)
    # us.Singleton.get_instance().flagChange()
    print("changed :" + str(us.Singleton.get_instance().getFlag()))
    # infected_matrix = np.zeros((size, size))
    #
    # for i in range(size):
    #     for j in range(size):
    #         cell_state = sirGrid.cells[(i, j)].state
    #         infected_matrix[i, j] = cell_state[1]  # Store the infected percentage
    #         print(f"Cell ({i}, {j}) state: {cell_state}")

    # Plot the heatmap
    # plt.figure(figsize=(10, 8))
    # sns.heatmap(infected_matrix, cmap='YlOrRd', annot=True)
    # plt.title("Infected Percentage in SIRGrid")
    # plt.show()
    # for i in range(size):
    #     for j in range(size):
    #         cell_state = sirGrid.cells[(i, j)].state
    #         print(f"Cell ({i}, {j}) state: {cell_state}")
    # TODO: store in a df 5 columns each
    # https://stackoverflow.com/questions/55517072/python-plotting-grid-based-on-values
    # plotly
    # https://python-graph-gallery.com/heatmap/
# main factor of energy consumption
# pdevs cost
# size vs consumption    10*10 --> 100*100 --> .... 10000 characteristic
# Compare this
#
# do certain number of sim