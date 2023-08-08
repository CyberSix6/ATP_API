#!/usr/bin/env python

"""@package DscSourceTests Teledyne LeCroy quantumdata Python API
examples for DSC source tests"""

# Copyright (c) 2021 Teledyne LeCroy, Inc.

## @file DscSourceTests.py
## @brief Sample code for running DSC Source tests

# This program is provided as a demonstration of how to use the
# Teledyne LeCroy quantumdata API suite for running DSC source compliance tests

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

ip = '10.30.196.166' # IP address for my quantumdata instrument

qdDev = TLqdConnectSsh(ip)

# Let's check that we're connected:

if not qdDev.connected: # Couldn't connect?
    # Generate a diagnostic and quit - no use trying to proceed
    print('Failed to connect to ' + ip)
    exit(1)

# We assume that the DUT is connected to the generator Tx port before every test

# Now we're ready to run a test

# This test will run HFR1-22.

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

def waitForReady(info):
    """Display information and return when ready

    @param info Information to display"""
    prompt = info + "\nHit enter when ready: "
    if sys.version_info >= (3, 0):
        input(prompt)
    else:
        raw_input(prompt)

testparam = TLqdTestParameters(callbackSrcSet=True)

def hfr122Callback1(stepNumber):

    info = """
    If you have control over your DUT, you should have it generate FRL
    output format DSC for 3 lanes which is required for HFR1-22."""
    waitForReady(info)
    return TLqdStatus.PASS

# Test DSC for 3 lanes
result = TLqdHFR1_22(qdDev, 1, callbackforSS=hfr122Callback1, testParameters=testparam)
# Show the test results:
showResults('HFR1-22 iteration 1', result)

def hfr122Callback2(stepNumber):

    info = """
    If you have control over your DUT, you should have it generate FRL
    output format deep color DSC for 4 lanes which is required for HFR1-22."""
    waitForReady(info)
    return TLqdStatus.PASS

# Test deep color DSC for 4 lanes
result = TLqdHFR1_22(qdDev, 2, 10, callbackforSS=hfr122Callback2, testParameters=testparam)
showResults('HFR1-22 iteration 2', result)


def hfr165Callback1(stepNumber):

    info = """
    Test the DUT for no CVTEMs with EDID DSC_1p2=0"""
    waitForReady(info)
    return TLqdStatus.PASS

# We will run all 3 iterations of HFR1-65.

# Test the DUT for no CVTEMs with EDID DSC_1p2=0
result = TLqdHFR1_65(qdDev, 1, callbackforSS=hfr165Callback1, testParameters=testparam)
showResults('HFR1-65 iteration 1', result)

def hfr165Callback2(stepNumber):

    info = """
    Test the DUT for CVTEMs with EDID DSC_1p2=1, FAPA_start_location=0"""
    waitForReady(info)
    return TLqdStatus.PASS

# Test the DUT for CVTEMs with EDID DSC_1p2=1, FAPA_start_location=0
result = TLqdHFR1_65(qdDev, 2, callbackforSS=hfr165Callback2, testParameters=testparam)
showResults('HFR1-65 iteration 2', result)

def hfr165Callback3(stepNumber):

    info = """
    Test the DUT for CVTEMs with EDID DSC_1p2=1, FAPA_start_location=1"""
    waitForReady(info)
    return TLqdStatus.PASS

# Test the DUT for CVTEMs with EDID DSC_1p2=1, FAPA_start_location=1
result = TLqdHFR1_65(qdDev, 3, callbackforSS=hfr165Callback3, testParameters=testparam)
showResults('HFR1-65 iteration 3', result)
cdfFile = 'D:\Python\LOG\cdf.txt'

