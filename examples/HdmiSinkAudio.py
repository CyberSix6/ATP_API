#!/usr/bin/env python

"""@package HdmiSinkAudio Teledyne LeCroy quantumdata Python API
examples for HDMI sink audio control"""

# Copyright (c) 2019 Teledyne LeCroy, Inc.

# Use and Disclosure of Data
# Information contained herein is classified as EAR99 under the U.S. Export
# Administration Regulations.  Export, reexport or diversion contrary to U.S.
# law is prohibited.
#
# Subsequent Pages:
#
# EAR99 Technology Subject to Restrictions Contained on the Cover Page.

## @file HdmiSinkAudio.py
## @brief Sample code for using audio an HDMI Sink

# This program is provided as a demonstration of how to use the
# Teledyne LeCroy quantumdata API suite for using audio on an HDMI receiver

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

# Your quantumdata instrument might be equipped with more than one HDMI
# analyzer card, such as the 18G Protocol Analyzer RX/TX, as well as the
# 48G RX/TX.
# If you have more than one HDMI analyzer installed on the quantumdata
# instrument you're using, it is probably necessary to use the API to set the
# card you're using.
# We provided an API to allow you to choose the card you wish to work with:

TLqdUse(qdDev, 1) # Use card #1

# Now we're ready to use audio on the HDMI analyzer

# Evaluate the incoming audio
print("\nAudio test:\n" + str(TLqdTestAudio(qdDev)))

def showAudio(audio):
    info = 'Audio: sampling:' + str(audio.sampling) + 'Hz'
    info = info + ', ' + str(audio.bitSize) + ' bits'
    info = info + ' ['
    delim = ''
    for chan in audio.channels:
        info = info + delim + str(chan.frequency) + 'Hz'
        info = info + ',' + str(chan.amplitude) + 'dB'
        delim = ';'
    info = info + ']'
    print(info)

# Some HDMI analyzers support ARC or eARC for sending audio in the reverse
# direction. Let's check this card.
print("\n")
if TLqdIsArcSupported(qdDev) or TLqdIsEarcSupported(qdDev):
    if TLqdIsArcSupported(qdDev):
        print("ARC audio is supported\n")
    if TLqdIsEarcSupported(qdDev):
        print("eARC audio is supported\n")

        # Transmit basic L-PCM audio:
        audio = TLqdAudio(48e3, 16)
        TLqdSetEarcAudio(qdDev, audio)

        audio = TLqdGetEarcAudio(qdDev)
        showAudio(audio)

        # Transmit 5.1 L-PCM audio:
        chan = TLqdAudioChannel(1000, -9) # Basic 1kHz sine wave
        sub = TLqdAudioChannel(100, -12) # Sub-woofer, 100Hz
        audio = TLqdAudio(96e3, 20, [chan, chan, chan, chan, chan, sub])
        TLqdSetEarcAudio(qdDev, audio)

        showAudio(TLqdGetEarcAudio(qdDev))

        # Get a list of available compressed audio formats
        comps = TLqdListEarcCompressedAudio(qdDev)
        for comp in comps:
            showCompAudio(comp)

        # Use a Dolby TrueHD compressed audio format
        TLqdSetEarcCompressedAudio(qdDev, '1k_20db7.pcm')

        # Get the compressed audio
        comp = TLqdGetEarcCompressedAudio(qdDev)
        print('Compressed format in use:')
        showCompAudio(comp)

        # Use an EAC3 compressed audio format in layout B
        TLqdSetEarcCompressedAudio(qdDev, '1k_20db5.pcm', True)

        # Get the compressed audio
        comp = TLqdGetEarcCompressedAudio(qdDev)
        print('Compressed format in use:')
        showCompAudio(comp)
else:
    print("Reverse audio isn't supported\n")

exit(0)
