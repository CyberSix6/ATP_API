#!/usr/bin/env python

"""@package HdmiSourceAudio Teledyne LeCroy quantumdata Python API
examples for HDMI source audio control"""

# Copyright (c) 2020 Teledyne LeCroy, Inc.

## @file HdmiSourceAudio.py
## @brief Sample code for using audio on an HDMI Source

# This program is provided as a demonstration of how to use the
# Teledyne LeCroy quantumdata API suite for audio operations on an
# HDMI transmitter

# from __future__ import print_function
from tlqd import *
from sys import exit
from time import strftime

ip = '10.30.196.165' # IP address for my quantumdata instrument

qdDev = TLqdConnectSsh(ip, user='qd', passwd='qd')

if not qdDev.connected: # Couldn't connect?
    # Generate a diagnostic and quit - no use trying to proceed
    print('Failed to connect to ' + ip)
    exit(1)

TLqdUse(qdDev, 1) # Use card #1

# Transmit basic L-PCM audio:
audio = TLqdAudio(48e3, 16)
TLqdSetAudio(qdDev, audio)

audio = TLqdGetAudio(qdDev)

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

showAudio(audio)

# Transmit 5.1 L-PCM audio:
chan = TLqdAudioChannel(1000, -9) # Basic 1kHz sine wave
sub = TLqdAudioChannel(100, -12) # Sub-woofer, 100Hz
audio = TLqdAudio(96e3, 20, [chan, chan, chan, chan, chan, sub])
TLqdSetAudio(qdDev, audio)

showAudio(TLqdGetAudio(qdDev))

def showCompAudio(comp):
    out = 'Name:"' + str(comp.name) + '"'
    out = out + ', type:' + str(comp.type)
    if comp.channels:
        out = out + ', channels:' + str(comp.channels)
    if comp.sampling:
        out = out + ', sampling:' + str(comp.sampling)
    if comp.layoutB:
        out = out + ', layout B'
    print('Compressed format: ' + str(out))

# Get a list of available compressed audio formats
comps = TLqdListCompressedAudio(qdDev)
for comp in comps:
    showCompAudio(comp)

# Use a Dolby TrueHD compressed audio format
TLqdSetCompressedAudio(qdDev, '1k_20db7.pcm')

# Get the compressed audio
comp = TLqdGetCompressedAudio(qdDev)
print('Compressed format in use:')
showCompAudio(comp)

# Some HDMI transmitters support ARC or eARC for receiving audio in the reverse
# direction. Let's check this card.
if TLqdIsEarcSupported(qdDev):
    print("eARC audio is supported\n")

    # Get the received eARC audio
    aud = TLqdGetReceivedEarcAudio(qdDev)

    def showRecvAudio(aud):
        if aud.lpcm is not None:
            print('L-PCM')
        elif aud.compressed is not None:
            print('Compressed')
        else:
            print('No eARC audio received')

    showRecvAudio(aud)

else:
    print("eARC audio isn't supported\n")

exit(0)
