#!/usr/bin/env python

"""@package HdmiSinkTests Teledyne LeCroy quantumdata Python API
examples for HDMI sink tests"""

# Copyright (c) 2019 Teledyne LeCroy, Inc.

## @file HdmiSinkTests.py
## @brief Sample code for running HDMI Sink tests

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

# Some of our compliance tests can be run on more than one card, such as
# the 18G generator, as well as the 18G RX/TX ("combo card").
# If you have more than one generator installed on the instrument you're testing
# with, it _might_ be necessary to use the API to set the card you're testing
# with.
# We provided an API to allow you to choose:

TLqdUse(qdDev, 4) # Use card #4 for testing

# We assume that the DUT is connected to the generator Tx port before every test

# Now we're ready to run a test

# This test will run HF2-5.
# This test requires a callback function to be provided so that the test can
# verify that the sink is receiving the proper image
# The callback is passed an information string and required to return
# a TLqdStatus object

def callback(info):
    return TLqdStatus.PASS

result = TLqdHF2_5(qdDev, callback)

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
showResults('HF2-5', result)

# Test HF2-6 can be used for VICs 96, 97, 101 or 102.
# The test also has a minimum or maximum TMDS adjustment

result = TLqdHF2_6(qdDev, callback, 97, False)

# Show the test results:
showResults('HF2-6 - maximum TMDS rate', result)

# Now run test HF2-6 at the minimum rate

result = TLqdHF2_6(qdDev, callback, 97, True)

# Show the test results:
showResults('HF2-6 - minimum TMDS rate', result)

# Test HF2-7 can be used for VICs 93, 94, 95, 98, 99 or 100 and color depths
# of 10-, 12- or 16-bits. The test also has a minimum or maximum TMDS rate.

# Run the test for VIC 94, 10-bit, maximum rate
result = TLqdHF2_7(qdDev, callback, 94, 10, False, False)

# Show the test results:
showResults('HF2-7 - 10-bit, maximum TMDS rate', result)

# Now run test HF2-7 again at the minimum rate

result = TLqdHF2_7(qdDev, callback, 94, 10, True, False)

# Show the test results:
showResults('HF2-7 - 10-bit, minimum TMDS rate', result)

# The test can also validate YCbCr 4:4:4
result = TLqdHF2_7(qdDev, callback, 94, 10, True, True)
showResults('HF2-7 - 10-bit, minimum TMDS rate, YCbCr 4:4:4', result)

# Test HF2-8 is for 3D and can be used for VICs 93-103 and 3D options
# of frame packing, top-and-bottom or side-by-side (half).
# The test also has a minimum or maximum TMDS rate.

# Run the test for VIC 93, frame packing, maximum rate
result = TLqdHF2_8(qdDev, callback, 93, 'F', False, False)

# Show the test results:
showResults('HF2-8 - frame packing, maximum TMDS rate', result)

# This test will run HF2-9 which can have 1 or 2 steps depending on the
# sinks EDID.

result = TLqdHF2_9(qdDev, callback, 1)

# Show the test results:
showResults('HF2-9', result)

# This test will run the second step for HF2-9

result = TLqdHF2_9(qdDev, callback, 2)

# Show the test results:
showResults('HF2-9', result)

# Test HF2-10 verifies that the sink has a proper HDMI Forum VSDB

# Run the test and display the results
showResults('HF2-10', TLqdHF2_10(qdDev))

# The YCbCr 4:2:0 test HF2-23 can run for VICs 96, 97, 101, 102, 106, or 106.
# There are two options for each VIC:
# 1. Low pixel clock (99.5%)
# 2. High pixel clock (100.5%)

# This test will run HF2-23 with the first step (low clock) for VIC 97

result = TLqdHF2_23(qdDev, callback, 97, 1)

# Show the test results:
showResults('HF2-23', result)

# Now run test HF2-23 with the second step (high clock) for VIC 97

result = TLqdHF2_23(qdDev, callback, 97, 2)

