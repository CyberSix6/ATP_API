#!/usr/bin/env python

"""@package DpSinkTests Teledyne LeCroy quantumdata Python API
examples for DisplayPort sink tests"""

# Copyright (c) 2022 Teledyne LeCroy, Inc.

## @file DpSinkTests.py
## @brief Sample code for running DisplayPort Sink tests

# This program is provided as a demonstration of how to use the
# Teledyne LeCroy quantumdata API suite for running DisplayPort sink
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

# All DP sink tests, can be run using a CDF file.
# Our GUI has an editor which allows you to describe the capabilities of your
# DUT and create a CDF file (which is in XML format).

# Create a simple, minimal CDF for Compliance test
cdfFile = 'D:/Python/LOG/cdf.txt' # Use whatever path suits you

cdfData = """
<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<DATAOBJ>
    <HEADER TYPE="DP_SINK14_CDF" VERSION="1.0"/>
    <DATA>
        <AUDIO_RECEPTION>YES</AUDIO_RECEPTION>
        <AUDIO_SUPPORTED_WITHOUT_VIDEO>NO</AUDIO_SUPPORTED_WITHOUT_VIDEO>
        <BRANCH_DEVICE>NO</BRANCH_DEVICE>
        <CDF_CTS_VERSION>Core R1.0</CDF_CTS_VERSION>
        <CEA_TIMINGS>1,2,3,4,5,6,7,8,9,10,11</CEA_TIMINGS>
        <CMPR_AUDIO_SUPPORTED>NO</CMPR_AUDIO_SUPPORTED>
        <COLORIMETRY>RGB VESA,RGB CTA,YCbCr 4:4:4,YCbCr 4:2:2</COLORIMETRY>
        <DEV_SPECIFIC_FIELDS>EEFFC0010000000000000000</DEV_SPECIFIC_FIELDS>
        <EDDC_SUPPORTED>YES</EDDC_SUPPORTED>
        <FAIL_SAFE_SUPPORTED>YES</FAIL_SAFE_SUPPORTED>
        <FEC_CRTBLE_BIT>YES</FEC_CRTBLE_BIT>
        <FEC_CRTBLE_BLK>YES</FEC_CRTBLE_BLK>
        <FEC_CRTBLE_PARITY_BIT>YES</FEC_CRTBLE_PARITY_BIT>
        <FEC_CRTBLE_PARITY_BLK>YES</FEC_CRTBLE_PARITY_BLK>
        <FEC_RECEPTION>YES</FEC_RECEPTION>
        <FEC_UNCRTBLE_BLK>YES</FEC_UNCRTBLE_BLK>
        <FIXED_TIMING>NO</FIXED_TIMING>
        <FT_BLANKING>Normal</FT_BLANKING>
        <FT_HRES>0</FT_HRES>
        <FT_SCAN>Progressive</FT_SCAN>
        <FT_VRAT>0.0</FT_VRAT>
        <FT_VRES>0</FT_VRES>
        <MAX_BPC>16</MAX_BPC>
        <MAX_CHANNEL_COUNT>4</MAX_CHANNEL_COUNT>
        <MAX_LANE_COUNT>4</MAX_LANE_COUNT>
        <MAX_LINK_RATE>8.10</MAX_LINK_RATE>
        <MULTI_SEG_EDID>YES</MULTI_SEG_EDID>
        <Manufacturer/>
        <Model/>
        <Port_Tested>1</Port_Tested>
        <RX_CAPS_FIELD>141EC4810100014000200408</RX_CAPS_FIELD>
        <SAMPLE_RATES>32.00,44.10,48.00,88.20,96.00</SAMPLE_RATES>
        <SAMPLE_SIZES>16,20,24</SAMPLE_SIZES>
        <TEST_AUTO_SUPPORTED>NO</TEST_AUTO_SUPPORTED>
        <TEST_DELAY>0</TEST_DELAY>
        <VESA_TIMINGS>1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21</VESA_TIMINGS>
        <VIDEO_RECEPTION>YES</VIDEO_RECEPTION>
    </DATA>
</DATAOBJ>"""

lFile = open(cdfFile, 'w')
lFile.write(cdfData)
lFile.close()

# Test the DP1.4 sink compliance test: Write Nine Bytes to Valid DPCD Addresses
showResults('5.2.1.4', TlqdDp14SinkTest(qdDev,'5.2.1.4', callback=None, testParameters=TLqdTestParameters(localDirectory='D:/Python/LOG', qdDirectory='/home/qd', cdf=cdfFile, collectAca=1, collectResult=1, collectEdid=0, collectSyslog=1, collectAlllogs=1)
))