cdfData = """
<?xml version="1.0" encoding="UTF-8" standalone="no"?>
    <DATAOBJ>
        <HEADER TYPE="DP_SRC14_CDF" VERSION="1.0"/>
        <DATA>
            <AUDIO_INFOFRM_SUPPORTED>YES</AUDIO_INFOFRM_SUPPORTED>
            <AUDIO_SUPPORTED_WITHOUT_VIDEO>YES</AUDIO_SUPPORTED_WITHOUT_VIDEO>
            <AUDIO_TRANSMISSION>YES</AUDIO_TRANSMISSION>
            <CDF_CTS_VERSION>Core R1.0</CDF_CTS_VERSION>
            <CEA_TIMINGS>1,2,3,4,5,6,7,8,9,10,11</CEA_TIMINGS>
            <CMPR_AUDIO_SUPPORTED>YES</CMPR_AUDIO_SUPPORTED>
            <COLORIMETRY>RGB VESA,RGB CTA,YCbCr 4:4:4,YCbCr 4:2:2</COLORIMETRY>
            <DEVICE_READY_INDICATOR>4</DEVICE_READY_INDICATOR>
            <DEVICE_TYPE>2</DEVICE_TYPE>
            <DRIVE_LEVEL3_SUPPORTED>YES</DRIVE_LEVEL3_SUPPORTED>
            <DSC_TRANSMISSION>NO</DSC_TRANSMISSION>
            <DSC_TX_BLOCK_PREDICTION>NO</DSC_TX_BLOCK_PREDICTION>
            <DSC_TX_COLOR/>
            <DSC_TX_COLOR_DEPTH>8</DSC_TX_COLOR_DEPTH>
            <DSC_TX_SLICE/>
            <DSC_TX_VERSION/>
            <EDDC_SUPPORTED>YES</EDDC_SUPPORTED>
            <FAIL_SAFE_SUPPORTED>YES</FAIL_SAFE_SUPPORTED>
            <FEC_DISABLE_SUPPORTED>YES</FEC_DISABLE_SUPPORTED>
            <FEC_TRANSMISSION>YES</FEC_TRANSMISSION>
            <FIXED_TIMING>NO</FIXED_TIMING>
            <FT_BLANKING>Normal</FT_BLANKING>
            <FT_HRES>0</FT_HRES>
            <FT_SCAN>Progressive</FT_SCAN>
            <FT_VRAT>0.0</FT_VRAT>
            <FT_VRES>0</FT_VRES>
            <LC_RED_NO_RETRAIN>NO</LC_RED_NO_RETRAIN>
            <LINK_STATUS_POLLED>NO</LINK_STATUS_POLLED>
            <MAX_BPC>18</MAX_BPC>
            <MAX_CHANNEL_COUNT>8</MAX_CHANNEL_COUNT>
            <MAX_LANE_COUNT>4</MAX_LANE_COUNT>
            <MAX_LINK_RATE>8.10</MAX_LINK_RATE>
            <Manufacturer/>
            <Model/>
            <PREEMP_LEVEL3_SUPPORTED>YES</PREEMP_LEVEL3_SUPPORTED>
            <Port_Tested>1</Port_Tested>
            <SAMPLE_RATES>32.00,44.10,48.00,88.20,96.00,176.40,192.00</SAMPLE_RATES>
            <SAMPLE_SIZES>16,20,24</SAMPLE_SIZES>
            <SPRD_SPEC_CLK>YES</SPRD_SPEC_CLK>
            <TEST_AUDIO_PATTERN>YES</TEST_AUDIO_PATTERN>
            <TEST_AUTOMATION>NO</TEST_AUTOMATION>
            <TEST_DELAY>10</TEST_DELAY>
            <TEST_EDID_READ>YES</TEST_EDID_READ>
            <TEST_LINK_TRAINING>YES</TEST_LINK_TRAINING>
            <TEST_VIDEO_PATTERN>YES</TEST_VIDEO_PATTERN>
            <VESA_TIMINGS>1,2,3,4,5,6,7,8,9,10,11,12,15,17,18,19,20,21</VESA_TIMINGS>
            <VIDEO_TRANSMISSION>YES</VIDEO_TRANSMISSION>
            <V_FMT_CHNG_NO_RETRAIN>YES</V_FMT_CHNG_NO_RETRAIN>
        </DATA>
    </DATAOBJ>"""

lFile = open(cdfFile, 'w')
lFile.write(cdfData)
lFile.close()

# Test the DUT for Retry on No-Reply During AUX Read after HPD Plug Event
result = TlqdDp14SourceTest(qdDev,'4.2.1.1', callback=None, testParameters=TLqdTestParameters(localDirectory='D:/Python/LOG', qdDirectory='/home/qd', cdf=cdfFile, collectAca=1, collectResult=1, collectEdid=0, collectSyslog=1, collectAlllogs=1)
)
showResults('4.2.1.1', result)


# The next test requires a callback function to be provided so that the test can
# verify that the source is receiving the step information for test execution
# The callback is passed an information string and required to return
# a TLqdStepStatus object from user

def callback(stepinfo):
    print("\nCallback info:\n")
    print("============================================================")
    print("                 Step file details:                         ")
    print("Step description:", stepinfo.description)
    print("Ok Option:", stepinfo.okOption)
    print("Fail Option:", stepinfo.noOption)
    print("Pass Option:", stepinfo.passOption)
    print("Fail Option:", stepinfo.failOption)
    print("Replay Option:", stepinfo.replayOption)
    print("=============================================================")
    return TLqdStepStatus.OK

# Test the DUT for Video Time Stamp Generation
testParameters=TLqdTestParameters(localDirectory='D:/Python/LOG', qdDirectory='/home/qd', cdf=cdfFile, collectAca=1, collectResult=1, collectEdid=0, collectSyslog=1, collectAlllogs=1)
result = TlqdDp14SourceTest(qdDev,'4.3.3.1', callback, testParameters)
showResults('4.3.3.1', result)

exit(0)
