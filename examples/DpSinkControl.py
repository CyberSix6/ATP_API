#!/usr/bin/env python

"""@package DpSinkControl Teledyne LeCroy quantumdata Python API
examples for DisplayPort sink control"""

# Copyright (c) 2019 Teledyne LeCroy, Inc.

# Use and Disclosure of Data
# Information contained herein is classified as EAR99 under the U.S. Export
# Administration Regulations.  Export, reexport or diversion contrary to U.S.
# law is prohibited.
#
# Subsequent Pages:
#
# EAR99 Technology Subject to Restrictions Contained on the Cover Page.

## @file DpSinkControl.py
## @brief Sample code for controlling a DisplayPort Sink

# This program is provided as a demonstration of how to use the
# Teledyne LeCroy quantumdata API suite for controlling a DisplayPort receiver

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
# analyzer card, such as the 1.4 Video Generator/Analyzer, as well as the
# DisplayPort 1.4 USB-C Video Generator/Analyzer.
# If you have more than one DisplayPort analyzer installed on the quantumdata
# instrument you're using, it is probably necessary to use the API to set the
# card you're using.
# For M41D or M42D use card #1.
# We provided an API to allow you to choose the card you wish to work with:

TLqdUse(qdDev, 1) # Use card #1

# Now we're ready to control the DisplayPort analyzer

# Get the current DPCD revision

rev = TLqdGetCapabilityRegisters(qdDev, 0, 1)
print('Rev=%X' % (rev[0], ))

# Set the max. lanes to 3 via DPCD

lane = TLqdGetCapabilityRegisters(qdDev, 2)
lane = (lane[0] & 0xE0) | 3
TLqdSetCapabilityRegisters(qdDev, 2, [lane])

# Grab a frame of video
bitmapFile = "/var/tmp/video.bmp" # Use whatever path suits you
result = TLqdGetVideoFrame(qdDev, bitmapFile)
if result.status:
    # Display the bitmapFile
    pass
else:
    print(str(result.errors))

# Get the input metrics (color space, subsampling, pixel depth, etc.)
metrics = TLqdGetReceivedFormat(qdDev)
print('Incoming video: ' + str(metrics))

redTag = 'R:'
greenTag = 'G:'
blueTag = 'B:'
# If the signal type needs subsampling, it's YCbCr
if metrics.SignalType and metrics.SignalType.needsSubsampling:
    redTag = 'Cr:'
    greenTag = 'Y:'
    blueTag = 'Cb:'
# Get one pixel
pixel = TLqdGetPixel(qdDev, 10, 10)
if not pixel.valid:
    print('Invalid pixel: ' + str(pixel))
else:
    print('\nPixel: ' + redTag + str(pixel.red) + ',' +
        greenTag + str(pixel.green) + ',' + blueTag + str(pixel.blue))

# Try to get an invalid pixel
pixel = TLqdGetPixel(qdDev, 123456789, 101112131415)
if not pixel.valid:
    print('Invalid pixel: ' + str(pixel))

# Perform a capture using 10% of memory.
# Note: The more memory used, the longer the capture will take and a larger
# amount of disk space will be needed.

from time import strftime
dir = '/var/tmp/' + strftime('%Y_%m_%d_%H_%M_%S')

result = TLqdCapture(qdDev, TLqdCaptureType.DpData, 10, getVideo=True,
                     localDirectory=dir)
if result.status == TLqdStatus.PASS:
    print('Capture results are in ' + dir)
else:
    print('Capture failed: ' + str(result.errors))

# Perform a capture using 96% of memory.
# Trigger on start of frame.
# Max Capture time limit is set 6000 milli second
# Note: The more memory used, the longer the capture will take and a larger
# amount of disk space will be needed.

result = TLqdCapture(qdDev, TLqdCaptureType.DpSdp, 96, triggerMode=TLqdTriggerMode.StartOfFrame,
                     captureTimeLimit=6000, localDirectory=dir)
if result.status == TLqdStatus.PASS:
    print('Capture results are in ' + dir)
else:
    print('Capture failed: ' + str(result.errors))

