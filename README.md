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
# Getting Started with MeasurementExecutor

Before diving into the API and specific measurement strategies, it's important to understand the foundational class at the core of this framework: `MeasurementExecutor`.

## Extending MeasurementExecutor

To effectively use the measurement strategies provided in this framework, you will need to extend the `MeasurementExecutor` class. This is the step allows you to integrate your specific measurable task (such as a simulation or any computational task) with the energy measurement process.

### Implementing `run_measurable`

After extending `MeasurementExecutor`, your primary task is to implement the `run_measurable` method. This method should contain the logic of your measurable task. During runtime, `MeasurementExecutor` will coordinate the execution of this task alongside the energy measurements, ensuring accurate and relevant energy consumption data is captured for your task.

### Example Skeleton

Here's a basic skeleton to get you started:

```python
from MeasurementExecutor import MeasurementExecutor

class YourCustomExecutor(MeasurementExecutor):
    def __init__(self):
        super().__init__()
        # Initialize your measurable task and any other necessary components here

    def run_measurable(self):
        # Implement the core logic of your measurable task here
        pass

# Example usage
executor = YourCustomExecutor()
executor.run_model()
```

Replace `YourCustomExecutor` with the name appropriate for your application. In the `__init__` method, set up your measurable task, and in `run_measurable`, implement its core logic.

## Next Steps

After setting up your custom executor by extending `MeasurementExecutor`, you're ready to dive into the Fluent API and Constructors to configure and utilize various measurement strategies.
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
from DurationBasedMeasurementStrategy import DurationBasedMeasurementStrategy

# Instantiate and configure the DurationBasedMeasurement strategy
duration_measure = DurationBasedMeasurementStrategy('energy_output.csv', 'data/').set_duration(5)
```
## FixedPeriodMeasurementStrategy

This strategy periodically measures energy consumption in a fixed period. 
- `FixedPeriodMeasurementStrategy(outfile_name, data_folder)`: Initializes a new instance of the FixedPeriodMeasurement class.
  - `outfile_name`: The name of the output file where the measurement data will be saved.
  - `data_folder:` The path to the directory where the output file will be stored.
#### API Methods:
- `set_duration(seconds)`: Sets the duration of each measurement period.
  - `seconds`: The duration of one measurement period in seconds.
- `set_period(total_seconds)`: Sets the fixed total duration for the measurement process.
  - `total_seconds`: The total time in seconds for the measurement, divided into periods as determined by set_duration

Example usage:
```python
from FixedPeriodMeasurementStrategy import FixedPeriodMeasurementStrategy

# Instantiate and configure the FixedPeriodMeasurement strategy using Fluent API
fixed_period_measure = FixedPeriodMeasurementStrategy('path/example.csv').set_duration(2).set_period(60)
```

## MeasurementExecutor

- `MeasurementExecutor` is a base class that coordinates the execution of a measurable object (like a simulation) alongside energy measurements of the entire machine while program running. Users should extend this class and implement the `run_measurable` method to define the behavior of their measurable object.

### Constructor:
- `MeasurementExecutor()`: Initializes a new instance of the MeasurementExecutor class. No parameters are required for the constructor.

### Fluent API Methods:
- `set_heat_up(heat_up: int)`: Specifies the heat-up duration before the measurable object start, which indicate the energy consumed by the operating system and other tasks before the program running.
  - `heat_up`: The number of seconds for the heat-up period.
- `set_cool_down(cool_down: int)`: Specifies the cool-down duration after the measurable object start, which indicate the energy consumed by the operating system and other tasks after the program running.
  - `cool_down`: The number of seconds for the cool-down period.
- `set_measurable(measurable)`: Assigns the measurable object that will be executed.
  - `measurable`: An object that will be used in the `run_measureable()` method.
- `set_strategy(new_strategy: MeasurementStrategy)`: Assigns the measurement strategy.
  - `new_strategy`: An instance of the `MeasurementStrategy` class.

### Abstract Methods:
- `run_measurable()`: An abstract method that should be implemented by the user to define the behavior of their measurable object.

### Example Usage:
Here's an example of how to extend `MeasurementExecutor` for a simulation using the `Simulator` class from the `pypdevs` package:

```python
from GridModel import *
from pypdevs.simulator import Simulator
from DurationBasedMeasurementStrategy import DurationBasedMeasurementStrategy
from MeasurementExecutor import MeasurementExecutor


class Demo(MeasurementExecutor):
    def __init__(self):
        super().__init__()
        # config the measurement strategy input file name and data folder
        measure_model = DurationBasedMeasurementStrategy("/file/to/store/your/data")
        # create demo measurable program
        sirGrid = SIRGrid(100)
        measuareable = Simulator(sirGrid)
        # config the MeasurementExecutor by calling fluent API methods
        self.set_strategy(measure_model).set_measuareable(measuareable).set_heat_up(10).set_cool_down(10)

    def run_measuareable(self):
        self.measuareable.setTerminationTime(10)
        total_sim = 100
        self.measuareable.setVerbose(None)
        current = 0
        while current < total_sim:
            self.measuareable.setTerminationTime(current + 1)
            self.measuareable.simulate()
            current += 1
            
if __name__ == '__main__':
    demo = Demo()
    demo.run_model()
```
Replace `your_simulation_model` and `YourSimulationModel` with your actual Measurable class. Implement the `run_measurable` method to perform the required simulation tasks.


# Demo
Profiling the energy consumption of PythonPDEVS, [here](/demo).