# Show the test results:
showResults('HF2-23', result)

# The Deep Color YCbCr 4:2:0 test HF2-24 can run for VICs 96, 97, 101, 102, 106,
# or 106.
# These are the supported pixel depths: 10, 12 or 16

# This test will run HF2-24 with 10 bits/color for VIC 96

result = TLqdHF2_24(qdDev, callback, 96, 10)

# Show the test results:
showResults('HF2-24', result)

# Now run test HF2-24 with 12 bits/color for VIC 96

result = TLqdHF2_24(qdDev, callback, 96, 12)

# Show the test results:
showResults('HF2-24', result)

# Test HF2-25 verifies the sink's EDID for 21x9 aspect ratio VICs
# The test has an EDID check, equivalent aspect ratio check (VICs 65 and 60,
# for example), minimal clock rate and maximum clock rate

# Test a subset of the valid VICs
for vic in [65, 66, 67, 68, 69]:

    result = TLqdHF2_25(qdDev, callback, vic, True, False, True, False)
    showResults('HF2-25 VIC ' + str(vic) + ' Aspect ratio 1', result)

    result = TLqdHF2_25(qdDev, callback, vic, True, True, False, False)
    showResults('HF2-25 VIC ' + str(vic) + ' Aspect ratio 2', result)

    result = TLqdHF2_25(qdDev, callback, vic, True, False, False, True)
    showResults('HF2-25 VIC ' + str(vic) + ' Minimum clock rate', result)

    result = TLqdHF2_25(qdDev, callback, vic, True, False, False, False)
    showResults('HF2-25 VIC ' + str(vic) + ' Maximum clock rate', result)

# Test HF2-26 verifies the sink's EDID for 21x9 aspect ratio VICs and HDMI VICs
# for DUTs that support > 340Mcsc

vics = [114, 115]

result = TLqdHF2_26(qdDev, vics, True)

# Show the test results:
showResults('HF2-26', result)

# All HDMI sink tests, including HF2-26, can be run using a CDF file.
# Our GUI has an editor which allows you to describe the capabilities of your
# DUT and create a CDF file (which is in XML format).

# Create a simple, minimal CDF for HF2-26

cdfFile = '/var/tmp/myCdf.txt'

cdfData = """
<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<DATAOBJ>
<HEADER TYPE="HDMI2_SINK_CDF" VERSION="1.0"/>
<DATA>
<SINK_Video_Formats_21by9>114, 115</SINK_Video_Formats_21by9>
</DATA>
</DATAOBJ>
"""

lFile = open(cdfFile, 'w')
lFile.write(cdfData)
lFile.close()

result = TLqdHF2_26(qdDev, [], False, cdfFile)

# Show the test results:
showResults('HF2-26 (CDF)', result)

# Test HF2-30 verifies multi-stream audio on the sink
# The test requires a callback to verify that the audio is properly received

result = TLqdHF2_30(qdDev, callback, stream=1)

# Show the test results:
showResults('HF2-30, stream #1', result)

result = TLqdHF2_30(qdDev, callback, stream=2)

# Show the test results:
showResults('HF2-30, stream #2', result)

# Now test the stream_flat bit behavior
result = TLqdHF2_30(qdDev, callback, flat=True)

# Show the test results:
showResults('HF2-30, flat', result)

# Test HF2-31 verifies the sink's EDID for 4K 4:2:0 VICs

# Tailor this list to the 4K 4:2:0 VICs your DUT supports
vics = [96, 97, 101, 102, 106, 107]

result = TLqdHF2_31(qdDev, vics)

# Show the test results:
showResults('HF2-31', result)

# Test HF2-32 verifies the sink's EDID for BT.2020 YCC and cYCC support

result = TLqdHF2_32(qdDev, True, True)

# Show the test results:
showResults('HF2-32', result)

# Test HF2-35 verifies the sink's EDID for YCbCr 4:2:0 deep-color support

