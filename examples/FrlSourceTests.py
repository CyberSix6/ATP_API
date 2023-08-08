#!/usr/bin/env python

"""@package FrlSourceTests Teledyne LeCroy quantumdata Python API
examples for FRL source tests"""

# Copyright (c) 2019 Teledyne LeCroy, Inc.

## @file FrlSourceTests.py
## @brief Sample code for running FRL Source tests

# This program is provided as a demonstration of how to use the
# Teledyne LeCroy quantumdata API suite for running FRL source compliance tests

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

# An example of an error which will cause a skipped test is for HFR1-11 which
# received TMDS or FRL with 4 lanes (which is required by the GCTS). The test
# will report the error in the error list and not run the test.

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

testparam = TLqdTestParameters(callbackSrcSet=True)

def hfr168Callback(stepNumber):

    info = """
    Let's run HFR1-68. This test will verify that the DUT polls
    update flags and retrains when requested by the Sink."""
    waitForReady(info)
    return TLqdStatus.PASS


result = TLqdHFR1_68(qdDev, callbackforSS=hfr168Callback, testParameters=testparam)

# Show the test results:
showResults('HFR1-68', result)

def hfr110Callback(stepNumber):

    info = """
    We assume that the DUT is connected to the analyzer Rx port before every test
    Now we're ready to run a test"""

    waitForReady(info)
    return TLqdStatus.PASS

# This test will run HFR1-10. No data will be saved,
# the test will generate an EDID and signal the DUT with a hot-plug:

result = TLqdHFR1_10(qdDev, callbackforSS=hfr110Callback, testParameters=testparam)

# Show the test result:
showResults('HFR1-10', result)


def hfr111Callback1(stepNumber):
    info = """
    If you have control over your DUT, you should have it generate FRL
    output format on 3 lanes which is required for HFR1-11."""

    waitForReady(info)
    return TLqdStatus.PASS

# Use a 7% capture size
shortTest = TLqdTestParameters(captureSizePct=7.0, callbackSrcSet=True)

# This test will run the first step of HFR1-11. No data will be saved,
# the test will generate an EDID and signal the DUT with a hot-plug:

result = TLqdHFR1_11(qdDev, 1, callbackforSS=hfr111Callback1, testParameters=shortTest)

# Show the test result:
showResults('HFR1-11', result)

def hfr111Callback2(stepNumber):
    info = """
    Now we can run the second step of the test. This step requires an FRL format
    with 4 lanes. You can cause your DUT to output this format or the DUT will
    follow the EDID we set."""

    waitForReady(info)
    return TLqdStatus.PASS


result = TLqdHFR1_11(qdDev, 2, callbackforSS=hfr111Callback2, testParameters=shortTest)
# Show the test results:
showResults('HFR1-11', result)

def hfr112Callback(stepNumber):
    info = """
    Now we'll run HFR1-12. This test will verify that the DUT link trains.
    You don't need to do anything to the DUT."""

    waitForReady(info)
    return TLqdStatus.PASS

result = TLqdHFR1_12(qdDev, callbackforSS=hfr112Callback, testParameters=testparam)
# Show the test results:
showResults('HFR1-12', result)

def hfr113Callback(stepNumber):
    info = """
    Now we'll run HFR1-13. This test will verify that the DUT link trains to a new
    rate. We'll set the maximum FRL rate to 6. Your DUT may have a lower rate."""

    waitForReady(info)
    return TLqdStatus.PASS

result = TLqdHFR1_13(qdDev, 6, callbackforSS=hfr113Callback, testParameters=testparam)
# Show the test results:
showResults('HFR1-13', result)

def hfr114Callback(stepNumber):
    info = """
    Now we'll run HFR1-14. This test will verify that the DUT supports 24-bit
    color for non-2160p formats. Set up your DUT for 480p60 - VIC 2."""

    waitForReady(info)
    return TLqdStatus.PASS

result = TLqdHFR1_14(qdDev, 2, callbackforSS=hfr114Callback, testParameters=shortTest)
# Show the test results:
showResults('HFR1-14', result)

