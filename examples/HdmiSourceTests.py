#!/usr/bin/env python

"""@package HdmiSourceTests Teledyne LeCroy quantumdata Python API
examples for HDMI source tests"""

# Copyright (c) 2019 Teledyne LeCroy, Inc.

## @file HdmiSourceTests.py
## @brief Sample code for running HDMI Source tests

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
ip = '10.30.196.195' # This is the IP address for my quantumdata instrument

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
# the 18G protocol analyzer, as well as the 18G RX/TX ("combo card").
# If you have more than one analyzer installed on the instrument you're testing
# with, it _might_ be necessary to use the API to set the card you're testing
# with.
# We provided an API to allow you to choose:

TLqdUse(qdDev, 2) # Use card #2 for testing

# Almost every test generates several "artifacts" - files from a capture, for
# example. You may choose to save this data on the instrument itself, the local
# host, both or neither. Our test API allows you to specify a "localDirectory"
# parameter to save files locally and a "qdDirectory" parameter to save
# files on the instrument. If you set "localDirectory", you do not need to set
# "qdDirectory" unless you want files saved on the instrument too.

# Every test can optionally issue a hot-plug to get the DUT to transmit a format
# that meets the requirements of the test. Additionally, although we provide an
# EDID that should coax the DUT into sending the expected format, we also
# allow you to provide your own EDID. Finally, if your DUT can be controlled
# directly, we allow the hot-plug to be avoided.

# We assume that the DUT is connected to the analyzer Rx port before every test

# Now we're ready to run a test

# Avoid HP
noHp = TLqdTestParameters(omitHp=True)

info = """
If you have control over your DUT, you should have it generate an
output format > 340Mcsc which is required for HF1-10.
If not, the EDID we set followed by a hot-plug _should_ do the trick."""

def waitForReady(info):
    """Display information and return when ready

    @param info Information to display"""
    prompt = info + "\nHit enter when ready: "
    if sys.version_info >= (3, 0):
        input(prompt)
    else:
        raw_input(prompt)

def hf110Callback1(stepNumber):

    info = """
    Now we can run the first step of HF1-10. No data will be saved,
    the test will generate an EDID, but will not signal the DUT with a hot-plug."""
    waitForReady(info)

    return TLqdStatus.PASS

# Use a 2% capture size
testparam = TLqdTestParameters(captureSizePct=2, saveCaptures=TLqdCaptureOption.Nothing,
                               localDirectory='D:/Python/LOG//HF1_10', callbackSrcSet=True, omitHp=True)

# This test will run the first step of HF1-10. No data will be saved,
# the test will generate an EDID, but will not signal the DUT with a hot-plug

result = TLqdHF1_10(qdDev, 1, hf110Callback1, testParameters=testparam)

# Every test returns a TLqdResult. The status member is a TLqdStatus object
# indicating the overall test result and will be one of SKIPPED (the test
# wasn't run), PASS (the test passed) or FAIL (the test failed).
# The info member will be a list of zero or more information
# strings. The errors member is a list of zero or more errors.
# Any errors would likely cause a test to be failed or skipped.

# An example of an error which will cause a skipped test is for HF1-10 which
# received a format of < 340Mcsc (which is required by the GCTS). The test will
# report the error in the error list and not run the test.

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


def hf110Callback2(stepNumber):

    info = """
    Now we can run the second step of the test. This step requires a format of
    720x480, 640x480 or 720x576. You can cause your DUT to output this format or
    DUT will follow the EDID we set."""
    waitForReady(info)

    return TLqdStatus.PASS

# Use a 2% capture size
testparam = TLqdTestParameters(captureSizePct=2, saveCaptures=TLqdCaptureOption.Nothing,
                               localDirectory='D:/Python/LOG//HF1_10', callbackSrcSet=True, omitHp=True)

result = TLqdHF1_10(qdDev, 2, hf110Callback2, testParameters=testparam)
# Show the test results:
showResults('HF1-10', result)


def hf111Callback(stepNumber):

    info = """
    The next test will run HF1-11 and save data in a local directory.
    The test will still generate an EDID and signal the DUT with a hot-plug.
    Make sure your DUT sends a format > 340Mcsc"""
    waitForReady(info)

    return TLqdStatus.PASS

# Use a 7% capture size
testparam = TLqdTestParameters(captureSizePct=2, saveCaptures=TLqdCaptureOption.Nothing,
                               localDirectory='D:/Python/LOG//HF1_11', callbackSrcSet=True)

result = TLqdHF1_11(qdDev, hf111Callback, testParameters=testparam)
showResults('HF1-11', result)

# The next test will run HF1-12
def hf112Callback(stepNumber):

    info = """
    The next test will run HF1-12 for step"""

    waitForReady(info)
    return TLqdStatus.PASS

# Use a 7% capture size
testparam = TLqdTestParameters(captureSizePct=2, saveCaptures=TLqdCaptureOption.Nothing,
                               localDirectory='D:/Python/LOG//HF1_12', callbackSrcSet=True, omitHp=True)

result = TLqdHF1_12(qdDev, hf112Callback, testParameters=testparam)
showResults('HF1-12', result)

def hf113Callback(stepNumber):

    info = """
    The next test will run HF1-13 without issuing a hot-plug.
    HF1-13 also has two steps.
    Step 1 tests scrambling < 300Mcsc.
    Step 2 verifies that the DUT does *not* scramble when the TE EDID
    doesn't support scrambling < 300Mcsc.

    Set your DUT for scrambling, 480p60 or 576p50."""

    waitForReady(info)
    return TLqdStatus.PASS

