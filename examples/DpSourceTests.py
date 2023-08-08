#!/usr/bin/env python

"""@package DpSourceTests Teledyne LeCroy quantumdata Python API
examples for DisplayPort source tests"""

# Copyright (c) 2022 Teledyne LeCroy, Inc.

## @file DpSourceTests.py
## @brief Sample code for running DisplayPort Source tests

# This program is provided as a demonstration of how to use the
# Teledyne LeCroy quantumdata API suite for running DisplayPort source
# compliance tests

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

# Your quantumdata instrument might be equipped with more than one DisplayPort
# analyzer card, such as the 1.4 Video Generator/Analyzer, as well as the
# DisplayPort 1.4 USB-C Video Generator/Analyzer.
# If you have more than one DisplayPort analyzer installed on the quantumdata
# instrument you're using, it is probably necessary to use the API to set the
# card you're using.
# For M41D or M42D use card #1.
# We provided an API to allow you to choose the card you wish to work with:

TLqdUse(qdDev, 1) # Use card #1

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
            print("\nInfo:")
        first = False
        print(item)
    first = True
    for item in result.errors:
        if first:
            print("\nErrors:")
        first = False
        print(item)

# All DP source tests, can be run using a CDF file.
# Our GUI has an editor which allows you to describe the capabilities of your
# DUT and create a CDF file (which is in XML format).

# Create a simple, minimal CDF for Compliance test
cdfFile = 'D:/Python/LOG/cdf.txt' # Use whatever path suits you

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

# Test the DP1.4 source compliance test: Retry on No-Reply During AUX Read after HPD Plug Event
showResults('4.2.1.1', TlqdDp14SourceTest(qdDev,'4.2.1.1', callback=None, testParameters=TLqdTestParameters(localDirectory='D:/Python/LOG', qdDirectory='/home/qd', cdf=cdfFile, collectAca=1, collectResult=1, collectEdid=0, collectSyslog=1, collectAlllogs=1)
))