def hfr115Callback(stepNumber):
    info = """
    Run test HFR1-15.
    This test requires you to provide the VIC and use deep color, so set-up your
    DUT to send VIC 63 (1080p120), 10-bits/color."""

    waitForReady(info)
    return TLqdStatus.PASS


result = TLqdHFR1_15(qdDev, 63, 10, callbackforSS=hfr115Callback, testParameters=shortTest)
# Show the test results:
showResults('HFR1-15', result)

def hfr116Callback(stepNumber):
    info = """
    Now run HFR1-16. This test will verify that the DUT can transmit 3D for a
    2160p format with FRL.
    Let's test 2160p24 (VIC 93) with frame packing 3D."""

    waitForReady(info)
    return TLqdStatus.PASS

result = TLqdHFR1_16(qdDev, 93, 'F', callbackforSS=hfr116Callback, testParameters=shortTest)
# Show the test results:
showResults('HFR1-16', result)

def hfr117Callback(stepNumber):
    info = """
    Let's run HFR1-17. This test will verify that the DUT handles an EDID with
    Max_FRL_RATE set to 8."""

    waitForReady(info)
    return TLqdStatus.PASS

result = TLqdHFR1_17(qdDev, callbackforSS=hfr117Callback, testParameters=testparam)
# Show the test results:
showResults('HFR1-17', result)

def hfr118Callback(stepNumber):
    info = """
    Let's run test HFR1-18. This will test your DUT for a 2160p format from
    300-600Mcsc over FRL. You can test with 2160p50 or 60, 2160p30 deep color or
    3D frame packing to achieve these rates."""

    waitForReady(info)
    return TLqdStatus.PASS


mediumTest = TLqdTestParameters(captureSizePct=10.0, callbackSrcSet=True)
result = TLqdHFR1_18(qdDev, 95, 10, callbackforSS=hfr118Callback, testParameters=mediumTest)
# Show the test results:
showResults('HFR1-18', result)

def hfr119Callback(stepNumber):
    info = """
    Now run test HFR1-19. The first step requires an FRL format with 3 lanes.
    You can cause your DUT to output this format or DUT will follow
    the EDID we set."""

    waitForReady(info)
    return TLqdStatus.PASS

result = TLqdHFR1_19(qdDev, 1, callbackforSS=hfr119Callback, testParameters=shortTest)
# Show the test results:
showResults('HFR1-19', result)

# Test HFR1-20 isn't implemented yet

# (result, info, errors) = TLqdHFR1_20(qdDev, 2)
# Show the test results:
# showResults('HFR1-20', result)

def hfr121Callback(stepNumber):
    info = """
    Run test HFR1-21. The second step requires an FRL format with 4 lanes.
    You can cause your DUT to output this format or DUT will follow
    the EDID we set."""

    waitForReady(info)
    return TLqdStatus.PASS


result = TLqdHFR1_21(qdDev, 2, callbackforSS=hfr121Callback, testParameters=shortTest)
# Show the test results:
showResults('HFR1-21', result)

# Run test HFR1-23.
result = TLqdHFR1_23(qdDev, testParameters=shortTest)
# Show the test results:
showResults('HFR1-23', result)

def hfr124Callback(stepNumber):
    info = """
    Now we'll run HFR1-24. This test will verify that the DUT supports 24-bit
    color for 2160p formats. Set up your DUT for 2160p60 - VIC 97."""

    waitForReady(info)
    return TLqdStatus.PASS

result = TLqdHFR1_24(qdDev, 97, callbackforSS=hfr124Callback, testParameters=shortTest)
# Show the test results:
showResults('HFR1-24', result)

def hfr125Callback(stepNumber):
    info = """
    Run test HFR1-25.
    This test requires you to provide the VIC and use deep color, so set-up your
    DUT to send VIC 97 (2160p60), 10-bits/color."""

    waitForReady(info)
    return TLqdStatus.PASS

result = TLqdHFR1_25(qdDev, 97, 10, callbackforSS=hfr125Callback, testParameters=shortTest)
# Show the test results:
showResults('HFR1-25', result)