# Run the test indicating support for 10-, 12- and 16-bit deep color
result = TLqdHF2_35(qdDev, [96, 97], True, True, True)

# Show the test results:
showResults('HF2-35', result)

# Test HF2-39 verifies the HDMI Audio Data Block in the sink's EDID

# Run the test indicating support for multi-stream audio
result = TLqdHF2_39(qdDev, True)

# Show the test results:
showResults('HF2-39', result)

# Test HF2-40 verifies that the Sink DUT correctly decodes and uses the
# information in the Vendor Specific InfoFrame, whenever it receives "Dual View"

# Run each step of the test indicating support for VIC 16, frame packing
for step in [1, 2, 3, 4]:
    result = TLqdHF2_40(qdDev, callback, 16, 'F', step)

    # Show the test results:
    showResults('HF2-40, step #' + str(step), result)

# Test HF2-41 verifies the independent view parameter of the HDMI Forum
# Data Block in the sink's EDID

# Run the test indicating support for independent view
result = TLqdHF2_41(qdDev, True)

# Show the test results:
showResults('HF2-41', result)

# Test HF2-43 verifies OSD Disparity for a DUT that supports it

# Run each option and step of the test for VIC 16, 3D frame packing
for opt in ['a', 'b', 'c', 'd']:
    for step in range(1, 5):
        result = TLqdHF2_43(qdDev, callback, 16, 'F', opt, step)

        # Show the test results:
        showResults('HF2-43 option ' + str(opt) + ', step #' + str(step),
                    result)

# Test HF2-53 verifies the HF-VSDB Data Block in the sink's EDID
# As you will see below, this test has many parameters to specify, so it
# may be easier to provide a CDF file instead of discrete values

# Run the test indicating support for SCDC, scrambling <= 340Mcsc,
# 4:2:0 10-, 12- and 16-bit deep color and rates above 340Mcsc
result = TLqdHF2_53(qdDev, scdc=True, lte340=True, dc10=True, dc12=True,
                    dc16=True, above340=True)

# Show the test results:
showResults('HF2-53', result)

# Test HFR2-53 verifies the HF-VSDB Data Block in the sink's EDID for HDMI 2.1
# As you can see in the method documentation, this test also has many
# parameters to specify, so it may be easier to provide a CDF file instead of
# discrete values

# Run the test indicating support for rates > 340Mcsc and max FRL of 6
result = TLqdHFR2_53(qdDev, above340=True, maxFrl=6)

# Show the test results:
showResults('HFR2-53', result)

# The EDID check for test HF2-54 verifies that the Sink DUT contains a valid
# HDR Static Metadata Data Block

# Run the test to check the EDID, with support for HDR Traditional SDR,
# HDR Traditional HDR, SMPTE ST.2084 and Hybrid Log Gamma
result = TLqdHF2_54(qdDev, None, True, sdr=True, hdr=True, smpte=True, hlg=True)

# Show the test results:
showResults('HF2-54 - EDID check', result)

# Now the test can be used to verify that the DUT can receive and decode
# the various formats

result = TLqdHF2_54(qdDev, callback, False, sdr=True)
showResults('HF2-54 - HDR Traditional SDR', result)

result = TLqdHF2_54(qdDev, callback, False, hdr=True)
showResults('HF2-54 - HDR Traditional HDR', result)

# There are 6 variations for SMPTE ST.2084
result = TLqdHF2_54(qdDev, callback, False, smpte=True, smpteOption=1)
showResults('HF2-54 - SMPTE ST.2084 R-G-B', result)

result = TLqdHF2_54(qdDev, callback, False, smpte=True, smpteOption=2)
showResults('HF2-54 - SMPTE ST.2084 R-B-G', result)

result = TLqdHF2_54(qdDev, callback, False, smpte=True, smpteOption=3)
showResults('HF2-54 - SMPTE ST.2084 G-R-B', result)

result = TLqdHF2_54(qdDev, callback, False, smpte=True, smpteOption=4)
showResults('HF2-54 - SMPTE ST.2084 G-B-R', result)

