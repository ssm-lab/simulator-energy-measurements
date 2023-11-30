from pypdevs.DEVS import CoupledDEVS
from SIRCell import *
from src.SIRCell_By_T import SIRCell_By_T


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