def hfr126Callback(stepNumber):
    info = """
    Now run HFR1-26. This test will verify that the DUT can transmit 3D for a
    non-2160p format with FRL.
    Let's test 1080p120 (VIC 63) with frame packing 3D."""

    waitForReady(info)
    return TLqdStatus.PASS


result = TLqdHFR1_26(qdDev, 63, 'F', callbackforSS=hfr126Callback, testParameters=shortTest)
# Show the test results:
showResults('HFR1-26', result)

def hfr127Callback(stepNumber):
    info = """
    Run test HFR1-27. This test requires a callback function to be provided so
    that a bitmap file of the captured source image can be judged. The callback
    function is required to return a TLqdStatus (SKIPPED, PASS, or FAIL)
    You should cause your DUT to output a deep-color (10-, 12- or 16-bit) YCbCr
    or RGB 4:4:4 image using the "YCbCrTest" pattern"""

    waitForReady(info)
    return TLqdStatus.PASS

def callback(bitmapFile):
    return TLqdStatus.PASS

result = TLqdHFR1_27(qdDev, callback, True, 10, callbackforSS=hfr127Callback, testParameters=shortTest)
# Show the test results:
showResults('HFR1-27', result)

def hfr128Callback(stepNumber):
    info = """
    Let's run test HFR1-28. This will test your DUT for a non-2160p format from
    300-600Mcsc over FRL. Set your DUT to 1080p120 (VIC 63), 10-bit deep color."""

    waitForReady(info)
    return TLqdStatus.PASS


result = TLqdHFR1_28(qdDev, 63, 10, callbackforSS=hfr128Callback, testParameters=shortTest)
# Show the test results:
showResults('HFR1-28', result)

def hfr129Callback(stepNumber):
    info = """
    Now we'll run test HFR1-29."""

    waitForReady(info)
    return TLqdStatus.PASS

result = TLqdHFR1_29(qdDev, callback, callbackforSS=hfr129Callback, testParameters=shortTest)
# Show the test results:
showResults('HFR1-29', result)

def hfr130Callback(stepNumber):
    info = """
    Run test HFR1-30. This test also requires a callback function.

    This test requires YCbCr 4:2:2 or 4:4:4. We'll test 4:2:2, so set-up your DUT
    to send that."""

    waitForReady(info)
    return TLqdStatus.PASS


result = TLqdHFR1_30(qdDev, callback, TLqdSubsampling.SS422,
                     callbackforSS=hfr130Callback, testParameters=shortTest)
# Show the test results:
showResults('HFR1-30', result)

def hfr131Callback(stepNumber):
    info = """
    Run test HFR1-31. This test also requires a callback function.

    This test requires you to provide the VIC and use YCbCr 4:2:0,
    so set-up your DUT to send VIC 97 (2160p60)."""

    waitForReady(info)
    return TLqdStatus.PASS


result = TLqdHFR1_31(qdDev, callback, 97, callbackforSS=hfr131Callback,
                     testParameters=shortTest)
# Show the test results:
showResults('HFR1-31', result)

def hfr132Callback(stepNumber):
    info = """
    Run test HFR1-32. This test also requires a callback function.

    This test requires you to provide the VIC and use YCbCr 4:2:0 deep color,
    so set-up your DUT to send VIC 97 (2160p60), 10-bits/color.
    You should cause your DUT to output a deep-color (10-, 12- or 16-bit)
    YCbCr 4:2:0 image using the "YCbCrTest" pattern."""

    waitForReady(info)
    return TLqdStatus.PASS

result = TLqdHFR1_32(qdDev, callback, 97, False, 10, callbackforSS=hfr132Callback,
                     testParameters=shortTest)
# Show the test results:
showResults('HFR1-32', result)

def hfr133Callback(stepNumber):
    info = """
    Now we'll run HFR1-33. This test will verify that the DUT supports YCbCr
    4:2:0.  Set up your DUT for 2160p60, YCbCr 4:2:0, 8-bit - VIC 97."""

    waitForReady(info)
    return TLqdStatus.PASS