# Use a 7% capture size
testparam = TLqdTestParameters(captureSizePct=2, saveCaptures=TLqdCaptureOption.Nothing,
                               localDirectory='D:/Python/LOG//HF1_13', callbackSrcSet=True, omitHp=True)

result = TLqdHF1_13(qdDev, 1, parms)
showResults('HF1-13', result)

edidData = ("00FFFFFFFFFFFF004489D40315CD5B070117010380502D781A0DC9A05747982712"
    "484C20000001010101010101010101010101010101011D007251D01E206E28550020C2310"
    "0001E000000100000000000000000000000000000000000FC0048444D4920416E616C797A"
    "6572000000FD0017F108963C000A202020202020018102034A704E5D606A616B656601020"
    "304111213485E5F676869626364320F7F07177F503F7FC0577F005F7F01677F00834F0000"
    "6E030C00100078442000800102030467D85DC401788000000000000000000000000000000"
    "0000000000000000000000000000000000000000000000000000000000000000000000000"
    "000000AB")

def hf114Callback(stepNumber):

    info = """
    The next test will run HF1-14 with custom EDID data.
    This test also requires a VIC to be specified - one of 96, 97, 101, 102, 106
    or 107.

    Set your DUT for 2160p60 (VIC 97)"""
    waitForReady(info)
    return TLqdStatus.PASS

# Use a 7% capture size
testparam = TLqdTestParameters(captureSizePct=2, saveCaptures=TLqdCaptureOption.Nothing,
                               localDirectory='D:/Python/LOG//HF1_14', callbackSrcSet=True, edidData=edidData)

result = TLqdHF1_14(qdDev, 97, hf114Callback, testParameters=testparam)
showResults('HF1-14', result)

def hf115Callback(stepNumber):

    info = """
    The next test will run HF1-15 for step {stepNumber}
    Set your DUT to transmit 2160p24, 12-bit RGB.""".format(stepNumber=stepNumber)

    waitForReady(info)
    return TLqdStatus.PASS

# Use a 7% capture size
testparam = TLqdTestParameters(captureSizePct=2, saveCaptures=TLqdCaptureOption.Nothing,
                               localDirectory='D:/Python/LOG//HF1_15_0', callbackSrcSet=True)

result = TLqdHF1_15(qdDev, 93, 12, 1, hf115Callback, testParameters=testparam)
showResults('HF1-15', result)


def hf115Callback1(stepNumber):

    info = """
    We'll test another format for HF1-15 for step 1.
    Set your DUT to transmit 2160p25, 12-bit RGB."""
    waitForReady(info)
    return TLqdStatus.PASS

# Use a 7% capture size
testparam = TLqdTestParameters(captureSizePct=2, saveCaptures=TLqdCaptureOption.Nothing,
                               localDirectory='D:/Python/LOG//HF1_15_1', callbackSrcSet=True)

result = TLqdHF1_15(qdDev, 94, 12, 1, hf115Callback1, testParameters=testparam)
showResults('HF1-15', result)


def hf115Callback2(stepNumber):

    info = """
    verifies that the DUT respects the EDID and
    doesn't send 12-bit."""

    waitForReady(info)
    return TLqdStatus.PASS

# Use a 7% capture size
testparam = TLqdTestParameters(captureSizePct=2, saveCaptures=TLqdCaptureOption.Nothing,
                               localDirectory='D:/Python/LOG//HF1_15_2', callbackSrcSet=True)

# This step verifies that the DUT respects the EDID and doesn't send 12-bit
result = TLqdHF1_15(qdDev, 0, 0, 2, hf115Callback2, testParameters=testparam)
showResults('HF1-15', result)

# The next test will run HF1-16 multiple times for a VIC and different 3D
# options

def hf116Callback(stepNumber):

    info = """
    Have the DUT transmit a 2160p format with 3D frame packing."""
    waitForReady(info)
    return TLqdStatus.PASS

# Use a 7% capture size
testparam = TLqdTestParameters(captureSizePct=2, saveCaptures=TLqdCaptureOption.Nothing,
                               localDirectory='D:/Python/LOG//HF1_16', callbackSrcSet=True,
                               omitHp=True)

result = TLqdHF1_16(qdDev, 93, 'F', hf116Callback, testParameters=testparam)
showResults('HF1-16', result)

# No set-up is needed for this test
result = TLqdHF1_17(qdDev, testParameters=noHp)
showResults('HF1-17', result)
def hf118Callback(stepNumber):

    info = """
    Set-up your DUT to transmit 2160p60 (VIC 97), 8-bit."""
    waitForReady(info)
    return TLqdStatus.PASS

# Use a 7% capture size
testparam = TLqdTestParameters(captureSizePct=7, saveCaptures=TLqdCaptureOption.Nothing,
                               localDirectory='D:/Python/LOG//HF1_18', callbackSrcSet=True,
                               omitHp=True)

result = TLqdHF1_18(qdDev, 97, hf118Callback, testParameters=testparam)
showResults('HF1-18 - 8-bit', result)


def hf118Callback1(stepNumber):

    info = """
    Set-up your DUT to transmit 2160p25 (VIC 94), 10-bit."""
    waitForReady(info)
    return TLqdStatus.PASS

