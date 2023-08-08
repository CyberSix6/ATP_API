#!/usr/bin/env python

"""@package FrlSinkTests Teledyne LeCroy quantumdata Python API
examples for FRL sink tests"""

# Copyright (c) 2019 Teledyne LeCroy, Inc.

## @file FrlSinkTests.py
## @brief Sample code for running FRL Sink tests

# This program is provided as a demonstration of how to use the
# Teledyne LeCroy quantumdata API suite for running FRL compliance tests

# First you'll need to import our Python library.
# We distribute our Python library and you can download it from:
# <https://www.quantumdata.com/downloads.html>

# You'll also need to set your PYTHONPATH or append to sys.path
# sys.path.append('fully qualified path to wherever lib is installed')

# from __future__ import print_function
from tlqd import *
from sys import exit
from time import strftime

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

# Now that we're connected, we might want to check information on this
# instrument

print(TLqdVersion(qdDev)) # Show version

# This query examines what cards are present

print("\nComponents:")
for card in TLqdDiscover(qdDev):
    print(str(card))

# This shows the licensed items

print("\nLicensed items:")
for lic in TLqdLicenses(qdDev):
    print(str(lic))

# We assume that the DUT is connected to the generator Tx port before every test

# Now we're ready to run a test

# This test will run HFR2-17.
# Since this test requires manually removing and re-inserting a cable,
# it is not implemented yet

# This test requires a callback function to be provided so that the test can
# verify that the sink is receiving the proper image
# The callback is passed an information string and required to return
# a TLqdStatus object

def callback(info):
    return TLqdStatus.PASS

result = TLqdHFR2_17(qdDev, callback)

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

# Show the test results:
showResults('HFR2-17', result)

# Run HFR2-18.
# Since this test requires manually removing and re-inserting a cable,
# it is not implemented yet
showResults('HFR2-18', TLqdHFR2_18(qdDev, callback))

# Run HFR2-19.
# Since this test requires manually removing and re-inserting a cable,
# it is not implemented yet
showResults('HFR2-19', TLqdHFR2_19(qdDev, callback))

# Run HFR2-20.
# Since this test requires manually removing and re-inserting a cable,
# it is not implemented yet
showResults('HFR2-20', TLqdHFR2_20(qdDev, callback))

# Run HFR2-21.
# Since this test requires manually removing and re-inserting a cable,
# it is not implemented yet
showResults('HFR2-21', TLqdHFR2_21(qdDev, callback))

# Run HFR2-22.
# Since this test requires manually removing and re-inserting a cable,
# it is not implemented yet
showResults('HFR2-22', TLqdHFR2_22(qdDev, callback))

# Run HFR2-48.
# Since this test requires manually removing and re-inserting a cable,
# it is not implemented yet
showResults('HFR2-48', TLqdHFR2_48(qdDev, callback))

# Run HFR2-49.
# Since this test requires manually removing and re-inserting a cable,
# it is not implemented yet
showResults('HFR2-49', TLqdHFR2_49(qdDev, callback))

# Run HFR2-50.
# Since this test requires manually removing and re-inserting a cable,
# it is not implemented yet
showResults('HFR2-50', TLqdHFR2_50(qdDev, callback))

# Run HFR2-51.
# Since this test requires manually removing and re-inserting a cable,
# it is not implemented yet
showResults('HFR2-51', TLqdHFR2_51(qdDev, callback))

# Run HFR2-52.
# Since this test requires manually removing and re-inserting a cable,
# it is not implemented yet
showResults('HFR2-52', TLqdHFR2_52(qdDev, callback))

exit(0)