result = TLqdHFR1_33(qdDev, 97, callbackforSS=hfr133Callback, testParameters=shortTest)
# Show the test results:
showResults('HFR1-33', result)

def hfr134Callback(stepNumber):
    info = """
    Run test HFR1-34.
    This test requires you to provide the VIC and use YCbCr 4:2:0 deep color,
    so set-up your DUT to send VIC 97 (2160p60), YCbCr 4:2:0 10-bits/color."""

    waitForReady(info)
    return TLqdStatus.PASS


result = TLqdHFR1_34(qdDev, 97, 10, callbackforSS=hfr134Callback, testParameters=shortTest)
# Show the test results:
showResults('HFR1-34', result)

def hfr135Callback(stepNumber):
    info = """
    Run test HFR1-35.
    This test requires you to provide the VIC for a 4320p format and use
    deep color, so set-up your DUT to send VIC 194 (4320p24), 10-bits/color."""

    waitForReady(info)
    return TLqdStatus.PASS


result = TLqdHFR1_35(qdDev, 194, 10, callbackforSS=hfr135Callback, testParameters=shortTest)
# Show the test results:
showResults('HFR1-35', result)

def hfr136Callback(stepNumber):
    info = """
    Run test HFR1-36.
    This test requires you to send 3D audio.  Set-up your DUT to send it."""

    waitForReady(info)
    return TLqdStatus.PASS

result = TLqdHFR1_36(qdDev, 2, callbackforSS=hfr136Callback, testParameters=shortTest)
# Show the test results:
showResults('HFR1-36', result)

def hfr137Callback(stepNumber):
    info = """
    Run test HFR1-37.
    This test requires you to send One Bit 3D audio.  Set-up your DUT to send it."""

    waitForReady(info)
    return TLqdStatus.PASS


result = TLqdHFR1_37(qdDev, callbackforSS=hfr137Callback, testParameters=shortTest)
# Show the test results:
showResults('HFR1-37', result)

def hfr138Callback(stepNumber):
    info = """
    Run test HFR1-38.
    This test requires you to send Multi-stream audio.
    Set-up your DUT to send it."""

    waitForReady(info)

    return TLqdStatus.PASS

result = TLqdHFR1_38(qdDev, callbackforSS=hfr138Callback, testParameters=shortTest)
# Show the test results:
showResults('HFR1-38', result)

def hfr139Callback(stepNumber):
    info = """
    Run test HFR1-39.
    This test requires you to send One Bit Multi-stream audio.
    Set-up your DUT to send it."""

    waitForReady(info)
    return TLqdStatus.PASS

result = TLqdHFR1_39(qdDev, callbackforSS=hfr139Callback, testParameters=shortTest)
# Show the test results:
showResults('HFR1-39', result)

def hfr140Callback(stepNumber):
    info = """
    Let's run HFR1-40. This test will verify that the DUT transmits MPEG4 or
    DRA audio over FRL.  Set up your DUT for any format, MPEG4 or DRA audio"""

    waitForReady(info)

    return TLqdStatus.PASS

result = TLqdHFR1_40(qdDev, callbackforSS=hfr140Callback, testParameters=shortTest)
# Show the test results:
showResults('HFR1-40', result)

def hfr141Callback(stepNumber):
    info = """
    Let's run HFR1-41. This test will verify that the DUT properly sends 3D audio.
    Set up your DUT for any format, 3D audio."""

    waitForReady(info)
    return TLqdStatus.PASS

result = TLqdHFR1_41(qdDev, callbackforSS=hfr141Callback, testParameters=shortTest)
# Show the test results:
showResults('HFR1-41', result)

def hfr143Callback(stepNumber):
    info = """
    Let's run HFR1-43. This test will verify that the DUT supports high bit-rate
    audio over FRL.  Set up your DUT for any format, HBR audio."""

    waitForReady(info)
    return TLqdStatus.PASS


