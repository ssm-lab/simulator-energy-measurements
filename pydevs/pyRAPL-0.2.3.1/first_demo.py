import pyRAPL
import time
import sys
sys.path.append("/home/yimoning/research/pydevs/PythonPDEVS-master/pythonpdevs/examples/trafficlight_realtime")
import experiment_loop_run as md

pyRAPL.setup()
# ===========================================
# Measuring a comsumption of a piece of code
measure = pyRAPL.Measurement('bar')
measure.begin()

md.run(10)
measure.end()
pass
# ===========================================
# Measuring the entire machine
# csv_output = pyRAPL.outputs.CSVOutput('result.csv')
#
# # @pyRAPL.measureit
# @pyRAPL.measureit(output=csv_output)
# def foo():
#     time.sleep(0.1)
#
# # Instructions to be evaluated.
# for _ in range(100):
#     foo()
# csv_output.save()

import pyRAPL

pyRAPL.setup()
measure = pyRAPL.Measurement('bar')
measure.begin()



measure.end()