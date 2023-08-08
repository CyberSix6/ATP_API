#!/usr/bin/env python

"""@package eArcSourceTests Teledyne LeCroy quantumdata Python API
examples for eARC source tests"""

# Copyright (c) 2019 Teledyne LeCroy, Inc.

## @file eArcSourceTests.py
## @brief Sample code for running eARC Source tests

# This program is provided as a demonstration of how to use the
# Teledyne LeCroy quantumdata API suite for running eARC source compliance tests

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

# This test will run HFR5-1-20. No data will be saved,

result = TLqdHFR5_1_20(qdDev)

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
showResults('HFR5-1-20', result)

# The next test will run HFR5-1-21

result = TLqdHFR5_1_21(qdDev)
showResults('HFR5-1-21', result)

# The next test will run HFR5-1-22

result = TLqdHFR5_1_22(qdDev)
showResults('HFR5-1-22', result)

# Run the remaining tests
showResults('HFR5-1-23', TLqdHFR5_1_23(qdDev))
showResults('HFR5-1-24', TLqdHFR5_1_24(qdDev))
showResults('HFR5-1-25', TLqdHFR5_1_25(qdDev))

# Test HFR5-1-28 verifies the DUT for 2-channel LPCM audio channel status
# Set-up your DUT to send 32kHz sampling, 16-bit samples

showResults('HFR5-1-28', TLqdHFR5_1_28(qdDev, 32, None, None))

# Now mute your DUT

showResults('HFR5-1-28', TLqdHFR5_1_28(qdDev, 32, 1, None))

# Now unmute your DUT

showResults('HFR5-1-28', TLqdHFR5_1_28(qdDev, 32, 0, None))

# Set up your DUT for 20-bit samples

showResults('HFR5-1-28', TLqdHFR5_1_28(qdDev, 32, None, 20))

# Test HFR5-1-29 verifies the DUT for multi-channel 2-channel LPCM audio
# channel status
# Set-up your DUT to send multi-channel, 44.1kHz sampling, 16-bit samples

showResults('HFR5-1-29', TLqdHFR5_1_29(qdDev, 44.1, None, None))

# Now mute your DUT

showResults('HFR5-1-29', TLqdHFR5_1_29(qdDev, 44.1, 1, None))

# Now unmute your DUT

showResults('HFR5-1-29', TLqdHFR5_1_29(qdDev, 44.1, 0, None))

# Set up your DUT for 20-bit samples

showResults('HFR5-1-29', TLqdHFR5_1_29(qdDev, 44.1, None, 20))

showResults('HFR5-1-26', TLqdHFR5_1_26(qdDev))

# Test HFR5-1-32 verifies the DUT for 2-channel LPCM audio rates

# This test requires a callback function to be provided so that the test can
# verify that the eARC source is sending proper audio
# The callback is passed an information string and required to return
# a TLqdStatus object

def callback(info):
    return TLqdStatus.PASS

# Set-up your DUT to send 48kHz sampling, 16-bit samples

showResults('HFR5-1-32', TLqdHFR5_1_32(qdDev, 48, callback))

# Test HFR5-1-33 verifies the DUT for multi-channel 2-channel LPCM audio rates
# Set-up your DUT to send multi-channel 44.1kHz sampling, 16-bit samples

showResults('HFR5-1-33', TLqdHFR5_1_33(qdDev, 44.1, callback))

# Test HFR5-1-34 verifies the DUT for channel allocation values with
# 8-channel LPCM audio
# Set-up your DUT to send 8-channel 48kHz sampling, 16-bit samples with channel
# allocation 13 (7.1)

showResults('HFR5-1-34', TLqdHFR5_1_34(qdDev, 48, 13, callback))

showResults('HFR5-1-35', TLqdHFR5_1_35(qdDev))
showResults('HFR5-1-36', TLqdHFR5_1_36(qdDev))
showResults('HFR5-1-37', TLqdHFR5_1_37(qdDev))

# Test HFR5-1-38 has two steps. The first step starts the test.
showResults('HFR5-1-38 step 1', TLqdHFR5_1_38(qdDev, 1))

# Now have the DUT enter then exit Standby, set HPD=0 for at least 100ms,
# then set HPD=1
showResults('HFR5-1-38 step 2', TLqdHFR5_1_38(qdDev, 2))

showResults('HFR5-1-39', TLqdHFR5_1_39(qdDev))
showResults('HFR5-1-50', TLqdHFR5_1_50(qdDev))
showResults('HFR5-1-51', TLqdHFR5_1_51(qdDev))
showResults('HFR5-1-52', TLqdHFR5_1_52(qdDev))
showResults('HFR5-1-55', TLqdHFR5_1_55(qdDev))

# Test HFR5-1-56 verifies the DUT for multi-channel 8-channel LPCM audio
# channel status
# Set-up your DUT to send multi-channel, 48kHz sampling, 16-bit samples
# with a CTA channel allocation of 13, 1F, 29, 2B, 2D, 2F or 31

showResults('HFR5-1-56', TLqdHFR5_1_56(qdDev, 48, None, None))

# Now mute your DUT

showResults('HFR5-1-56', TLqdHFR5_1_56(qdDev, 48, 1, None))

# Now unmute your DUT

showResults('HFR5-1-56', TLqdHFR5_1_56(qdDev, 48, 0, None))

# Set up your DUT for 20-bit samples

showResults('HFR5-1-56', TLqdHFR5_1_56(qdDev, 48, None, 20))

# Test HFR5-1-58 verifies the DUT for multi-channel 16-channel LPCM audio
# channel status
# Set-up your DUT to send multi-channel, 48kHz sampling, 16-bit samples with
# a CTA channel allocation of FE

speakers="55,FF,0F"
showResults('HFR5-1-58', TLqdHFR5_1_58(qdDev, 48, speakers, None))

# Now mute your DUT

showResults('HFR5-1-58', TLqdHFR5_1_58(qdDev, 48, speakers, 1))

# Now unmute your DUT

showResults('HFR5-1-58', TLqdHFR5_1_58(qdDev, 48, speakers, 0))

# Test HFR5-1-59 verifies the DUT for multi-channel 32-channel LPCM audio
# channel status
# Set-up your DUT to send multi-channel, 48kHz sampling, 16-bit samples with
# a CTA channel allocation of FF

speakers="[20,00],[21,01]"
showResults('HFR5-1-59', TLqdHFR5_1_59(qdDev, 48, speakers, None))

# Now mute your DUT

showResults('HFR5-1-59', TLqdHFR5_1_59(qdDev, 48, speakers, 1))

# Now unmute your DUT

showResults('HFR5-1-59', TLqdHFR5_1_59(qdDev, 48, speakers, 0))

exit(0)