cdfData = """
<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<DATAOBJ>
    <HEADER TYPE="DP_SRC20_CDF" VERSION="1.0"/>
    <DATA>
        <AUDIO_INFOFRM_SUPPORTED>YES</AUDIO_INFOFRM_SUPPORTED>
        <AUDIO_SUPPORTED_WITHOUT_VIDEO>NO</AUDIO_SUPPORTED_WITHOUT_VIDEO>
        <AUDIO_TRANSMISSION>YES</AUDIO_TRANSMISSION>
        <CDF_CTS_VERSION>Core R1.0</CDF_CTS_VERSION>
        <CEA_TIMINGS>1,2,3,4,5,6,7,8,9,10,11</CEA_TIMINGS>
        <CMPR_AUDIO_SUPPORTED>NO</CMPR_AUDIO_SUPPORTED>
        <COLORIMETRY>RGB VESA,RGB CTA</COLORIMETRY>
        <DEVICE_READY_INDICATOR>4</DEVICE_READY_INDICATOR>
        <DEVICE_TYPE>2</DEVICE_TYPE>
        <DRIVE_LEVEL3_SUPPORTED>YES</DRIVE_LEVEL3_SUPPORTED>
        <DSC_TRANSMISSION>YES</DSC_TRANSMISSION>
        <DSC_TX_BLOCK_PREDICTION>YES</DSC_TX_BLOCK_PREDICTION>
        <DSC_TX_COLOR>RGB,4:4:4,Simple 4:2:2,Native 4:2:2,Native 4:2:0</DSC_TX_COLOR>
        <DSC_TX_COLOR_DEPTH>8</DSC_TX_COLOR_DEPTH>
        <DSC_TX_SLICE>1,2,4,8,10</DSC_TX_SLICE>
        <DSC_TX_TIMINGS>31</DSC_TX_TIMINGS>
        <DSC_TX_VERSION>DSC Version 1.1,DSC Version 1.2</DSC_TX_VERSION>
        <EDDC_SUPPORTED>YES</EDDC_SUPPORTED>
        <FAIL_SAFE_SUPPORTED>YES</FAIL_SAFE_SUPPORTED>
        <FEC_DISABLE_SUPPORTED>NO</FEC_DISABLE_SUPPORTED>
        <FEC_TRANSMISSION>YES</FEC_TRANSMISSION>
        <FIXED_TIMING>NO</FIXED_TIMING>
        <FT_BLANKING>Normal</FT_BLANKING>
        <FT_HRES>0</FT_HRES>
        <FT_SCAN>Progressive</FT_SCAN>
        <FT_VRAT>0.0</FT_VRAT>
        <FT_VRES>0</FT_VRES>
        <LC_RED_NO_RETRAIN>NO</LC_RED_NO_RETRAIN>
        <LINK_STATUS_POLLED>NO</LINK_STATUS_POLLED>
        <MAX_BPC>8</MAX_BPC>
        <MAX_CHANNEL_COUNT>8</MAX_CHANNEL_COUNT>
        <MAX_LANE_COUNT>4</MAX_LANE_COUNT>
        <MAX_LINK_BW_POLICY>YES</MAX_LINK_BW_POLICY>
        <MAX_LINK_RATE>8.10</MAX_LINK_RATE>
        <MIN_BW_SUPPORTED>1LRBR</MIN_BW_SUPPORTED>
        <Manufacturer>Teledyne LeCroy</Manufacturer>
        <Model>M42D</Model>
        <PREEMP_LEVEL3_SUPPORTED>YES</PREEMP_LEVEL3_SUPPORTED>
        <Port_Tested>1</Port_Tested>
        <SAMPLE_RATES>32.00,44.10,48.00,88.20,96.00,176.40,192.00</SAMPLE_RATES>
        <SAMPLE_SIZES>16,20,24</SAMPLE_SIZES>
        <SPEAKER_ALLOCATION>0,1,2,3,4,9</SPEAKER_ALLOCATION>
        <SPRD_SPEC_CLK>YES</SPRD_SPEC_CLK>
        <TEST_AUDIO_PATTERN>YES</TEST_AUDIO_PATTERN>
        <TEST_AUTOMATION>NO</TEST_AUTOMATION>
        <TEST_DELAY>1</TEST_DELAY>
        <TEST_EDID_READ>YES</TEST_EDID_READ>
        <TEST_LINK_TRAINING>YES</TEST_LINK_TRAINING>
        <TEST_VIDEO_PATTERN>YES</TEST_VIDEO_PATTERN>
        <UHBR_LT_LTTPR_COUNT>0</UHBR_LT_LTTPR_COUNT>
        <UHBR_RATE_SUPPORTED>10.0(UHBR),13.5(UHBR),20.0(UHBR)</UHBR_RATE_SUPPORTED>
        <VESA_TIMINGS>1,2,3,4,5,6,7,8,9,10,11,12,13,14,16,17,18,20,21</VESA_TIMINGS>
        <VIDEO_TRANSMISSION>YES</VIDEO_TRANSMISSION>
        <V_FMT_CHNG_NO_RETRAIN>YES</V_FMT_CHNG_NO_RETRAIN>
    </DATA>
</DATAOBJ>"""

lFile = open(cdfFile, 'w')
lFile.write(cdfData)
lFile.close()

# Test the DP2.0 source compliance test: Retry on No-Reply During AUX Read after HPD Plug Event
showResults('4.3.1.2', TlqdDp20SourceTest(qdDev,'4.3.1.2', callback=None, testParameters=TLqdTestParameters(localDirectory='D:/Python/LOG', qdDirectory='/home/qd', cdf=cdfFile, collectAca=1, collectResult=1, collectEdid=0, collectSyslog=1, collectAlllogs=1)
))

