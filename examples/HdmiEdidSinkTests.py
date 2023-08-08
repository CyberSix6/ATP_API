#!/usr/bin/env python

"""@package HdmiEdidSinkTests Teledyne LeCroy quantumdata Python API
examples for HDMI Edid Sink tests"""

# Copyright (c) 2019 Teledyne LeCroy, Inc.

## @file HdmiEdidSinkTests.py
## @brief Sample code for running HDMI EDID Sink tests

# This program is provided as a demonstration of how to use the
# Teledyne LeCroy quantumdata API suite for running HDMI compliance tests

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

# It's necessary to connect to the quantumdata instrument. We assume your
# quantumdata instrument can be accessed via the internet from where this
# program is run

# The following will try to connect to the quantumdata instrument

# You'll want to set this to your instrument's actual IP address
ip = '127.0.0.1'
ip = '10.30.196.165' # This is the IP address for my quantumdata instrument

# The recommended method to connect is ssh, but we can also use telnet.
# Our API uses the Paramiko library for ssh.
# You can download Paramiko from here: < http://www.paramiko.org/ >

# The default user ID and password are shown below - you may omit these or use
# your own values if you've changed either
qdDev = TLqdConnectSsh(ip, user='qd', passwd='qd')
# qdDev = TLqdConnectSsh(ip) # Same as above

# Here's how to connect with telnet
# qdDev = TLqdConnectTelnet(ip, user='qd', passwd='qd')

# Let's check that we're connected:

if not qdDev.connected: # Couldn't connect?
    # Generate a diagnostic and quit - no use trying to proceed
    print('Failed to connect to ' + ip)
    exit(1)

TLqdUse(qdDev, 2) # Use card #2
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

parms = TLqdTestParameters(localDirectory='D:/Python/LOG//EditTest',
                           saveCaptures=TLqdCaptureOption.Nothing, callbackSrcSet=False)

EdidTestIds = [
    "8-1","8-2","8-3",
    "8-17","8-18","8-19",
    "8-20",
    "HF2-10","HF2-26",
    "HF2-31","HF2-32",
    "HF2-35","HF2-39",
    "HF2-41","HF2-53",
    "HF2-66","HF2-74",
    "HF2-95","HF2-96",
    "HF2-97","HF2-98",
    "HFR2-53","HFR2-70"]

for testId in EdidTestIds:
  showResults(testId , TlqdEdidSinkTest(qdDev, testId, testParameters=parms))
