#!/usr/bin/env python

"""@package DpSourceControl Teledyne LeCroy quantumdata Python API
examples for DisplayPort source control"""

# Copyright (c) 2019 Teledyne LeCroy, Inc.

## @file DpSourceControl.py
## @brief Sample code for controlling a DisplayPort Source

# This program is provided as a demonstration of how to use the
# Teledyne LeCroy quantumdata API suite for controlling a DisplayPort
# transmitter

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
ip = '10.30.196.166' # This is the IP address for my quantumdata instrument

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

print(TLqdVersion(qdDev)) # Print version

# This query examines what cards are present which is only necessary on
# quantumdata instruments that can be equipped with multiple cards

print("\nComponents:")
for card in TLqdDiscover(qdDev):
    print(str(card))

# Your quantumdata instrument might be equipped with more than one DisplayPort
# card, such as the 1.4 Video Generator/Analyzer, as well as the DisplayPort
# 1.4 USB-C Video Generator/Analyzer.
# If you have more than one DisplayPort card installed on the quantumdata
# instrument you're using, it is probably necessary to use the API to set the
# card you're using.
# For M41D or M42D use card #1.
# We provided an API to allow you to choose the card you wish to work with:

TLqdUse(qdDev, 1) # Use card #1

# Now we're ready to control the DisplayPort generator

# This query the number of lanes supported by the DP sink
lanes = TLqdReadCapabilityRegisters(qdDev, 2)
print('DP sink supports ' + str(lanes[0] & 0x1F) + ' lanes')

# This query finds the available formats

print("\nAvailable formats:")
for format in TLqdListFormats(qdDev):
    print(str(format))

# This query finds the available images

print("\nAvailable images:")
for image in TLqdListImages(qdDev):
    print(str(image))

# Let's have it send CVT1950D RGB 10-bit:
TLqdSetFormat(qdDev, "CVT1950D", colorSpace=TLqdColorSpace.RGB, bitDepth=10)

# Print the current format data
print(TLqdGetFormat(qdDev))

# Let's have it send DMT0659
TLqdSetFormat(qdDev, "DMT0659")

# Now let's output an image - an all green screen
TLqdSetImage(qdDev, "Flat_G")

# Print the current image name
print(TLqdGetImage(qdDev))

# Use a format with a higher pixel rate
TLqdSetFormat(qdDev, "DMT2075")

# We can also query format parameters

parms = TLqdGetFormatParameters(qdDev)
print(parms)

# This variation gets *all* of the format parameters

parms = TLqdGetFormatParameters(qdDev, True)
print(parms)

def showResults(cmd, result):

    """Display command results
    @param cmd Information about the command
    @param result TLqdResult
    """

    print('Result for "' + cmd + '": ' + str(result.status))
    for item in result.info:
        print(item)
    for item in result.errors:
        print('Error: ' + item)

# You can also roll your own format.
# This requires setting each of the necessary format parameters

parms = TLqdVideoFormatParameters()
parms.HorizontalRate = 31500.469
parms.HorizontalResolution = 640
parms.HorizontalSyncPulseDelay = 16
parms.HorizontalSyncPulsePolarity = TLqdPolarity.Negative
parms.HorizontalSyncPulseWidth = 96
parms.HorizontalTotal = 800
parms.NumberClocksPerPixel = 1
parms.ScanType = TLqdScanType.Progressive
parms.VerticalResolution = 480
parms.VerticalSyncPulseDelay = 10
parms.VerticalSyncPulsePolarity = TLqdPolarity.Negative
parms.VerticalSyncPulseWidth = 2
parms.VerticalTotal = 525
parms.SignalType = TLqdColorSpace.RGB
parms.SamplingMode = 0
showResults('New format', TLqdUseFormatParameters(qdDev, parms))

def printTxLinkTrainStatus(dpTxLinkTrainingStatus):
    """Print Tx Link Training Status"""
    print("\nTx link training status information:")
    import re
    print("Main Stream:", dpTxLinkTrainingStatus.mainStream)
    print("Link Lane Count:", dpTxLinkTrainingStatus.activeLanes)
    print("Link Bandwidth:", dpTxLinkTrainingStatus.bandWidth)
    for i in range(0, len(dpTxLinkTrainingStatus.dpLaneStatus)):
        print("Lane",i," CR Status:", dpTxLinkTrainingStatus.dpLaneStatus[i].crStatus)
        print("Lane",i," Channel Eq Status:", dpTxLinkTrainingStatus.dpLaneStatus[i].ceqStatus)
        print("Lane",i," Sym Lock Status:", dpTxLinkTrainingStatus.dpLaneStatus[i].slckStatus)
        if(float(re.findall(r'\d+\.\d+', dpTxLinkTrainingStatus.bandWidth)[0]) < 10.00 ):
            print("Lane",i," Volt Swing Level:", dpTxLinkTrainingStatus.dpLaneStatus[i].volSwing)
            print("Lane",i," Pre Emp Level:", dpTxLinkTrainingStatus.dpLaneStatus[i].preEmp)
        else:
            print("Lane",i," ffe Preset:", dpTxLinkTrainingStatus.dpLaneStatus[i].ffe)
    print("Inter-lane Alignment:", dpTxLinkTrainingStatus.interLaneAlign)

