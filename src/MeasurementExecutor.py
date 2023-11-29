from src.MeasureStrategy import MeasurementStrategy


class MeasurementExecutor:
    def __init__(self, strategy: MeasurementStrategy):
        self.strategy = strategy

    def set_strategy(self, new_strategy: MeasurementStrategy):
        self.strategy = new_strategy

    def execute(self):
        self.strategy.measure()

