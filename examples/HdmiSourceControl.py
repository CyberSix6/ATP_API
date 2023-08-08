#!/usr/bin/env python

"""@package HdmiSourceControl Teledyne LeCroy quantumdata Python API
examples for HDMI source control"""

# Copyright (c) 2019 Teledyne LeCroy, Inc.

## @file HdmiSourceControl.py
## @brief Sample code for controlling an HDMI Source

# This program is provided as a demonstration of how to use the
# Teledyne LeCroy quantumdata API suite for controlling an HDMI transmitter

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

print(TLqdVersion(qdDev)) # Print version

# This query examines what cards are present which is only necessary on
# quantumdata instruments that can be equipped with multiple cards

print("\nComponents:")
for card in TLqdDiscover(qdDev):
    print(str(card))

# Your quantumdata instrument might be equipped with more than one HDMI
# generator card, such as the 18G generator, as well as the 48G RX/TX.
# If you have more than one HDMI generator installed on the quantumdata
# instrument you're using, it is probably necessary to use the API to set the
# card you're using.
# We provided an API to allow you to choose the card you wish to work with:

TLqdUse(qdDev, 2) # Use card #2

# Now we're ready to control the HDMI generator

# This query finds the available formats

print("\nAvailable formats:")
for format in TLqdListFormats(qdDev):
    print(str(format))

# This query finds the available images

print("\nAvailable images:")
for image in TLqdListImages(qdDev):
    print(str(image))

# Let's have it send 2160p60 4:2:0 10-bit:
TLqdSetFormat(qdDev, "2160p60", colorSpace=TLqdColorSpace.YCbCr709,
              subsampling=TLqdSubsampling.SS420, bitDepth=10)

# Print the current format data
print(TLqdGetFormat(qdDev))

# Print the current scrambling
print("Scrambling: " + str(TLqdGetScrambling(qdDev)))

# Let's have it send 480p60
TLqdSetFormat(qdDev, "480p60")

# Print the current scrambling
print("Scrambling: " + str(TLqdGetScrambling(qdDev)))

# Turn scrambling on
TLqdSetScrambling(qdDev, True)

# Print the current scrambling
print("Scrambling: " + str(TLqdGetScrambling(qdDev)))

# Turn scrambling off
TLqdSetScrambling(qdDev, False)

# Now let's output an image - an all blue screen
TLqdSetImage(qdDev, "Flat_B")

# Print the current image name
print(TLqdGetImage(qdDev))

# Use a format with a higher pixel rate
TLqdSetFormat(qdDev, "1080p60")

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

# This example shows how to increase the pixel rate by 0.5%

rate = parms.HorizontalRate
parms = TLqdVideoFormatParameters()
parms.HorizontalRate = rate * 1.005
showResults('Update rate 100.5%', TLqdUpdateFormatParameters(qdDev, parms))

# Restore the pixel rate to 100%

parms.HorizontalRate = rate
showResults('Restore rate', TLqdUpdateFormatParameters(qdDev, parms))

# This example shows how to set YCbCr 4:2:0 10-bit:

parms = TLqdVideoFormatParameters()
parms.SignalType = TLqdColorSpace.YCbCr709
parms.SamplingMode = TLqdSubsampling.SS420
parms.NumberBitsPerColor = 10
showResults('4:2:0 deep color', TLqdUpdateFormatParameters(qdDev, parms))

# You can also roll your own format.
# This requires setting each of the necessary format parameters

parms = TLqdVideoFormatParameters()
parms.VideoIdentificationCode = 1
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
showResults('New format VIC 1', TLqdUseFormatParameters(qdDev, parms))

# Here's how to set a 3D format

# Set 3D frame packing
threeD = TLqd3dData(TLqd3dOption.FramePacking)
resp = TLqdSet3dFormat(qdDev, threeD)
print(resp)

# Query the 3D format
result = TLqdGet3dFormat(qdDev)
print(result)

# Turn off 3D
threeD.option = TLqd3dOption.Off
resp = TLqdSet3dFormat(qdDev, threeD)
print(resp)

exit(0)