result = TLqdHFR1_43(qdDev, callbackforSS=hfr143Callback, testParameters=shortTest)
# Show the test results:
showResults('HFR1-43', result)

def hfr145Callback(stepNumber):
    info = """
    Let's run HFR1-45. This test will verify that the DUT supports L-PCM audio
    over FRL.  Set up your DUT for any format, L-PCM, 48kHz sampling,
    2-channel audio."""

    waitForReady(info)
    return TLqdStatus.PASS


result = TLqdHFR1_45(qdDev, 48000, 0, shorcallbackforSS=hfr145Callback, testParameters=shortTest)
# Show the test results:
showResults('HFR1-45', result)

def hfr110Callback(stepNumber):
    info = """
    Run HFR1-46. This test will verify that the DUT Audio Sample Packet is
    transmitted with the supported sample frequency while in FRL Mode.
    Set up your DUT for any format, L-PCM."""

    waitForReady(info)
    return TLqdStatus.PASS


result = TLqdHFR1_46(qdDev, callbackforSS=hfr118Callback, testParameters=shortTest)
# Show the test results:
showResults('HFR1-46', result)

def hfr150Callback(stepNumber):
    info = """
    Now we'll run HFR1-50. This test will verify that the DUT supports 24-bit
    4320p.  Set up your DUT for 4320p24 - VIC 194."""

    waitForReady(info)
    return TLqdStatus.PASS


result = TLqdHFR1_50(qdDev, 194, callbackforSS=hfr150Callback, testParameters=shortTest)
# Show the test results:
showResults('HFR1-50', result)

def hfr151Callback(stepNumber):
    info = """
    Let's run HFR1-51. This test will verify that the DUT sends YCbCr 4:2:0
    signaling information in the AVI InfoFrame. Let's run all 4 iterations for
    VIC 97 (2160p60)."""

    waitForReady(info)
    return TLqdStatus.PASS


for iter in xrange(1, 5):
    (result, info, errors) = TLqdHFR1_51(qdDev, 97, iter,
                                         callbackforSS=hfr151Callback, testParameters=testparam)
    # Show the test results:
    showResults('HFR1-51 iteration ' + str(iter), result)

def hfr152Callback(stepNumber):
    info = """
    Let's run HFR1-52. This test will verify that the DUT sends YCbCr BT.2020
    4:2:0 signaling information in the AVI InfoFrame. Let's run all 4 iterations
    for VIC 97 (2160p60)."""

    waitForReady(info)
    return TLqdStatus.PASS


for iter in xrange(1, 5):
    (result, info, errors) = TLqdHFR1_52(qdDev, iter,
                                         callbackforSS=hfr152Callback, testParameters=testparam)
    # Show the test results:
    showResults('HFR1-52 iteration ' + str(iter), result)

def hfr180Callback(stepNumber):
    info = """
    Let's run HFR1-80. This test will verify that the DUT sends DSC for
    2160p 8-bit formats. If your DUT can output the DSC test image, pass in True
    for the supportsTestImage parameter. We assume it cannot. The test requires
    a callback to verify the decoded DSC image.
    Run both iterations for VIC 97 (2160p60)."""

    waitForReady(info)
    return TLqdStatus.PASS

result = TLqdHFR1_80(qdDev, 97, 1, callback, False,
                     callbackforSS=hfr180Callback, testParameters=testparam)
showResults('HFR1-80 iteration 1', result)

result = TLqdHFR1_80(qdDev, 97, 2, callback, False,

                     callbackforSS=hfr180Callback, testParameters=testparam)
showResults('HFR1-80 iteration 2', result)

def hfr181Callback(stepNumber):
    info = """
    Let's run HFR1-81. This test will verify that the DUT sends DSC for
    4320p 8-bit formats. If your DUT can output the DSC test image, pass in True
    for the supportsTestImage parameter. We assume it cannot. The test requires
    a callback to verify the decoded DSC image.
    Run both iterations for VIC 194 (4320p24)."""

    waitForReady(info)
    return TLqdStatus.PASS


