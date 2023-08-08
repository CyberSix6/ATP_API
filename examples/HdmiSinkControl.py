#!/usr/bin/env python

"""@package HdmiSinkControl Teledyne LeCroy quantumdata Python API
examples for HDMI sink control"""

# Copyright (c) 2019 Teledyne LeCroy, Inc.

# Use and Disclosure of Data
# Information contained herein is classified as EAR99 under the U.S. Export
# Administration Regulations.  Export, reexport or diversion contrary to U.S.
# law is prohibited.
#
# Subsequent Pages:
#
# EAR99 Technology Subject to Restrictions Contained on the Cover Page.

## @file HdmiSinkControl.py
## @brief Sample code for controlling an HDMI Sink

# This program is provided as a demonstration of how to use the
# Teledyne LeCroy quantumdata API suite for controlling an HDMI receiver

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

print(TLqdVersion(qdDev)) # Print version

# This query examines what cards are present which is only necessary on
# quantumdata instruments that can be equipped with multiple cards

print("\nComponents:")
for card in TLqdDiscover(qdDev):
    print(str(card))

# Your quantumdata instrument might be equipped with more than one HDMI
# analyzer card, such as the 18G Protocol Analyzer RX/TX, as well as the
# 48G RX/TX.
# If you have more than one HDMI analyzer installed on the quantumdata
# instrument you're using, it is probably necessary to use the API to set the
# card you're using.
# We provided an API to allow you to choose the card you wish to work with:

TLqdUse(qdDev, 4) # Use card #4

# Now we're ready to control the HDMI analyzer

# Set an EDID

edidData = "00FFFFFFFFFFFF004489D40311000000001B0103808048780ADAFFA3584AA22917494B2108003140454061408180010101010101010108E80030F2705A80B0588A00BA882100001E023A801871382D40582C4500BA882100001E000000FC0051443938302048444D49205258000000FD0017F10FFFF0000A202020202020015C02035FF0591005202204030207065D5E5F606162646566C2C4C376757E7D230F7F0778030C001000F8442FC88A01020304814100160608005658006DD85DC401788867000000CF673FE2004B837F0000E10FE40EC7C6C5E3060F01E305FF0100000000000000000000000000000000000000000000000000000000000000001A"

TLqdSetEdidData(qdDev, edidData)

exit(0)

# Grab a frame of video
bitmapFile = "/var/tmp/video.bmp" # Use whatever path suits you
result = TLqdGetVideoFrame(qdDev, bitmapFile)
if result.status == TLqdStatus.PASS:
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
print('\nPixel: ' + redTag + str(pixel.red) + ',' +
    greenTag + str(pixel.green) + ',' +
    blueTag + str(pixel.blue))

# Try to get an invalid pixel
pixel = TLqdGetPixel(qdDev, 123456789, 101112131415)
if not pixel.valid:
    print('Invalid pixel: ' + str(pixel))

# Grab an AVI infoframe and show it
(result, info, octets) = TLqdGetAviInfoframe(qdDev)
print("\nAVI infoframe " + info)

# Perform a TMDS capture using 10% of memory.
# Note: The more memory used, the longer the capture will take and a larger
# amount of disk space will be needed.

from time import strftime
dir = '/var/tmp/' + strftime('%Y_%m_%d_%H_%M_%S')

result = TLqdCapture(qdDev, TLqdCaptureType.TmdsAnalysis, 10,
                     localDirectory=dir)
if result.status == TLqdStatus.PASS:
    print('Capture results are in ' + dir)
else:
    print('Capture failed: ' + str(result.errors))

# Evaluate the incoming audio
print("\nAudio test:\n" + str(TLqdTestAudio(qdDev)))

exit(0)
