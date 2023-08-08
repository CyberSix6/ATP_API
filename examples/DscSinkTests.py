#!/usr/bin/env python

"""@package DscSinkTests Teledyne LeCroy quantumdata Python API
examples for DSC sink tests"""

# Copyright (c) 2019 Teledyne LeCroy, Inc.

## @file DscSinkTests.py
## @brief Sample code for running DSC Sink tests

# This program is provided as a demonstration of how to use the
# Teledyne LeCroy quantumdata API suite for running DSC compliance tests

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

# This test will run HFR2-80.

# This test requires a callback function to be provided so that the test can
# verify that the sink is receiving the proper image
# The callback is passed an information string and required to return
# a TLqdStatus object

def callback(info):
    print("\n"+info)
    sys.stdout.write("Pass? ")
    resp = raw_input()
    if len(resp) == 0 or resp.upper()[0] == 'Y':
        return TLqdStatus.PASS
    return TLqdStatus.FAIL

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

# The test verifies the following 2160p VICs
for vic in [103, 104, 105, 106, 107, 117, 118, 119, 120, 124, 125, 126, 127,
            193, 218, 219]:

    # There are 8 combinations of options for each VIC

    for rgb in [True, False]:
        rgbOpt = "RGB"
        if not rgb:
            rgbOpt = "YCbCr 4:4:4"

        for minRate in [True, False]:
            rateOpt = "99.5%"
            if not minRate:
                rateOpt = "100.5%"

            for maxFrl in [True, False]:
                frlOpt = "highest FRL"
                if not maxFrl:
                    frlOpt = "lowest FRL"

                # Test DSC for the VIC
                result = TLqdHFR2_80(qdDev, callback, vic, rgb, minRate, maxFrl)

                # Show the test results:
                showResults('HFR2-80 VIC ' + str(vic) + ', ' + rgbOpt + ', ' +
                            rateOpt + ' pixel rate, ' + frlOpt + ' rate',
                            result)

# The test verifies the following 4320p VICs
for vic in [194, 195, 196, 202, 203, 204, 210, 211, 212]:

    # There are 8 combinations of options for each VIC

    for rgb in [True, False]:
        rgbOpt = "RGB"
        if not rgb:
            rgbOpt = "YCbCr 4:4:4"

        for minRate in [True, False]:
            rateOpt = "99.5%"
            if not minRate:
                rateOpt = "100.5%"

            for maxFrl in [True, False]:
                frlOpt = "highest FRL"
                if not maxFrl:
                    frlOpt = "lowest FRL"

                # Test DSC for the VIC
                result = TLqdHFR2_81(qdDev, callback, vic, rgb, minRate, maxFrl)

                # Show the test results:
                showResults('HFR2-81 VIC ' + str(vic) + ', ' + rgbOpt + ', ' +
                            rateOpt + ' pixel rate, ' + frlOpt + ' rate',
                            result)

# The test verifies the following 2160p VICs
for vic in [103, 104, 105, 106, 107, 117, 118, 119, 120, 124, 125, 126, 127,
            193, 218, 219]:

    # There are 8 combinations of options for each VIC

    for tenBit in [True, False]:
        bitOpt = "10-bpc"
        if not tenBit:
            bitOpt = "12-bpc"

        for minRate in [True, False]:
            rateOpt = "99.5%"
            if not minRate:
                rateOpt = "100.5%"

            for maxFrl in [True, False]:
                frlOpt = "highest FRL"
                if not maxFrl:
                    frlOpt = "lowest FRL"

                # Test DSC for the VIC
                result = TLqdHFR2_82(qdDev, callback, vic, tenBit, minRate,
                                     maxFrl)

                # Show the test results:
                showResults('HFR2-82 VIC ' + str(vic) + ', ' + bitOpt + ', ' +
                            rateOpt + ' pixel rate, ' + frlOpt + ' rate',
                            result)

# The test verifies the following 4320p VICs
for vic in [194, 195, 196, 202, 203, 204, 210, 211, 212]:

    # There are 8 combinations of options for each VIC

    for tenBit in [True, False]:
        bitOpt = "10-bpc"
        if not tenBit:
            bitOpt = "12-bpc"

        for minRate in [True, False]:
            rateOpt = "99.5%"
            if not minRate:
                rateOpt = "100.5%"

            for maxFrl in [True, False]:
                frlOpt = "highest FRL"
                if not maxFrl:
                    frlOpt = "lowest FRL"

                # Test DSC for the VIC
                result = TLqdHFR2_83(qdDev, callback, vic, tenBit, minRate,
                                     maxFrl)

                # Show the test results:
                showResults('HFR2-83 VIC ' + str(vic) + ', ' + bitOpt + ', ' +
                            rateOpt + ' pixel rate, ' + frlOpt + ' rate',
                            result)

# The test verifies the following 2160p VICs
for vic in [96, 97, 101, 102, 106, 107, 114, 115, 116, 117, 118, 119, 120, 121,
            122, 123, 124, 125, 126, 218, 219]:

    # There are 8 combinations of options for each VIC

    for ycc420 in [True, False]:
        yccOpt = "4:2:0"
        if not ycc420:
            yccOpt = "4:2:2"

        for minRate in [True, False]:
            rateOpt = "99.5%"
            if not minRate:
                rateOpt = "100.5%"

            for maxFrl in [True, False]:
                frlOpt = "highest FRL"
                if not maxFrl:
                    frlOpt = "lowest FRL"

                # Test DSC for the VIC
                result = TLqdHFR2_84(qdDev, callback, vic, ycc420, minRate,
                                     maxFrl)

                # Show the test results:
                showResults('HFR2-84 VIC ' + str(vic) + ', YCbCr ' + yccOpt +
                            ', ' + rateOpt + ' pixel rate, ' + frlOpt + ' rate',
                            result)

# The test verifies the following 4320p VICs
for vic in [194, 195, 196, 202, 203, 204]:

    # There are 8 combinations of options for each VIC

    for ycc420 in [True, False]:
        yccOpt = "4:2:0"
        if not ycc420:
            yccOpt = "4:2:2"

        for minRate in [True, False]:
            rateOpt = "99.5%"
            if not minRate:
                rateOpt = "100.5%"

            for maxFrl in [True, False]:
                frlOpt = "highest FRL"
                if not maxFrl:
                    frlOpt = "lowest FRL"

                # Test DSC for the VIC
                result = TLqdHFR2_85(qdDev, callback, vic, ycc420, minRate,
                                     maxFrl)

                # Show the test results:
                showResults('HFR2-85 VIC ' + str(vic) + ', YCbCr ' + yccOpt +
                            ', ' + rateOpt + ' pixel rate, ' + frlOpt + ' rate',
                            result)

exit(0)