# Use a 7% capture size
testparam = TLqdTestParameters(captureSizePct=7, saveCaptures=TLqdCaptureOption.Nothing,
                               localDirectory='D:/Python/LOG//HF1_18', callbackSrcSet=True,
                               omitHp=True)

result = TLqdHF1_18(qdDev, 94, bitDepth=10, callbackforSS=hf118Callback1, testParameters=testparam)
showResults('HF1-18 - 10-bit', result)

def hf118Callback2(stepNumber):

    info = """
    Set-up your DUT to transmit 2160p24 (VIC 93), 3D frame packing."""
    waitForReady(info)
    return TLqdStatus.PASS

# Use a 7% capture size
testparam = TLqdTestParameters(captureSizePct=7, saveCaptures=TLqdCaptureOption.Nothing,
                               localDirectory='D:/Python/LOG//HF1_18', callbackSrcSet=True,
                               omitHp=True)

result = TLqdHF1_18(qdDev, 93, threeD='F', callbackforSS=hf118Callback2, testParameters=testparam)
showResults('HF1-18 - 3D frame packing', result)

def hf118Callback3(stepNumber):

    info = """
    Set-up your DUT to transmit 2160p60 (VIC 96), BT.2020 cYCC."""
    waitForReady(info)
    return TLqdStatus.PASS

# Use a 7% capture size
testparam = TLqdTestParameters(captureSizePct=7, saveCaptures=TLqdCaptureOption.Nothing,
                               localDirectory='D:/Python/LOG//HF1_18', callbackSrcSet=True,
                               omitHp=True)

result = TLqdHF1_18(qdDev, 96, bt2020=1, callbackforSS=hf118Callback3, testParameters=testparam)
showResults('HF1-18 - BT.2020 cYCC', result)

def hf118Callback4(stepNumber):

    info = """
    Set-up your DUT to transmit 2160p60 (VIC 96), no BT.2020 colorimetry."""
    waitForReady(info)
    return TLqdStatus.PASS

# Use a 7% capture size
testparam = TLqdTestParameters(captureSizePct=7, saveCaptures=TLqdCaptureOption.Nothing,
                               localDirectory='D:/Python/LOG//HF1_18', callbackSrcSet=True,
                               omitHp=True)
result = TLqdHF1_18(qdDev, 96, bt2020=0, callbackforSS=hf118Callback4, testParameters=testparam)
showResults('HF1-18 - not BT.2020', result)


def hf118Callback5(stepNumber):

    info = """
    Set-up your DUT to transmit 2160p60 (VIC 96), BT.2020 RGB."""
    waitForReady(info)
    return TLqdStatus.PASS

# Use a 7% capture size
testparam = TLqdTestParameters(captureSizePct=7, saveCaptures=TLqdCaptureOption.Nothing,
                               localDirectory='D:/Python/LOG//HF1_18', callbackSrcSet=True,
                               omitHp=True)

result = TLqdHF1_18(qdDev, 96, bt2020=2, callbackforSS=hf118Callback5, testParameters=testparam)
showResults('HF1-18 - BT.2020 RGB', result)


# No set-up is needed for this test
result = TLqdHF1_20(qdDev, testParameters=noHp)
showResults('HF1-20', result)

def hf121Callback(stepNumber):

    info = """
    Set-up your DUT to transmit a non-2160p format like 2560x1080p120."""
    waitForReady(info)
    return TLqdStatus.PASS

testparam = TLqdTestParameters(captureSizePct=2, saveCaptures=TLqdCaptureOption.Nothing,
                               localDirectory='D:/Python/LOG//HF1_21', callbackSrcSet=True,
                               omitHp=True)
result = TLqdHF1_21(qdDev, hf121Callback, testParameters=testparam)
showResults('HF1-21', result)

def hf122Callback(stepNumber):

    info = """
    Set-up your DUT to transmit a non-2160p format like 2560x1080p120."""
    waitForReady(info)
    return TLqdStatus.PASS

testparam = TLqdTestParameters(captureSizePct=2, saveCaptures=TLqdCaptureOption.Nothing,
                               localDirectory='D:/Python/LOG//HF1_21', callbackSrcSet=True,
                               omitHp=True)
result = TLqdHF1_21(qdDev, hf122Callback, testParameters=testparam)
showResults('HF1-22', result)

# No set-up is needed for this test
result = TLqdHF1_23(qdDev, testParameters=noHp)
showResults('HF1-23', result)

def hf124Callback(stepNumber):

    info = """
    Set-up your DUT to transmit a non-2160p format like 2560x1080p120."""
    waitForReady(info)
    return TLqdStatus.PASS

# Use a 2% capture size
testparam = TLqdTestParameters(captureSizePct=2, saveCaptures=TLqdCaptureOption.Nothing,
                               localDirectory='D:/Python/LOG//HF1_24', callbackSrcSet=True,
                               omitHp=True)

# Set-up your DUT to transmit a non-2160p format like 2560x1080p120
result = TLqdHF1_24(qdDev, 92, callbackforSS=hf124Callback, testParameters=testparam)
showResults('HF1-24', result)


def hf125Callback(stepNumber):

    info = """
    Set-up your DUT to transmit a deep color non-2160p format 1080p120 (VIC 63)
    12-bit"""
    waitForReady(info)
    return TLqdStatus.PASS