# Get and Print the Tx Link Training Status
dpTxLinkTrainingStatus = TlqdGetTxLinkTrainingStatus(qdDev)
if isinstance(dpTxLinkTrainingStatus, TLqdTxLinkTrainingStatus):
    printTxLinkTrainStatus(dpTxLinkTrainingStatus)
else:
    print(dpTxLinkTrainingStatus)

def printCrcParam(dpCrcInfo, dsc):

    print("\nTx Crc paramters information:")
    print("Option:", dpCrcInfo.option)
    if dsc == True:
        print(dpCrcInfo.dscStatus)
        print("Crc 0:", dpCrcInfo.crc0)
        print("Crc 1:", dpCrcInfo.crc1)
        print("Crc 2:", dpCrcInfo.crc2)

    print("Crc R Cr:", dpCrcInfo.crcRCr)
    print("Crc G Y:", dpCrcInfo.crcGY)
    print("Crc B Cb:", dpCrcInfo.crcBCb)

# Get and Print the Tx Crc information
port=TLqdPort.PortTx
dsc=False
dpCrcInfo = TlqdGetCrc(qdDev, port, dsc)
printCrcParam(dpCrcInfo, dsc)

# Get and Print the Tx Crc information with dsc
dsc=True
dpCrcInfo = TlqdGetCrc(qdDev, port, dsc)
printCrcParam(dpCrcInfo, dsc)

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

def printHdcpParam(dpHdcpInfo):
    print("HdcpStatus:", dpHdcpInfo.hdcpStatus)
    print("Key:", dpHdcpInfo.key)

# Set Tx HDCP2.3
port = TLqdPort.PortTx
mode = TLqdHdcpMode.HDCP23Mode
showResults('Set Tx HDCP2.3',TlqdSetHdcp(qdDev, port, mode, key=2)) # acceptable HDCP2.3 Tx key are 1,2
dpHdcpInfo = TlqdGetHdcp(qdDev, port, mode)
printHdcpParam(dpHdcpInfo)

# Set LTTPR
showResults('Set LTTPR', TlqdSetLttpr(qdDev, revision=TLqdLttprRevision.Revision20, eqInterlaneAlign=2, cdsInterlaneAlign=5, eqDone=1, count=1))

# Set link training for lane count 2, link rate HBR3(0x1E)
showResults('Set Link training', TLqdSetLinkTraining(qdDev, linkTrainingType=TLqdLinkTrainingType.LinkTrainingTypeAdaptive, laneCount=2, linkRate=TLqdLinkRate.LinkRateHBR3))

# Set Dsc for image "2kClrSq", format 1080p30
showResults('Set DSC',TLqdSetDsc(qdDev, "2kClrSq",format="1080p30", colorMode=TLqdDscColorMode.ColorMode420Native, blockPredictionDisable=True))

# Set USB for Pin Assignment Mode CE
showResults('Set USB', TlqdSetUsb(qdDev, port=TLqdPort.PortTx, pinAssignment=TLqdPinAssignmentMode.PinAssignmentModeCE))

# Set MST for Mode MST
showResults('Set MST', TlqdSetMst(qdDev, port=TLqdPort.PortTx, mode=TLqdMstMode.MSTMode))

# Set the Test auto link training for 2 lane and HBR2 rate.
print(TLqdSetTestAutoRegister(qdDev, 0x201, 1))
print(TLqdSetTestAutoRegister(qdDev, 0x218, 1))
print(TLqdSetTestAutoRegister(qdDev, 0x219, 0x14))
print(TLqdSetTestAutoRegister(qdDev, 0x220, 2))

showResults('Set HotPlug',TlqdSetHotPlug(qdDev, 1))

print(TLqdSetTestAutoRegister(qdDev, 0x201, 0))
print(TLqdSetTestAutoRegister(qdDev, 0x218, 0))
print(TLqdSetTestAutoRegister(qdDev, 0x219, 0))
print(TLqdSetTestAutoRegister(qdDev, 0x220, 0))

# Get Test Description
print("Test Description ", TLqdGetDpTestDescr(qdDev, TLqdDisplayPortCtsType.Dp20SourceCore, "4.3.1.23"))

exit(0)
