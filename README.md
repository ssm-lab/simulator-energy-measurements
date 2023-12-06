A wrapper for energy profiling of Python programs.
It uses the [pyJoules](https://pyjoules.readthedocs.io/en/latest/) toolkit and adds some high-level configuration options to implement measurement best practices, e.g., warm-up and cool-down periods.

# Supported platforms
Only for UNIX systems.
pyJoules uses the Intel Running Average Power Limit (RAPL) technology to estimate energy consumption, and RAPL is implemented only for UNIX systems.

# Repository Structure
- `util/` - Utility scripts and helper functions to support the main application.
- `DurationBasedMeasurementStrategy.py` - Implements duration-based energy measurement extending the MeasurementStrategy, which measure the energy consumed the energy consumed by each machine component periodically until a signal has been received.
- `FixedPeriodMeasurementStrategy.py` - Implements fixed-period energy measurement extending the MeasurementStrategy, which periodically measure the energy consumed over a specific period.
- `MeasurementStrategy.py` - Abstract base class providing the template for energy measurement strategies.
- `MeasurementExecutor.py` - Executes a measurement strategy instance.

# Setup guide
- Clone this repository.
- Install requirements via ```pip install -r requirements.txt```.

# How to Use

## Fluent API and Constructors

The Fluent API enables you to set up your measurement strategies by chaining method calls, resulting in a clear setup. Each strategy can be instantiated and configured using its constructor and fluent API methods.

## DurationBasedMeasurement

This strategy is designed for measuring the energy consumed by each machine component periodically until a signal has been received.

### Constructor:
- `DurationBasedMeasurement(outfile_name, data_folder)`: Initializes a new instance of the DurationBasedMeasurement class.
  - `outfile_name`: The name of the output file where the measurement data will be saved.
  - `data_folder`: The path to the directory where the output file will be stored.

#### API Methods:
- `set_duration(seconds)`: Set the duration for energy measurement.
  - `seconds`: The number of seconds for which to measure energy consumption.

Example usage:
```python
from src.DurationBasedMeasurement import DurationBasedMeasurement

# Instantiate and configure the DurationBasedMeasurement strategy
duration_measure = DurationBasedMeasurement('energy_output.csv', 'data/').set_duration(5)
```
## FixedPeriodMeasurement

This strategy periodically measures energy consumption in a fixed period. 
- `FixedPeriodMeasurement(outfile_name, data_folder)`: Initializes a new instance of the FixedPeriodMeasurement class.
  - `outfile_name`: The name of the output file where the measurement data will be saved.
  - `data_folder:` The path to the directory where the output file will be stored.
#### API Methods:
- `set_duration(seconds)`: Sets the duration of each measurement period.
  - `seconds`: The duration of one measurement period in seconds.
- `set_period(total_seconds)`: Sets the fixed total duration for the measurement process.
  - `total_seconds`: The total time in seconds for the measurement, divided into periods as determined by set_duration

Example usage:
```python
from src.FixedPeriodMeasurement import FixedPeriodMeasurement

# Instantiate and configure the FixedPeriodMeasurement strategy using Fluent API
fixed_period_measure = FixedPeriodMeasurement('energy_output.csv', 'data/').set_duration(2).set_period(60)
```

## ModelExecutor

- `ModelExecutor` is a base class that coordinates the execution of a measurable object (like a simulation) alongside energy measurements of the entire machine while program running. Users should extend this class and implement the `run_measurable` method to define the behavior of their measurable object.

### Constructor:
- `ModelExecutor()`: Initializes a new instance of the ModelExecutor class. No parameters are required for the constructor.

### Fluent API Methods:
- `set_heat_up(heat_up: int)`: Specifies the heat-up duration before the measurable object start, which indicate the energy consumed by the operating system and other tasks before the program running.
  - `heat_up`: The number of seconds for the heat-up period.
- `set_cool_down(cool_down: int)`: Specifies the cool-down duration after the measurable object start, which indicate the energy consumed by the operating system and other tasks after the program running.
  - `cool_down`: The number of seconds for the cool-down period.
- `set_measurable(measurable)`: Assigns the measurable object that will be executed.
  - `measurable`: An object that will be used in the `run_measureable()` method.
- `set_executor(measure_executor: MeasurementExecutor)`: Assigns the measurement executor that will carry out the measurement strategy.
  - `measure_executor`: An instance of the `MeasurementExecutor` class.

### Abstract Methods:
- `run_measurable()`: An abstract method that should be implemented by the user to define the behavior of their measurable object.

### Example Usage:
Here's an example of how to extend `ModelExecutor` for a simulation using the `Simulator` class from the `pypdevs` package:

```python
from pypdevs.simulator import Simulator

from src.DurationBasedMeasurement import DurationBasedMeasurement
from GridModel import *
from src.ModelExecutor import ModelExecutor
from src.MeasurementExecutor import MeasurementExecutor
from util.singletonFlag import Singleton


class Demo(ModelExecutor):
    def __init__(self):
        super().__init__()
        # config the measurement input file name and data folder
        measure_model = DurationBasedMeasurement("test",
                                                 "/home/yimoning/mcmaster/fall2023/sim_energy_measurements/data/")
        # set up measurement executor
        measure_executor = MeasurementExecutor(measure_model)
        # create demo measurable program
        sirGrid = SIRGrid(100)
        measuareable = Simulator(sirGrid)
        # config the ModelExecutor by calling fluent API methods
        self.set_executor(measure_executor).set_measuareable(measuareable).set_heat_up(10).set_cool_down(10)

    def run_measuareable(self):
        # define the behavior of their measurable object.
        self.measuareable.setTerminationTime(1)
        total_sim = 10
        self.measuareable.setVerbose(None)
        current = 0
        while current < total_sim:
            self.measuareable.setTerminationTime(current + 1)
            self.measuareable.simulate()
            current += 1
        Singleton.get_instance().store_time(label="sim_end")
        self.measurable_end()

if __name__ == '__main__':
    demo = Demo()
    demo.run_model()
```
Replace `your_simulation_model` and `YourSimulationModel` with your actual Measurable class. Implement the `run_measurable` method to perform the required simulation tasks.


# Demo
Profiling the energy consumption of PythonPDEVS, [here](/demo).