testparam = TLqdTestParameters(captureSizePct=2, saveCaptures=TLqdCaptureOption.Nothing,
                               localDirectory='D:/Python/LOG//HF1_25', callbackSrcSet=True,
                               omitHp=True)

result = TLqdHF1_25(qdDev, 63, 1, 12, callbackforSS=hf125Callback, testParameters=testparam)
showResults('HF1-25', result)

result = TLqdHF1_25(qdDev, 0, 2, 0, callbackforSS=hf125Callback, testParameters=testparam)
showResults('HF1-25', result)


def hf126Callback1(stepNumber):

    info = """
    Set-up your DUT to transmit a 3D, non-2160p format 1080p120 (VIC 63),
    frame packing."""
    waitForReady(info)
    return TLqdStatus.PASS

testparam = TLqdTestParameters(captureSizePct=2, saveCaptures=TLqdCaptureOption.Nothing,
                               localDirectory='D:/Python/LOG//HF1_26', callbackSrcSet=True,
                               omitHp=True)


result = TLqdHF1_26(qdDev, 63, 'F', callbackforSS=hf126Callback1, testParameters=testparam)
showResults('HF1-26', result)


def hf126Callback2(stepNumber):

    info = """
    Set-up your DUT to transmit 3D, non-2160p format 1080p120 (VIC 63),
    side-by-side."""
    waitForReady(info)
    return TLqdStatus.PASS

result = TLqdHF1_26(qdDev, 63, 'S', callbackforSS=hf126Callback2, testParameters=testparam)
showResults('HF1-26', result)

# No set-up is needed for this test
result = TLqdHF1_27(qdDev, testParameters=noHp)
showResults('HF1-27', result)


def hf128Callback1(stepNumber):

    info = """
    Set-up your DUT to transmit 2560x1080p100 (VIC 91)."""
    waitForReady(info)
    return TLqdStatus.PASS

testparam = TLqdTestParameters(captureSizePct=2, saveCaptures=TLqdCaptureOption.Nothing,
                               localDirectory='D:/Python/LOG//HF1_28', callbackSrcSet=True,
                               omitHp=True)

result = TLqdHF1_28(qdDev, 91, hf128Callback1, testParameters=testparam)
showResults('HF1-28 - 8-bit', result)

def hf128Callback2(stepNumber):

    info = """
    Set-up your DUT to transmit 1080p120 (VIC 63), 10-bit."""
    waitForReady(info)
    return TLqdStatus.PASS

result = TLqdHF1_28(qdDev, 94, bitDepth=10, callbackforSS=hf128Callback2, testParameters=testparam)
showResults('HF1-28 - 10-bit', result)

def hf128Callback3(stepNumber):

    info = """
    Set-up your DUT to transmit VIC 63, 3D frame packing."""
    waitForReady(info)
    return TLqdStatus.PASS

result = TLqdHF1_28(qdDev, 63, threeD='F', callbackforSS=hf128Callback3, testParameters=testparam)
showResults('HF1-28 - 3D frame packing', result)

def hf128Callback4(stepNumber):

    info = """
    Set-up your DUT to transmit 2560x1080p100 (VIC 91), BT.2020 cYCC."""
    waitForReady(info)
    return TLqdStatus.PASS

result = TLqdHF1_28(qdDev, 91, bt2020=1, callbackforSS=hf128Callback4, testParameters=testparam)
showResults('HF1-28 - BT.2020 cYCC', result)

def hf128Callback5(stepNumber):

    info = """
    Set-up your DUT to transmit VIC 91, no BT.2020 colorimetry."""
    waitForReady(info)
    return TLqdStatus.PASS

result = TLqdHF1_28(qdDev, 91, bt2020=0, callbackforSS=hf128Callback5, testParameters=testparam)
showResults('HF1-28 - not BT.2020', result)

def hf128Callback6(stepNumber):

    info = """
    Set-up your DUT to transmit VIC 91, BT.2020 RGB."""
    waitForReady(info)
    return TLqdStatus.PASS

result = TLqdHF1_28(qdDev, 91, bt2020=2, callbackforSS=hf128Callback6, testParameters=testparam)
showResults('HF1-28 - BT.2020 RGB', result)

# After starting the test, the DUT is expected to read the EDID, write the
# RR_Enable bit, then read the 7 bytes of the error count registers in one
# transaction
result = TLqdHF1_29(qdDev, testParameters=noHp)
showResults('HF1-29', result)

def hf131Callback(stepNumber):

    info = """
    Set-up your DUT to transmit YCbCr 4:2:0 2160p60 (VIC 97)."""
    waitForReady(info)
    return TLqdStatus.PASS


testparam = TLqdTestParameters(captureSizePct=2, saveCaptures=TLqdCaptureOption.Nothing,
                               localDirectory='D:/Python/LOG//HF1_31', callbackSrcSet=True,
                               omitHp=True)
result = TLqdHF1_31(qdDev, 97, 1, callbackforSS=hf131Callback, testParameters=testparam)
showResults('HF1-31', result)

result = TLqdHF1_31(qdDev, 0, 2, callbackforSS=hf131Callback, testParameters=testparam)
showResults('HF1-31', result)

def hf132Callback(stepNumber):

    info = """
    Set-up your DUT to transmit deep color YCbCr 4:2:0 2160p50 (VIC 96),
    10-bit."""
    waitForReady(info)
    return TLqdStatus.PASS