result = TLqdHF2_54(qdDev, callback, False, smpte=True, smpteOption=5)
showResults('HF2-54 - SMPTE ST.2084 B-R-G', result)

result = TLqdHF2_54(qdDev, callback, False, smpte=True, smpteOption=6)
showResults('HF2-54 - SMPTE ST.2084 B-G-R', result)

result = TLqdHF2_54(qdDev, callback, False, hlg=True)
showResults('HF2-54 - Hybrid Log Gamma', result)

# Test HFR2-70 verifies the Sink DUT EDID reserved bits in the SCDS

# Run the test
result = TLqdHFR2_70(qdDev)

# Show the test results:
showResults('HFR2-70', result)

# The YCbCr 4:2:0 test HF2-71 can run for CTA-861-G VICs 114, 115, 116, 117,
# 118, 119, 120, 124, 125, 126, 194, 195, 196, 202, 203, 204, 218 or 219.
# There are two options for each VIC:
# 1. Low pixel clock (99.5%)
# 2. High pixel clock (100.5%)

# This test will run HF2-71 with the first step (low clock) for VIC 117

result = TLqdHF2_71(qdDev, callback, 117, 1)

# Show the test results:
showResults('HF2-71', result)

# Now run test HF2-71 with the second step (high clock) for VIC 117

result = TLqdHF2_71(qdDev, callback, 117, 2)

# Show the test results:
showResults('HF2-71', result)

# The Deep Color YCbCr 4:2:0 test HF2-72 can run for CTA-861-G VICs 114, 115,
# 116, 117, 118, 119, 120, 124, 125, 126, 194, 195, 196, 202, 203, 204, 218
# or 219.
# These are the supported pixel depths: 10, 12 or 16

# This test will run HF2-72 with 10 bits/color for VIC 196

result = TLqdHF2_72(qdDev, callback, 196, 10)

# Show the test results:
showResults('HF2-72', result)

# Now run test HF2-72 with 12 bits/color for VIC 196

result = TLqdHF2_72(qdDev, callback, 196, 12)

# Show the test results:
showResults('HF2-72', result)

# Test HF2-94 confirms that the DUT supports basic audio
# The are 3 audio sampling rates (32, 44.1 and 48kHz).
# Each audio sampling rate is tested 4 times:
# 1. Nominal ("normal" N)
# 2. Minimum (smallest N)
# 3. Nominal (second nominal check)
# 4. Maximum (largest N)

showResults('HF2-94, 32kHz nominal N', TLqdHF2_94(qdDev,callback,32,"nominal"))
showResults('HF2-94, 32kHz minimum N', TLqdHF2_94(qdDev,callback,32,"minimum"))
showResults('HF2-94, 32kHz nominal N', TLqdHF2_94(qdDev,callback,32,"nominal"))
showResults('HF2-94, 32kHz maximum N', TLqdHF2_94(qdDev,callback,32,"maximum"))
showResults('HF2-94, 44.1kHz nominal N',
            TLqdHF2_94(qdDev,callback,44.1,"nominal"))
showResults('HF2-94, 44.1kHz minimum N',
            TLqdHF2_94(qdDev, callback, 44.1, "minimum"))
showResults('HF2-94, 44.1kHz nominal N',
            TLqdHF2_94(qdDev, callback, 44.1, "nominal"))
showResults('HF2-94, 44.1kHz maximum N',
            TLqdHF2_94(qdDev, callback, 44.1, "maximum"))
showResults('HF2-94, 48kHz nominal N', TLqdHF2_94(qdDev,callback,48,"nominal"))
showResults('HF2-94, 48kHz minimum N', TLqdHF2_94(qdDev,callback,48,"minimum"))
showResults('HF2-94, 48kHz nominal N', TLqdHF2_94(qdDev,callback,48,"nominal"))
showResults('HF2-94, 48kHz maximum N', TLqdHF2_94(qdDev,callback,48,"maximum"))

exit(0)