# Get and Print the Error Info
ErrorInfo = TlqdGetErrorInfo(qdDev)
print("FEC:", ErrorInfo.fec)
print("UnCorrected Errors:", ErrorInfo.unCorrectedErrors)
print("Corrected Errors:",ErrorInfo.correctedErrors)
print("Bit Errors:", ErrorInfo.bitErrors)
print("Parity Block Errors:", ErrorInfo.parityBlockErrors)
print("8b10b Training:", ErrorInfo.bitEightTenTraining)
print("Symbol Error:", ErrorInfo.symbolError)
print("Disparity Error:", ErrorInfo.disparityError)

def printRxLinkTrainStatus(dpRxLinkTraingStatus):
    """Print Rx Link Training Status"""

    print("\nRx link training status information:")
    import re
    print("Link Lane Count:", dpRxLinkTraingStatus.activeLanes)
    print("Link Bandwidth:", dpRxLinkTraingStatus.bandWidth)
    for i in range(0, len(dpRxLinkTraingStatus.dpLaneStatus)):
        print("Lane",i," CR Status:", dpRxLinkTraingStatus.dpLaneStatus[i].crStatus)
        print("Lane",i," Channel Eq Status:", dpRxLinkTraingStatus.dpLaneStatus[i].ceqStatus)
        print("Lane",i," Sym Lock Status:", dpRxLinkTraingStatus.dpLaneStatus[i].slckStatus)
        if float(re.findall(r'\d+\.\d+', dpRxLinkTraingStatus.bandWidth)[0]) < 10.00:
            print("Lane",i," Volt Swing Level:", dpRxLinkTraingStatus.dpLaneStatus[i].volSwing)
            print("Lane",i," Pre Emp Level:", dpRxLinkTraingStatus.dpLaneStatus[i].preEmp)
        else:
            print("Lane",i," ffe Preset:", dpRxLinkTraingStatus.dpLaneStatus[i].ffe)

# Get and Print the Rx Link Training Status
dpRxLinkTraingStatus = TlqdGetRxLinkTrainingStatus(qdDev)
if isinstance(dpRxLinkTraingStatus, TLqdRxLinkTrainingStatus):
    printRxLinkTrainStatus(dpRxLinkTraingStatus)
else:
    print(dpRxLinkTraingStatus)

def printCrcParam(dpCrcInfo, dsc):

    print("\nRx Crc paramters information:")
    print("Option:", dpCrcInfo.option)
    if dsc == True:
        print(dpCrcInfo.dscStatus)
        print("Crc 0:", dpCrcInfo.crc0)
        print("Crc 1:", dpCrcInfo.crc1)
        print("Crc 2:", dpCrcInfo.crc2)

    print("Crc R Cr:", dpCrcInfo.crcRCr)
    print("Crc G Y:", dpCrcInfo.crcGY)
    print("Crc B Cb:", dpCrcInfo.crcBCb)

# Get and Print the Rx Crc information
port=TLqdPort.PortRx
dsc=False
dpCrcInfo = TlqdGetCrc(qdDev, port, dsc)
printCrcParam(dpCrcInfo,dsc)

# Get and Print the Rx Crc information with dsc
dsc=True
dpCrcInfo = TlqdGetCrc(qdDev, port, dsc)
printCrcParam(dpCrcInfo,dsc)


# Set the Test auto link training for 2 lane and HBR2 rate.
print(TLqdSetTestAutoRegister(qdDev, 0x201, 1))
print(TLqdSetTestAutoRegister(qdDev, 0x218, 1))
print(TLqdSetTestAutoRegister(qdDev, 0x219, 0x14))
print(TLqdSetTestAutoRegister(qdDev, 0x220, 2))
TlqdSetHotPlug(qdDev, 1)
print(TLqdSetTestAutoRegister(qdDev, 0x201, 0))
print(TLqdSetTestAutoRegister(qdDev, 0x218, 0))
print(TLqdSetTestAutoRegister(qdDev, 0x219, 0))
print(TLqdSetTestAutoRegister(qdDev, 0x220, 0))
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

port = TLqdPort.PortRx
mode = TLqdHdcpMode.HDCP23Mode
showResults('Set Rx HDCP2.3',TlqdSetHdcp(qdDev, port, mode, key=2, repeater=1, repDepth=2, repDeviceCount=2)) # acceptable HDCP2.3 Rx key are 1,2 and 3
dpHdcpInfo = TlqdGetHdcp(qdDev, port, mode)
printHdcpParam(dpHdcpInfo)