testparam = TLqdTestParameters(captureSizePct=2, saveCaptures=TLqdCaptureOption.Nothing,
                               localDirectory='D:/Python/LOG//HF1_32', callbackSrcSet=True,
                               omitHp=True)

result = TLqdHF1_32(qdDev, 96, 1, 10, callbackforSS=hf132Callback, testParameters=testparam)
showResults('HF1-32', result)

result = TLqdHF1_32(qdDev, 0, 2, 10, callbackforSS=hf132Callback, testParameters=testparam)
showResults('HF1-32', result)

def hf133Callback(stepNumber):

    info = """
    Set-up your DUT to transmit YCbCr 4:2:0 2160p50 (VIC 96)."""
    waitForReady(info)
    return TLqdStatus.PASS

testparam = TLqdTestParameters(captureSizePct=2, saveCaptures=TLqdCaptureOption.Nothing,
                               localDirectory='D:/Python/LOG//HF1_33', callbackSrcSet=True,
                               omitHp=True)

result = TLqdHF1_33(qdDev, 96, callbackforSS=hf133Callback, testParameters=testparam)
showResults('HF1-33', result)

def hf134Callback(stepNumber):

    info = """
    Set-up your DUT to transmit deep color YCbCr 4:2:0 2160p60 (VIC 97)
    10-bit."""
    waitForReady(info)
    return TLqdStatus.PASS

testparam = TLqdTestParameters(captureSizePct=2, saveCaptures=TLqdCaptureOption.Nothing,
                               localDirectory='D:/Python/LOG//HF1_34', callbackSrcSet=True,
                               omitHp=True)

result = TLqdHF1_34(qdDev, 97, 10, callbackforSS=hf134Callback, testParameters=testparam)
showResults('HF1-34', result)

def hf135Callback(stepNumber):

    info = """
    Set-up your DUT to transmit a wide format format 2560x1080p24 (VIC 86)."""
    waitForReady(info)
    return TLqdStatus.PASS

testparam = TLqdTestParameters(captureSizePct=2, saveCaptures=TLqdCaptureOption.Nothing,
                               localDirectory='D:/Python/LOG//HF1_35', callbackSrcSet=True,
                               omitHp=True)

result = TLqdHF1_35(qdDev, 86, callbackforSS=hf135Callback, testParameters=testparam)
showResults('HF1-35', result)

testparam = TLqdTestParameters(callbackSrcSet=True, omitHp=True)
def hf141Callback(stepNumber):

    info = """
    Set-up your DUT to transmit 3D audio."""
    waitForReady(info)
    return TLqdStatus.PASS

result = TLqdHF1_41(qdDev, callbackforSS=hf141Callback, testParameters=testparam)
showResults('HF1-41', result)

def hf143Callback(stepNumber):

    info = """
    Set-up your DUT to transmit HBR audio."""
    waitForReady(info)
    return TLqdStatus.PASS

result = TLqdHF1_43(qdDev, callbackforSS=hf143Callback, testParameters=testparam)
showResults('HF1-43', result)

def hf144Callback(stepNumber):

    info = """
    Set-up your DUT to transmit One Bit 3D or One Bit Multi-stream audio."""
    waitForReady(info)
    return TLqdStatus.PASS

result = TLqdHF1_44(qdDev, callbackforSS=hf144Callback, testParameters=testparam)
showResults('HF1-44', result)

def hf145Callback(stepNumber):

    info = """
    Set-up your DUT to transmit L-PCM or IEC 61937 compressed audio."""
    waitForReady(info)
    return TLqdStatus.PASS

result = TLqdHF1_45(qdDev, callbackforSS=hf145Callback, testParameters=testparam)
showResults('HF1-45', result)

def hf147Callback1(stepNumber):

    info = """
    Set-up your DUT to transmit any non-3D format."""
    waitForReady(info)
    return TLqdStatus.PASS

result = TLqdHF1_47(qdDev, 1, callbackforSS=hf147Callback1, testParameters=testparam)
showResults('HF1-47', result)

def hf147Callback2(stepNumber):

    info = """
    Set-up your DUT to transmit any 3D format, no OSD disparity in an HDMI Forum
    InfoFrame."""
    waitForReady(info)
    return TLqdStatus.PASS

result = TLqdHF1_47(qdDev, 2, callbackforSS=hf147Callback2, testParameters=testparam)
showResults('HF1-47', result)

def hf147Callback3(stepNumber):

    info = """
    Set-up your DUT to transmit a top/bottom or side-by-side 3D format, with
    OSD disparity data in an HDMI Forum InfoFrame."""
    waitForReady(info)
    return TLqdStatus.PASS

result = TLqdHF1_47(qdDev, 3, callbackforSS=hf147Callback3, testParameters=testparam)
showResults('HF1-47', result)

def hf148Callback1(stepNumber):

    info = """
    Set-up your DUT to transmit Dual View with top/bottom or side-by-side 3D
    format, with an HDMI Forum InfoFrame."""
    waitForReady(info)
    return TLqdStatus.PASS

result = TLqdHF1_48(qdDev, 1, callbackforSS=hf148Callback1, testParameters=testparam)
showResults('HF1-48', result)

def hf148Callback2(stepNumber):

    info = """
    It is required to have your DUT switch to a 2D format *after* starting the
    test. The test allows up to 45 seconds to wait for the switch from 3D Dual
    View to 2D."""
    waitForReady(info)
    return TLqdStatus.PASS

