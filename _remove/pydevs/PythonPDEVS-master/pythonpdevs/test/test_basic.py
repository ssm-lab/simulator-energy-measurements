# Copyright 2014 Modelling, Simulation and Design Lab (MSDL) at 
# McGill University and the University of Antwerp (http://msdl.cs.mcgill.ca/)
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import subprocess
import sys
import unittest

from testActions import TestActions
from testExceptions import TestExceptions
from testGVT import TestGVT
from testHelpers import TestHelpers
from testLocal import TestLocal
from testLogger import TestLogger
from testMessageScheduler import TestMessageScheduler
from testScheduler import TestScheduler
from testTermination import TestTermination
from testTestUtils import TestTestUtils
from testWait import TestWait

if __name__ == '__main__':
    local = unittest.TestLoader().loadTestsFromTestCase(TestLocal)
    actions = unittest.TestLoader().loadTestsFromTestCase(TestActions)
    termination = unittest.TestLoader().loadTestsFromTestCase(TestTermination)
    gvt = unittest.TestLoader().loadTestsFromTestCase(TestGVT)
    exceptions = unittest.TestLoader().loadTestsFromTestCase(TestExceptions)
    wait = unittest.TestLoader().loadTestsFromTestCase(TestWait)
    helpers = unittest.TestLoader().loadTestsFromTestCase(TestHelpers)
    scheduler = unittest.TestLoader().loadTestsFromTestCase(TestScheduler)
    mscheduler = unittest.TestLoader().loadTestsFromTestCase(TestMessageScheduler)
    testutils = unittest.TestLoader().loadTestsFromTestCase(TestTestUtils)
    logger = unittest.TestLoader().loadTestsFromTestCase(TestLogger)

    allTests = unittest.TestSuite()
    allTests.addTest(testutils)
    allTests.addTest(actions)
    allTests.addTest(helpers)
    allTests.addTest(gvt)
    allTests.addTest(termination)
    allTests.addTest(exceptions)
    allTests.addTest(wait)
    allTests.addTest(scheduler)
    allTests.addTest(logger)
    allTests.addTest(local)

    unittest.TextTestRunner(verbosity=2, failfast=True).run(allTests)