port = TLqdPort.PortRx
mode = TLqdHdcpMode.HDCP13Mode
showResults('Set Rx HDCP1.3',TlqdSetHdcp(qdDev, port, mode, key=3)) # acceptable HDCP1.3 Rx key are 1,2 and 3
dpHdcpInfo = TlqdGetHdcp(qdDev, port, mode)
printHdcpParam(dpHdcpInfo)
# Get the current Link Training Time
def printLttime(dpLinkTrainingTime):
    print("Current Link Training Time:")
    print("RX PHY LOCKED:", dpLinkTrainingTime.rxPhyLocked)
    print("LANE 0 CLOCK LOCKED:", dpLinkTrainingTime.lane0ClkLock)
    print("LANE 1 CLOCK LOCKED:", dpLinkTrainingTime.lane1ClkLock)
    print("LANE 2 CLOCK LOCKED:", dpLinkTrainingTime.lane2ClkLock)
    print("LANE 3 CLOCK LOCKED:", dpLinkTrainingTime.lane3ClkLock)
    print("TPS2 DETECTED:", dpLinkTrainingTime.tps2Detected)
    print("TPS3 DETECTED:", dpLinkTrainingTime.tps3Detected)
    print("TPS4 DETECTED:", dpLinkTrainingTime.tps4Detected)
    print("LANE 0 TRAINED:", dpLinkTrainingTime.lane0Trained)
    print("LANE 1 TRAINED:", dpLinkTrainingTime.lane1Trained)
    print("LANE 2 TRAINED:", dpLinkTrainingTime.lane2Trained)
    print("LANE 3 TRAINED:", dpLinkTrainingTime.lane3Trained)
    print("NO TP DETECTED:", dpLinkTrainingTime.noTpDetected)
    print("LT COMPLETE:", dpLinkTrainingTime.ltComplete)
    print("VSTREAM DETECT:", dpLinkTrainingTime.vstreamDetect)

dpLinkTrainingTime = TLqdGetLinkTrainingTime(qdDev)
if isinstance(dpLinkTrainingTime, TLqdLinkTrainingTime):
    printLttime(dpLinkTrainingTime)
else:
    print(dpLinkTrainingTime)

# Set Usb for Pin Assignment Mode CE
showResults('Set USB', TlqdSetUsb(qdDev, port=TLqdPort.PortRx, pinAssignment=TLqdPinAssignmentMode.PinAssignmentModeCE))

# Set Mst for Mode MST
showResults('Set MST', TlqdSetMst(qdDev, port=TLqdPort.PortRx, mode=TLqdMstMode.MSTMode, channelToShow=1, channelCount=4))

# Set SPDIF with enable spdif output true, enable trigger output true
showResults('Set SPDIF', TlqdSetSpdif(qdDev, enableSpdifOutput=1, enableTriggerOutput=1))

# Get a Timing report for msa
showResults('Get Timing Report',TLqdGetTimingReport(qdDev, type='msa', reportTime=1000, localDirectory='D:/Python/LOG//TimeReport'))

# Generate Test pattern training
showResults('Genereate Test pattern',TLqdGenerateTestPattern(qdDev, testPatternType=TLqdTestPatterType.TestPatternTraining, linkRate='HBR2', testPatternSet='TPS1', vsLevel=0, peLevel=2))

# Generate Test pattern panel replay
showResults('Genereate Test pattern',TLqdGenerateTestPattern(qdDev, testPatternType=TLqdTestPatterType.TestPatternPanelReplay, selectiveInterval=2, rfbInterval=120))

# Generate Test pattern square
showResults('Genereate Test pattern',TLqdGenerateTestPattern(qdDev, testPatternType=TLqdTestPatterType.TestPatternSquare, minRefreshRate=60.0, maxRefreshRate=65.2, totalChangePeriod=10))

# Generate Test pattern split sdp
showResults('Genereate Test pattern',TLqdGenerateTestPattern(qdDev, testPatternType=TLqdTestPatterType.TestPatternSplitSdp, minRefreshRate=60.0, maxRefreshRate=65.2, incrementStep=0.25, decrementStep=0.25))

# Generate Test pattern stop
showResults('Genereate Test pattern',TLqdGenerateTestPattern(qdDev, testPatternType=TLqdTestPatterType.TestPatternStop))

exit(0)