result = TLqdHF1_48(qdDev, 2, callbackforSS=hf148Callback2, testParameters=testparam)
showResults('HF1-48', result)

def hf149Callback1(stepNumber):

    info = """
    Set-up your DUT to transmit Independent View with top/bottom or side-by-side
    3D format, with an HDMI Forum InfoFrame."""
    waitForReady(info)
    return TLqdStatus.PASS

result = TLqdHF1_49(qdDev, 1, callbackforSS=hf149Callback1, testParameters=testparam)
showResults('HF1-49', result)

def hf149Callback2(stepNumber):

    info = """
    It is required to have your DUT switch to a 2D format *after* starting the
    test. The test allows up to 45 seconds to wait for the switch from 3D
    Independent View to 2D."""
    waitForReady(info)
    return TLqdStatus.PASS

result = TLqdHF1_49(qdDev, 2, callbackforSS=hf149Callback2, testParameters=testparam)
showResults('HF1-49', result)

def hf151Callback1(stepNumber):

    info = """
    Set-up your DUT to transmit YCbCr 4:2:0 2160p60 (VIC 97)."""
    waitForReady(info)
    return TLqdStatus.PASS

result = TLqdHF1_51(qdDev, 97, 1, callbackforSS=hf151Callback1, testParameters=testparam)
showResults('HF1-51', result)

result = TLqdHF1_51(qdDev, 97, 2, testParameters=testparam)
showResults('HF1-51', result)

result = TLqdHF1_51(qdDev, 97, 3, testParameters=testparam)
showResults('HF1-51', result)

result = TLqdHF1_51(qdDev, 97, 4, testParameters=testparam)
showResults('HF1-51', result)

def hf152Callback1(stepNumber):

    info = """
    Set-up your DUT to transmit BT.2020 YCbCr 4:2:0 10- or 12- bit YCC."""
    waitForReady(info)
    return TLqdStatus.PASS

result = TLqdHF1_52(qdDev, 1, callbackforSS=hf152Callback1, testParameters=testparam)
showResults('HF1-52', result)

result = TLqdHF1_52(qdDev, 2, testParameters=testparam)
showResults('HF1-52', result)

# Set-up your DUT to transmit BT.2020 YCbCr 4:2:0 10- or 12- bit cYCC
result = TLqdHF1_52(qdDev, 3, testParameters=testparam)
showResults('HF1-52', result)

result = TLqdHF1_52(qdDev, 4, testParameters=testparam)
showResults('HF1-52', result)

def hf153Callback(stepNumber):

    info = """
    Set-up your DUT to transmit Dynamic Range and Mastering, Traditional SDR."""
    waitForReady(info)
    return TLqdStatus.PASS

result = TLqdHF1_53(qdDev, 1, callbackforSS=hf153Callback, testParameters=testparam)
showResults('HF1-53', result)

def hf171Callback(stepNumber):

    info = """
    Set-up your DUT to transmit VIC 114 YCbCr 4:2:0"""
    waitForReady(info)
    return TLqdStatus.PASS

# Use a 7% capture size
testparam = TLqdTestParameters(captureSizePct=2, saveCaptures=TLqdCaptureOption.Nothing,
                               localDirectory='D:/Python/LOG//HF1_71', callbackSrcSet=True)

result = TLqdHF1_71(qdDev, 114, hf171Callback, testparam)
showResults('HF1-71 VIC 114', result)

def hf172Callback(stepNumber):

    info = """
    Set-up your DUT to transmit VIC 115 YCbCr 4:2:0 12-bit"""
    waitForReady(info)
    return TLqdStatus.PASS

testparam = TLqdTestParameters(captureSizePct=2, saveCaptures=TLqdCaptureOption.Nothing,
                               localDirectory='D:/Python/LOG//HF1_72', callbackSrcSet=True)

result = TLqdHF1_72(qdDev, 115, 12, callbackforSS=hf172Callback, testParameters=testparam)
showResults('HF1-72 VIC 115 12-bit', result)

testparam = TLqdTestParameters(callbackSrcSet=True)

def ct716Callback(stepNumber):

    info = """
    HDMI 1.4 Legal Codes:
    Set-up your DUT to transmit VIC 2 (480p60)"""
    waitForReady(info)
    return TLqdStatus.PASS

result = TLqd7_16(qdDev, 2, callbackforSS=ct716Callback, testParameters=testparam)
showResults('7-16 VIC 2', result)

def ct717Callback(stepNumber):

    info = """
    HDMI 1.4 Basic Protocol:
    Set-up your DUT to transmit VIC 2 (480p60)"""
    waitForReady(info)
    return TLqdStatus.PASS

result = TLqd7_17(qdDev, 2, callbackforSS=ct717Callback, testParameters=testparam)
showResults('7-17 VIC 2', result)

def ct718Callback(stepNumber):

    info = """
    HDMI 1.4 Extended Control Period:
    Set-up your DUT to transmit VIC 2 (480p60)"""
    waitForReady(info)
    return TLqdStatus.PASS

result = TLqd7_18(qdDev, 2, callbackforSS=ct718Callback, testParameters=testparam)
showResults('7-18 VIC 2', result)

def ct719Callback(stepNumber):

    info = """
    HDMI 1.4 Packet Types:
    Set-up your DUT to transmit VIC 2 (480p60)"""
    waitForReady(info)
    return TLqdStatus.PASS

result = TLqd7_19(qdDev, 2, callbackforSS=ct719Callback, testParameters=testparam)
showResults('7-19 VIC 2', result)