cdfData = """
<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<DATAOBJ>
    <HEADER TYPE="DP_EDID_SRC_CDF" VERSION="1.0"/>
    <DATA>
        <AS_DUR_INC_DEC_SUPPORTED>NO</AS_DUR_INC_DEC_SUPPORTED>
        <AS_FIX_AVG_VTOTAL_SUPPORTED>NO</AS_FIX_AVG_VTOTAL_SUPPORTED>
        <AS_MIN_REF_RATE>59.94</AS_MIN_REF_RATE>
        <AS_TIMINGS>true,60.0000,1;false,60.0000,1;false,60.0000,1;false,60.0000,1;false,60.0000,1;false,60.0000,1;false,60.0000,1;false,60.0000,1</AS_TIMINGS>
        <AS_TRANSMISSION>YES</AS_TRANSMISSION>
        <AUDIO_INFOFRM_SUPPORTED>NO</AUDIO_INFOFRM_SUPPORTED>
        <AUDIO_SUPPORTED_WITHOUT_VIDEO>NO</AUDIO_SUPPORTED_WITHOUT_VIDEO>
        <AUDIO_TRANSMISSION>NO</AUDIO_TRANSMISSION>
        <CDF_CTS_VERSION>R1.4</CDF_CTS_VERSION>
        <CMPR_AUDIO_SUPPORTED>NO</CMPR_AUDIO_SUPPORTED>
        <COLORIMETRY>RGB VESA</COLORIMETRY>
        <CTA_TIMINGS>1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16</CTA_TIMINGS>
        <CVT_TIMINGS>1,2,3,4,5,6,7,8,9,10,11</CVT_TIMINGS>
        <DEVICE_READY_INDICATOR>4</DEVICE_READY_INDICATOR>
        <DEVICE_TYPE>1</DEVICE_TYPE>
        <DISPLAYID_TIMING_BLOCK/>
        <DMT_TIMINGS>13</DMT_TIMINGS>
        <DRIVE_LEVEL3_SUPPORTED>YES</DRIVE_LEVEL3_SUPPORTED>
        <EDDC_SUPPORTED>YES</EDDC_SUPPORTED>
        <FAIL_SAFE_SUPPORTED>YES</FAIL_SAFE_SUPPORTED>
        <LC_RED_NO_RETRAIN>NO</LC_RED_NO_RETRAIN>
        <MAX_BPC>6</MAX_BPC>
        <MAX_CHANNEL_COUNT>1</MAX_CHANNEL_COUNT>
        <MAX_LANE_COUNT>4</MAX_LANE_COUNT>
        <MAX_LINK_RATE>8.10</MAX_LINK_RATE>
        <MIN_PE_LEVEL>1</MIN_PE_LEVEL>
        <MIN_VS_LEVEL>0</MIN_VS_LEVEL>
        <Manufacturer/>
        <Model/>
        <PREEMP_LEVEL3_SUPPORTED>YES</PREEMP_LEVEL3_SUPPORTED>
        <Port_Tested>1</Port_Tested>
        <SAMPLE_RATES/>
        <SAMPLE_SIZES>16</SAMPLE_SIZES>
        <SPEAKER_ALLOCATION/>
        <SPRD_SPEC_CLK>YES</SPRD_SPEC_CLK>
        <TEST_AUDIO_PATTERN>NO</TEST_AUDIO_PATTERN>
        <TEST_AUTOMATION>NO</TEST_AUTOMATION>
        <TEST_DELAY>0</TEST_DELAY>
        <TEST_EDID_READ>NO</TEST_EDID_READ>
        <TEST_LINK_TRAINING>NO</TEST_LINK_TRAINING>
        <TEST_VIDEO_PATTERN>NO</TEST_VIDEO_PATTERN>
        <VIDEO_TRANSMISSION>YES</VIDEO_TRANSMISSION>
        <V_FMT_CHNG_NO_RETRAIN>NO</V_FMT_CHNG_NO_RETRAIN>
    </DATA>
</DATAOBJ>"""

lFile = open(cdfFile, 'w')
lFile.write(cdfData)
lFile.close()

# Test the Edid source compliance test:Preferred Timing
showResults('4.7.1.2', TlqdDpEdidSourceTest(qdDev,'4.7.1.2', callback=None, testParameters=TLqdTestParameters(localDirectory='D:/Python/LOG', qdDirectory='/home/qd', cdf=cdfFile, collectAca=1, collectResult=1, collectEdid=0, collectSyslog=1, collectAlllogs=1)
))


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

    if stepinfo.okOption:
        return TLqdStepStatus.OK
    elif stepinfo.passOption:
        return TLqdStepStatus.PASS
    else:
        return TLqdStepStatus.OK

testParameters=TLqdTestParameters(localDirectory='D:/Python/LOG', qdDirectory='/qd/home/', cdf=cdfFile, collectAca=1, collectResult=1, collectEdid=1, collectSyslog=1, collectAlllogs=1)
print(TlqdDp14SourceTest(qdDev,'4.3.3.1', callback, testParameters))

# Test the HDCP 2.X source compliance test
showResults('1A_01',TlqdHdcp2xTest(qdDev, '1A_01', testParameters=TLqdTestParameters(localDirectory='D:/Python/LOG//1A_01')))

exit(0)
