#!/usr/bin/env python

"""@package GamingSourceTests Teledyne LeCroy quantumdata Python API
examples for Gaming source tests"""

# Copyright (c) 2019 Teledyne LeCroy, Inc.

## @file GamingSourceTests.py
## @brief Sample code for running Gaming Source tests

# This program is provided as a demonstration of how to use the
# Teledyne LeCroy quantumdata API suite for running Gaming source compliance tests

# First you'll need to import our Python library.
# We distribute our Python library and you can download it from:
# <https://www.quantumdata.com/downloads.html>

# You'll also need to set your PYTHONPATH or append to sys.path
# sys.path.append('fully qualified path to wherever lib is installed')

# from __future__ import print_function
from tlqd import *
from sys import exit
from time import strftime, sleep
from math import ceil

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

def waitForReady(info):
    """Display information and return when ready

    @param info Information to display"""
    prompt = info + "\nHit enter when ready: "
    if sys.version_info >= (3, 0):
        input(prompt)
    else:
        raw_input(prompt)

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

def getColorSpace(csName):

    """ Get ColorSpace
    @param csName String identifying the color space
    @return TLqdColorSpace object for provided colorspace."""

    for cs in TLqdColorSpace.All:
        if cs.name == csName:
          return cs

def setImageAndFormat(entry):

    """ Set a Image, Format and Image parameters
    @param entry list of required inputs for source setup"""

    # To setup TMDS or Gaming mode
    # TMDS (0G0L), Gaming(12G4L)
    TLqdSetLinkTraining(qdDev, laneCount=0, linkRate=0)

    if int(entry[1]) == 3:
        TLqdSetImage(qdDev, "Master")
    else:
        TLqdSetImage(qdDev, "VRR_Test_1")
        TLqdSetFormat(qdDev, entry[2], colorSpace=getColorSpace(entry[3]),
                    subsampling=entry[4], bitDepth= entry[5])

        # 1. we need the vertical total of the VIC 
        format_parameters = TLqdGetFormatParameters(qdDev) #format_parameters.VerticalTotal = 1125

        # 2. next we figure out how many lines to add, in order to slow the timing to 48 frames per second
        lines_to_add = ceil((format_parameters.VerticalTotal * int(entry[6])) / int(entry[7])) - format_parameters.VerticalTotal # result is 282 lines to add

        if int(entry[1]) == 1:
            # 3. update the VRR image
            TLqdSetImageParameter(qdDev, 'VRR_Test_1', 'MODE', 0) # sets source to output timing at 48 Hz
            TLqdSetImageParameter(qdDev, 'VRR_Test_1', 'MVRR', lines_to_add)
            TLqdUpdateImage(qdDev)
        else:
            # 3. update the VRR image
            TLqdSetImageParameter(qdDev, 'VRR_Test_1', 'MODE', 1)
            TLqdSetImageParameter(qdDev, 'VRR_Test_1', 'MAX_MVRR', lines_to_add)
            TLqdSetImageParameter(qdDev, 'VRR_Test_1', 'MIN_MVRR', 0)
            TLqdUpdateImage(qdDev)

def setupCallback(stepNumber):

    """ Perform Source Setup
    @param stepNumber Stepnumber to fetch the parameter values for source setup
    @return TLqdStatus"""
    inFile = 'gamein.csv'
    with open(inFile) as inf: # open the input file
        next(inf)
        for line in inf:
            entry = line.strip('\r\n').split(',')
            if int(entry[0]) == stepNumber:
                setImageAndFormat(entry)
                break
    return TLqdStatus.PASS

parms = TLqdTestParameters(localDirectory='D:/Python/LOG//HF1_58/', saveCaptures=TLqdCaptureOption.Nothing, maxFrl=6)

for i in range(1, 30):
    result = TLqdHF1_58(qdDev, i, setupCallback, testParameters=parms)
    showResults('HF1-58 Validation ' + str(i), result)

exit(0)