def ct723Callback(stepNumber):

    info = """
    HDMI 1.4 Pixel Encoding RGB:
    Set-up your DUT to transmit VIC 2 (480p60), RGB"""
    waitForReady(info)
    return TLqdStatus.PASS

'''
# The next test requires a callback function to be provided so that the test can
# verify that the sink is receiving the proper image
# The callback is passed an information string and required to return
# a TLqdStatus object
'''
def callback(info):
    print("\nCallback info: " + str(info))
    return TLqdStatus.PASS

parms = TLqdTestParameters(localDirectory='D:/Python/LOG//CT7_23_1', omitHp=True)
result = TLqd7_23(qdDev, 2, callback, callbackforSS=ct723Callback, testParameters=parms)
showResults('7-23 VIC 2', result)

def hf132vCallback(stepNumber):

    info = """
    Set-up your DUT to transmit deep color YCbCr 4:2:0 2160p50 (VIC 96),
    10-bit."""
    waitForReady(info)
    return TLqdStatus.PASS

result = TLqdHF1_32v(qdDev, 96, 1, 10, callback, True, callbackforSS=hf132vCallback, testParameters=parms)
showResults('HF1-32', result)

def ct724Callback(stepNumber):

    info = """
    HDMI 1.4 Pixel Encoding YCbCr:
    Set-up your DUT to transmit VIC 2 (480p60), YCbCr"""
    waitForReady(info)
    return TLqdStatus.PASS

result = TLqd7_24(qdDev, 2, callback, callbackforSS=ct724Callback, testParameters=testparam)
showResults('7-24 VIC 2', result)

def ct725Callback(stepNumber):

    info = """
    HDMI 1.4 Video Format Timing:
    Set-up your DUT to transmit VIC 2 (480p60)"""
    waitForReady(info)
    return TLqdStatus.PASS

result = TLqd7_25(qdDev, 2, callbackforSS=ct725Callback, testParameters=testparam)
showResults('7-25 VIC 2', result)

def ct726Callback(stepNumber):

    info = """
    HDMI 1.4 Pixel Repetition:
    Set-up your DUT to transmit VIC 2 (480p60)"""
    waitForReady(info)
    return TLqdStatus.PASS

result = TLqd7_26(qdDev, 2, callbackforSS=ct726Callback, testParameters=testparam)
showResults('7-26 VIC 2', result)

def ct727Callback(stepNumber):

    info = """
    HDMI 1.4 AVI InfoFrame:
    Set-up your DUT to transmit VIC 2 (480p60)"""
    waitForReady(info)
    return TLqdStatus.PASS

result = TLqd7_27(qdDev, 2, callbackforSS=ct727Callback, testParameters=testparam)
showResults('7-27 VIC 2', result)

def ct728Callback1(stepNumber):

    info = """
    HDMI 1.4 IEC 60958/IEC 61937:
    Set-up your DUT to transmit VIC 2 (480p60), basic audio"""
    waitForReady(info)
    return TLqdStatus.PASS

result = TLqd7_28(qdDev, 1, callbackforSS=ct728Callback1, testParameters=testparam)
showResults('7-28 VIC 2, step 1', result)

def ct728Callback2(stepNumber):

    info = """
    HDMI 1.4 IEC 60958/IEC 61937:
    Set-up your DUT to transmit multi-channel audio"""
    waitForReady(info)
    return TLqdStatus.PASS

result = TLqd7_28(qdDev, 2, callbackforSS=ct728Callback2, testParameters=testparam)
showResults('7-28, step 2', result)

def ct728Callback3(stepNumber):

    info = """
    HDMI 1.4 IEC 60958/IEC 61937:
    Set-up your DUT to transmit HBRA audio"""
    waitForReady(info)
    return TLqdStatus.PASS

result = TLqd7_28(qdDev, 3, callbackforSS=ct728Callback3, testParameters=testparam)
showResults('7-28, step 3', result)

def ct729Callback1(stepNumber):

    info = """
    HDMI 1.4 ACR:
    Set-up your DUT to transmit VIC 2, basic audio"""
    waitForReady(info)
    return TLqdStatus.PASS

result = TLqd7_29(qdDev, 1, callbackforSS=ct729Callback1, testParameters=testparam)
showResults('7-29, step 1', result)

def ct729Callback2(stepNumber):

    info = """
    HDMI 1.4 ACR:
    Set-up your DUT to transmit VIC 2, deep color, basic audio"""
    waitForReady(info)
    return TLqdStatus.PASS

result = TLqd7_29(qdDev, 2, callbackforSS=ct729Callback2, testParameters=testparam)
showResults('7-29, step 2', result)

def ct730Callback1(stepNumber):

    info = """
    HDMI 1.4 Audio Sample Packet Jitter:
    Set-up your DUT to transmit VIC 6, 3-channel audio, 96kHz sampling"""
    waitForReady(info)
    return TLqdStatus.PASS

result = TLqd7_30(qdDev, 1, 6, 96e3, 3, callbackforSS=ct730Callback1, testParameters=testparam)
showResults('7-30, step 1', result)

def ct730Callback2(stepNumber):

    info = """
    HDMI 1.4 Basic Protocol:
    Set-up your DUT to transmit VIC 2 (480p60)"""
    waitForReady(info)
    return TLqdStatus.PASS