cdfData = """
<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<DATAOBJ>
    <HEADER TYPE="DP_SINK20_CDF" VERSION="1.0"/>
    <DATA>
        <AUDIO_RECEPTION>YES</AUDIO_RECEPTION>
        <AUDIO_SUPPORTED_WITHOUT_VIDEO>NO</AUDIO_SUPPORTED_WITHOUT_VIDEO>
        <BRANCH_DEVICE>NO</BRANCH_DEVICE>
        <CDF_CTS_VERSION>Core R1.0</CDF_CTS_VERSION>
        <CDF_OVERRIDE>NO</CDF_OVERRIDE>
        <CEA_TIMINGS>1,2,3,4,5,6,7,8,9,10,11</CEA_TIMINGS>
        <CMPR_AUDIO_SUPPORTED>NO</CMPR_AUDIO_SUPPORTED>
        <COLORIMETRY>RGB VESA,RGB CTA,YCbCr 4:4:4,YCbCr 4:2:2</COLORIMETRY>
        <DEV_SPECIFIC_FIELDS>EEFFC0010000000000000000</DEV_SPECIFIC_FIELDS>
        <DSC_444_CRC_FOR_SIMPLE422>NO</DSC_444_CRC_FOR_SIMPLE422>
        <DSC_RECEPTION>YES</DSC_RECEPTION>
        <DSC_RX_BLOCK_PREDICTION>YES</DSC_RX_BLOCK_PREDICTION>
        <DSC_RX_COLOR>RGB,4:4:4,Simple 4:2:2,Native 4:2:2,Native 4:2:0</DSC_RX_COLOR>
        <DSC_RX_COLOR_DEPTH>12</DSC_RX_COLOR_DEPTH>
        <DSC_RX_SLICE>1,2,4,8,10,12,16,20,24</DSC_RX_SLICE>
        <DSC_RX_VERSION>DSC Version 1.1,DSC Version 1.2</DSC_RX_VERSION>
        <DSC_TIMINGS>11,12</DSC_TIMINGS>
        <EDDC_SUPPORTED>YES</EDDC_SUPPORTED>
        <FAIL_SAFE_SUPPORTED>YES</FAIL_SAFE_SUPPORTED>
        <FEC_CRTBLE_BIT>YES</FEC_CRTBLE_BIT>
        <FEC_CRTBLE_BLK>YES</FEC_CRTBLE_BLK>
        <FEC_CRTBLE_PARITY_BIT>YES</FEC_CRTBLE_PARITY_BIT>
        <FEC_CRTBLE_PARITY_BLK>YES</FEC_CRTBLE_PARITY_BLK>
        <FEC_RECEPTION>YES</FEC_RECEPTION>
        <FEC_UNCRTBLE_BLK>YES</FEC_UNCRTBLE_BLK>
        <FIXED_TIMING>NO</FIXED_TIMING>
        <FT_BLANKING>Normal</FT_BLANKING>
        <FT_HRES>0</FT_HRES>
        <FT_SCAN>Progressive</FT_SCAN>
        <FT_VRAT>0.0</FT_VRAT>
        <FT_VRES>0</FT_VRES>
        <MAX_BPC>16</MAX_BPC>
        <MAX_CHANNEL_COUNT>4</MAX_CHANNEL_COUNT>
        <MAX_LANE_COUNT>4</MAX_LANE_COUNT>
        <MAX_LINK_RATE>8.10</MAX_LINK_RATE>
        <MULTI_SEG_EDID>YES</MULTI_SEG_EDID>
        <Manufacturer/>
        <Model/>
        <Port_Tested>1</Port_Tested>
        <RX_CAPS_FIELD>1414C4810101030100200408</RX_CAPS_FIELD>
        <SAMPLE_RATES>32.00,44.10,48.00,88.20,96.00</SAMPLE_RATES>
        <SAMPLE_SIZES>16,20,24</SAMPLE_SIZES>
        <TEST_AUTO_SUPPORTED>NO</TEST_AUTO_SUPPORTED>
        <TEST_DELAY>0</TEST_DELAY>
        <UHBR_RATE_SUPPORTED>10.0(UHBR),13.5(UHBR),20.0(UHBR)</UHBR_RATE_SUPPORTED>
        <VESA_TIMINGS>1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21</VESA_TIMINGS>
        <VIDEO_RECEPTION>YES</VIDEO_RECEPTION>
    </DATA>
</DATAOBJ>"""

lFile = open(cdfFile, 'w')
lFile.write(cdfData)
lFile.close()
# Test the DP2.0 sink compliance test: Write EDID Offset (One Byte I2C-Over-AUX Write)
showResults('5.2.1.5', TlqdDp20SinkTest(qdDev,'5.2.1.5', callback=None, testParameters=TLqdTestParameters(localDirectory='D:/Python/LOG', qdDirectory='/home/qd', cdf=cdfFile, collectAca=1, collectResult=1, collectEdid=0, collectSyslog=1, collectAlllogs=1)
))

cdfData = """
<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<DATAOBJ>
    <HEADER TYPE="DP_SINKEDID_CDF" VERSION="1.0"/>
    <DATA>
        <BRANCH_DEVICE>NO</BRANCH_DEVICE>
        <CDF_CTS_VERSION>Core R1.2</CDF_CTS_VERSION>
        <CEA_TIMINGS/>
        <CMPR_AUDIO_SUPPORTED>NO</CMPR_AUDIO_SUPPORTED>
        <COLORIMETRY>RGB VESA,RGB CTA,YCbCr 4:4:4,YCbCr 4:2:2</COLORIMETRY>
        <MAX_BPC>16</MAX_BPC>
        <MAX_CHANNEL_COUNT>1</MAX_CHANNEL_COUNT>
        <Manufacturer/>
        <Model/>
        <Port_Tested>1</Port_Tested>
        <SAMPLE_RATES/>
        <SAMPLE_SIZES>16</SAMPLE_SIZES>
        <TEST_DELAY>0</TEST_DELAY>
        <VESA_TIMINGS/>
    </DATA>
</DATAOBJ>"""

lFile = open(cdfFile, 'w')
lFile.write(cdfData)
lFile.close()
# Test the EDID sink compliance test: Physical Display Characteristics
showResults('5.7.1.2', TlqdDpEdidSinkTest(qdDev,'5.7.1.2', callback=None, testParameters=TLqdTestParameters(localDirectory='D:/Python/LOG', qdDirectory='/home/qd', cdf=cdfFile, collectAca=1, collectResult=1, collectEdid=0, collectSyslog=1, collectAlllogs=1)
))

# Test the HDCP 2.X sink compliance test
showResults('2C_01',TlqdHdcp2xTest(qdDev, '2C_01', testParameters=TLqdTestParameters(localDirectory='D:/Python/LOG//2C_01')))

exit(0)