result = TLqdHFR1_81(qdDev, 194, 1, callback, False,
                     callbackforSS=hfr181Callback, testParameters=testparam)
showResults('HFR1-81 iteration 1', result)

result = TLqdHFR1_81(qdDev, 194, 2, callback, False,
                     callbackforSS=hfr181Callback, testParameters=testparam)
showResults('HFR1-81 iteration 2', result)

def hfr182Callback(stepNumber):
    info = """
    Let's run HFR1-82. This test will verify that the DUT sends DSC for
    <=2160p 10- or 12-bit formats. If your DUT can output the DSC test image,
    pass in True for the supportsTestImage parameter. We assume it cannot. The test
    requires a callback to verify the decoded DSC image.
    Run both iterations for VIC 97 (2160p60), 12-bit."""

    waitForReady(info)
    return TLqdStatus.PASS


result = TLqdHFR1_82(qdDev, 97, 12, 1, callback, False,
                     callbackforSS=hfr182Callback, testParameters=testparam)
showResults('HFR1-82 iteration 1', result)

result = TLqdHFR1_82(qdDev, 97, 12, 2, callback, False,
                     callbackforSS=hfr182Callback,  testParameters=testparam)
showResults('HFR1-82 iteration 2', result)

def hfr183Callback(stepNumber):
    info = """
    Let's run HFR1-83. This test will verify that the DUT sends DSC for
    4320p 10- or 12-bit formats. If your DUT can output the DSC test image,
    pass in True for the supportsTestImage parameter. We assume it cannot. The test
    requires a callback to verify the decoded DSC image.
    Run both iterations for VIC 195 (4320p25), 10-bit."""

    waitForReady(info)
    return TLqdStatus.PASS


result = TLqdHFR1_83(qdDev, 195, 10, 1, callback, False,
                     callbackforSS=hfr182Callback, testParameters=testparam)
showResults('HFR1-83 iteration 1', result)

result = TLqdHFR1_83(qdDev, 195, 10, 2, callback, False,
                     callbackforSS=hfr182Callback, testParameters=testparam)
showResults('HFR1-83 iteration 2', result)

def hfr184Callback(stepNumber):
    info = """
    Let's run HFR1-84. This test will verify that the DUT sends DSC for
    <= 2160p YCbCr 4:4:4, 4:2:2 and/or 4:2:0 formats. If your DUT can output the
    DSC test image, pass in True for the supportsTestImage parameter. We assume it
    cannot. The test requires a callback to verify the decoded DSC image.
    Run both iterations for VIC 97 (2160p60), YCbCr 4:4:4."""

    waitForReady(info)
    return TLqdStatus.PASS


result = TLqdHFR1_84(qdDev, 97, TLqdSubsampling.SS444, 1, callback, False,
                     callbackforSS=hfr184Callback, testParameters=testparam)
showResults('HFR1-84 iteration 1', result)

result = TLqdHFR1_84(qdDev, 97, TLqdSubsampling.SS444, 2, callback, False,
                     callbackforSS=hfr184Callback, testParameters=testparam)
showResults('HFR1-84 iteration 2', result)

def hfr185Callback(stepNumber):
    info = """
    Let's run HFR1-85. This test will verify that the DUT sends DSC for
    4320p YCbCr 4:4:4, 4:2:2 and/or 4:2:0 formats. If your DUT can output the
    DSC test image, pass in True for the supportsTestImage parameter. We assume it
    cannot. The test requires a callback to verify the decoded DSC image.
    Run both iterations for VIC 197 (4320p48), YCbCr 4:2:2."""

    waitForReady(info)

    return TLqdStatus.PASS

result = TLqdHFR1_85(qdDev, 197, TLqdSubsampling.SS422, 1, callback, False,
                     callbackforSS=hfr185Callback, testParameters=testparam)
showResults('HFR1-85 iteration 1', result)

result = TLqdHFR1_85(qdDev, 197, TLqdSubsampling.SS422, 2, callback, False,
                     callbackforSS=hfr185Callback, testParameters=testparam)
showResults('HFR1-85 iteration 2', result)

exit(0)
