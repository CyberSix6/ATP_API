#!/usr/bin/env python

"""@package HdcpSinkTests Teledyne LeCroy quantumdata Python API
examples for HDCP sink tests"""

# Copyright (c) 2021 Teledyne LeCroy, Inc.

## @file HdcpSinkTests.py
## @brief Sample code for running HDCP Source tests

# This program is provided as a demonstration of how to use the
# Teledyne LeCroy quantumdata API suite for running HDCP sink compliance tests

# First you'll need to import our Python library.
# We distribute our Python library and you can download it from:
# <https://www.quantumdata.com/downloads.html>

# You'll also need to set your PYTHONPATH or append to sys.path
# sys.path.append('fully qualified path to wherever lib is installed')

# from __future__ import print_function
from tlqd import *
from sys import exit

# Our API is designed to allow you to use object oriented *or* functional
# programming techniques

# Connect to the quantumdata instrument

ip = '10.30.196.165' # IP address for my quantumdata instrument

qdDev = TLqdConnectSsh(ip)

# Let's check that we're connected:

if not qdDev.connected: # Couldn't connect?
    # Generate a diagnostic and quit - no use trying to proceed
    print('Failed to connect to ' + ip)
    exit(1)

# We assume that the DUT is connected to the generator Tx port before every test

# Now we're ready to run a test

# Every test returns a TLqdResult. The status member is a TLqdStatus object
# indicating the overall test result and will be one of SKIPPED (the test
# wasn't run), PASS (the test passed) or FAIL (the test failed).
# The info member will be a list of zero or more information
# strings. The errors member is a list of zero or more errors.
# Any errors would likely cause a test to be failed or skipped.

# Define a function to show the test results:

def showResults(test, result):

    """Display test results
    @param test Information about the test
    @param result TLqdResult test result"""

    print("\n" + test + ' result: ' + str(result.status))
    first = True
    for item in result.info:
        if first:
            print("Info:")
        first = False
        print(item)
    first = True
    for item in result.errors:
        if first:
            print("Errors:")
        first = False
        print(item)

# Test the HDCP 2.X sink compliance tests
testParameters=TLqdTestParameters(localDirectory='D:/Python/LOG//2C_01')
showResults('2C_01',TlqdHdcp2xTest(qdDev, '2C_01', testParameters))

testParameters=TLqdTestParameters(localDirectory='D:/Python/LOG//2C_06')
showResults('2C_06',TlqdHdcp2xTest(qdDev, '2C_06', testParameters))

exit(0)