info = """
HDMI 1.4 Audio Sample Packet Jitter:
Set-up your DUT to transmit VIC 2, basic 2-channel audio, 48kHz sampling"""
waitForReady(info)
result = TLqd7_30(qdDev, 2, 2, 48e3, 2, callbackforSS=ct730Callback2, testParameters=testparam)
showResults('7-30, step 2', result)

def ct731Callback1(stepNumber):

    info = """
    HDMI 1.4 Audio InfoFrame:
    Set-up your DUT to transmit VIC 2, basic 2-channel audio, 48kHz sampling"""
    waitForReady(info)
    return TLqdStatus.PASS

result = TLqd7_31(qdDev, 1, 2, callbackforSS=ct731Callback1, testParameters=testparam)
showResults('7-31, step 1', result)

def ct731Callback2(stepNumber):

    info = """
    HDMI 1.4 Audio InfoFrame:
    Set-up your DUT to transmit basic audio, 3 or more channels, 48kHz sampling"""
    waitForReady(info)
    return TLqdStatus.PASS

result = TLqd7_31(qdDev, 2, 0, callbackforSS=ct731Callback2, testParameters=testparam)
showResults('7-31, step 2', result)

def ct732Callback1(stepNumber):

    info = """
    HDMI 1.4 Audio Sample Packet Layout:
    Set-up your DUT to transmit basic 2-channel audio, 48kHz sampling"""
    waitForReady(info)
    return TLqdStatus.PASS

result = TLqd7_32(qdDev, 1, callbackforSS=ct732Callback1, testParameters=testparam)
showResults('7-31, step 1', result)

def ct732Callback2(stepNumber):

    info = """
    HDMI 1.4 Audio Sample Packet Layout:
    Set-up your DUT to transmit basic audio, 3 or more channels, 48kHz sampling"""
    waitForReady(info)
    return TLqdStatus.PASS

result = TLqd7_32(qdDev, 2, callbackforSS=ct732Callback2, testParameters=testparam)
showResults('7-32, step 2', result)

def ct733Callback(stepNumber):

    info = """
    HDMI 1.4 Interoperability with DVI:
    Set-up your DUT to transmit DVI"""
    waitForReady(info)
    return TLqdStatus.PASS

result = TLqd7_33(qdDev, 1, callbackforSS=ct733Callback, testParameters=testparam)
showResults('7-33, step 1', result)

def ct733aCallback(stepNumber):

    info = """
    HDMI 1.4 Interoperability with multiple VSDB:
    Set-up your DUT to transmit HDMI"""
    waitForReady(info)
    return TLqdStatus.PASS

result = TLqd7_33a(qdDev, callbackforSS=ct733aCallback, testParameters=testparam)
showResults('7-33a', result)

def ct734Callback(stepNumber):

    info = """
    HDMI 1.4 Deep Color:
    Set-up your DUT to transmit VIC 2, 12-bits/color"""
    waitForReady(info)
    return TLqdStatus.PASS

result = TLqd7_34(qdDev, 2, 12, callbackforSS=ct734Callback, testParameters=testparam)
showResults('7-34, VIC 2, 12bpc', result)

def ct735Callback(stepNumber):

    info = """
    HDMI 1.4 Gamut Metadata Transmission:
    Set-up your DUT to transmit an xvYCC-encoded signal"""
    waitForReady(info)
    return TLqdStatus.PASS

result = TLqd7_35(qdDev, callbackforSS=ct735Callback, testParameters=testparam)
showResults('7-35', result)

def ct736Callback(stepNumber):

    info = """
    HDMI 1.4 High Bitrate Audio:
    Set-up your DUT to transmit Dolby TrueHD audio"""
    waitForReady(info)
    return TLqdStatus.PASS

result = TLqd7_36(qdDev, 1, callbackforSS=ct736Callback, testParameters=testparam)
showResults('7-36, Dolby TrueHD', result)

def ct737Callback(stepNumber):

    info = """
    HDMI 1.4 One Bit Audio:
    Set-up your DUT to transmit One Bit audio"""
    waitForReady(info)
    return TLqdStatus.PASS

result = TLqd7_37(qdDev, callbackforSS=ct737Callback, testParameters=testparam)
showResults('7-37', result)

def ct738Callback(stepNumber):

    info = """
    HDMI 1.4 3D Video Format Timing:
    Set-up your DUT to transmit VIC 16, 3D frame packing video"""
    waitForReady(info)
    return TLqdStatus.PASS

result = TLqd7_38(qdDev, 16, 'F', callback, callbackforSS=ct738Callback, testParameters=testparam)
showResults('7-38, VIC 16, 3D frame packing', result)

def ct739Callback(stepNumber):

    info = """
    HDMI 1.4 4K x 2K Video Format Timing:
    Set-up your DUT to transmit HDMI VIC 1"""
    waitForReady(info)
    return TLqdStatus.PASS

result = TLqd7_39(qdDev, 1, callback, callbackforSS=ct739Callback, testParameters=testparam)
showResults('7-39, HDMI VIC 1', result)

def ct740Callback(stepNumber):

    info = """
    HDMI 1.4 Extended Colorimetry Transmission (without xvYCC):
    Set-up your DUT to transmit sYCC601"""
    waitForReady(info)
    return TLqdStatus.PASS

result = TLqd7_40(qdDev, 1, callbackforSS=ct740Callback, testParameters=testparam)
showResults('7-40, step 1', result)
exit(0)
