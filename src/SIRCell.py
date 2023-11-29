from pypdevs.DEVS import AtomicDEVS


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
        # if not self.flag:
        #     return self.state
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
