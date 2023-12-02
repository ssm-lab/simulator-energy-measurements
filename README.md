A wrapper for energy profiling of Python programs.
It uses the [pyJoules](https://pyjoules.readthedocs.io/en/latest/) toolkit and adds some high-level configuration options to implement measurement best practices, e.g., warm-up and cool-down periods.

# Supported platforms
Only for UNIX systems.
pyJoules uses the Intel Running Average Power Limit (RAPL) technology to estimate energy consumption, and RAPL is implemented only for UNIX systems.

# Repository structure
- TODO


# Setup guide
- Clone this repository.
- Install requirements via ```pip install -r requirements.txt```.

# How to use
- TODO

# Demo
Profiling the energy consumption of PythonPDEVS, [here](/demo).
