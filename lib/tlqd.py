#!/usr/bin/env python

# Copyright (c) 2019 Teledyne LeCroy, Inc.

"""@package tlqd Teledyne LeCroy quantumdata Python API library
@file tlqd.py
@brief API library for a Teledyne LeCroy quantumdata instrument

Interface class for a Teledyne LeCroy quantumdata instrument"""

import sys

## @cond
if sys.version_info < (3,):
    def b(x):
        return x
else:
    import codecs
    def b(x):
        return codecs.latin_1_encode(x)[0]
## @endcond

## @cond
TLqdApiTag = "*TLQDAPI:"
RemoteEdidFile = '/tmp/ApiTestEdid.xml'
RemoteCdfFile = '/tmp/ApiTestCdf.txt'
RemoteVideoBitmapFile = '/tmp/ApiVideo.bmp'
CdfFile = '/home/qd/cdf.txt'
## @endcond

## @{ DP compliance test
DpEdidFile = '/home/qd/dp_edid_cts'
## @param resultsFile Output file from test script
DpResultsFile = '/home/qd/dpct_results.log'
## @param stepsFile Output file from test script
DpStepsFile = '/home/qd/dp_cts_steps.log'
## @param debugFile Output file from test script
DpDebugFile = '/home/qd/dpct_debug.log'
## @param System log Output file from test script
DpSystemFile = '/qd/dpscope'
## @param ACA Output file from test script
DpAcaFile = '/home/qd/tmpAca.zip'
## @} DP compliance test

## @cond
class SubsamplingValue(object):
    def __init__(self, name, key):
        self.name = name
        self.key = key

    def __eq__(self, other):
        # Check for another SubsamplingValue
        if isinstance(other, SubsamplingValue):
            return self.name.lower() == other.name.lower() or \
                self.key == other.key
        # Check for a string
        if isinstance(other, self.name.__class__):
            return self.name.lower() == other.lower()
        # Check for a number
        if isinstance(other, self.key.__class__):
            return self.key == other
        # Who knows what we were given
        return self.name.lower() == str(other).lower()

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        return self.name

class IntValue(object):
    def __init__(self, value):
        self.value = value

    def __eq__(self, other):
        # Check for another IntValue
        if isinstance(other, IntValue):
            return self.value == other.value
        # Check for a number
        if isinstance(other, self.value.__class__):
            return self.value == other
        # Who knows what we were given
        return self.value == float(other)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        return str(self.value)

class DoubleValue(object):
    def __init__(self, value):
        self.value = value

    def __eq__(self, other):
        # Check for another DoubleValue
        if isinstance(other, DoubleValue):
            return self.value == other.value
        # Check for a number
        if isinstance(other, self.value.__class__):
            return self.value == other
        # Who knows what we were given
        return self.value == float(other)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        return str(self.value)

class ScanType(IntValue):
    def __init__(self, value):
        IntValue.__init__(self, value)

    def __str__(self):
        if int(self.value) == 1:
            return 'Progressive'
        if int(self.value) == 2:
            return 'Interlaced'
        return str(self.value)

class Polarity(IntValue):
    def __init__(self, value):
        IntValue.__init__(self, value)

    def __str__(self):
        if int(self.value) == 1:
            return 'Positive'
        if int(self.value) == 0:
            return 'Negative'
        return str(self.value)

class ColorSpaceValue(object):
    def __init__(self, name, key, needsSubsampling):
        self.name = name
        self.key = key
        self.needsSubsampling = needsSubsampling

    def __eq__(self, other):
        # Check for another ColorSpaceValue
        if isinstance(other, ColorSpaceValue):
            return self.name.lower() == other.name.lower() or \
                self.key == other.key
        # Check for a string
        if isinstance(other, self.name.__class__):
            return self.name.lower() == other.lower()
        # Check for a number
        if isinstance(other, self.key.__class__):
            return self.key == other
        # Who knows what we were given
        return self.name.lower() == str(other).lower()

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        return self.name

class StatusValue(object):
    def __init__(self, value):
        self.value = value

    def __eq__(self, other):
        # Check for another StatusValue
        if isinstance(other, StatusValue):
            return self.value.lower() == other.value.lower()
        # Check for a string
        if isinstance(other, self.value.__class__):
            return self.value.lower() == other.lower()
        # Who knows what we were given
        return self.value.lower() == str(other).lower()

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        return self.value

class VideoFormatParameter(object):
    def __init__(self, shortTag, longTag, manditory=False, type=int):
        self.shortTag = shortTag # Command/query
        self.longTag = longTag # Descriptive name
        self.type = type
        self.manditory = manditory # Required parameter

class CaptureOption(IntValue):
    def __init__(self, value):
        IntValue.__init__(self, value)

    def __str__(self):
        if int(self.value) == 0:
            return 'Nothing'
        if int(self.value) == 1:
            return 'All'
        if int(self.value) == 2:
            return 'Failures'
        return str(self.value)

class ThreeDoption(IntValue):
    def __init__(self, value):
        IntValue.__init__(self, value)

    def __str__(self):
        if int(self.value) < 0:
            return 'Off'
        if int(self.value) == 0:
            return 'Frame Packing'
        if int(self.value) == 2:
            return 'Line Alt'
        if int(self.value) == 3:
            return 'Side-Full'
        if int(self.value) == 4:
            return 'L+Depth'
        if int(self.value) == 6:
            return 'Top-Bottom'
        if int(self.value) == 8:
            return 'Side-Half'
        return str(self.value)

class ThreeDextOption(IntValue):
    def __init__(self, value):
        IntValue.__init__(self, value)

    def __str__(self):
        if int(self.value) < 0:
            return 'N/A'
        if int(self.value) == 0:
            return 'Horizontal Sub-Sampling'
        if int(self.value) == 1:
            return 'Quincunx Odd/Odd'
        if int(self.value) == 2:
            return 'Quincunx Odd/Even'
        if int(self.value) == 3:
            return 'Quincunx Even/Odd'
        if int(self.value) == 4:
            return 'Quincunx Even/Even'
        return str(self.value)

## @endcond

## API version
version = '1.2.0'

class TLqdPixel(object):

    """@brief Pixel value

    Class for providing a pixel value"""

    def __init__(self, red=None, green=None, blue=None, error=None):

        """Create a pixel

        @param self The new TLqdPixel object
        @param red Red or Cr value
        @param green Green or Y value
        @param blue Blue or Cb value
        @param error Error information"""

        ## @param red Red or Cr value
        if red is None:
            self.red = red
        else:
            self.red = int(red)
        ## @param green Green or Y value
        if green is None:
            self.green = green
        else:
            self.green = int(green)
        ## @param blue Blue or Cb value
        if blue is None:
            self.blue = blue
        else:
            self.blue = int(blue)
        ## @param error Error information
        self.error = error
        ## @param valid Indicates a valid pixel
        self.valid = self.red is not None and self.green is not None and \
            self.blue is not None

    def __str__(self):
        if self.valid:
            return '(' + str(self.red) + ',' + str(self.green) + ',' + \
                str(self.blue) + ')'
        return str(self.error)

class TLqdEdidComplianceTestVersion(DoubleValue):
    """@brief EDID Compliance Test Version

    Supported versions of the EDID Compliance Tests"""

    def __init__(self, value):

        """Create a version

        @param self The new TLqdStatus object
        @param value float"""

        DoubleValue.__init__(self, value)

    ## Version 2.0
    Version2_0 = DoubleValue(2.0)
    ## Version 2.1
    Version2_1 = DoubleValue(2.1)

class TLqdCallbackState(IntValue):
    """@brief Callback state information

        used to provide callback state info to user"""
    def __init__(self, value):

        """Create a callback states

        @param self The new TLqdCallbackState object
        @param value int"""

        DoubleValue.__init__(self, value)

    ## Callback begin
    init = IntValue(1)
    ## Callback end
    complete = IntValue(2)

class TLqdInstrument(object):

    """@brief Instrument interface

    Interface class for a Teledyne LeCroy quantumdata instrument

    An attempt to establish a connection is performed when this object is
    created"""

    def __init__(self, ipAddr, user='qd', passwd='qd', useSsh=True, port=None):

        """Create an interface to a quantumdata instrument at the given IP
        address.
        After the connection is established, /qd/ptalk will be started
        and used to issue commands.

        @param self The new TLqdInstrument object
        @param ipAddr IP address or name of remote host
        @param user Optional user name - defaults to "qd"
        @param passwd Optional password - defaults to "qd"
        @param useSsh Indicates SSH should be tried - defaults to True
        @param port port number to use"""

        ## @param ipAddr IP address or host name
        self.ipAddr = ipAddr
        ## @param client client connection
        self.client = None
        ## @param channel Communication channel
        self.channel = None
        ## @param user User ID
        self.user = user
        ## @param passwd Password
        self.passwd = passwd
        ## @param portNumber port number used to connect
        self.portNumber = port
        ## @param prompt Command line prompt
        self.prompt = '\n'
        ## @param connected Connection status
        self.connected = False
        ## @param cardUsed Card in use
        self.cardUsed = None

        ## @param i2crVerb Verb to read I2C
        self.i2crVerb = 'i2cr'
        ## @param i2cwVerb Verb to write I2C
        self.i2cwVerb = 'i2cw'

        if useSsh:
            self.connectSsh()
        else:
            self.connectTelnet()

        if self.connected:
            self.setPrompt()
            self.checkVersion()

    def command(self, cmd):

        """Send a command to the quantumdata instrument

        @param self The TLqdInstrument object
        @param cmd Command to send (newline isn't needed)
        @return String output from command"""

        if cmd.find('\n') < 0: # No newline?
            cmd = cmd + '\n' # Add it

        self.channel.send(cmd.encode('utf-8'))

        result = ""
        emptyCount = 0
        while True:
            # Quit if we have a prompt and found it
            if len(self.prompt) and result.find(self.prompt) >= 0:
                break
            # Quit if we don't have a prompt and have something
            if len(self.prompt) == 0 and len(result) and emptyCount > 5:
                break
            latest = self.receive()

            # Check for disk space issue
            noSpaceTag = 'ERROR: Very Low Storage Space'
            if latest.find(noSpaceTag) >= 0:
                self.close()
                raise RuntimeError(noSpaceTag)

            if len(latest):
                emptyCount = 0
            else:
                emptyCount = emptyCount + 1
            result = result + latest

        # Strip the prompt and command from the output and return what's left
        return self.strip(self.strip(result, self.prompt, allOc=True),
                          cmd).rstrip('\n') # Toss trailing NLs

    ## @cond
    def strip(self, inp, target, allOc=False):

        """Remove a string from a string

        @param self The TLqdInstrument object
        @param inp Input string
        @param target String to remove
        @param allOc Remove all occurrences, defaults to false
        @return Input string - target"""

        pos = inp.find(target)
        if pos >= 0:
            tlen = len(target)
            inp = inp[:pos] + inp[pos+tlen:]
            if allOc and tlen > 0:
                return self.strip(inp, target, allOc)
            return inp
        return inp
    ## @endcond

    def close(self):

        """Close the connection to the quantumdata instrument
        @param self The TLqdInstrument object"""

        if self.channel:
            self.channel.close()
            self.channel = None
        if self.client:
            self.client.close()
            self.client = None
        self.connected = False

    ## @cond
    def receive(self):

        """Get any pending output from the quantumdata instrument

        @param self The TLqdInstrument object
        @return String containing all unread output"""

        from socket import timeout

        value = ''
        haveInput = True
        while haveInput:
            try:
                input = self.channel.recv(256).decode()
            except timeout:
                input = ''
            haveInput = len(input) > 0
            value = value + input

        return value.replace('\r', '') # Toss CRs
    ## @endcond

    ## @cond
    def getPrompt(self):

        """Get the prompt used by ptalk

        @param self The TLqdInstrument object
        @return String containing the prompt"""

        return self.prompt
    ## @endcond

    def getFiles(self, remote, local):

        """Get all files of a directory from the quantumdata instrument via FTP

        @param self the TLqdInstrument object
        @param remote folder name on the quantumdata instrument
        @param local folder name on the local machine"""

        import os
        from ftplib import FTP
        found = 0

        ftp = FTP(self.ipAddr, self.user, self.passwd)
        ftp.login(self.user, self.passwd)

        for name in ftp.nlst():
            if name == os.path.basename(remote):
                found = 1
                ftp.cwd(remote)

        if found:
            filelist = []
            filelist = ftp.nlst()
            for file in filelist:
                ftp.retrbinary("RETR " + file, open(os.path.join(local, file),"wb").write)

    def getFile(self, remote, local=None):

        """Get a file from the quantumdata instrument via FTP

        @param self the TLqdInstrument object
        @param remote File name on the quantumdata instrument
        @param local Optional file name on the local machine"""

        from ftplib import FTP
        ftp = FTP(self.ipAddr, self.user, self.passwd)
        ftp.login(self.user, self.passwd)

        if not local:
            local = remote

        found = []

        ftp.retrlines('LIST ' + remote, found.append)

        if 'cannot' not in found[0]: # check if file exists
            lFile = open(local, "wb")
            ftp.retrbinary('RETR ' + remote, lFile.write)
            ftp.quit()
            lFile.close()

    def putFile(self, local, remote=None):

        """Put a file on the quantumdata instrument via FTP

        @param self the TLqdInstrument object
        @param local File name on the local machine
        @param remote Optional file name on the quantumdata instrument"""

        from ftplib import FTP
        ftp = FTP(self.ipAddr, self.user, self.passwd)
        ftp.login(self.user, self.passwd)

        if not remote:
            remote = local

        lFile = open(local, "rb")
        ftp.storbinary('STOR ' + remote, lFile)
        ftp.quit()
        lFile.close()

    def deleteFile(self, remote):

        """Remove a file from the quantumdata instrument via FTP

        @param self the TLqdInstrument object
        @param remote File name on the quantumdata instrument
        @return True if the remote file was removed"""

        from ftplib import FTP
        ftp = FTP(self.ipAddr, self.user, self.passwd)
        ftp.login(self.user, self.passwd)

        ret = False
        try:
            ret = ftp.delete(remote)
        except:
            ret = False
        ftp.quit()
        return ret

    def deleteDirectory(self, remote, force=False):

        """Remove a directory from the quantumdata instrument via FTP

        @param self the TLqdInstrument object
        @param remote Directory name on the quantumdata instrument
        @param force If set, will remove non-empty directories
        @return True if the remote directory was removed"""

        from ftplib import FTP
        ftp = FTP(self.ipAddr, self.user, self.passwd)
        ftp.login(self.user, self.passwd)

        ret = False
        try:
            if force:
                for sub in ftp.nlst(remote):
                    if not self.deleteFile(sub):
                        self.deleteDirectory(sub)

            ret = ftp.rmd(remote)
        except:
            ret = False
        ftp.quit()
        return ret

    def connectSsh(self):

        """Connect via ssh

        @param self the TLqdInstrument object"""

        # from paramiko import util
        # util.log_to_file('/dev/tty')
        from paramiko import SSHClient, SSHException, AutoAddPolicy

        self.client = SSHClient()
        self.client.set_missing_host_key_policy(AutoAddPolicy())
        self.client.load_system_host_keys()

        import os.path
        sshDir = os.path.expanduser('~') + '/.ssh/'
        knownHosts = sshDir + '/known_hosts'
        try:
            self.client.load_host_keys(knownHosts)
        except IOError:
            if not os.path.isdir(sshDir):
                from os import mkdir
                mkdir(sshDir)
            try:
                lFile = open(knownHosts, "w")
                lFile.close()
            except:
                pass

        from socket import error

        try:
            port = self.portNumber
            if port is None:
                port = 22
            self.client.connect(self.ipAddr, username=self.user,
                                password=self.passwd, port=port)
        except (error, SSHException):
            raise RuntimeError('Cannot connect to ' + self.ipAddr +
                               ' via ssh.')

        self.channel = self.client.invoke_shell()

        # Don't wait more than 3/10 second for output
        self.channel.settimeout(0.3)

        self.connected = True

    def connectTelnet(self):

        """Connect via telnet

        @param self the TLqdInstrument object"""

        import telnetlib
        from socket import error

        try:
            port = self.portNumber
            if port is None:
                port = 23
            self.client = telnetlib.Telnet(self.ipAddr, port)
        except error:
            return

        # Log in
        self.client.write(b('\n'))
        info = self.client.read_until(b('\n'))
        if info.find(b('inux')) < 0:
            raise RuntimeError('Not a quantumdata instrument: ' + self.ipAddr)

        loggedIn = False
        while not loggedIn:
            # Close and re-open the telnet session so login works
            self.client.close()
            self.client.open(self.ipAddr)
            self.client.get_socket().settimeout(1)

            self.client.read_until(b('login: '))
            self.client.write(self.user.encode('utf-8')+b('\n'))
            self.client.read_until(b('sword: '), 5)
            self.client.write(self.passwd.encode('utf-8')+b('\n'))
            ret = self.client.read_until(b('Last login:'), 5)
            loggedIn = ret.find(b('Last login:')) >= 0

        self.channel = self.client.get_socket()

        # Don't wait more than 1/2 second for output
        self.channel.settimeout(0.5)

        self.connected = True

    ## @cond
    def setPrompt(self):

        """Connect via telnet

        @param self the TLqdInstrument object"""

        diag = ''
        junk = self.command('')
        diag = diag + junk
        # verify junk got a prompt back
        retry = 0
        while junk.count('>') == 0 and retry != 5:
            junk = self.command('')
            diag = diag + junk
            retry += 1
        if retry == 5:
            raise RuntimeError('Could not get a prompt: ' + self.ipAddr +
                ' (' + diag + ')')

        self.prompt = ''
        self.prompt = self.command('').strip()
        pos = self.prompt.rfind('\n')
        if pos > 0:
            self.prompt = self.prompt[pos+1:]
    ## @endcond

    def getVersion(self):

        """Obtain version data about the quantumdata instrument

        @param self the TLqdInstrument object
        @return String with version information"""

        return self.command(TLqdApiTag + 'version')

    ## @cond
    def checkVersion(self):
        ver = self.getVersion()
        invalid = ver.find('Command Invalid:')
        APIverTag = 'API version: '
        verPos = ver.find(APIverTag)
        if invalid >= 0 or verPos < 0: # Version query failed?
            raise RuntimeError('The API is not compatible with this ' +
                               'quantumdata instrument')
        remoteVersion = ver[verPos+len(APIverTag):]
        pos = remoteVersion.find('\n')
        if pos > 0:
            remoteVersion = remoteVersion[0:pos]
        myVer = version.split('.')
        otherVer = remoteVersion.split('.')
        if len(myVer) != 3:
            raise RuntimeError("Unexpected API version '" + str(version) + "'")
        if len(otherVer) != 3:
            raise RuntimeError('Unexpected quantumdata instrument API ' +
                               "version '" + str(remoteVersion) + "'")
        index = 0
        for part in myVer:
            i = int(part)
            j = int(otherVer[index])
            if i != j: # Parts differ?
                newer = 'newer'
                if i < j:
                    newer = 'older'
                print('*WARNING*: This version of the API (' + str(version) +
                      ') is ' + newer +
                      ' than the quantumdata instrument API (' +
                      str(remoteVersion) + ")")
                return
            index = index + 1
    ## @endcond

    ## @cond
    def listify(self, output):

        """Convert a string with multiple lines into a list of strings

        @param self the TLqdInstrument object
        @param output String with one or more lines
        @return list of strings for each line"""

        return output.split('\n')
    ## @endcond

    ## @cond
    def stringify(self, input):

        """Convert a list to a comma separated string

        @param self the TLqdInstrument object
        @param input list to convert
        @return comma separated string"""

        ret = ''
        comma = ''
        for item in input:
            ret = ret + comma + str(item)
            comma = ','
        return ret
    ## @endcond

    def getDiscover(self):

        """Obtain data about what is installed on the quantumdata instrument

        @param self the TLqdInstrument object
        @return list of installed cards"""

        return self.listify(self.command(TLqdApiTag + 'discover'))

    def getLicenses(self):

        """Obtain data about what is licensed on the quantumdata instrument

        @param self the TLqdInstrument object
        @return list of licenses"""

        return self.listify(self.command(TLqdApiTag + 'license'))

    def setCardUsed(self, cardNumber):

        """Select a card for use

        @param self the TLqdInstrument object
        @param cardNumber Installed card number to use"""

        self.cardUsed = int(cardNumber)
        self.command(TLqdApiTag + 'use ' + str(cardNumber))

    ## @cond
    def compileCommandResult(self, output):

        """Analyze output from a command and compile the data

        @param self the TLqdInstrument object
        @param output Output from running a command
        @return TLqdResult"""

        result = TLqdStatus.PASS
        info = []
        errors = []
        for line in output.split('\n'):
            errorTag = 'error: '
            if line.lower().find(errorTag) == 0:
                errors.append(line[len(errorTag):])
                result = TLqdStatus.FAIL
            elif len(line):
                info.append(line)
        return TLqdResult(result, info, errors)
    ## @endcond

    def setFormat(self, name, colorSpace=None, subsampling=None, bitDepth=None,
                  vic=None):

        """Set a video format

        @param self the TLqdInstrument object
        @param name Format name
        @param colorSpace TLqdColorSpace
        @param subsampling TLqdSubsampling
        @param bitDepth Number of bits/pixel
        @param vic Video identification code
        @return TLqdResult"""

        cmd = TLqdApiTag + 'set_format ' + str(name)
        needsSubsampling = False
        if colorSpace:
            cmd = cmd + ' -c ' + str(colorSpace)
            needsSubsampling = colorSpace.needsSubsampling
        if subsampling:
            cmd = cmd + ' -s ' + str(subsampling)
        elif needsSubsampling:
            return TLqdResult(TLqdStatus('SKIPPED'), [],
                              ['Color space ' + str(colorSpace) +
                              ' requires sub-sampling to be given'])
        if bitDepth:
            cmd = cmd + ' -n ' + str(bitDepth)
        if vic:
            cmd = cmd + ' -v ' + str(vic)
        return self.compileCommandResult(self.command(cmd))

    def createBitmaporText(self, frame, mode=None, localDirectory=None, qdDirectory=None):

        """Create Video frame Bitmap or Text file

        @param qdDev Interface to quantumdata instrument
        @param frame frame number to render,
        @param mode Optional TLqdExportMode
        @param localDirectory Optional Folder path to store generated files
        @param qdDirectory Optional Instrument directory path to store files
        @return TLqdResult"""

        # Transfer the file to the quantumdata instrument
        RemoteVideoFile = '/tmp/ApiTestvideo.img'
        self.putFile(localDirectory+ '/video.img', RemoteVideoFile)

        cmd = TLqdApiTag + 'create_bitmap_or_txt'
        cmd =  cmd + ' -i ' + RemoteVideoFile

        if frame:
            cmd = cmd + ' -f ' +  str(frame)
        if mode:
            cmd = cmd + ' -m ' +  str(mode)

        deleteRemote = qdDirectory is None
        if (localDirectory is not None or
            qdDirectory is not None):
            qdDirectory = self.prepareDirectories(localDirectory, qdDirectory)
            cmd = cmd + ' -d ' + qdDirectory

        result = self.command(cmd)
        self.transferResults(localDirectory, qdDirectory)

        # Clean up the directory on the quantumdata instrument
        if deleteRemote and qdDirectory is not None:
            self.command('exec rm -fr ' + qdDirectory)

        return self.compileCommandResult(result)

    def updateVtem(self, vrrEn=None, mConst=None, reducedBlanking=None,
                   fvaFactorM1=None, baseVfront=None, baseRefreshRate=None):

        """Update Video Timing Extended Metadata

        @param vrrEn Vrr enable
        @param mConst mConst value
        @param reducedBlanking Reduced blanking value
        @param fvaFactorM1 Fast vactive factor minus 1
        @param baseVfront Base vfront
        @param baseRefreshRate Base refresh rate
        @return TLqdResult"""

        cmd = TLqdApiTag + 'update_vtem'
        if vrrEn:
            cmd = cmd + ' -v ' + str(vrrEn)
        if mConst:
            cmd = cmd + ' -c ' + str(mConst)
        if reducedBlanking:
            cmd = cmd + ' -b ' + str(reducedBlanking)
        if fvaFactorM1:
            cmd = cmd + ' -f ' + str(fvaFactorM1)
        if baseVfront:
            cmd = cmd + ' -t ' + str(baseVfront)
        if baseRefreshRate:
            cmd = cmd + ' -r ' + str(baseRefreshRate)
        return self.compileCommandResult(self.command(cmd))

    def configInfoFrame(self, type=None, enable=False):

        """Enable/Disable the Info frame packets

        @param type TLqdInfoFrameType
        @param enable bool to enable/disable InfoFrame packets
        @return TLqdResult"""

        cmd = TLqdApiTag + 'config_if' + ' -t ' + str(type)
        if enable:
            cmd = cmd + ' -e ' + '+'
        else:
            cmd = cmd + ' -e ' + '-'

        return self.compileCommandResult(self.command(cmd))

    def setInfoFrameData(self, count=None, valid=None, status=None,
                  isrc1Data=None, isrc2Data=None, acpType=None,
                  acpData=None):

        """Update International Standard Recording Code

        @param count Isrc1 count value
        @param valid Isrc1 valid value
        @param status Isrc1 status value
        @param isrc1Data Isrc1 data value
        @param isrc2Data Isrc2 data value
        @param acpType Acp type value
        @param acpData Acp data value
        @return TLqdResult"""

        cmd = TLqdApiTag + 'set_infoframe'
        if count:
            cmd = cmd + ' -c ' + str(count)
        if valid:
            cmd = cmd + ' -v ' + str(valid)
        if status:
            cmd = cmd + ' -s ' + str(status)
        if isrc1Data:
            cmd = cmd + ' -d ' + str(isrc1Data)
        if isrc2Data:
            cmd = cmd + ' -e ' + str(isrc2Data)
        if acpType:
            cmd = cmd + ' -a ' + str(acpType)
        if acpData:
            cmd = cmd + ' -p ' + str(acpData)
        return self.compileCommandResult(self.command(cmd))

    def getInfoFrameData(self):

        """Get the Info Frame Packet data(ISRC1, ISRC2 and ACP)

        @param qdDev Interface to quantumdata instrument
        @return string describing the Info Frame packets data"""

        return self.command(TLqdApiTag + 'get_infoframe')

    def set3dFormat(self, threeDformat, name=None):

        """Set a 3D video format

        @param self the TLqdInstrument object
        @param threeDformat the TLqd3dData object
        @param name Optional format name
        @return TLqdResult"""

        cmd = TLqdApiTag + 'set_3d_format'
        if threeDformat.option != TLqd3dOption.Off:
            cmd = cmd + ' -3' + str(threeDformat.option)
            if threeDformat.ext != TLqd3dExtOption.NoExt:
                cmd = cmd + ' -e' + str(threeDformat.ext)
            if name is not None:
                cmd = cmd + ' -f' + str(name)
        return self.compileCommandResult(self.command(cmd))

    def setLinkTraining(self, linkTrainingType=None, linkTrainingMethod=None,
                        lttpr8b10bMethod=None, laneCount=None, linkRate=None,
                        vsLevel=None, peLevel=None, ffe=None, retry=True,
                        fec=False, synchronousClock=True, spreadSpectrum=False):

        """Set link training

        @param self the TLqdInstrument object
        @param linkTrainingType Optional TLqdLinkTrainingType, defaults to
            adaptive
        @param linkTrainingMethod Optional TLqdLinkTrainingMethod
        @param lttpr8b10bMethod Optional TLqdLttpr8b10bMethod
        @param laneCount Lane Count [1,2,4]
        @param linkRate Optional TLqdLinkRate
        @param vsLevel volatage Swing level [0-3]
        @param peLevel preEmphasis level [0-3]
        @param ffe ffe preset value [0-15]
        @param retry retry during link training
        @param fec fec enable/disable
        @param synchronousClock synchronousClock enable/disable
        @param spreadSpectrum spreadSpectrum enable/disable
        @return TLqdResult"""

        cmd = TLqdApiTag + 'set_link_training'
        if linkTrainingType:
            cmd = cmd + ' -t' + str(linkTrainingType)
        if linkTrainingMethod:
            cmd = cmd + ' -m' + str(linkTrainingMethod)
        if lttpr8b10bMethod:
            cmd = cmd + ' -b' + str(lttpr8b10bMethod)
        if laneCount:
            cmd = cmd + ' -l' + str(laneCount)
        if linkRate:
            cmd = cmd + ' -r' + str(linkRate)
        if vsLevel:
            cmd = cmd + ' -v' + str(vsLevel)
        if peLevel:
            cmd = cmd + ' -p' + str(peLevel)
        if ffe:
            cmd = cmd + ' -f' + str(ffe)
        if retry:
            cmd = cmd + ' -R '
        if fec:
            cmd = cmd + ' -F '
        if synchronousClock:
            cmd = cmd + ' -C '
        if spreadSpectrum:
            cmd = cmd + ' -S '

        return self.compileCommandResult(self.command(cmd))

    def setHotPlug(self, duration=None, mode=None):

        """ Set Hot Plug

        @param self the TLqdInstrument object
        @param duration Hot Plug duration in milliseconds
        @param mode Optional TLqdHotPlugMode
        @return TLqdResult"""

        cmd = TLqdApiTag + 'set_hot_plug'
        if duration:
            cmd = cmd + ' -t' + str(duration)
        if mode:
            cmd = cmd + ' -m' + str(mode)
        return self.compileCommandResult(self.command(cmd))

    ## @cond
    def parseRxLinkTrainingStatus(self, output):

        """Parse Rx link training status

        @param self the TLqdInstrument object
        @param output Rx link training status as string
        @return TLqdRxLinkTrainingStatus"""

        sep = ': '
        tag = ['RX Main Link Lane Count', 'RX Main Link Bandwidth Setting',
               'Lane 0', 'Lane 1', 'Lane 2', 'Lane 3']
        activeLanes = None
        bandWidth = ''
        dpLaneStatus = []
        if output.find('Lost') >= 0:
            return output
        for entry in self.listify(output):
            pos = entry.find(sep)
            if pos > 0:
                key = entry[:pos].lstrip()
                value = entry[pos+len(sep):].lstrip()
                if tag[0] == key:
                    activeLanes = value
                if tag[1] == key:
                    bandWidth = value
                if tag[2] == key:
                    dpLaneStatus.append(self.getDpLaneStatus(value, bandWidth))
                if tag[3] == key:
                    dpLaneStatus.append(self.getDpLaneStatus(value, bandWidth))
                if tag[4] == key:
                    dpLaneStatus.append(self.getDpLaneStatus(value, bandWidth))
                if tag[5] == key:
                    dpLaneStatus.append(self.getDpLaneStatus(value, bandWidth))
        return TLqdRxLinkTrainingStatus(activeLanes, bandWidth, dpLaneStatus)
    ## @endcond

    ## @cond
    def parseDPFec8b10bErrorInfo(self, output):

        """Parse DP Fec 8b10b Error info

        @param self the TLqdInstrument object
        @param output Error info as string
        @return TLqdDpErrorInfoParameters"""

        sep = ': '
        tag = ['FEC', 'UnCorrected Errors', 'Corrected Errors', 'Bit Errors',
               'Parity Block Errors', '8b10b Training', 'Symbol Error',
               'Disparity Error']
        fec = ''
        unCorrectedErrors = []
        correctedErrors = []
        bitErrors = []
        parityBlockErrors = []
        bitEightTenTraining = ''
        symbolError = []
        disparityError = []
        for entry in self.listify(output):
            pos = entry.find(sep)
            if pos > 0:
                key = entry[:pos].lstrip()
                value = entry[pos+len(sep):].lstrip()
                if tag[0] == key:
                    fec = value
                if tag[1] == key:
                    unCorrectedErrors = value.split(',')
                if tag[2] == key:
                    correctedErrors = value.split(',')
                if tag[3] == key:
                    bitErrors = value.split(',')
                if tag[4] == key:
                    parityBlockErrors = value.split(',')
                if tag[5] == key:
                    bitEightTenTraining = value
                if tag[6] == key:
                    symbolError = value.split(',')
                if tag[7] == key:
                    disparityError = value.split(',')
        return TLqdDpErrorInfoParameters(fec, unCorrectedErrors,
            correctedErrors, bitErrors, parityBlockErrors, bitEightTenTraining,
            symbolError, disparityError)
    ## @endcond

    ## @cond
    def getDpLaneStatus(self, value, bandWidth):

        """Get the Dp Lane status

        @param self the TLqdInstrument object
        @param value Lane status as string
        @param bandWidth Link bandwidth
        @return TLqdDpLaneStatus"""

        import re
        laneSts = []
        volSwing = preEmp = ffe = None

        temp = re.findall(r'\d+', (re.findall(r'\[.*?\]', value)[0])[1:-1])
        if float(re.findall(r'\d+\.\d+', bandWidth)[0]) < 10.00:
            volSwing = temp[0]
            preEmp = temp[1]
        else:
            ffe = temp[0]
        temp = re.sub("\[.*?\]", "", value).split(',')
        for i in range(0, len(temp)):
            laneSts.append(temp[i].strip().split(' ')[1])

        return TLqdDpLaneStatus(laneSts[0], laneSts[1], laneSts[2], volSwing,
                                preEmp, ffe)
    ## @endcond

    ## @cond
    def parseTxLinkTrainingStatus(self, output):

        """Parse Tx link training status

        @param self the TLqdInstrument object
        @param output Tx link training status as string
        @return TLqdTxLinkTrainingStatus"""

        import re
        sep = ': '
        tag = ['Main Stream', 'Active Lanes', 'Link Bandwidth', 'lane 0',
               'lane 1', 'lane 2', 'lane 3', 'inter-lane Alignment']

        mainStream = ''
        activeLanes = None
        bandWidth = ''
        dpLaneStatus = []
        interLaneAlign = ''
        if output.find('disabled') >= 0:
            return output
        for entry in self.listify(output):
            pos = entry.find(sep)
            if pos > 0:
                key = entry[:pos].rstrip()
                value = entry[pos+len(sep):].lstrip()
                if tag[0] == key:
                    mainStream = value
                if tag[1] == key:
                    activeLanes = value
                if tag[2] == key:
                    bandWidth = value
                if tag[3] == key:
                    dpLaneStatus.append(self.getDpLaneStatus(value, bandWidth))
                if tag[4] == key:
                    dpLaneStatus.append(self.getDpLaneStatus(value, bandWidth))
                if tag[5] == key:
                    dpLaneStatus.append(self.getDpLaneStatus(value, bandWidth))
                if tag[6] == key:
                    dpLaneStatus.append(self.getDpLaneStatus(value, bandWidth))
                if tag[7] == key:
                    interLaneAlign = value
        return TLqdTxLinkTrainingStatus(mainStream, activeLanes, bandWidth,
                                        dpLaneStatus, interLaneAlign)
    ## @endcond

    def getRxLinkTrainingStatus(self):

        """Get Rx link training status

        @param self the TLqdInstrument object
        @return TLqdRxLinkTrainingStatus"""

        cmd = TLqdApiTag + 'get_rx_lt_status'
        return self.parseRxLinkTrainingStatus(self.command(cmd))

    def getErrorInfo(self):

        """Get Error info

        @param self the TLqdInstrument object
        @return TLqdDpErrorInfoParameters"""

        cmd = TLqdApiTag + 'get_err_info'
        return self.parseDPFec8b10bErrorInfo(self.command(cmd))

    def getTxLinkTrainingStatus(self):

        """Get Tx link training status

        @param self the TLqdInstrument object
        @return TLqdTxLinkTrainingStatus"""

        cmd = TLqdApiTag + 'get_tx_lt_status'
        return self.parseTxLinkTrainingStatus(self.command(cmd))

    def getValue(self, data):

        """Get an integer value .

        @param self
        @param data String data to be converted
        @return converted integer"""

        value = data.split()[-1]
        return value

   ## @cond
    def parseVstat(self,output):

        """Parse Vstat information

        @param self the TLqdInstrument object
        @param output Vstat information as string
        @return TLqdVstatParameters"""

        data = self.listify(output)
        if len(data) == 0:
            return None

        # Link
        link = self.getValue(data[0])
        # Lane Count
        laneCount = self.getValue(data[1])
        # Bandwidth
        bandwidth = self.getValue(data[2])
        # Horizontal resolution (Hactive)
        horizontalResolution = self.getValue(data[3])
        # Horizontal total
        horizontalTotal = self.getValue(data[4])
        # Vertical resolution(Vactive)
        verticalResolution = self.getValue(data[5])
        # Vertical total
        verticalTotal = self.getValue(data[6])
        # Scan type
        scan = self.getValue(data[7])
        # Number bits/channel
        numberBitsPerChannel = self.getValue(data[8])
        # Color
        color = self.getValue(data[9])
        # Digital video signal mode
        digtalVideoSignalMode = self.getValue(data[10])
        # HDCP encryption
        hdcpEncrption = self.getValue(data[11])
        # Vertical rate
        verticalRate = self.getValue(data[12])
        # Downspread
        downSpread = self.getValue(data[13])

        return TLqdVstatParameters(link, laneCount, bandwidth, horizontalResolution, horizontalTotal,
                                   verticalResolution, verticalTotal, scan, numberBitsPerChannel, color,
                                   digtalVideoSignalMode, hdcpEncrption, verticalRate, downSpread)
    ## @endcond

   ## @cond
    def parseMsa(self, output):

        """Parse Msa information

        @param self the TLqdInstrument object
        @param output Msa information as string
        @return TLqdMsaParameters"""

        data = self.listify(output)
        if len(data) == 0:
            return None

         # Horiz. total
        horizontalTotal = self.getValue(data[0])
         # Horiz. sync pulse pol
        horizontalSyncPolarity = self.getValue(data[1])
        # Vertical total
        verticalTotal = self.getValue(data[2])
        # Vertical sync pulse pol
        verticalSyncPolarity = self.getValue(data[3])
        # Horiz. sync pulse width
        horizontalSyncWidth = self.getValue(data[4])
        # Vert. sync pulse width
        verticalSyncWidth = self.getValue(data[5])
        # Horizontal resolution
        horizontalResolution = self.getValue(data[6])
        # Vertical resolution
        verticalResolution = self.getValue(data[7])
        # Horizontal Start
        horizontalStart = self.getValue(data[8])
        # Vertical Start
        verticalStart = self.getValue(data[9])
        # Misc0
        misc0 = self.getValue(data[10])
        # Misc1
        misc1 = self.getValue(data[11])
        # Vertical frequency
        verticalFrequency = self.getValue(data[12])
        # Stream Clock
        streamClock = self.getValue(data[13])
        # VB-ID
        vbId = self.getValue(data[14])
        # Afreq
        aFrequency = self.getValue(data[15])
        return TLqdMsaParameters(horizontalTotal, horizontalSyncPolarity, verticalTotal, verticalSyncPolarity,
                                 horizontalSyncWidth, verticalSyncWidth, horizontalResolution, verticalResolution,
                                 horizontalStart, verticalStart, misc0, misc1, verticalFrequency, streamClock, vbId, aFrequency)
    ## @endcond

    def getSinkStatus(self):

        """Get Sink status

        @param self the TLqdInstrument object
        @return TLqdMsaParameters, TLqdVstatParameters"""

        cmd = TLqdApiTag + 'get_vstat'
        vstat = self.command(cmd)

        cmd = TLqdApiTag + 'get_msa'
        msa = self.command(cmd)

        return self.parseVstat(vstat), self.parseMsa(msa)

    ## @cond
    def parseLinkTrainingTime(self, output):

        """Parse Link training time info

        @param self the TLqdInstrument object
        @param output Link training time as string
        @return TLqdLinkTrainingTime"""

        sep = ':'
        tag = ['RX PHY LOCKED', 'TPS2 DETECTED', 'TPS3 DETECTED', 'TPS4 DETECTED',
               'LANE 0 TRAINED', 'LANE 1 TRAINED', 'LANE 2 TRAINED', 'LANE 3 TRAINED',
               'NO TP DETECTED', 'LT COMPLETE', 'VSTREAM DETECT',
               'LANE 0 CLOCK LOCKED', 'LANE 1 CLOCK LOCKED', 'LANE 2 CLOCK LOCKED', 'LANE 3 CLOCK LOCKED']
        rxPhyLocked = tps2Detected = tps3Detected = tps4Detected = 0
        lane0Trained = lane1Trained = lane2Trained = lane3Trained = 0
        noTpDetected = ltComplete = vstreamDetect = 0
        lane0ClkLock = lane1ClkLock = lane2ClkLock = lane3ClkLock = 0

        if output.find('not') >= 0:
            return output

        for entry in self.listify(output):
            pos = entry.find(sep)
            if pos > 0:
                key = entry[:pos].strip()
                value = entry[pos+len(sep):].lstrip()
                if tag[0] == key:
                    rxPhyLocked = value
                if tag[1] == key:
                    tps2Detected = value
                if tag[2] == key:
                    tps3Detected = value
                if tag[3] == key:
                    tps4Detected = value
                if tag[4] == key:
                    lane0Trained = value
                if tag[5] == key:
                    lane1Trained = value
                if tag[6] == key:
                    lane2Trained = value
                if tag[7] == key:
                    lane3Trained = value
                if tag[8] == key:
                    noTpDetected = value
                if tag[9] == key:
                    ltComplete = value
                if tag[10] == key:
                    vstreamDetect = value
                if tag[11] == key:
                    lane0ClkLock = value
                if tag[12] == key:
                    lane1ClkLock = value
                if tag[13] == key:
                    lane2ClkLock = value
                if tag[14] == key:
                    lane3ClkLock = value

        return TLqdLinkTrainingTime(rxPhyLocked, tps2Detected, tps3Detected, tps4Detected,
                                    lane0Trained, lane1Trained, lane2Trained, lane3Trained,
                                    noTpDetected,ltComplete, vstreamDetect,
                                    lane0ClkLock, lane1ClkLock, lane2ClkLock, lane3ClkLock)
    ## @endcond

    def getLinkTrainingTime(self):

        """Get Link Training Time

        @param self the TLqdInstrument object
        @return TLqdLinkTrainingTime"""

        return self.parseLinkTrainingTime(self.command(TLqdApiTag + 'get_lt_time'))

    def getTimingReport(self, type, reportTime= None, localDirectory=None, qdDirectory=None):

        """Get Time report

        @param self the TLqdInstrument object
        @param type Type of timing report
        @param reportTime Optional Time to capture timing report in milliseconds
        @param localDirectory Optional Folder path to store timing report
        @param qdDirectory Optional Instrument directory path to timing report
        @return TLqdResult"""

        cmd = 'get_timing_report -d ' + str(type)
        if reportTime:
            cmd = cmd + ' -t ' + str(reportTime)

        deleteRemote = qdDirectory is None
        if (localDirectory is not None or
            qdDirectory is not None):
            qdDirectory = self.prepareDirectories(localDirectory, qdDirectory)
            cmd = cmd + ' -U' + qdDirectory

        result = self.command(TLqdApiTag + cmd)
        self.transferResults(localDirectory, qdDirectory)

        # Clean up the directory on the quantumdata instrument
        if deleteRemote and qdDirectory is not None:
            self.command('exec rm -fr ' + qdDirectory)

        return self.compileCommandResult(result)

    def generateTestPattern(self, testPatternType=None, linkRate=None, testPatternSet=None,
                            vsLevel=None, peLevel=None, selectiveInterval=None,
                            rfbInterval=None, minRefreshRate=None, maxRefreshRate=None,
                            totalChangePeriod=None, incrementStep=None, decrementStep=None,
                            splitOption=None, sdpLocation=None, sdpClockCycles=None):

        """"Generate Test pattern

        @param self the TLqdInstrument object
        @param testPatternType Optional TLqdTestPatterType
        @param linkRate Optional TLqdLinkRate [RBR | HBR | HBR2 | HBR3]
        @param testPatternSet Optional Test pattern Set [TPS1 | TPS2| TPS3]
        @param vsLevel Optional volatage Swing level [0-3]
        @param peLevel Optional preEmphasis level [0-3]
        @param selectiveInterval Optional Selective Updates interval in frames
        @param rfbInterval Optional full frame RFB update interval in frames
        @param minRefreshRate Optional Minimum refresh rate, floating point number
        @param maxRefreshRate Optional Maximum refresh rate, floating point number
        @param totalChangePeriod Optional Total change period in frames
        @param incrementStep Optional Increment step in miliseconds
        @param decrementStep Optional Decrement step in miliseconds
        @param splitOption Optional Split SDP Options
        @param sdpLocation Optional SDP Clock Cycles
        @param sdpClockCycles Optional SDP location
        @return TLqdResult"""

        cmd = TLqdApiTag + 'generate_test_pattern'
        if testPatternType:
            cmd = cmd + ' -t ' + str(testPatternType)
        if linkRate:
            cmd = cmd + ' -r ' + linkRate
        if testPatternSet:
            cmd = cmd + ' -p ' + testPatternSet
        if vsLevel:
            cmd = cmd + ' -v ' +  str(vsLevel)
        if peLevel:
            cmd = cmd + ' -e ' +  str(peLevel)
        if selectiveInterval:
            cmd = cmd + ' -s ' + str(selectiveInterval)
        if rfbInterval:
            cmd = cmd + ' -f ' + str(rfbInterval)
        if minRefreshRate:
            cmd = cmd + ' -m ' + str(minRefreshRate)
        if maxRefreshRate:
            cmd = cmd + ' -x ' + str(maxRefreshRate)
        if totalChangePeriod:
            cmd = cmd + ' -c ' + str(totalChangePeriod)
        if incrementStep:
            cmd = cmd + ' -i ' + str(incrementStep)
        if decrementStep:
            cmd = cmd + ' -d ' + str(decrementStep)
        if splitOption:
            cmd = cmd + ' -o ' + str(splitOption)
        if sdpLocation:
            cmd = cmd + ' -l ' + str(sdpLocation)
        if sdpClockCycles:
            cmd = cmd + ' -y ' + str(sdpClockCycles)
        result = self.command(cmd)

        return self.compileCommandResult(result)

    ## @cond
    def parseCrc(self, output):

        """Parse Crc info

        @param self the TLqdInstrument object
        @param output Crc as string
        @return TLqdCrcParameters"""

        sep = ':'
        tag = ['Rx DSC CRC', 'Rx Video', 'Tx DSC CRC', 'Tx Video',
               'Rx SW DSC Video', 'Rx HW DSC Video', 'crc_R_Cr',
               'crc_G_Y', 'crc_B_Cb', 'crc_0', 'crc_1', 'crc_2']
        crcRxDsc, crcRx, crcTxDsc, crcTx, crcSwDsc, crcHwDsc = False, False, False, False, False, False
        crcRCr = crcGY = crcBCb = crc0 = crc1 = crc2 = 0
        dscStatus = ''
        option = ''

        for entry in self.listify(output):
            if entry.find('not') >= 0:
                dscStatus = entry
            pos = entry.find(sep)
            if pos > 0:
                key = entry[:pos].strip()
                if tag[0] == key:
                    crcRxDsc = True
                if tag[1] == key:
                    crcRx = True
                if tag[2] == key:
                    crcTxDsc = True
                if tag[3] == key:
                    crcTx = True
                if tag[4] == key:
                    crcSwDsc = True
                if tag[5] == key:
                    crcHwDsc = True
                if not crcSwDsc and not crcHwDsc:
                    option = key
            if pos < 0:
                value = entry.split()
                if crcRxDsc or crcTxDsc:
                    if tag[9] == value[0]:
                        crc0 = value[1]
                    if tag[10] == value[0]:
                        crc1 = value[1]
                    if tag[11] == value[0]:
                        crc2 = value[1]
                if crcSwDsc and not crcHwDsc or crcRx or crcTx:
                    if tag[6] == value[0]:
                        crcRCr = value[1]
                    if tag[7] == value[0]:
                        crcGY = value[1]
                    if tag[8] == value[0]:
                        crcBCb = value[1]
                elif not crcSwDsc and crcHwDsc:
                    if tag[6] == value[0]:
                        crcRCr = value[1]
                    if tag[7] == value[0]:
                        crcGY = value[1]
                    if tag[8] == value[0]:
                        crcBCb = value[1]

        return TLqdCrcParameters(option, crc0, crc1, crc2, crcRCr, crcGY,
                                 crcBCb, dscStatus)
    ## @endcond

    def getCrc(self, port, dsc=False):

        """Get Crc Info

        @param self the TLqdInstrument object
        @param port TLqdPort
        @param dsc optional to parameter to collect dsc crc
        @return TLqdCrcParameters"""

        cmd = TLqdApiTag + 'get_crc -p ' + str(port)

        if dsc:
           cmd = cmd + ' -d'
        return self.parseCrc(self.command(cmd))

    def getDpTestDescr(self, type, testID):

        """Get DP Compliance test description for the given test

        @param type Optional TLqdDisplayPortCtsType, defaults to DP 1.4a Source CTS Core
        @param testId Optional Test ID, defaults to 4.3.1.1
        @return String containing test description"""

        cmd = TLqdApiTag + 'get_test_description -t ' + str(type) + ' -n ' + str(testID)
        return self.command(cmd)

  ## @cond
    def parseSinkTestCrc(self, input):

        """Parse Sink Test Crc info

        @param self the TLqdInstrument object
        @param input Crc as string
        @return TLqdCrcParameters"""
        sep = '='
        input = input.split(";")
        crcList = [None] * 6
        i = 0
        for entry in input:
            pos = entry.find(sep)
            if pos > 0:
                value = entry[pos+len(sep):].lstrip()
                crcList[i] = value
            i = i+1
        return TLqdCrcParameters('Test Crc', crcList[3], crcList[4], crcList[5], crcList[0], crcList[1],
                                 crcList[2], '')
    ## @endcond

    def getSinkTestCrc(self):

        """Get Sink Test Crc Info

        @param self the TLqdInstrument object
        @return TLqdCrcParameters"""

        prefix = ''
        if self.cardUsed is not None:
            prefix = 'OUT' + str(self.cardUsed) + '0:'

        return self.parseSinkTestCrc(self.command(prefix + 'cts print crc'))

    def setDsc(self, image, format=None, colorMode=None,
                 bitsPerCompoment=None, bitsPerPixel=None, sliceWidth=None,
                 sliceHeight=None, blockPredictionDisable=False,
                 lineBuffer=None):
        """Set DSC Paramters

        @param self the TLqdInstrument object
        @param image image name
        @param format Dsc timinig format
        @param colorMode Optional TLqdDscColorMode
        @param bitsPerCompoment bits per compoments
        @param bitsPerPixel bits per pixel
        @param sliceWidth Dsc slice Width
        @param sliceHeight Dsc slice Height
        @param blockPredictionDisable block prediction disable
        @param lineBuffer line buffer depth
        @return TLqdResult"""

        cmd = TLqdApiTag + 'set_dsc ' + str(image)
        if format:
            cmd = cmd + ' -f' + str(format)
        if colorMode:
            cmd = cmd + ' -c' + str(colorMode)
        if bitsPerCompoment:
            cmd = cmd + ' -b' + str(bitsPerCompoment)
        if bitsPerPixel:
            cmd = cmd + ' -p' + str(bitsPerPixel)
        if sliceWidth:
            cmd = cmd + ' -w' + str(sliceWidth)
        if sliceHeight:
            cmd = cmd + ' -h' + str(sliceHeight)
        if blockPredictionDisable:
            cmd = cmd + ' -k'
        if lineBuffer:
            cmd = cmd + ' -l' + str(lineBuffer)
        return self.compileCommandResult(self.command(cmd))

    def setLttpr(self, revision=None, eqInterlaneAlign=None,
                 cdsInterlaneAlign=None, eqDone=None, lttpr_count=None):
        """Set LTTPR emulation

        @param self the TLqdInstrument object
        @param revision Optional TLqdLttprRevision
        @param eqInterlaneAlign delay during EQ interlane Alignment
        @param cdsInterlaneAlign delay during CDS interlane Alignment
        @param eqDone return value of F0008 for EQ done status per LTTPR
        @param count number of LTTPR emulated
        @return TLqdResult"""

        cmd = TLqdApiTag + 'set_lttpr'
        if revision:
            cmd = cmd + ' -v' + str(revision)
        if eqInterlaneAlign:
            cmd = cmd + ' -e' + str(eqInterlaneAlign)
        if cdsInterlaneAlign:
            cmd = cmd + ' -c' + str(cdsInterlaneAlign)
        if eqDone:
            cmd = cmd + ' -d' + str(eqDone)
        if lttpr_count:
            cmd = cmd + ' -l' + str(lttpr_count)
        return self.compileCommandResult(self.command(cmd))

    def setMst(self, port, mode=None, channelToShow=None, channelCount=None):
        """Set MST

        @param self the TLqdInstrument object
        @param port Optional TLqdPort
        @param mode Optional TLqdMstMode
        @param channelToShow virtual channel to show [1-4]
        @param channelCount number of virtual channel to configure [1-4]
        @return TLqdResult"""

        cmd = TLqdApiTag + 'set_mst -p' + str(port)
        if mode:
            cmd = cmd + ' -m' + str(mode)
        if channelToShow:
            cmd = cmd + ' -c' + str(channelToShow)
        if channelCount:
            cmd = cmd + ' -s' + str(channelCount)
        return self.compileCommandResult(self.command(cmd))

    def setSpdif(self, enableSpdifOutput=None, enableTriggerOutput=None):
        """Set SPDIF

        @param self the TLqdInstrument object
        @param enableSpdifOutput SPDIF output enable
        @param enableTriggerOutput trigger output enable
        @return TLqdResult"""

        cmd = TLqdApiTag + 'set_spdif'
        if enableSpdifOutput:
            cmd = cmd + ' -s' + str(enableSpdifOutput)
        if enableTriggerOutput:
            cmd = cmd + ' -t' + str(enableTriggerOutput)
        return self.compileCommandResult(self.command(cmd))

    def setUsb(self, port, pinAssignment=None, powerRoleSwap=None):
        """set Usb

        @param self the TLqdInstrument object
        @param port Optional TLqdPort
        @param pinAssignment Optional TLqdPinAssignmentMode
        @param powerRoleSwap power role swap
        @return TLqdResult"""

        cmd = TLqdApiTag + 'set_usb -p' + str(port)
        if pinAssignment:
            cmd = cmd + ' -a' + str(pinAssignment)
        if powerRoleSwap:
            cmd = cmd + ' -r' + str(powerRoleSwap)
        return self.compileCommandResult(self.command(cmd))

    ## @cond
    def getHdcpKeyType(self, key):
        """get HDCP key type name

        @param self the TLqdInstrument object
        @param key key passed as integer
        @return String key type"""

        switcher = {
            1: 'prod',
            2: 'facsimile1',
            3: 'facsimile2'
        }
        return switcher.get(key, "nothing")
    ## @endcond

    def setHdcp(self, port, mode, key=None, repeater=None, repDepth=None, repDeviceCount=None):

        """Set HDCP

        @param self the TLqdInstrument object
        @param port TLqdPort
        @param mode TLqdHdcpMode
        @param key Optional HDCP Key (1:prod, 2:facsimile1, 3:facsimile2)
        @param repeater Optional Repeater config value
        @param repDepth Optional Repeater depth value
        @param repDeviceCount Optional Repeater device count value
        @return TLqdResult"""

        cmd = TLqdApiTag + 'set_hdcp -p ' + str(port) + ' -m ' + \
              str(mode)
        if key is None:
            cmd = cmd + ' -k ' + str(self.getHdcpKeyType(1))
        else:
            cmd = cmd + ' -k ' + str(self.getHdcpKeyType(key))
        if repeater:
            cmd = cmd + ' -r '
        if repDepth:
            cmd = cmd + ' -d ' + str(repDepth)
        if repDeviceCount:
            cmd = cmd + ' -c ' + str(repDeviceCount)

        return self.compileCommandResult(self.command(cmd))

    ## @cond
    def parseHdcpStatus(self, output):

        """Parse HDCP Status, Key Type info

        @param self the TLqdInstrument object
        @param output as string
        @return TLqdHdcpParameters"""

        tag = ['HDCP2ENABLED', 'HDCP', 'HDCP RX I2C', 'RX KEY', 'TX KEY']
        hdcpStatusVal=''
        keyVal=''
        sep=':'
        key=''

        for entry in self.listify(output):
            pos=entry.find(sep)
            if pos>0:
                key = entry[:pos].strip()
                if tag[0] == key:
                    hdcpStatusVal = entry[pos+len(sep):].lstrip()
                if tag[1] == key:
                    hdcpStatusVal = entry[pos+len(sep):].lstrip()
                if tag[2] == key:
                    hdcpStatusVal = entry[pos+len(sep):].lstrip()
                if tag[3] == key:
                    keyVal = entry[pos+len(sep):].lstrip()
                if tag[4] == key:
                    keyVal = entry[pos+len(sep):].lstrip()
        return TLqdHdcpParameters(hdcpStatusVal, keyVal)
    ## @endcond

    def getHdcp(self, port, mode):

        """Get HDCP

        @param self the TLqdInstrument object
        @param port TLqdPort
        @param mode TLqdHdcpMode
        @return TLqdHdcpParameters"""

        cmd = TLqdApiTag + 'get_hdcp -p ' + str(port) + ' -m ' + str(mode)
        return self.parseHdcpStatus(self.command(cmd))

    def dpGetExtraStep(self, stepInfo):

        """Get Step information

        @param self the TLqdInstrument object
        @param stepInfo step file information
        @return String containing step information with delimiter"""

        extraStep = ''
        if stepInfo:
            stepInfo = stepInfo[0].split(' ')
            index = 2
            while index < len(stepInfo):
                extraStep += (stepInfo[index])
                if index < len(stepInfo) - 1:
                    extraStep += "*"
                index = index + 1
            return extraStep
        return extraStep

    def dpProcessComplianceStepFile(self, callback, stepFileInfo):

        """Process step information based on user inputs from callback

        @param self the TLqdInstrument object
        @param callback Callback function to verify results
        @param stepFileInfo Step file information to execute the test
        @return String containing additional step information"""

        import re
        qdStep = TLqdStep()

        stepInfo = re.findall('.*{pattern},(.*\d+\s+\d+.*)'.format(pattern="PASS"), stepFileInfo)
        passOption = self.dpGetExtraStep(stepInfo)
        if passOption:
            qdStep.passOption = True
        stepInfo = re.findall('.*{pattern},(.*\d+\s+\d+.*)'.format(pattern="FAIL"), stepFileInfo)
        failOption = self.dpGetExtraStep(stepInfo)
        if failOption:
            qdStep.failOption = True
        stepInfo = re.findall('.*{pattern},(.*\d+\s+\d+.*)'.format(pattern="OK"), stepFileInfo)
        okOption = self.dpGetExtraStep(stepInfo)
        if okOption:
            qdStep.okOption = True
        stepInfo = re.findall('.*{pattern},(.*\d+\s+\d+.*)'.format(pattern="NO"), stepFileInfo)
        noOption = self.dpGetExtraStep(stepInfo)
        if noOption:
            qdStep.noOption = True
        stepInfo = re.findall('.*{pattern},(.*\d+\s+\d+.*)'.format(pattern="REPLAY"), stepFileInfo)
        replayOption = self.dpGetExtraStep(stepInfo)
        if replayOption:
            qdStep.replayOption = True
        qdStep.description = re.findall(r'.*text:((?:[^.]*.){5})', stepFileInfo, flags=re.MULTILINE)

        ret = str(callback(qdStep)).upper()

        extraStep = ''
        if ret == "PASS":
            extraStep = passOption
        elif ret == "FAIL":
            extraStep = failOption
        elif ret == "OK":
            extraStep = okOption
        elif ret == "REPLAY":
            extraStep = replayOption
        elif ret == "NO":
            extraStep = noOption
        return extraStep

    def dpInitialize(self):

        """Remove the logs before test execution

        @param self the TLqdInstrument object"""

        self.deleteFile(DpResultsFile)
        self.deleteFile(DpStepsFile)
        self.deleteFile(DpDebugFile)
        self.command('log truncate')
        self.deleteDirectory(DpEdidFile, True)

    def dpGetComplianceResult(self):

        """Get the compliance test execution results

        @param self the TLqdInstrument object
        @return TLqdResult"""

        import re
        import tempfile
        from os import close
        resultFileInfo = ''

        localFile = tempfile.mkstemp('.log', 'tlqdctresults')
        close(localFile[0])

        localFile = localFile[1]
        self.getFile(DpResultsFile, localFile)
        lFile = open(localFile, "r")
        resultFileInfo = lFile.read()

        result = 'PASS'
        info = []
        errors = []

        for line in resultFileInfo.split('\n'):
            if re.search(r'^.*Note_\d:.*$', line.strip()):
                info.append(line)
            if re.search(r'^.*Warn_\d:.*$', line.strip()):
                info.append(line)
            if re.search(r'^.*Skipped_\d:.*$', line.strip()):
                info.append(line)
                result = 'SKIPPED'
            if re.search(r'^.*Fail_\d:.*$', line.strip()):
                errors.append(line)

        if errors:
            result = 'FAIL'

        return TLqdResult(TLqdStatus(result), info, errors)

    def dpProcessComplianceResults(self, testName, tp):

        """Transfer remote data to local using FTP based on test result status
        and user choices

        @param self the TLqdInstrument object
        @param testName Testname to execute
        @param tp TLqdTestParameters
        @return TLqdResult"""

        import os.path
        if tp.localDirectory is None:
            return TLqdResult(TLqdStatus.FAIL, [], [])

        directory = os.path.join(tp.localDirectory,
                                 "{subdir}".format(subdir=testName))
        if not os.path.exists(directory):
            os.makedirs(directory)

        # Get version
        lFile = open(os.path.join(directory, "ver.txt"), 'w')
        lFile.write(self.command("ver"))
        lFile.close()

        self.getFile(DpResultsFile, self.appendFile(directory,
            os.path.basename(DpResultsFile)))

        # Reterive compliance results
        results = self.dpGetComplianceResult()

        if results.status == "FAIL":
            self.getFile(DpAcaFile, self.appendFile(directory,
                os.path.basename(DpAcaFile)))
            if self.cardUsed is not None:
                systemFile = DpSystemFile + str(self.cardUsed) + '.log'
                self.getFile(systemFile, self.appendFile(directory,
                os.path.basename(systemFile)))
        else:
            if tp.collectAca:
                self.getFile(DpAcaFile, self.appendFile(directory,
                    os.path.basename(DpAcaFile)))
            if not tp.collectResult:
                self.deleteFile(self.appendFile(directory,
                    os.path.basename(DpResultsFile)))
            if tp.collectEdid:
               self.getFiles(DpEdidFile, directory)

            if tp.collectSyslog:
                if self.cardUsed is not None:
                    systemFile = DpSystemFile + str(self.cardUsed) + '.log'
                    self.getFile(systemFile, self.appendFile(directory,
                    os.path.basename(systemFile)))

        return results

    ## @cond
    def dpRunComplianceTest(self, cmd, testName, callback, tp):

        """Run a test

        @param self the TLqdInstrument object
        @param cmd Command to execute
        @param testName Testname to execute
        @param callback Callback function to verify step file information
        @param tp TLqdTestParameters
        @return TLqdResult"""

        # Remove the logs before test execution
        self.dpInitialize()

        # Transfer Cdf file to Remote Directory
        if tp.cdf:
            self.putFile(tp.cdf, CdfFile)

        results = self.compileCommandResult(self.command(cmd))
        if results.status == "PASS" and callback:
            while True:
                import tempfile
                from os import close
                stepFileInfo = ''
                extraStep = ''

                localFile = tempfile.mkstemp('.log', 'tlqdctssteps')
                close(localFile[0])

                localFile = localFile[1]
                self.getFile(DpStepsFile, localFile)
                lFile = open(localFile, "r")
                stepFileInfo = lFile.read()

                # Test finished in case no more steps exist
                if len(stepFileInfo) == 0:
                    break

                extraStep = self.dpProcessComplianceStepFile(callback,
                    stepFileInfo)
                self.deleteFile(DpStepsFile)

                if len(extraStep) == 0:
                    raise RuntimeError('Step file {stepsFile} is empty'.format(stepsFile=DpStepsFile))
                else:
                    newCmd = cmd + ' -s ' + extraStep
                    results = self.compileCommandResult(self.command(newCmd))

                if results.status != "PASS":
                    break

        if results.status != "PASS":
            return results

        return self.dpProcessComplianceResults(testName, tp)
    ## @endcond

    def runHdcp2xTest(self, testId, testParameters):

        """Execute HDCP 2.x compliance test

        @param self the TLqdInstrument object
        @param testId Test ID to execute
        @param testParameters TLqdTestParameters
        @return TLqdResult"""

        cmd = 'execute_hdcp_test -N ' + str(testId)
        return self.runTest(cmd, testParameters)

    def runHdcp1xTest(self, testId, testParameters):

        """Execute HDCP 1.x source compliance test

        @param self the TLqdInstrument object
        @param testId Test ID to execute
        @param testParameters TLqdTestParameters
        @return TLqdResult"""

        cmd = 'ct HDCP14 -N '+ str(testId)
        return self.runTest(cmd, testParameters)

    def runEdidSinkTest(self, testId, testParameters):

        """Execute EDID sink compliance test

        @param self the TLqdInstrument object
        @param testId Test ID to execute
        @param testParameters TLqdTestParameters
        @return TLqdResult"""

        cmd = 'ct EdidCT -N '+ str(testId)
        return self.runTest(cmd, testParameters)

    def runDp14SourceTest(self, testName, callback, testParameters):

        """Execute DP 1.4 source compliance test

        @param self the TLqdInstrument object
        @param testName Testname to execute Source test case
        @param callback Callback function to verify step file information
        @param testParameters TLqdTestParameters
        @return TLqdResult"""

        cmd = TLqdApiTag + 'execute_compliance_test -t dpct14'

        acacmd = cmd
        self.command(acacmd + ' -n startACA')
        if testName:
            cmd = cmd + ' -n ' + str(testName)

        results = self.dpRunComplianceTest(cmd, testName, callback, testParameters)
        self.command(acacmd + ' -n stopACA')
        return results

    def runDp14SinkTest(self, testName, callback, testParameters):

        """Execute DP 1.4 sink compliance test

        @param self the TLqdInstrument object
        @param testName Testname to execute Sink test case
        @param callback Callback function to verify step file information
        @param testParameters TLqdTestParameters
        @return TLqdResult"""

        cmd = TLqdApiTag + 'execute_compliance_test -t dpct14'

        acacmd = cmd
        self.command(acacmd + ' -n startACA')
        if testName:
            cmd = cmd + ' -n ' + str(testName)

        results = self.dpRunComplianceTest(cmd, testName, callback, testParameters)
        self.command(acacmd + ' -n stopACA')
        return results

    def runDp12SourceTest(self, testName, callback, testParameters):

        """Execute DP 1.2 source compliance test

        @param self the TLqdInstrument object
        @param testName Testname to execute Source test case
        @param callback Callback function to verify step file information
        @param testParameters TLqdTestParameters
        @return TLqdResult"""

        cmd = TLqdApiTag + 'execute_compliance_test -t dpct12'

        acacmd = cmd
        self.command(acacmd + ' -n startACA')
        if testName:
            cmd = cmd + ' -n ' + str(testName)

        results = self.dpRunComplianceTest(cmd, testName, callback, testParameters)
        self.command(acacmd + ' -n stopACA')
        return results

    def runDp12SinkTest(self, testName, callback, testParameters):

        """Execute DP 1.2 sink compliance test

        @param self the TLqdInstrument object
        @param testName Testname to execute Sink test case
        @param callback Callback function to verify step file information
        @param testParameters TLqdTestParameters
        @return TLqdResult"""

        cmd = TLqdApiTag + 'execute_compliance_test -t dpct12'

        acacmd = cmd
        self.command(acacmd + ' -n startACA')
        if testName:
            cmd = cmd + ' -n ' + str(testName)

        results = self.dpRunComplianceTest(cmd, testName, callback, testParameters)
        self.command(acacmd + ' -n stopACA')
        return results

    def runDp20SourceTest(self, testName, callback, testParameters):

        """Execute DP 2.0 source compliance test

        @param self the TLqdInstrument object
        @param testName Testname to execute Source test case
        @param callback Callback function to verify step file information
        @param testParameters TLqdTestParameters
        @return TLqdResult"""

        cmd = TLqdApiTag + 'execute_compliance_test -t dpct20'
        acacmd = cmd
        self.command(acacmd + ' -n startACA')
        if testName:
            cmd = cmd + ' -n ' + str(testName)

        results = self.dpRunComplianceTest(cmd, testName, callback, testParameters)
        self.command(acacmd + ' -n stopACA' )
        return results

    def runDp20SinkTest(self, testName, callback, testParameters):

        """Execute DP 2.0 sink compliance test

        @param self the TLqdInstrument object
        @param testName Testname to execute Sink test case
        @param callback Callback function to verify step file information
        @param testParameters TLqdTestParameters
        @return TLqdResult"""

        cmd = TLqdApiTag + 'execute_compliance_test -t dpct20'
        acacmd = cmd
        self.command(acacmd + ' -n startACA')
        if testName:
            cmd = cmd + ' -n ' + str(testName)

        results = self.dpRunComplianceTest(cmd, testName, callback, testParameters)
        self.command(acacmd + ' -n stopACA')
        return results

    def runDpEdidSourceTest(self, testName, callback, testParameters):

        """Execute DP Edid source compliance test

        @param self the TLqdInstrument object
        @param testName Testname to execute Source test case
        @param callback Callback function to verify step file information
        @param testParameters TLqdTestParameters
        @return TLqdResult"""

        cmd = TLqdApiTag + 'execute_compliance_test -t dpctedid'
        acacmd = cmd
        self.command(acacmd + ' -n startACA')
        if testName:
            cmd = cmd + ' -n ' + str(testName)

        results = self.dpRunComplianceTest(cmd, testName, callback, testParameters)
        self.command(acacmd + ' -n stopACA')
        return results

    def runDpEdidSinkTest(self, testName, callback, testParameters):

        """Execute DP Edid sink compliance test

        @param self the TLqdInstrument object
        @param testName Testname to execute Sink test case
        @param callback Callback function to verify step file information
        @param testParameters TLqdTestParameters
        @return TLqdResult"""

        cmd = TLqdApiTag + 'execute_compliance_test -t dpctedid'
        acacmd = cmd
        self.command(acacmd + ' -n startACA')
        if testName:
            cmd = cmd + ' -n ' + str(testName)

        results = self.dpRunComplianceTest(cmd, testName, callback, testParameters)
        self.command(acacmd + ' -n stopACA')
        return results


    def getFormat(self):

        """Get the current video format data being transmitted

        @param self the TLqdInstrument object
        @return current format data"""

        return self.command(TLqdApiTag + 'get_format')

    def get3dFormat(self):

        """Get the current 3D video format data being transmitted

        @param self the TLqdInstrument object
        @return TLqd3dData 3D format data"""

        ret = TLqd3dData()
        data = self.command(TLqdApiTag + 'get_3d_format')
        parts = data.split(',')
        if len(parts):
            on = int(parts[0])
            if on > 0 and len(parts) > 1:
                ret.option = TLqd3dOption(int(parts[1]))
                on = len(parts) > 3 and int(parts[2])
                if on:
                    ret.ext = TLqd3dExtOption(int(parts[3]))
            else:
                ret.option = TLqd3dOption.Off
        return ret

    ## @cond
    def outCommand(self, cmd):
        prefix = ''
        if self.cardUsed is not None:
            prefix = 'OUT' + str(self.cardUsed) + '0:'
        return self.command(prefix + cmd)
    ## @endcond

    def getFormatParameters(self, all=False):

        """Get the video format parameters

        @param self the TLqdInstrument object
        @param all Retrieve all format parameters
        @return TLqdVideoFormatParameters"""

        params = TLqdVideoFormatParameters()
        for tag in TLqdVideoFormatParameters.tags:
            if tag.shortTag == "LANES" or tag.shortTag == "LRAT":
                continue
            else:
                if all or tag.manditory:
                    value = self.outCommand(tag.shortTag + '?')
                    badQuery = 'Command Invalid:[2] Invalid query'
                    if value.find(badQuery) < 0: # Valid query?
                        params.__dict__[tag.longTag] = tag.type(value)
        return params

    def updateFormatParameters(self, params):

        """Update video format parameters

        @param self the TLqdInstrument object
        @param params TLqdVideoFormatParameters
        @return TLqdResult"""

        errs = []
        for tag in TLqdVideoFormatParameters.tags:
            if tag.longTag in params.__dict__:
                value = params.__dict__[tag.longTag]
                if value is not None:
                    code = params.getCode(tag.type, value)
                    if code is not None:
                        self.outCommand(tag.shortTag + ' ' + str(code))
                    else:
                        if len(errs):
                            errs.append(', ')
                        errs.append(str(value))
        if len(errs):
            errs = ['Invalid parameters: ' + ''.join(errs)]
            return TLqdResult(TLqdStatus.FAIL, [], errs)

        return self.compileCommandResult(self.outCommand('FMTU'))

    def useFormatParameters(self, params):

        """Set a new video format using parameters

        @param self the TLqdInstrument object
        @param params TLqdVideoFormatParameters
        @return TLqdResult"""

        # Make sure the required parameters are present
        errs = []
        for tag in TLqdVideoFormatParameters.tags:
            if tag.longTag in params.__dict__:
                value = params.__dict__[tag.longTag]
                if value is None and tag.manditory:
                    if len(errs):
                        errs.append(', ')
                    errs.append('' + tag.longTag)
        if len(errs):
            errs = ['Missing mandatory parameter(s): ' + ''.join(errs)]
            return TLqdResult(TLqdStatus.FAIL, [], errs)

        self.outCommand('FMTN')
        self.outCommand('FMTB')
        errs = []
        for tag in TLqdVideoFormatParameters.tags:
            if tag.longTag in params.__dict__:
                value = params.__dict__[tag.longTag]
                if value is not None:
                    code = params.getCode(tag.type, value)
                    if code is not None:
                        self.outCommand(tag.shortTag + ' ' + str(code))
                    else:
                        if len(errs):
                            errs.append(', ')
                        errs.append(str(value))
        if len(errs):
            errs = ['Invalid parameters: ' + ''.join(errs)]
            return TLqdResult(TLqdStatus.FAIL, [], errs)
        self.outCommand('FMTE')
        return self.compileCommandResult(self.outCommand('FMTU'))

    def listFormats(self):

        """Get the list of available video formats

        @param self the TLqdInstrument object
        @return list of format names"""

        return self.listify(self.command(TLqdApiTag + 'list_formats'))

    def setImage(self, name):

        """Set a video image

        @param self the TLqdInstrument object
        @param name Image name
        @return TLqdResult"""

        cmd = TLqdApiTag + 'set_image ' + str(name)
        return self.compileCommandResult(self.command(cmd))

    def updateImage(self):

        """Update the current video image

        @param self the TLqdInstrument object"""

        cmd = TLqdApiTag + 'update_image'
        return self.compileCommandResult(self.command(cmd))

    def getImage(self):

        """Get the current video image name

        @param self the TLqdInstrument object
        @return current image name"""

        return self.command(TLqdApiTag + 'get_image')

    def listImages(self):

        """Get the list of available video images

        @param self the TLqdInstrument object
        @return list of image names"""

        return self.listify(self.command(TLqdApiTag + 'list_images'))

    def getImageParameters(self, name=None):

        """Get the video image parameters

        @param self the TLqdInstrument object
        @param name Optional image name, default is current image in use
        @return list of image parameters"""

        cmd = TLqdApiTag + 'get_image_parameters'
        if name:
            cmd = cmd + ' ' + str(name)
        return self.listify(self.command(cmd))

    def getImageParameter(self, name, parameter):

        """Get the video image parameter value

        @param self the TLqdInstrument object
        @param name Image name
        @param parameter Parameter name
        @return image parameter value"""

        cmd = TLqdApiTag + 'get_image_parameter' + ' ' + str(name) + ' ' + \
            str(parameter)
        return self.command(cmd)

    def setImageParameter(self, name, parameter, value):

        """Set a video image parameter value

        @param self the TLqdInstrument object
        @param name Image name
        @param parameter Parameter name
        @param value image parameter value"""

        cmd = TLqdApiTag + 'set_image_parameter' + ' ' + str(name) + ' ' + \
            str(parameter) + ' ' + str(value)
        self.command(cmd)

    def getImageRenditions(self):

        """Get the number of video image renditions

        @param self the TLqdInstrument object
        @return number of image renditions"""

        return self.command(TLqdApiTag + 'get_image_renditions')

    def getImageRendition(self):

        """Get the video image parameter value

        @param self the TLqdInstrument object
        @return current image rendition value"""

        return self.command(TLqdApiTag + 'get_image_rendition')

    def setImageRendition(self, value):

        """Set the video image rendition value

        @param self the TLqdInstrument object
        @param value image rendition value"""

        cmd = TLqdApiTag + 'set_image_rendition' + + ' ' + str(value)
        self.command(cmd)

    def setScrambling(self, is_scrambled):

        """Set scrambling mode

        @param self the TLqdInstrument object
        @param is_scrambled Indicates new scrambling
        @return TLqdResult"""

        scramble = "0"
        if is_scrambled:
            scramble = "1"
        cmd = TLqdApiTag + 'set_scrambling ' + scramble
        return self.compileCommandResult(self.command(cmd))

    def getScrambling(self):

        """Get the current scrambling mode

        @param self the TLqdInstrument object
        @return True if scrambling"""

        cmd = TLqdApiTag + 'get_scrambling'
        return self.command(cmd) == "1"

    ## @cond
    def compileTestResults(self, output):

        """Analyze output from a test and compile the data

        @param self the TLqdInstrument object
        @param output Output from running a test
        @return TLqdResult"""

        result = 'SKIPPED'
        info = []
        errors = []

        resultTag = 'Test result: '
        errorTag = 'ERROR: '
        errTag = 'err_'
        for line in output.split('\n'):
            if line.find(resultTag) == 0:
                result = line[len(resultTag):]
            elif line.lower().find(errTag) == 0:
                errors.append(line)
            elif line.find(errorTag) == 0:
                errors.append(line[len(errorTag):])
            elif len(line):
                info.append(line)
        return TLqdResult(TLqdStatus(result), info, errors)
    ## @endcond

    ## @cond
    def prepareDirectories(self, localDirectory, qdDirectory):

        """Create directories as needed

        @param self the TLqdInstrument object
        @param localDirectory Folder path to store test result artifacts
        @param qdDirectory instrument directory path with test result artifacts
        @return quantumdata instrument directory path"""

        if localDirectory is None:
            return qdDirectory

        if qdDirectory is None:
            from time import strftime
            qdDirectory = '/tmp/' + strftime('%Y_%m_%d_%H_%M_%S')

        import os
        if not os.path.exists(localDirectory):
            os.mkdir(localDirectory)

        return qdDirectory
    ## @endcond

    ## @cond

    def appendFile(self, directory, file):

        """Append a file name to a directory

        @param self the TLqdInstrument object
        @param directory Directory string
        @param file File name
        @return directory + / + file"""

        retFile = directory
        if retFile[-1] != '/':
            retFile = retFile + '/'
        return retFile + file

    ## @endcond

    ## @cond
    def transferResults(self, localDirectory, qdDirectory):

        """Transfer remote data to local using FTP

        @param self the TLqdInstrument object
        @param localDirectory Folder path to store test result artifacts
        @param qdDirectory instrument directory path with test result
            artifacts"""

        if localDirectory is None or qdDirectory is None:
            return

        from ftplib import FTP
        ftp = FTP(self.ipAddr, self.user, self.passwd)
        ftp.login(self.user, self.passwd)

        found = []

        ftp.retrlines('LIST ' + qdDirectory, found.append)

        from os import mkdir
        from os import path

        for f in found:
            if f.find('cannot access') >= 0 or f.find('No such file') >= 0:
                return
            pos = f.find(':') # Find the colon in the timestamp
            if pos > 0:
                name = f[pos+4:]
                lf = self.appendFile(localDirectory, name)
                rf = self.appendFile(qdDirectory, name)
                if f[0] == 'd': # Sub-directory
                    if not path.exists(lf):
                        mkdir(lf)
                    self.transferResults(lf, rf)
                else:
                    lFile = open(lf, "wb")
                    ftp.retrbinary('RETR ' + rf, lFile.write)
                    lFile.close()
    ## @endcond

    def saveEdidFile(self, edidFile):

        """Transfer an EDID file to the quantumdata instrument

        @param self the TLqdInstrument object
        @param edidFile Local EDID file
        @return string for using the EDID with the test"""

        # Transfer the file to the quantumdata instrument
        self.putFile(edidFile, RemoteEdidFile)
        return ' -Q' + RemoteEdidFile

    def saveEdidData(self, edidData):

        """Save EDID data to a file, transfer it to the quantumdata instrument

        @param self the TLqdInstrument object
        @param edidData EDID data string
        @return string for using the EDID with the test"""

        # Create an EDID file from the data:

        preamble = ('<?xml version="1.0" encoding="UTF-8" standalone="no"?>'
            "\n<DATAOBJ>\n"
            '<HEADER TYPE="DID" VERSION="1.0"/>'
            "\n<DATA>\n")
        postamble = "</DATA>\n</DATAOBJ>\n"

        import tempfile
        from os import close, remove

        edidFile = tempfile.mkstemp('.xml', 'tlqdapiedid')
        close(edidFile[0])
        edidFile = edidFile[1]

        edidOut = open(edidFile, 'w')
        edidOut.write(preamble)

        block = 0
        start = 0
        blockLen = 256
        while len(edidData) >= start + blockLen:
            edidOut.write("<BLOCK" + str(block) + ">")
            edidOut.write(edidData[start:start+blockLen])
            edidOut.write("</BLOCK" + str(block) + ">\n")
            block = block + 1
            start = start + blockLen

        edidOut.write(postamble)
        edidOut.close()

        # Transfer the file to the quantumdata instrument
        self.putFile(edidFile, RemoteEdidFile)
        remove(edidFile)
        return ' -Q' + RemoteEdidFile

    def saveCdfFile(self, cdfFile):

        """Transfer a CDF file to the quantumdata instrument

        @param self the TLqdInstrument object
        @param cdfFile Local CDF file
        @return string for using the CDF with the test"""

        # Transfer the file to the quantumdata instrument
        self.putFile(cdfFile, RemoteCdfFile)
        return ' -P' + RemoteCdfFile

    ## @cond
    def toList(self, input):
        if len(input) > 3 and input[0] == '[' and input[-1] == ']':
            return input[1:-1].split(',')
        return []
    ## @endcond

    def getVideoFrame(self, fileName):

        """Get a frame of video

        @param self the TLqdInstrument object
        @param fileName Fully qualified output bitmap file name
        @return TLqdResult"""

        cmd = TLqdApiTag + 'get_video_frame ' + str(RemoteVideoBitmapFile)
        ret = self.compileCommandResult(self.command(cmd))
        if ret.status == TLqdStatus.PASS:
            self.getFile(RemoteVideoBitmapFile, fileName)
        return ret

    def getPixel(self, x, y):

        """Get one pixel

        @param self the TLqdInstrument object
        @param x X coordinate
        @param y Y coordinate
        @return TLqdPixel"""

        cmd = TLqdApiTag + 'get_pixel ' + str(x) + ' ' + str(y)
        ret = self.compileCommandResult(self.command(cmd))
        if ret.status == TLqdStatus.PASS:
            if len(ret.info) == 1:
                rgb = ret.info[0].split(',')
                if len(rgb) == 3:
                    return TLqdPixel(int(rgb[0]), int(rgb[1]), int(rgb[2]))
            return TLqdPixel(error=ret.errors)
        return TLqdPixel(error=ret.status)

    ## @cond
    def compileInfoframeResult(self, output):

        """Analyze output from an infoframe query and compile the data

        @param self the TLqdInstrument object
        @param output Output from running a command
        @return tuple of (result, error or decoded infoframe,
            infoframe octets)"""

        info = []
        octets = []
        first = True

        for line in output.split('\n'):
            errorTag = 'error'
            if line.lower().find(errorTag) == 0:
                return (False, line, [])
            elif first:
                octets = self.toList(line)
            elif len(line):
                info.append(line)
            first = False
        return (True, '\n'.join(info), octets)
    ## @endcond

    ## @cond
    def getInfoframe(self, infoframe):

        """Get an infoframe

        @param self the TLqdInstrument object
        @param infoframe Infoframe ID
        @return tuple of (result, error or decoded infoframe,
            infoframe octets)"""

        # Make sure there is an object to reference
        cmd = TLqdApiTag + 'infoframe ' + str(infoframe)
        return self.compileInfoframeResult(self.command(cmd))
    ## @endcond

    def getAudioInfoframe(self):

        """Get an audio infoframe

        @param self the TLqdInstrument object
        @return tuple of (result, error or decoded infoframe,
            infoframe octets)"""

        return self.getInfoframe('Audio')

    def getAviInfoframe(self):

        """Get an AVI infoframe

        @param self the TLqdInstrument object
        @return tuple of (result, error or decoded infoframe,
            infoframe octets)"""

        return self.getInfoframe('AVI')

    def getDrmInfoframe(self):

        """Get a dynamic range and mastering infoframe

        @param self the TLqdInstrument object
        @return tuple of (result, error or decoded infoframe,
            infoframe octets)"""

        return self.getInfoframe('DRM')

    def getGcp(self):

        """Get a general control packet

        @param self the TLqdInstrument object
        @return tuple of (result, error or decoded infoframe,
            infoframe octets)"""

        return self.getInfoframe('GCP')

    def getVendorSpecificInfoframe(self):

        """Get a vendor specific infoframe

        @param self the TLqdInstrument object
        @return tuple of (result, error or decoded infoframe,
            infoframe octets)"""

        return self.getInfoframe('VS')

    ## @cond
    def parseFormat(self, format):

        params = TLqdVideoFormatParameters()
        sep = ': '
        for entry in self.listify(format):
            pos = entry.find(sep)
            if pos > 0:
                key = entry[:pos]
                value = entry[pos+len(sep):]
                for tag in TLqdVideoFormatParameters.tags:

                    if tag.shortTag == key:
                        params.__dict__[tag.longTag] = tag.type(value)
        return params
    ## @endcond

    def getReceivedFormat(self):

        """Get the video format parameters being received

        @param self the TLqdInstrument object
        @return TLqdVideoFormatParameters"""

        format = self.command(TLqdApiTag + 'get_received_format')
        return self.parseFormat(format)

    def testAudio(self):

        """Evaluate incoming audio

        @param self the TLqdInstrument object
        @return audio test report"""

        return self.command(TLqdApiTag + 'test_audio')

    def isArcSupported(self):

        """Is ARC supported?

        @param self the TLqdInstrument object
        @return True if ARC is supported"""

        return self.command(TLqdApiTag + 'arc') == "1"

    def isEarcSupported(self):

        """Is eARC supported?

        @param self the TLqdInstrument object
        @return True if eARC is supported"""

        return self.command(TLqdApiTag + 'earc') == "1"

    ## @cond
    def runTest(self, cmd, testParameters, callback= False):

        """Run a test

        @param self the TLqdInstrument object
        @param cmd Command to execute
        @param callback Callback function to do source setup
        @param testParameters TLqdTestParameters
        @return TLqdResult"""

        # Make sure there is an object to reference
        if testParameters is None:
            testParameters = TLqdTestParameters() # Dummy values

        if testParameters.edidFile is not None:
            cmd = cmd + self.saveEdidFile(testParameters.edidFile)
        elif testParameters.edidData is not None:
            cmd = cmd + self.saveEdidData(testParameters.edidData)

        if testParameters.maxFrl is not None:
            cmd = cmd + ' -M' + str(testParameters.maxFrl)

        if testParameters.cdf is not None:
            cmd = cmd + self.saveCdfFile(testParameters.cdf)

        # Pass along save captures indicator if saving locally
        if (testParameters.localDirectory is not None or \
            testParameters.qdDirectory is not None) and \
            testParameters.saveCaptures is not None:
            cmd = cmd + ' -Z' + str(int(testParameters.saveCaptures.value))

        qdDirectory = None
        deleteRemote = testParameters.qdDirectory is None
        if (testParameters.localDirectory is not None or
            testParameters.qdDirectory is not None):
            qdDirectory = self.prepareDirectories(testParameters.localDirectory,
                                                  testParameters.qdDirectory)
            cmd = cmd + ' -U' + qdDirectory
        if testParameters.captureSizePct is not None:
            cmd = cmd + ' -J' + str(testParameters.captureSizePct)
        elif testParameters.captureSizeFrames is not None:
            cmd = cmd + ' -K' + str(testParameters.captureSizeFrames)

        firstcmd, secondcmd = cmd, cmd

        if testParameters.omitHp:
            firstcmd += ' -h'

        if testParameters.callbackSrcSet:
            firstcmd += ' -z' + str(TLqdCallbackState.init)

        output = self.command(TLqdApiTag + firstcmd)
        if callback:
            pos = cmd.find('-i')
            stepNumber = 0
            if pos >= 0:
                stepNumber = cmd[pos+2:pos+4]
            result = self.setupCallback(callback, stepNumber, self.compileTestResults(output))

            if result.status == "PASS":
                if testParameters.callbackSrcSet:
                    secondcmd += ' -z' + str(TLqdCallbackState.complete)
                    output = self.command(TLqdApiTag + secondcmd)

        self.transferResults(testParameters.localDirectory, qdDirectory)

        # Clean up the directory on the quantumdata instrument
        if deleteRemote and qdDirectory is not None:
            self.command('exec rm -fr ' + qdDirectory)

        return self.compileTestResults(output)
    ## @endcond

    ## @cond
    def runRequireHpTest(self, cmd, testParameters, callback=False):

        """Run a test and ensure HP is not bypassed

        @param self the TLqdInstrument object
        @param cmd test to execute
        @param testParameters TLqdTestParameters
        @param callback Callback function to do source setup
        @return TLqdResult"""

        # Make sure there is an object to reference
        if testParameters is None:
            testParameters = TLqdTestParameters() # Dummy values
        hpInfo = None
        if testParameters.omitHp:
            hpInfo = "HP cannot be skipped for this test"
        testParameters.omitHp = False

        ret = self.runTest(cmd, testParameters, callback)

        if hpInfo:
            ret.info.insert(0, hpInfo)
        return ret
    ## @endcond

    ## @cond
    def runRequireCallbackTest(self, cmd, callback, callbackforSS, testParameters):

        """Ensure a callback is provided, then run a test

        @param self the TLqdInstrument object
        @param cmd test to execute
        @param callback Required callback function
        @param callbackforSS Callback function to do source setup
        @param testParameters TLqdTestParameters
        @return TLqdResult"""

        if not callback:
            return TLqdResult(TLqdStatus('SKIPPED'),[],['No callback provided'])

        return self.runTest(cmd, testParameters, callbackforSS)
    ## @endcond

    ## @cond
    def getStepsFileName(self, results):

        """Get the steps file name from results

        @param self the TLqdInstrument object
        @param results TLqdResult
        @return steps file name or None"""

        # See if there is a step file information
        for detail in results.info:
            info = detail.find("Info_")
            stepsTag = "Additional steps: "
            steps = detail.find(stepsTag)
            # See if there is a steps file indicated
            if info == 0 and steps > info:
                steps = steps + len(stepsTag)
                return detail[steps:]

        return None
    ## @endcond

    ## @cond
    def getBitmapFileName(self, stepsFile):

        """Get the bitmap file name from the steps file

        @param self the TLqdInstrument object
        @param stepsFile Local file containing steps
        @return bitmap file name or None"""

        ret = None

        lFile = open(stepsFile, "r")
        for line in lFile:
            line = line.rstrip('\n') # Toss trailing NLs
            verifyTag = "Verify image: "
            verify = line.find(verifyTag)
            # See if there is an image file indicated
            if verify >= 0:
                verify = verify + len(verifyTag)
                ret = line[verify:]
                break
        lFile.close()

        return ret
    ## @endcond

    ## @cond
    def imageCallback(self, callback, results):

        """Process results to verify an image via callback

        @param self the TLqdInstrument object
        @param callback Callback function to verify bitmap image
        @param results TLqdResult
        @return TLqdResult"""

        # See if there is a step file information
        stepsFile = self.getStepsFileName(results)
        if not callback or not stepsFile:
            return results

        import tempfile
        from os import close

        localFile = tempfile.mkstemp('.log', 'tlqdapisteps')
        close(localFile[0])
        localFile = localFile[1]

        self.getFile(stepsFile, localFile)

        bmpRemote = self.getBitmapFileName(localFile)

        if bmpRemote:
            bmpFile = tempfile.mkstemp('.bmp', 'tlqdapiimage')
            close(bmpFile[0])
            bmpFile = bmpFile[1]

            self.getFile(bmpRemote, bmpFile)
            self.deleteFile(bmpRemote)
            ret = str(callback(bmpFile)).upper()
            info = "Verification of " + bmpRemote + ": " + ret
            if ret == "SKIPPED" or ret == "PASS":
                results.info.append(info)
            elif ret == "FAIL":
                results.status = ret
                results.errors.append(info)
            else:
                info = 'Unexpected return value from callback: "' + ret + '"'
                results.errors.append(info)

        return results
    ## @endcond

    ## @cond
    def setupCallback(self, callback, stepNumber, results):

        """Inform user to do source setup via callback

        @param self the TLqdInstrument object
        @param callback Callback function to do source setup
        @param stepNumber Test step number
        @param results TLqdResult
        @return TLqdResult"""

        # See if there is a step file information
        stepsFile = self.getStepsFileName(results)
        if not callback or not stepsFile:
            return results

        import tempfile
        from os import close
        ret = ""

        localFile = tempfile.mkstemp('.log', 'tlqdapisteps')
        close(localFile[0])
        localFile = localFile[1]

        self.getFile(stepsFile, localFile)
        lFile = open(localFile, "r")
        for line in lFile:
            line = line.rstrip('\n') # Toss trailing NLs
            verifyTag = "Callback indicator: "
            verify = line.find(verifyTag)
            # See if there is an image file indicated
            if verify >= 0:
                verify = verify + len(verifyTag)
                ret = line[verify:]
                break
        lFile.close()

        if ret.strip() == "SetupSource":
            ret = str(callback(int(stepNumber))).upper()
            info = "Setup Source status: " + ret
            if ret == "SKIPPED" or ret == "PASS":
                results.info.append(info)
                results.status = ret
            elif ret == "FAIL":
                results.status = ret
                results.errors.append(info)
            else:
                info = 'Unexpected return value from callback: "' + ret + '"'
                results.errors.append(info)
        return results
    ## @endcond

    ## @cond
    def runEarcTest(self, cmd, testParameters):
        """Run an eARC test

        @param self the TLqdInstrument object
        @param cmd Command to execute
        @param testParameters TLqdTestParameters
        @return TLqdResult"""

        if testParameters is not None and testParameters.durationMs is not None:
            cmd = cmd + ' -D' + str(testParameters.durationMs)
        return self.runRequireHpTest(cmd, testParameters)
    ## @endcond

    def run7_16(self, vic, callbackforSS=False, testParameters=None):

        """Execute HDMI 1.4 source test 7-16

        This test verifies that the source only outputs legal 10-bit codes

        @param self the TLqdInstrument object
        @param vic Video identification code
        @param callbackforSS Callback function to do source setup
        @param testParameters TLqdTestParameters
        @return TLqdResult"""

        return self.runTest('ct 7-16 -v' + str(vic), testParameters, callbackforSS)

    def run7_17(self, vic, callbackforSS=False, testParameters=None):

        """Execute HDMI 1.4 source test 7-17

        This test verifies that the source only outputs code sequences for
        Control Periods, Data Island Periods and Video Data Periods
        corresponding to basic HDMI protocol rules

        @param self the TLqdInstrument object
        @param vic Video identification code
        @param callbackforSS Callback function to do source setup
        @param testParameters TLqdTestParameters
        @return TLqdResult"""

        return self.runTest('ct 7-17 -v' + str(vic), testParameters, callbackforSS)

    def run7_18(self, vic, callbackforSS=False, testParameters=None):

        """Execute HDMI 1.4 source test 7-18

        This test verifies that the source only outputs an Extended Control
        Period within the required period

        @param self the TLqdInstrument object
        @param vic Video identification code
        @param callbackforSS Callback function to do source setup
        @param testParameters TLqdTestParameters
        @return TLqdResult"""

        return self.runTest('ct 7-18 -v' + str(vic), testParameters, callbackforSS)

    def run7_19(self, vic, stepNumber, callbackforSS=False, testParameters=None):

        """Execute HDMI 1.4 source test 7-19

        This test verifies that the source only transmits permitted Packet
        Types and that reserved fields are zero

        @param self the TLqdInstrument object
        @param vic Video identification code
        @param stepNumber Test step number, 1 or 2
        @param callbackforSS Callback function to do source setup
        @param testParameters TLqdTestParameters
        @return TLqdResult"""

        cmd = 'ct 7-19 -v' + str(vic) + ' -i' + str(stepNumber)
        return self.runTest(cmd, testParameters, callbackforSS)

    def run7_23(self, vic, callback, callbackforSS=False, testParameters=None):

        """Execute HDMI 1.4 source test 7-23

        This test verifies that the Source DUT always outputs required pixel
        encoding (RGB), which also correlates with Y0 and Y1 in AVI InfoFrame
        when connected to an RGB-only Sink.

        Also verify that the Source DUT outputs AVI InfoFrame with default
        range value in Q and YQ field when a Sink device does not support
        selectable RGB Quantization Range

        @param self the TLqdInstrument object
        @param vic Video identification code
        @param callback Callback function to verify bitmap image
        @param callbackforSS Callback function to do source setup
        @param testParameters TLqdTestParameters
        @return TLqdResult"""

        ret = self.runRequireCallbackTest('ct 7-23 -v' + str(vic),
            callback, callbackforSS, testParameters)
        return self.imageCallback(callback, ret)

    def run7_24(self, vic, callback, callbackforSS=False, testParameters=None):

        """Execute HDMI 1.4 source test 7-24

        This test verifies that the Source DUT always outputs required
        pixel encoding that correlates with Y0 and Y1 fields in AVI InfoFrame
        when presented with a YCbCr-capable Sink and that DUT is capable of
        supporting YCbCr pixel encoding when required.

        Also verify that the Source DUT outputs AVI InfoFrame with default range
        value in Q and YQ field when a Sink device does not support selectable
        YCC Quantization Range

        @param self the TLqdInstrument object
        @param vic Video identification code
        @param callback Callback function to verify bitmap image
        @param callbackforSS Callback function to do source setup
        @param testParameters TLqdTestParameters
        @return TLqdResult"""

        ret = self.runRequireCallbackTest('ct 7-24 -v' + str(vic),
            callback, callbackforSS, testParameters)
        return self.imageCallback(callback, ret)

    def run7_25(self, vic, callbackforSS=False, testParameters=None):

        """Execute HDMI 1.4 source test 7-25

        This test verifies that Source DUT, whenever transmitting any CEA video
        format, complies with all required pixel and line counts and pixel
        clock frequency range

        @param self the TLqdInstrument object
        @param vic Video identification code
        @param callbackforSS Callback function to do source setup
        @param testParameters TLqdTestParameters
        @return TLqdResult"""

        return self.runTest('ct 7-25 -v' + str(vic), testParameters)

    def run7_26(self, vic, callbackforSS=False, testParameters=None):

        """Execute HDMI 1.4 source test 7-26

        This test verifies that Source DUT indicates Pixel Repetition values in
        AVI InfoFrame as required and that the pixels are actually repeated the
        indicated number of times

        @param self the TLqdInstrument object
        @param vic Video identification code
        @param callbackforSS Callback function to do source setup
        @param testParameters TLqdTestParameters
        @return TLqdResult"""

        return self.runTest('ct 7-26 -v' + str(vic), testParameters, callbackforSS)

    def run7_27(self, vic, callbackforSS=False, testParameters=None):

        """Execute HDMI 1.4 source test 7-27

        This test verifies that at least one AVI InfoFrame is transmitted for
        every two video fields when required and that any AVI InfoFrame
        transmitted is accurate

        @param self the TLqdInstrument object
        @param vic Video identification code
        @param callbackforSS Callback function to do source setup
        @param testParameters TLqdTestParameters
        @return TLqdResult"""

        return self.runTest('ct 7-27 -v' + str(vic), testParameters, callbackforSS)

    def run7_28(self, stepNumber, callbackforSS=False, testParameters=None):

        """Execute HDMI 1.4 source test 7-28

        This test verifies that the behavior of all fields within the Audio
        Sample or High-Bitrate Audio Stream Subpackets follow the corresponding
        rules specified in the IEC 60959 or IEC 61937 specifications

        There are three steps for this test:
            - stepNumber=1: Verifies 2-channel, basic audio
            - stepNumber=2: Verifies multi-channel audio, maximum sampling rate
            - stepNumber=3: Verifies high-bitrate audio

        @param self the TLqdInstrument object
        @param stepNumber Test step number, 1, 2 or 3
        @param callbackforSS Callback function to do source setup
        @param testParameters TLqdTestParameters
        @return TLqdResult"""

        cmd = 'ct 7-28 -i' + str(stepNumber)
        return self.runTest(cmd, testParameters, callbackforSS)

    def run7_29(self, stepNumber, callbackforSS=False, testParameters=None):

        """Execute HDMI 1.4 source test 7-29

        This test verifies that the relationship between the parameters (N,
        CTS, audio sample rate) is correct with respect to the Audio Clock
        Regeneration mechanism

        There are two steps for this test:
            - stepNumber=1: Verifies basic audio
            - stepNumber=2: Verifies deep color, basic audio

        @param self the TLqdInstrument object
        @param stepNumber Test step number, 1 or 2
        @param callbackforSS Callback function to do source setup
        @param testParameters TLqdTestParameters
        @return TLqdResult"""

        cmd = 'ct 7-29 -i' + str(stepNumber)
        return self.runTest(cmd, testParameters, callbackforSS)

    def run7_30(self, stepNumber, vic, samplingRate, maxChannels,
                callbackforSS=False, testParameters=None):

        """Execute HDMI 1.4 source test 7-30

        This test verifies that the source audio packet jitter is within the
        limits specified

        There are two steps for this test:
            - stepNumber=1: Verifies 3 or more channels
            - stepNumber=2: Verifies 2 L-PCM channels or Compressed Audio

        @param self the TLqdInstrument object
        @param stepNumber Test step number, 1 or 2
        @param vic Video identification code
        @param samplingRate L-PCM sampling rate in Hz
        @param maxChannels maximum number of audio channels
        @param callbackforSS Callback function to do source setup
        @param testParameters TLqdTestParameters
        @return TLqdResult"""

        cmd = 'ct 7-30 -i' + str(stepNumber) + ' -v' + str(vic) + ' -s' + \
              str(samplingRate) + ' -m' + str(maxChannels)
        return self.runTest(cmd, testParameters, callbackforSS)

    def run7_31(self, stepNumber, vic, callbackforSS=False, testParameters=None):

        """Execute HDMI 1.4 source test 7-31

        This test verifies that the source transmits an Audio InfoFrame whenever
        required and that the contents are valid

        There are two steps for this test:
            - stepNumber=1: Verifies 2 L-PCM channels for VIC 2 or 3
            - stepNumber=2: Verifies 3 or more channels

        @param self the TLqdInstrument object
        @param stepNumber Test step number, 1 or 2
        @param vic Video identification code
        @param callbackforSS Callback function to do source setup
        @param testParameters TLqdTestParameters
        @return TLqdResult"""

        cmd = 'ct 7-31 -i' + str(stepNumber) + ' -v' + str(vic)
        return self.runTest(cmd, testParameters, callbackforSS)

    def run7_32(self, stepNumber, callbackforSS, testParameters=None):

        """Execute HDMI 1.4 source test 7-32

        This test verifies that the source transmits audio using the permitted
        Layout type

        There are two steps for this test:
            - stepNumber=1: Verifies 2 L-PCM channels
            - stepNumber=2: Verifies 3 or more channels

        @param self the TLqdInstrument object
        @param stepNumber Test step number, 1 or 2
        @param callbackforSS Callback function to do source setup
        @param testParameters TLqdTestParameters
        @return TLqdResult"""

        cmd = 'ct 7-32 -i' + str(stepNumber)
        return self.runTest(cmd, testParameters, callbackforSS)

    def run7_33(self, stepNumber, callbackforSS=False, testParameters=None):

        """Execute HDMI 1.4 source test 7-33

        This test verifies that the source never outputs a Video Guard Band or
        Data Island to a device without an HDMI VSDB

        There are five steps for this test:
            - stepNumber=1: Verifies DVI
            - stepNumber=2: Verifies HDMI with a VSDB=5
            - stepNumber=3: Verifies HDMI with a VSDB>5
            - stepNumber=4: Verifies DVI with a 4-block EDID
            - stepNumber=5: Verifies HDMI with a 4-block EDID

        @param self the TLqdInstrument object
        @param stepNumber Test step number, 1-5
        @param callbackforSS Callback function to do source setup
        @param testParameters TLqdTestParameters
        @return TLqdResult"""

        cmd = 'ct 7-33 -i' + str(stepNumber)
        return self.runTest(cmd, testParameters, callbackforSS)

    def run7_33a(self, callbackforSS=False, testParameters=None):

        """Execute HDMI 1.4 source test 7-33a

        This test verifies that the source outputs Video Guard Bands and
        Data Islands to a device with multiple HDMI VSDBs

        @param self the TLqdInstrument object
        @param callbackforSS Callback function to do source setup
        @param testParameters TLqdTestParameters
        @return TLqdResult"""

        return self.runTest('ct 7-33a', testParameters, callbackforSS)

    def run7_34(self, vic, bitDepth, callbackforSS=False, testParameters=None):

        """Execute HDMI 1.4 source test 7-34

        This test verifies that a Deep Color-capable Source DUT outputs correct
        Deep Color packing and signaling

        @param self the TLqdInstrument object
        @param vic Video Identification code
        @param bitDepth Number of bits/color (only 12-bit is supported)
        @param callbackforSS Callback function to do source setup
        @param testParameters TLqdTestParameters
        @return TLqdResult"""

        cmd = 'ct 7-34 -v' + str(vic) + ' -n' + str(bitDepth)
        return self.runTest(cmd, testParameters, callbackforSS)

    def run7_35(self, callbackforSS=False, testParameters=None):

        """Execute HDMI 1.4 source test 7-35

        This test verifies that an xvYCC-capable Source outputs valid
        Gamma Metadata Packets

        @param self the TLqdInstrument object
        @param callbackforSS Callback function to do source setup
        @param testParameters TLqdTestParameters
        @return TLqdResult"""

        return self.runTest('ct 7-35', testParameters, callbackforSS)

    def run7_36(self, stepNumber, callbackforSS=False, testParameters=None):

        """Execute HDMI 1.4 source test 7-36

        This test verifies that a High-Bitrate Audio-capable source is able to
        transmit High-Bitrate Audio Stream Packets with packet jitter limited
        to compliant values

        There are two steps for this test:
            - stepNumber=1: Verifies Dolby TrueHD
            - stepNumber=2: Verifies DTS-HD MA

        @param self the TLqdInstrument object
        @param stepNumber Test step number, 1-2
        @param callbackforSS Callback function to do source setup
        @param testParameters TLqdTestParameters
        @return TLqdResult"""

        cmd = 'ct 7-36 -i' + str(stepNumber)
        return self.runTest(cmd, testParameters, callbackforSS)

    def run7_37(self, callbackforSS=False, testParameters=None):

        """Execute HDMI 1.4 source test 7-37

        This test verifies that a One Bit Audio-capable source is able to
        transmit One Bit Audio Packets in a compliant manner

        @param self the TLqdInstrument object
        @param callbackforSS Callback function to do source setup
        @param testParameters TLqdTestParameters
        @return TLqdResult"""

        return self.runTest('ct 7-37', testParameters, callbackforSS)

    def run7_38(self, vic, threeD, callback, callbackforSS=False, testParameters=None):

        """Execute HDMI 1.4 source test 7-38

        This test verifies that a Source DUT, whenever transmitting a supported
        mandatory 3D video format or other primary 3D video format, complies
        with all required pixel and line counts and pixel clock frequency range

        @param self the TLqdInstrument object
        @param vic Video Identification Code
        @param threeD 3D option, None, 'F', 'T' or 'S'
        @param callback Optional callback function to verify bitmap image
        @param callbackforSS Callback function to do source setup
        @param testParameters TLqdTestParameters
        @return TLqdResult"""

        cmd = 'ct 7-38 -v' + str(vic)
        if threeD:
            cmd = cmd + ' -3' + str(threeD)
        if callback:
            cmd = cmd + ' -V'
        ret = self.runTest(cmd, testParameters, callbackforSS)
        if callback:
            ret = self.imageCallback(callback, ret)
        return ret

    def run7_39(self, hdmiVic, callback, callbackforSS=False, testParameters=None):

        """Execute HDMI 1.4 source test 7-39

        This test verifies that a Source DUT, whenever transmitting any 4K x 2K
        video format, complies with all required pixel and line counts and pixel
        clock frequency range

        @param self the TLqdInstrument object
        @param hdmiVic HDMI Video Identification Code
        @param callback Callback function to verify bitmap image
        @param callbackforSS Callback function to do source setup
        @param testParameters TLqdTestParameters
        @return TLqdResult"""

        cmd = 'ct 7-39 -v' + str(hdmiVic)
        ret = self.runTest(cmd, testParameters, callbackforSS)
        return self.imageCallback(callback, ret)

    def run7_40(self, stepNumber, callbackforSS=False, testParameters=None):

        """Execute HDMI 1.4 source test 7-40

        This test verifies that (a) Source does not transmit sYCC601 or
        opYCC601 or opRGB to a Sink which does not support these Colorimetries

        There are three steps for this test:
            - stepNumber=1: Verifies sYCC601
            - stepNumber=2: Verifies opYCC601
            - stepNumber=3: Verifies opRGB

        @param self the TLqdInstrument object
        @param stepNumber Test step number, 1-3
        @param callbackforSS Callback function to do source setup
        @param testParameters TLqdTestParameters
        @return TLqdResult"""

        cmd = 'ct 7-40 -i' + str(stepNumber)
        return self.runTest(cmd, testParameters, callbackforSS)

    def runHf1_10(self, stepNumber, callbackforSS=False, testParameters=None):

        """Execute HDMI source test HF1-10

        This test verifies that the source writes the correct clock ratio via
        SCDC according to the expected TMDS character rates

        There are two steps for this test:
            - stepNumber=1: Verifies that the DUT sets the clock ratio to 1/40
            - stepNumber=2: Verifies that the DUT sets the clock ratio to 1/10

        The first step of the test requires a video timing > 340Mcsc.

        The second step of the test requires one of these video timings from
        the DUT:
            - 640x480p
            - 720x480p
            - 720x576p

        @param self the TLqdInstrument object
        @param stepNumber Test step number, 1 or 2
        @param callbackforSS Callback function to do source setup
        @param testParameters TLqdTestParameters
        @return TLqdResult"""

        return self.runTest('ct HF1-10 -i'+str(stepNumber), testParameters, callbackforSS)

    def runHf1_11(self, callbackforSS=False, testParameters=None):

        """Execute HDMI source test HF1-11

        This test verifies legal 10-bit codes for 2160p video formats with a
        TMDS character rate above 340Mcsc.

        The test will verify that it is receiving a 2160p format and a TMDS
        character rate above 340Mcsc before performing a capture.

        @param self the TLqdInstrument object
        @param callbackforSS Callback function to do source setup
        @param testParameters TLqdTestParameters
        @return TLqdResult"""

        return self.runTest('ct HF1-11', testParameters, callbackforSS)

    def runHf1_12(self, callbackforSS=False, testParameters=None):

        """Execute HDMI source test HF1-12

        This test verifies code sequences for Control Periods, Data Island
        Periods and Video Data Periods for 2160p video formats with a TMDS
        character rate above 340Mcsc.

        The test will verify that it is receiving a 2160p format and a TMDS
        character rate above 340Mcsc before performing a capture.

        @param self the TLqdInstrument object
        @param callbackforSS Callback function to do source setup
        @param testParameters TLqdTestParameters
        @return TLqdResult"""

        return self.runTest('ct HF1-12', testParameters, callbackforSS)

    def runHf1_13(self, stepNumber, callbackforSS=False, testParameters=None):

        """Execute HDMI source test HF1-13

        This test verifies that the source enables or disables scrambling
        according to the scrambling capability set by the TE for character
        rates at or below 340Mcsc.

        The test requires one of these video timings from the DUT:
            - 720x480p 59.94/60
            - 720x576p 50

        There are two steps for this test:
            - stepNumber=1: Verifies that the DUT performs scrambling
            - stepNumber=2: Verifies that the DUT does *not* scramble

        Step 2 will ignore the omitHp parameter

        @param self the TLqdInstrument object
        @param stepNumber Test step number, 1 or 2
        @param callbackforSS Callback function to do source setup
        @param testParameters TLqdTestParameters
        @return TLqdResult"""

        return self.runTest('ct HF1-13 -i'+str(stepNumber), testParameters, callbackforSS)

    def runHf1_14(self, vic, callbackforSS=False, testParameters=None):

        """Execute HDMI source test HF1-14

        This test verifies pixel and line counts for 2160p formats.

        The test requires a VIC and is expected to be one of: 96, 97, 101, 102,
        106 or 107

        @param self the TLqdInstrument object
        @param vic Video identification code
        @param callbackforSS Callback function to do source setup
        @param testParameters TLqdTestParameters
        @return TLqdResult"""

        return self.runTest('ct HF1-14 -v'+str(vic), testParameters, callbackforSS)

    def runHf1_15(self, vic, bitDepth, stepNumber, callbackforSS=False,
                  testParameters=None):

        """Execute HDMI source test HF1-15

        This test verifies deep color 2160p video formats for character rates
        above 340Mcsc.

        There are two parts to this test:
            - Step 1: Verify that the DUT sends a deep-color format for the
            given VIC and color depth
            - Step 2: Verify that the DUT repects the EDID and does *not*
            send a 12-bit format. This step will always generate a hot-plug

        The test requires a VIC for step 1 and is expected to be one of: 93,
        94, 95, 98, 99, 100, 103, 104 or 105

        The test requires a bit depth to be specified for step 1: 10 or 12

        @param self the TLqdInstrument object
        @param vic Video identification code
        @param stepNumber Test step number, 1 or 2
        @param bitDepth Bit depth, 10 or 12
        @param callbackforSS Callback function to do source setup
        @param testParameters TLqdTestParameters
        @return TLqdResult"""

        cmd = 'ct HF1-15 -v' + str(vic) + ' -i' + str(stepNumber)
        cmd = cmd + ' -n' + str(bitDepth)
        return self.runTest(cmd, testParameters, callbackforSS)

    def runHf1_16(self, vic, threeD, callbackforSS=False, testParameters=None):

        """Execute HDMI source test HF1-16

        This test verifies 3D 2160p formats for character rates above 340Mcsc.

        The test requires a VIC and is expected to range from 93-102

        The test requires a 3D format to be specified:
            - F: Frame packing
            - T: Top/bottom
            - S: Side-by-side (half)

        @param self the TLqdInstrument object
        @param vic Video identification code
        @param threeD 3D option, F, T or S
        @param callbackforSS Callback function to do source setup
        @param testParameters TLqdTestParameters
        @return TLqdResult"""

        return self.runTest('ct HF1-16 -v' + str(vic) + ' -3' + str(threeD),
                            testParameters, callbackforSS)

    def runHf1_17(self, callbackforSS=False, testParameters=None):

        """Execute HDMI source test HF1-17

        This test verifies the DUT reads the Sink's RR_Capable bit before
        enabling the SCDC Read Request feature.

        @param self the TLqdInstrument object
        @param callbackforSS Callback function to do source setup
        @param testParameters TLqdTestParameters
        @return TLqdResult"""

        return self.runTest('ct HF1-17', testParameters, callbackforSS)

    def runHf1_18(self, vic, bitDepth=None, threeD=None, bt2020=None,
                  callbackforSS=False, testParameters=None):

        """Execute HDMI source test HF1-18

        This test verifies AVI infoframes and GCP packets for 2160p video
        formats with a TMDS character rate above 340Mcsc.

        This test can verify:

        - 8-bit formats, such as VIC 96.
            - Required arguments:
                - vic: The expected VIC
        - 10- or 12-bit deep color formats such as VIC 93.
            - Required arguments:
                - vic: The expected VIC
                - bitDepth: 10 or 12
        - 3D formats such as frame packing with VIC 94.
            - Required arguments:
                - vic: The expected VIC
                - threeD:
                    - F: Frame packing
                    - S: Side-by-side
                    - T: Top-bottom
        - ITU-R BT.2020 cYCC and RGB/YCC colorimetry.
            - Required arguments:
                - vic: The expected VIC
                - bt2020:
                    - 0: No BT.2020 colorimetry permitted
                    - 1: BT.2020 cYCC colorimetry expected
                    - 2: BT.2020 RGB or YCC colorimetry expected

        @param self the TLqdInstrument object
        @param vic Video identification code
        @param bitDepth Bit depth, None, 10 or 12
        @param threeD 3D option, None, F, T or S
        @param bt2020 BT.2020 option, None, 0, 1 or 2
        @param callbackforSS Callback function to do source setup
        @param testParameters TLqdTestParameters
        @return TLqdResult"""

        cmd = 'ct HF1-18 -v' + str(vic)
        if bitDepth:
            cmd = cmd + ' -n' + str(bitDepth)
        if threeD:
            cmd = cmd + ' -3' + str(threeD)
        return self.runTest(cmd, testParameters, callbackforSS)

    def runHf1_20(self,  callbackforSS=False, testParameters=None):

        """Execute HDMI source test HF1-20

        This test verifies the DUT reads the Sink's SCDC Update Flag

        @param self the TLqdInstrument object
        @param callbackforSS Callback function to do source setup
        @param testParameters TLqdTestParameters
        @return TLqdResult"""

        return self.runTest('ct HF1-20', testParameters, callbackforSS)

    def runHf1_21(self, callbackforSS=False, testParameters=None):

        """Execute HDMI source test HF1-21

        This test verifies legal 10-bit codes for non-2160p video formats with a
        TMDS character rate above 340Mcsc.

        The test will verify that it is receiving a non-2160p format and a TMDS
        character rate above 340Mcsc before performing a capture.

        @param self the TLqdInstrument object
        @param callbackforSS Callback function to do source setup
        @param testParameters TLqdTestParameters
        @return TLqdResult"""

        return self.runTest('ct HF1-21', testParameters, callbackforSS)

    def runHf1_22(self, callbackforSS=False, testParameters=None):

        """Execute HDMI source test HF1-22

        This test verifies code sequences for Control Periods, Data Island
        Periods and Video Data Periods for non-2160p video formats with a TMDS
        character rate above 340Mcsc.

        The test will verify that it is receiving a non-2160p format and a TMDS
        character rate above 340Mcsc before performing a capture.

        @param self the TLqdInstrument object
        @param callbackforSS Callback function to do source setup
        @param testParameters TLqdTestParameters
        @return TLqdResult"""

        return self.runTest('ct HF1-22', testParameters, callbackforSS)

    def runHf1_23(self, callbackforSS=False, testParameters=None):

        """Execute HDMI source test HF1-23

        This test verifies the DUT delays DDC transactions with sinks that use
        clock stretching.

        @param self the TLqdInstrument object
        @param callbackforSS Callback function to do source setup
        @param testParameters TLqdTestParameters
        @return TLqdResult"""

        return self.runTest('ct HF1-23', testParameters, callbackforSS)

    def runHf1_24(self, vic, callbackforSS=False, testParameters=None):

        """Execute HDMI source test HF1-24

        This test verifies pixel and line counts for non-2160p formats.

        The test requires a VIC to be provided.

        The test will verify that it is receiving a non-2160p format and a TMDS
        character rate above 340Mcsc before performing a capture.

        @param self the TLqdInstrument object
        @param vic Video identification code
        @param callbackforSS Callback function to do source setup
        @param testParameters TLqdTestParameters
        @return TLqdResult"""

        return self.runTest('ct HF1-24 -v' + str(vic), testParameters, callbackforSS)

    def runHf1_25(self, vic, stepNumber, bitDepth, callbackforSS=False, testParameters=None):

        """Execute HDMI source test HF1-25

        This test verifies deep color non-2160p video formats for character
        rates above 340Mcsc.

        There are two parts to this test:
            - Step 1: Verify that the DUT sends a deep-color format for the
            given VIC and color depth
            - Step 2: Verify that the DUT repects the EDID and does *not*
            send a 12-bit format. This step will always generate a hot-plug

        The test requires a non-2160p VIC for step 1.

        The test requires a bit depth to be specified for step 1: 10 or 12

        @param self the TLqdInstrument object
        @param vic Video identification code
        @param stepNumber Test step number, 1 or 2
        @param bitDepth Bit depth, 10 or 12
        @param callbackforSS Callback function to do source setup
        @param testParameters TLqdTestParameters
        @return TLqdResult"""

        cmd = 'ct HF1-25 -v' + str(vic) + ' -i' + str(stepNumber)
        cmd = cmd + ' -n' + str(bitDepth)
        return self.runTest(cmd, testParameters, callbackforSS)

    def runHf1_26(self, vic, threeD, callbackforSS=False, testParameters=None):

        """Execute HDMI source test HF1-26

        This test verifies 3D non-2160p formats for character rates above
        340Mcsc.

        The test requires a non-2160p VIC.

        The test requires a 3D format to be specified:
            - F: Frame packing
            - T: Top/bottom
            - S: Side-by-side (half)

        @param self the TLqdInstrument object
        @param vic Video identification code
        @param threeD 3D option, F, T or S
        @param callbackforSS Callback function to do source setup
        @param testParameters TLqdTestParameters
        @return TLqdResult"""

        return self.runTest('ct HF1-26 -v' + str(vic) + ' -3' + str(threeD),
                            testParameters, callbackforSS)

    def runHf1_27(self, callbackforSS=False, testParameters=None):

        """Execute HDMI source test HF1-27

        This test verifies the DUT reads the sink's RR_Capable bit before
        enabling the SCDC Read Request feature.

        @param self the TLqdInstrument object
        @param callbackforSS Callback function to do source setup
        @param testParameters TLqdTestParameters
        @return TLqdResult"""

        return self.runTest('ct HF1-27', testParameters, callbackforSS)

    def runHf1_28(self, vic, bitDepth=None, threeD=None, bt2020=None,
                  callbackforSS=False, testParameters=None):

        """Execute HDMI source test HF1-28

        This test verifies AVI infoframes and GCP packets for non-2160p video
        formats with a TMDS character rate above 340Mcsc.

        This test can verify:

        - 8-bit formats, such as VIC 91.
            - Required arguments:
                - vic: The expected VIC
        - 10- or 12-bit deep color formats such as VIC 63.
            - Required arguments:
                - vic: The expected VIC
                - bitDepth: 10 or 12
        - 3D formats such as frame packing with VIC 64.
            - Required arguments:
                - vic: The expected VIC
                - threeD:
                    - F: Frame packing
                    - S: Side-by-side
                    - T: Top-bottom
        - ITU-R BT.2020 cYCC and RGB/YCC colorimetry.
            - Required arguments:
                - vic: The expected VIC
                - bt2020:
                    - 0: No BT.2020 colorimetry permitted
                    - 1: BT.2020 cYCC colorimetry expected
                    - 2: BT.2020 RGB or YCC colorimetry expected

        @param self the TLqdInstrument object
        @param vic Video identification code
        @param bitDepth Bit depth, None, 10 or 12
        @param threeD 3D option, None, F, T or S
        @param bt2020 BT.2020 option, None, 0, 1 or 2
        @param callbackforSS Callback function to do source setup
        @param testParameters TLqdTestParameters
        @return TLqdResult"""

        cmd = 'ct HF1-28 -v' + str(vic)
        if bitDepth:
            cmd = cmd + ' -n' + str(bitDepth)
        if threeD:
            cmd = cmd + ' -3' + str(threeD)
        return self.runTest(cmd, testParameters, callbackforSS)

    def runHf1_29(self, callbackforSS=False, testParameters=None):

        """Execute HDMI source test HF1-29

        This test verifies the DUT reads all 7 bytes of the error count
        registers and checksum in a single SCDC transaction.

        @param self the TLqdInstrument object
        @param callbackforSS Callback function to do source setup
        @param testParameters TLqdTestParameters
        @return TLqdResult"""

        return self.runTest('ct HF1-29', testParameters, callbackforSS)

    def runHf1_31v(self, vic, callback, supportsTestImage=False,
                    callbackforSS=False, testParameters=None):

        """Execute HDMI source test HF1-31 with a visual check

        This test verifies 2160p YCbCr 4:2:0 video formats for character
        rates below 340Mcsc.

        Verifies that the DUT sends a YCbCr 4:2:0 format (with or without the
        GCTS test image) for the given VIC

        @param self the TLqdInstrument object
        @param vic Video identification code
        @param callback Callback function to verify bitmap image
        @param supportsTestImage Indicates the DUT supports the test image
        @param callbackforSS Callback function to do source setup
        @param testParameters TLqdTestParameters
        @return TLqdResult"""

        cmd = 'ct HF1-31 -V -i1'
        if supportsTestImage:
            cmd = cmd + ' -T'
        cmd = cmd + ' -v' + str(vic)
        ret = self.runTest(cmd, testParameters, callbackforSS)
        if callback:
            ret = self.imageCallback(callback, ret)
        return ret

    def runHf1_31(self, vic, stepNumber,  callbackforSS=False, testParameters=None):

        """Execute HDMI source test HF1-31

        This test verifies 2160p YCbCr 4:2:0 video formats for character
        rates below 340Mcsc.

        There are two parts to this test:
            - Step 1: Verify that the DUT sends a YCbCr 4:2:0 format for the
            given VIC
            - Step 2: Verify that the DUT repects the EDID and does *not*
            send a YCbCr 4:2:0 format. This step will always generate a hot-plug

        The test requires a 2160p VIC for step 1.

        The test requires a step number to be specified: 1 or 2

        @param self the TLqdInstrument object
        @param vic Video identification code
        @param stepNumber Test step number, 1 or 2
        @param callbackforSS Callback function to do source setup
        @param testParameters TLqdTestParameters
        @return TLqdResult"""

        return self.runTest('ct HF1-31 -v' + str(vic) + ' -i' + str(stepNumber),
                            testParameters, callbackforSS)

    def runHf1_32v(self, vic, bitDepth, callback, supportsTestImage,
                   callbackforSS=False, testParameters=None):

        """Execute HDMI source test HF1-32

        This test verifies 2160p YCbCr 4:2:0 deep color video formats for
        character rates above 340Mcsc.

        Verifies that the DUT sends a YCbCr 4:2:0 deep color format for the
        given VIC with a visual check

        The test requires a bit depth: 10 or 12

        @param self the TLqdInstrument object
        @param vic Video identification code
        @param bitDepth Bit depth, 10 or 12
        @param callback Callback function to verify bitmap image
        @param supportsTestImage Indicates the DUT supports the test image
        @param callbackforSS Callback function to do source setup
        @param testParameters TLqdTestParameters
        @return TLqdResult"""

        cmd = 'ct HF1-32 -V -i1'
        if supportsTestImage:
            cmd = cmd + ' -T'
        cmd = cmd + ' -v' + str(vic) + ' -n' + str(bitDepth)
        ret = self.runTest(cmd, testParameters, callbackforSS)
        if callback:
            ret = self.imageCallback(callback, ret)
        return ret

    def runHf1_32(self, vic, stepNumber, bitDepth, callbackforSS=False,
                  testParameters=None):

        """Execute HDMI source test HF1-32

        This test verifies 2160p YCbCr 4:2:0 deep color video formats for
        character rates above 340Mcsc.

        There are two parts to this test:
            - Step 1: Verify that the DUT sends a YCbCr 4:2:0 deep color format
            for the given VIC
            - Step 2: Verify that the DUT repects the EDID and does *not*
            send a YCbCr 4:2:0 deep color format. This step will always
            generate a hot-plug

        The test requires a 2160p VIC for step 1.

        The test requires a bit depth for step 1: 10 or 12

        The test requires a step number to be specified: 1 or 2

        @param self the TLqdInstrument object
        @param vic Video identification code
        @param stepNumber Test step number, 1 or 2
        @param bitDepth Bit depth, 10 or 12
        @param callbackforSS Callback function to do source setup
        @param testParameters TLqdTestParameters
        @return TLqdResult"""

        cmd = 'ct HF1-32 -v' + str(vic) + ' -i' + str(stepNumber)
        cmd = cmd + ' -n' + str(bitDepth)
        return self.runTest(cmd, testParameters, callbackforSS)

    def runHf1_33(self, vic, callbackforSS=False, testParameters=None):

        """Execute HDMI source test HF1-33

        This test verifies timings for 2160p YCbCr 4:2:0 video formats for
        character rates below 340Mcsc.

        The test requires a 2160p VIC.

        @param self the TLqdInstrument object
        @param vic Video identification code
        @param callbackforSS Callback function to do source setup
        @param testParameters TLqdTestParameters
        @return TLqdResult"""

        return self.runTest('ct HF1-33 -v' + str(vic), testParameters,
                            callbackforSS)

    def runHf1_34(self, vic, bitDepth, callbackforSS=False, testParameters=None):

        """Execute HDMI source test HF1-34

        This test verifies 2160p YCbCr 4:2:0 deep color video formats for
        character rates above 340Mcsc.

        The test requires a 2160p VIC.

        The test requires a bit depth: 10 or 12

        @param self the TLqdInstrument object
        @param vic Video identification code
        @param bitDepth Bit depth, 10 or 12
        @param callbackforSS Callback function to do source setup
        @param testParameters TLqdTestParameters
        @return TLqdResult"""

        return self.runTest('ct HF1-34 -v' + str(vic) + ' -n' + str(bitDepth),
                            testParameters, callbackforSS)

    def runHf1_35v(self, vic, callback, callbackforSS=False, testParameters=None):

        """Execute HDMI source test HF1-35

        This test verifies wide (21:9 or 64:27 pixel ratio) video formats with
        a visual check

        The test requires a wide format VIC.

        @param self the TLqdInstrument object
        @param vic Video identification code
        @param callback Callback function to verify bitmap image
        @param callbackforSS Callback function to do source setup
        @param testParameters TLqdTestParameters
        @return TLqdResult"""

        ret = self.runTest('ct HF1-35 -V -v' + str(vic), testParameters,
                           callbackforSS)
        if callback:
            ret = self.imageCallback(callback, ret)
        return ret

    def runHf1_35(self, vic, callbackforSS=False, testParameters=None):

        """Execute HDMI source test HF1-35

        This test verifies wide (21:9 or 64:27 pixel ratio) video formats

        The test requires a wide format VIC.

        @param self the TLqdInstrument object
        @param vic Video identification code
        @param callbackforSS Callback function to do source setup
        @param testParameters TLqdTestParameters
        @return TLqdResult"""

        return self.runTest('ct HF1-35 -v' + str(vic), testParameters,
                            callbackforSS)

    def runHf1_41(self, callbackforSS=False, testParameters=None):

        """Execute HDMI source test HF1-41

        This test verifies 3D audio from the DUT

        @param self the TLqdInstrument object
        @param callbackforSS Callback function to do source setup
        @param testParameters TLqdTestParameters
        @return TLqdResult"""

        return self.runRequireHpTest('ct HF1-41', testParameters, callbackforSS)

    def runHf1_43(self, callbackforSS=False, testParameters=None):

        """Execute HDMI source test HF1-43

        This test verifies high bit rate (HBR) audio from the DUT

        @param self the TLqdInstrument object
        @param callbackforSS Callback function to do source setup
        @param testParameters TLqdTestParameters
        @return TLqdResult"""

        return self.runRequireHpTest('ct HF1-43', testParameters, callbackforSS)

    def runHf1_44(self, callbackforSS=False, testParameters=None):

        """Execute HDMI source test HF1-44

        This test verifies One Bit 3D or One Bit Multi-stream audio from the DUT

        @param self the TLqdInstrument object
        @param callbackforSS Callback function to do source setup
        @param testParameters TLqdTestParameters
        @return TLqdResult"""

        return self.runRequireHpTest('ct HF1-44', testParameters, callbackforSS)

    def runHf1_45(self, callbackforSS=False, testParameters=None):

        """Execute HDMI source test HF1-45

        This test verifies L-PCM or IEC 61937 compressed audio from the DUT

        @param self the TLqdInstrument object
        @param callbackforSS Callback function to do source setup
        @param testParameters TLqdTestParameters
        @return TLqdResult"""

        return self.runRequireHpTest('ct HF1-45', testParameters, callbackforSS)

    def runHf1_47(self, stepNumber, callbackforSS=False, testParameters=None):

        """Execute HDMI source test HF1-47

        This test verifies 3D video formats with OSD Disparity and that the DUT
        follows the Colorimetry Data Block in the EDID.

        There are three parts to this test:
            - Step 1: Verify that the DUT does *not* transmit a 3D format
            - Step 2: Verify that the DUT follows the EDID and transmits a 3D
                format, but no OSD Disparity
            - Step 3: Verify that the DUT follows the EDID and transmits a 3D
                format, with OSD Disparity

        @param self the TLqdInstrument object
        @param stepNumber Test step number, 1 - 3
        @param callbackforSS Callback function to do source setup
        @param testParameters TLqdTestParameters
        @return TLqdResult"""

        cmd = 'ct HF1-47 -i' + str(stepNumber)
        return self.runRequireHpTest(cmd, testParameters, callbackforSS)

    def runHf1_48(self, stepNumber, callbackforSS=False, testParameters=None):

        """Execute HDMI source test HF1-48

        This test verifies 3D video formats with Dual View

        There are two parts to this test:
            - Step 1: Verify that the DUT transmits a Dual View image and
                uses the HDMI Forum InfoFrame
            - Step 2: The DUT needs to switch from Dual View to a 2D format
                while the test is running. The test allows for up to 45 seconds
                for the DUT to switch modes. The DUT is not allowed to restart
                the video signal and there can be no loss of sync.

        @param self the TLqdInstrument object
        @param stepNumber Test step number, 1 - 2
        @param callbackforSS Callback function to do source setup
        @param testParameters TLqdTestParameters
        @return TLqdResult"""

        cmd = 'ct HF1-48 -i' + str(stepNumber)
        return self.runTest(cmd, testParameters, callbackforSS)

    def runHf1_49(self, stepNumber, callbackforSS=False, testParameters=None):

        """Execute HDMI source test HF1-49

        This test verifies 3D video formats with Independent View

        There are two parts to this test:
            - Step 1: Verify that the DUT transmits an Independent View image
                and uses the HDMI Forum InfoFrame
            - Step 2: The DUT needs to switch from Independent View to a 2D
                format while the test is running. The test allows for up to 45
                seconds for the DUT to switch modes. The DUT is not allowed to
                restart the video signal and there can be no loss of sync.

        @param self the TLqdInstrument object
        @param stepNumber Test step number, 1 - 2
        @param callbackforSS Callback function to do source setup
        @param testParameters TLqdTestParameters
        @return TLqdResult"""

        cmd = 'ct HF1-49 -i' + str(stepNumber)
        return self.runTest(cmd, testParameters, callbackforSS)

    def runHf1_51(self, vic, stepNumber, callbackforSS=False, testParameters=None):

        """Execute HDMI source test HF1-51

        This test verifies YCbCr 4:2:0 2160p video formats and that the DUT
        follows the Y420 Video Data Block and/or the YCbCr 4:2:0 Capabilites
        Map Data Block in the EDID.

        There are four parts to this test:
            - Step 1: Verify that the DUT follows the EDID Y420 Video Data Block
            - Step 2: Verify that the DUT follows the EDID YCbCr 4:2:0
                Capabilites Map Data Block
            - Step 3: Verify that the DUT follows the EDID with an empty
                YCbCr 4:2:0 Capabilites Map Data Block
            - Step 4: Verify that the DUT does not transmit YCbCr 4:2:0 based
                on the EDID data

        The test requires a 2160p VIC: 96, 97, 101, 102, 106 or 107

        @param self the TLqdInstrument object
        @param vic Video identification code
        @param stepNumber Test step number, 1 - 4
        @param callbackforSS Callback function to do source setup
        @param testParameters TLqdTestParameters
        @return TLqdResult"""

        cmd = 'ct HF1-51 -v' + str(vic) + ' -i' + str(stepNumber)
        return self.runTest(cmd, testParameters, callbackforSS)

    def runHf1_52(self, stepNumber, callbackforSS=False, testParameters=None):

        """Execute HDMI source test HF1-52

        This test verifies YCbCr 4:2:0 BT.2020 video formats and that the DUT
        follows the Colorimetry Data Block in the EDID.

        There are four parts to this test:
            - Step 1: Verify that the DUT transmits BT.2020 YCC
            - Step 2: Verify that the DUT follows the EDID and does *not*
                transmit BT.2020 YCC
            - Step 3: Verify that the DUT transmits BT.2020 cYCC
            - Step 4: Verify that the DUT follows the EDID and does *not*
                transmit BT.2020 cYCC

        @param self the TLqdInstrument object
        @param stepNumber Test step number, 1 - 4
        @param callbackforSS Callback function to do source setup
        @param testParameters TLqdTestParameters
        @return TLqdResult"""

        cmd = 'ct HF1-52 -i' + str(stepNumber)
        return self.runRequireHpTest(cmd, testParameters, callbackforSS)

    def runHf1_53(self, stepNumber, callbackforSS=False, testParameters=None):

        """Execute HDMI source test HF1-53

        This test verifies that the Source DUT sends the Dynamic Range and
        Mastering InfoFrame when it is sending HDR content

        There are eleven parts to this test:
            - Step 1: Verify that the DUT transmits DRM with traditional SDR
            - Step 2: Verify that the DUT transmits DRM with traditional HDR
            - Step 3: Verify that the DUT transmits DRM with SMPTE ST.2084
            - Step 4: Verify that the DUT transmits DRM with HLG
            - Step 5: Verify that the DUT properly switches from DRM with
                traditional SDR to SDR without DRM
            - Step 6: Verify that the DUT properly switches from DRM with
                traditional HDR to SDR without DRM
            - Step 7: Verify that the DUT properly switches from DRM with
                SMPTE ST.2084 to SDR without DRM
            - Step 8: Verify that the DUT properly switches from DRM with HLG
                to SDR without DRM
            - Step 9: Verify that the DUT does not transmit DRM with traditional
                HDR when the EDID does not support HDR
            - Step 10: Verify that the DUT does not transmit DRM with SMPTE
                ST.2084 when the EDID does not support SMPTE ST.2084
            - Step 11: Verify that the DUT does not transmit DRM with HLG
                when the EDID does not support HLG

        @param self the TLqdInstrument object
        @param stepNumber Test step number, 1 - 11
        @param callbackforSS Callback function to do source setup
        @param testParameters TLqdTestParameters
        @return TLqdResult"""

        cmd = 'ct HF1-53 -i' + str(stepNumber)
        return self.runRequireHpTest(cmd, testParameters, callbackforSS)

    def runHf1_57(self, stepNumber, fvaTiming=None,
                  callbackforSS=False, testParameters=None):

        """Execute HDMI source test HF1-57

        @param self the TLqdInstrument object
        @param stepNumber Test step number, 1 - 6
        @param callback Callback function to do source setup
        @param fvaTiming Fva timing structure.
            "HorizontalxVertical-BRR*Range"
            where Range can be 2FFMAX (all), FF#, or FF#-#.
            example: 1920x1080-60*2FFMAX
        @param callbackforSS Callback function to do source setup
        @param testParameters TLqdTestParameters
        @return TLqdResult"""

        ret = TLqdResult(TLqdStatus.FAIL, [], [])

        cmd = 'ct HF1-57 -i' + str(stepNumber)
        if fvaTiming:
            cmd = cmd + ' -t ' + str(fvaTiming)
        ret = self.runTest(cmd, testParameters, callbackforSS)
        return ret

    def runHf1_58(self, stepNumber, itFormat=None,
                  callbackforSS=False, testParameters=None):

        """Execute HDMI source test HF1-58

        @param self the TLqdInstrument object
        @param stepNumber Test step number, 1 - 33
        @param callback Callback function to do source setup
        @param itFormat IT format timing structure
            "HorizontalxVertical-RefreshRate-Blanking",
            with Blanking being 0-Standard, 1-Reduced Ver1, 2- Reduced Ver2.
            example: 2560x1440-60-1
        @param callbackforSS Callback function to do source setup
        @param testParameters TLqdTestParameters
        @return TLqdResult"""

        ret = TLqdResult(TLqdStatus.FAIL, [], [])

        cmd = 'ct HF1-58 -i' + str(stepNumber)
        if itFormat:
            cmd = cmd + ' -f ' + str(itFormat)
        ret = self.runTest(cmd, testParameters, callbackforSS)
        return ret

    def runHf1_60(self, stepNumber, fvaTiming=None, itFormat=None,
                  callbackforSS=False, testParameters=None):

        """Execute HDMI source test HF1-60

        @param self the TLqdInstrument object
        @param stepNumber Test step number, 1 - 33
        @param fvaTiming Fva timing structure.
            "HorizontalxVertical-BRR*Range"
            where Range can be 2FFMAX (all), FF#, or FF#-#.
            example: 1920x1080-60*2FFMAX
        @param itFormat IT format timing structure
            "HorizontalxVertical-RefreshRate-Blanking",
            with Blanking being 0-Standard, 1-Reduced Ver1, 2- Reduced Ver2.
            example: 2560x1440-60-1
        @param callbackforSS Callback function to do source setup
        @param testParameters TLqdTestParameters
        @return TLqdResult"""

        ret = TLqdResult(TLqdStatus.FAIL, [], [])

        cmd = 'ct HF1-60 -i' + str(stepNumber)
        if fvaTiming:
            cmd = cmd + ' -t ' + str(fvaTiming)
        if itFormat:
            cmd = cmd + ' -f ' + str(itFormat)

        ret = self.runTest(cmd, testParameters, callbackforSS)
        return ret

    def runHf1_66(self, stepNumber, vic=None,
                  callbackforSS=False, testParameters=None):

        """Execute HDMI source test HF1-66

        @param self the TLqdInstrument object
        @param stepNumber Test step number, 1 - 6
        @param vic Video identification code
        @param callbackforSS Callback function to do source setup
        @param testParameters TLqdTestParameters
        @return TLqdResult"""

        ret = TLqdResult(TLqdStatus.FAIL, [], [])

        cmd = 'ct HF1-66 -i' + str(stepNumber)
        if vic:
            cmd = cmd + ' -v ' + str(vic)
        ret = self.runTest(cmd, testParameters, callbackforSS)
        return ret

    def runHf1_71(self, vic, callbackforSS=False, testParameters=None):

        """Execute HDMI source test HF1-71

        This test verifies that the Source DUT outputs the correct timing for
        YCbCr 4:2:0 timings introduced in the CTA-861-G

        @param self the TLqdInstrument object
        @param vic The CTA-861-G 4:2:0 Video ID code
        @param callbackforSS Callback function to do source setup
        @param testParameters TLqdTestParameters
        @return TLqdResult"""

        cmd = 'ct HF1-71 -v' + str(vic)
        return self.runRequireHpTest(cmd, testParameters, callbackforSS)

    def runHf1_72(self, vic, bitDepth, callbackforSS=False, testParameters=None):

        """Execute HDMI source test HF1-72

        This test verifies that the Source DUT outputs the correct timing for
        YCbCr 4:2:0 Deep Color timings

        @param self the TLqdInstrument object
        @param vic The CTA-861-G 4:2:0 Video ID code
        @param bitDepth Bit depth, 10, 12 or 16
        @param callbackforSS Callback function to do source setup
        @param testParameters TLqdTestParameters
        @return TLqdResult"""

        cmd = 'ct HF1-72 -v' + str(vic) + ' -n' + str(bitDepth)
        return self.runRequireHpTest(cmd, testParameters, callbackforSS)

    def runHf1_74(self, vic, bitDepth, stepNumber=None, callbackforSS=False, testParameters=None):

        """Execute HDMI source test HF1-74

        This test verifies the correct deep color 861G video timing for
        VICs above 107 using TMDS.

        The test requires a VIC and is expected to be one of:
        108, 109, 110, 111, 112, 113, 121, 122 or 123

        The test requires a bit depth to be specified for each VIC

        @param self the TLqdInstrument object
        @param vic Video identification code
        @param bitDepth Bit depth, 10
        @param stepNumber Test step number, 1 - 9
        @param callbackforSS Callback function to do source setup
        @param testParameters TLqdTestParameters
        @return TLqdResult"""

        cmd = 'ct HF1-74 -i' + str(stepNumber)

        if vic:
            cmd = cmd + ' -v ' + str(vic)
        if bitDepth:
            cmd = cmd + ' -n ' + str(bitDepth)

        return self.runTest(cmd, testParameters, callbackforSS)

    def runHf1_75(self, vic, stepNumber=None, callbackforSS=False, testParameters=None):

        """Execute HDMI source test HF1-75

        The test requires a VIC and is expected to be one of: 108, 109, 110, 111,
        112, 113, 114, 115, 116, 121, 122 or 123

        @param self the TLqdInstrument object
        @param vic Video identification code
        @param stepNumber Test step number, 1 - 12
        @param callbackforSS Callback function to do source setup
        @param testParameters TLqdTestParameters
        @return TLqdResult"""

        cmd = 'ct HF1-75 -i' + str(stepNumber)
        if vic:
            cmd = cmd + ' -v ' + str(vic)

        return self.runTest(cmd, testParameters, callbackforSS)

    def runHfr1_10(self, callbackforSS=False, testParameters=None):

        """Execute FRL source test HFR1-10

        This test verifies that the source DUT supports the required
        FRL Link Training patterns LTP1 through LTP8

        @param self the TLqdInstrument object
        @param callbackforSS Callback function to do source setup
        @param testParameters TLqdTestParameters
        @return TLqdResult"""

        return self.runRequireHpTest('ct HFR1-10', testParameters,
                                     callbackforSS)

    def runHfr1_11(self, stepNumber, callbackforSS=False, testParameters=None):

        """Execute FRL source test HFR1-11

        This test verifies that the source DUT sends legal 18-bit codes.

        There are two parts to this test:
            - Step 1: Verify legal codes for FRL with 3 lanes
            - Step 2: Verify legal codes for FRL with 4 lanes

        @param self the TLqdInstrument object
        @param stepNumber Test step number, 1 - 2
        @param callbackforSS Callback function to do source setup
        @param testParameters TLqdTestParameters
        @return TLqdResult"""

        cmd = 'ct HFR1-11 -i' + str(stepNumber)
        return self.runRequireHpTest(cmd, testParameters, callbackforSS)

    def runHfr1_12(self, callbackforSS=False, testParameters=None):

        """Execute FRL source test HFR1-12

        This test verifies that the source DUT performs FRL link training

        @param self the TLqdInstrument object
        @param callbackforSS Callback function to do source setup
        @param testParameters TLqdTestParameters
        @return TLqdResult"""

        return self.runRequireHpTest('ct HFR1-12', testParameters, callbackforSS)

    def runHfr1_13(self, maxFrlRate=6, callbackforSS=False, testParameters=None):

        """Execute FRL source test HFR1-13

        This test verifies that the source DUT follows the required FRL link
        training process prior to transmitting FRL

        @param self the TLqdInstrument object
        @param maxFrlRate Maximum FRL rate 0-6
        @param callbackforSS Callback function to do source setup
        @param testParameters TLqdTestParameters
        @return TLqdResult"""

        cmd = 'ct HFR1-13 -M' + str(maxFrlRate)
        return self.runRequireHpTest(cmd, testParameters, callbackforSS)

    def runHfr1_14(self, vic, callbackforSS=False, testParameters=None):

        """Execute FRL source test HFR1-14

        This test verifies that the Source DUT supports 24-bit Color Depth
        Video Formats below 2160p when in FRL mode

        @param self the TLqdInstrument object
        @param vic Video ID code
        @param callbackforSS Callback function to do source setup
        @param testParameters TLqdTestParameters
        @return TLqdResult"""

        cmd = 'ct HFR1-14 -v ' + str(vic)
        return self.runRequireHpTest(cmd, testParameters, callbackforSS)

    def runHfr1_15(self, vic, bitDepth=8, callbackforSS=False, testParameters=None):

        """Execute FRL source test HFR1-15

        This test verifies that the Source DUT supports Deep Color Video Formats
        below 2160p when in FRL mode

        @param self the TLqdInstrument object
        @param vic Video ID code
        @param bitDepth Bit depth, 8, 10, 12 or 16
        @param callbackforSS Callback function to do source setup
        @param testParameters TLqdTestParameters
        @return TLqdResult"""

        cmd = 'ct HFR1-15 -n ' + str(bitDepth) + ' -v ' + str(vic)
        return self.runRequireHpTest(cmd, testParameters, callbackforSS)

    def runHfr1_16(self, vic, threeD, callbackforSS=False, testParameters=None):

        """Execute FRL source test HFR1-16

        This test verifies that the Source transmits compliant uncompressed
        2160p 3D Video Formats while in FRL Mode

        The test requires a 3D format to be specified:
            - F: Frame packing
            - T: Top/bottom
            - S: Side-by-side (half)

        @param self the TLqdInstrument object
        @param vic Video ID code for a 2160p format
        @param threeD 3D option, F, T or S
        @param callbackforSS Callback function to do source setup
        @param testParameters TLqdTestParameters
        @return TLqdResult"""

        cmd = 'ct HFR1-16 -v' + str(vic) + ' -3' + str(threeD)
        return self.runRequireHpTest(cmd, testParameters, callbackforSS)

    def runHfr1_17(self, callbackforSS=False, testParameters=None):

        """Execute FRL source test HFR1-17

        This test verifies that the source DUT handles a future value for the
        Max_FRL_Rate

        @param self the TLqdInstrument object
        @param callbackforSS Callback function to do source setup
        @param testParameters TLqdTestParameters
        @return TLqdResult"""

        return self.runRequireHpTest('ct HFR1-17', testParameters, callbackforSS)

    def runHfr1_18(self, vic, bitDepth=None, threeD=None, bt2020=None,
                  callbackforSS=False, testParameters=None):

        """Execute FRL source test HFR1-18

        This test verifies that the Source, whenever transmitting any 2160p
        Video Format that falls within a TMDS Character Rate between 340 Mcsc
        and 600 Mcsc (hereafter referred to as "legacy 2160p") while in FRL
        mode, transmits an accurate AVI InfoFrame at least once per every two
        video fields and appropriate color depth as indicated by GCP

        This test can verify:

        - 8-bit formats, such as VIC 96.
            - Required arguments:
                - vic: The expected VIC
        - 10- or 12-bit deep color formats such as VIC 93.
            - Required arguments:
                - vic: The expected VIC
                - bitDepth: 10 or 12
        - 3D formats such as frame packing with VIC 94.
            - Required arguments:
                - vic: The expected VIC
                - threeD:
                    - F: Frame packing
                    - S: Side-by-side
                    - T: Top-bottom
        - ITU-R BT.2020 cYCC and RGB/YCC colorimetry.
            - Required arguments:
                - vic: The expected VIC
                - bt2020:
                    - 0: No BT.2020 colorimetry permitted
                    - 1: BT.2020 cYCC colorimetry expected
                    - 2: BT.2020 RGB or YCC colorimetry expected

        @param self the TLqdInstrument object
        @param vic Video identification code
        @param bitDepth Bit depth, None, 10 or 12
        @param threeD 3D option, None, F, T or S
        @param bt2020 BT.2020 option, None, 0, 1 or 2
        @param callbackforSS Callback function to do source setup
        @param testParameters TLqdTestParameters
        @return TLqdResult"""

        cmd = 'ct HFR1-18 -v' + str(vic)
        if bitDepth:
            cmd = cmd + ' -n' + str(bitDepth)
        if threeD:
            cmd = cmd + ' -3' + str(threeD)
        return self.runRequireHpTest(cmd, testParameters, callbackforSS)

    def runHfr1_19(self, stepNumber, callbackforSS=False, testParameters=None):

        """Execute FRL source test HFR1-19

        This test verifies that the source DUT sends legal FRL Map Characters.

        There are two parts to this test:
            - Step 1: Verify FRL Map Characters for FRL with 3 lanes
            - Step 2: Verify FRL Map Characters for FRL with 4 lanes

        @param self the TLqdInstrument object
        @param stepNumber Test step number, 1 - 2
        @param callbackforSS Callback function to do source setup
        @param testParameters TLqdTestParameters
        @return TLqdResult"""

        cmd = 'ct HFR1-19 -i' + str(stepNumber)
        return self.runRequireHpTest(cmd, testParameters, callbackforSS)

    def runHfr1_20(self, stepNumber, callbackforSS=False, testParameters=None):

        """Execute FRL source test HFR1-20

        This test verifies that the source DUT sends legal contol periods

        There are two parts to this test:
            - Step 1: Verify FRL legal contol periods for FRL with 3 lanes
            - Step 2: Verify FRL legal contol periods for FRL with 4 lanes

        @param self the TLqdInstrument object
        @param stepNumber Test step number, 1 - 2
        @param callbackforSS Callback function to do source setup
        @param testParameters TLqdTestParameters
        @return TLqdResult"""

        cmd = 'ct HFR1-20 -i' + str(stepNumber)
        return self.runRequireHpTest(cmd, testParameters, callbackforSS)

    def runHfr1_21(self, stepNumber, callbackforSS=False, testParameters=None):

        """Execute FRL source test HFR1-21

        This test verifies that the source DUT only outputs legal Active Video
        FRL Packets

        There are two parts to this test:
            - Step 1: Verify FRL outputs legal Active Video Packets with 3 lanes
            - Step 2: Verify FRL outputs legal Active Video Packets with 4 lanes

        @param self the TLqdInstrument object
        @param stepNumber Test step number, 1 - 2
        @param callbackforSS Callback function to do source setup
        @param testParameters TLqdTestParameters
        @return TLqdResult"""

        cmd = 'ct HFR1-21 -i' + str(stepNumber)
        return self.runRequireHpTest(cmd, testParameters, callbackforSS)

    def runHfr1_22(self, stepNumber, bitDepth=None, callbackforSS=False, testParameters=None):

        """Execute FRL source test HFR1-22

        This test verifies that the source only outputs legal Active Video FRL
        Packets when Compressed Video Transport is active

        There are two parts to this test:
            - Step 1: Verify FRL outputs legal Active Video Packets with 3 lanes
            - Step 2: Verify FRL outputs legal Active Video Packets with 4 lanes

        @param self the TLqdInstrument object
        @param stepNumber Test step number, 1 - 2
        @param bitDepth Bit depth, 8, 10 or 12
        @param callbackforSS Callback function to do source setup
        @param testParameters TLqdTestParameters
        @return TLqdResult"""

        cmd = 'ct HFR1-22 -i' + str(stepNumber)
        if bitDepth is not None and bitDepth > 8:
            cmd = cmd + ' -n' + str(bitDepth)
        return self.runRequireHpTest(cmd, testParameters, callbackforSS)

    def runHfr1_23(self, callbackforSS=False, testParameters=None):

        """Execute FRL source test HFR1-23

        This test verifies that the source DUT packs the FRL Stream with
        compliant Packet Jitter

        @param self the TLqdInstrument object
        @param callbackforSS Callback function to do source setup
        @param testParameters TLqdTestParameters
        @return TLqdResult"""

        return self.runRequireHpTest('ct HFR1-23', testParameters, callbackforSS)

    def runHfr1_24(self, vic, callbackforSS=False, testParameters=None):

        """Execute FRL source test HFR1-24

        This test verifies that the Source DUT supports 24-bit Color Depth
        2160p Video Formats when in FRL mode

        @param self the TLqdInstrument object
        @param vic Video ID code
        @param callbackforSS Callback function to do source setup
        @param testParameters TLqdTestParameters
        @return TLqdResult"""

        cmd = 'ct HFR1-24 -v ' + str(vic)
        return self.runRequireHpTest(cmd, testParameters, callbackforSS)

    def runHfr1_25(self, vic, bitDepth=8, callbackforSS=False, testParameters=None):

        """Execute FRL source test HFR1-25

        This test verifies that the Source DUT supports 2160p Deep Color Video
        Formats when in FRL mode

        @param self the TLqdInstrument object
        @param vic Video ID code
        @param bitDepth Bit depth, 8, 10, 12 or 16
        @param callbackforSS Callback function to do source setup
        @param testParameters TLqdTestParameters
        @return TLqdResult"""

        cmd = 'ct HFR1-25 -n ' + str(bitDepth) + ' -v ' + str(vic)
        return self.runRequireHpTest(cmd, testParameters, callbackforSS)

    def runHfr1_26(self, vic, threeD, callbackforSS=False, testParameters=None):

        """Execute FRL source test HFR1-26

        This test verifies that the Source transmits compliant uncompressed
        non-2160p 3D Video Formats while in FRL Mode

        The test requires a 3D format to be specified:
            - F: Frame packing
            - T: Top/bottom
            - S: Side-by-side (half)

        @param self the TLqdInstrument object
        @param vic Video ID code for a non-2160p format
        @param threeD 3D option, F, T or S
        @param callbackforSS Callback function to do source setup
        @param testParameters TLqdTestParameters
        @return TLqdResult"""

        cmd = 'ct HFR1-26 -v' + str(vic) + ' -3' + str(threeD)
        return self.runRequireHpTest(cmd, testParameters, callbackforSS)

    def runHfr1_27(self, callback, supportsTestImage=False, bitDepth=8,
                   callbackforSS=False, testParameters=None):

        """Execute FRL source test HFR1-27

        This test verifies that a source DUT outputs correct RGB or YCbCr 4:4:4
        deep color pixel encoding and signaling while in FRL Mode. In the case
        where a Source DUT can output a standardized test image, the test
        verifies the proper position of the pixels and the order of the
        color-component data of the test pixels with fully saturated
        (extreme-value) color-components.

        @param self the TLqdInstrument object
        @param callback Callback function to verify bitmap image
        @param supportsTestImage Indicates the DUT supports the test image
        @param bitDepth Bit depth, 8, 10, 12 or 16
        @param callbackforSS Callback function to do source setup
        @param testParameters TLqdTestParameters
        @return TLqdResult"""

        cmd = 'ct HFR1-27'
        if supportsTestImage:
            cmd = cmd + ' -t'
        cmd = cmd + ' -n ' + str(bitDepth)
        ret = self.runRequireHpTest(cmd, testParameters, callbackforSS)
        if callback:
            ret = self.imageCallback(callback, ret)
        return ret

    def runHfr1_28(self, vic, bitDepth=None, threeD=None, bt2020=None,
                   callbackforSS=False, testParameters=None):

        """Execute FRL source test HFR1-28

        This test verifies that the Source, whenever transmitting any non-2160p
        Video Format that falls within a TMDS Character Rate between 340 Mcsc
        and 600 Mcsc (hereafter referred to as "legacy non-2160p") while in FRL
        mode, transmits an accurate AVI InfoFrame at least once per every two
        video fields and appropriate color depth as indicated by GCP

        This test can verify:

        - 8-bit formats, such as VIC 92.
            - Required arguments:
                - vic: The expected VIC
        - 10- or 12-bit deep color formats such as VIC 63.
            - Required arguments:
                - vic: The expected VIC
                - bitDepth: 10 or 12
        - 3D formats such as frame packing with VIC 63.
            - Required arguments:
                - vic: The expected VIC
                - threeD:
                    - F: Frame packing
                    - S: Side-by-side
                    - T: Top-bottom
        - ITU-R BT.2020 cYCC and RGB/YCC colorimetry.
            - Required arguments:
                - vic: The expected VIC
                - bt2020:
                    - 0: No BT.2020 colorimetry permitted
                    - 1: BT.2020 cYCC colorimetry expected
                    - 2: BT.2020 RGB or YCC colorimetry expected

        @param self the TLqdInstrument object
        @param vic Video identification code
        @param bitDepth Bit depth, None, 10 or 12
        @param threeD 3D option, None, F, T or S
        @param bt2020 BT.2020 option, None, 0, 1 or 2
        @param callbackforSS Callback function to do source setup
        @param testParameters TLqdTestParameters
        @return TLqdResult"""

        cmd = 'ct HFR1-28 -v' + str(vic)
        if bitDepth:
            cmd = cmd + ' -n' + str(bitDepth)
        if threeD:
            cmd = cmd + ' -3' + str(threeD)
        return self.runRequireHpTest(cmd, testParameters, callbackforSS)

    def runHfr1_29(self, callback, supportsTestImage=False,
                   callbackforSS=False, testParameters=None):

        """Execute FRL source test HFR1-29

        This test verifies that a source DUT outputs correct RGB pixel encoding
        and signaling while in FRL Mode. In the case where a Source DUT can
        output a standardized test image, the test verifies the proper position
        of the pixels and the order of the color-component data of the test
        pixels with fully saturated (extreme-value) color-components.

        @param self the TLqdInstrument object
        @param callback Callback function to verify bitmap image
        @param supportsTestImage Indicates the DUT supports the test image
        @param callbackforSS Callback function to do source setup
        @param testParameters TLqdTestParameters
        @return TLqdResult"""

        cmd = 'ct HFR1-29'
        if supportsTestImage:
            cmd = cmd + ' -t'
        ret = self.runRequireHpTest(cmd, testParameters, callbackforSS)
        if callback:
            ret = self.imageCallback(callback, ret)
        return ret

    def runHfr1_30(self, callback, subSampling, supportsTestImage=False,
                  callbackforSS=False, testParameters=None):

        """Execute FRL source test HFR1-30

        This test verifies that a source DUT outputs correct YCbCr pixel
        encoding and signaling while in FRL Mode. In the case where a Source
        DUT can output a standardized test image, the test verifies the proper
        position of the pixels and the order of the color-component data of the
        test pixels with fully saturated (extreme-value) color-components.

        @param self the TLqdInstrument object
        @param callback Callback function to verify bitmap image
        @param subSampling TLqdSubsampling
        @param supportsTestImage Indicates the DUT supports the test image
        @param callbackforSS Callback function to do source setup
        @param testParameters TLqdTestParameters
        @return TLqdResult"""

        cmd = 'ct HFR1-30'
        if supportsTestImage:
            cmd = cmd + ' -t'
        if subSampling == TLqdSubsampling.SS422:
            subSampling = 2
        elif subSampling == TLqdSubsampling.SS444:
            subSampling = 4
        cmd = cmd + ' -c' + str(subSampling)
        ret = self.runRequireHpTest(cmd, testParameters, callbackforSS)
        if callback:
            ret = self.imageCallback(callback, ret)
        return ret

    def runHfr1_31(self, callback, callbackforSS, vic, supportsTestImage=False,
                   testParameters=None):

        """Execute FRL source test HFR1-31

        This test verifies that a source DUT outputs correct YCbCr pixel
        encoding and signaling while in FRL Mode. In the case where a Source
        DUT can output a standardized test image, the test verifies the proper
        position of the pixels and the order of the color-component data of the
        test pixels with fully saturated (extreme-value) color-components.

        @param self the TLqdInstrument object
        @param callback Callback function to verify bitmap image
        @param callbackforSS Callback function to do source setup
        @param vic Video ID code
        @param supportsTestImage Indicates the DUT supports the test image
        @param callbackforSS Callback function to do source setup
        @param testParameters TLqdTestParameters
        @return TLqdResult"""

        cmd = 'ct HFR1-31'
        if supportsTestImage:
            cmd = cmd + ' -t'
        cmd = cmd + ' -v' + str(vic)
        ret = self.runRequireHpTest(cmd, testParameters, callbackforSS)
        if callback:
            ret = self.imageCallback(callback, ret)
        return ret

    def runHfr1_32(self, callback, vic, supportsTestImage=False, bitDepth=8,
                   callbackforSS=False, testParameters=None):

        """Execute FRL source test HFR1-32

        This test verifies that a source DUT outputs correct YCbCr 4:2:0
        deep color pixel encoding and signaling while in FRL Mode. In the case
        where a Source DUT can output a standardized test image, the test
        verifies the proper position of the pixels and the order of the
        color-component data of the test pixels with fully saturated
        (extreme-value) color-components.

        @param self the TLqdInstrument object
        @param callback Callback function to verify bitmap image
        @param vic Video ID code
        @param supportsTestImage Indicates the DUT supports the test image
        @param bitDepth Bit depth, 8, 10, 12 or 16
        @param callbackforSS Callback function to do source setup
        @param testParameters TLqdTestParameters
        @return TLqdResult"""

        cmd = 'ct HFR1-32'
        if supportsTestImage:
            cmd = cmd + ' -t'
        cmd = cmd + ' -n ' + str(bitDepth) + ' -v ' + str(vic)
        ret = self.runRequireHpTest(cmd, testParameters, callbackforSS)
        if callback:
            ret = self.imageCallback(callback, ret)
        return ret

    def runHfr1_33(self, vic, callbackforSS, testParameters=None):

        """Execute FRL source test HFR1-33

        This test verifies that the Source outputs the correct timing for
        YCbCr 4:2:0 timings while in FRL Mode

        @param self the TLqdInstrument object
        @param vic Video ID code
        @param callbackforSS Callback function to do source setup
        @param testParameters TLqdTestParameters
        @return TLqdResult"""

        cmd = 'ct HFR1-33 -v ' + str(vic)
        return self.runRequireHpTest(cmd, testParameters, callbackforSS)

    def runHfr1_34(self, vic, bitDepth=8, callbackforSS=False, testParameters=None):

        """Execute FRL source test HFR1-34

        This test verifies the Source outputs the correct timing for
        YCbCr 4:2:0 Deep Color timings while in FRL Mode

        @param self the TLqdInstrument object
        @param vic Video ID code
        @param bitDepth Bit depth, 8, 10, 12 or 16
        @param callbackforSS Callback function to do source setup
        @param testParameters TLqdTestParameters
        @return TLqdResult"""

        cmd = 'ct HFR1-34 -n ' + str(bitDepth) + ' -v ' + str(vic)
        return self.runRequireHpTest(cmd, testParameters, callbackforSS)

    def runHfr1_35(self, vic, bitDepth=8, callbackforSS=False, testParameters=None):

        """Execute FRL source test HFR1-35

        This test verifies that the Source DUT supports 4320p Deep Color Video
        Formats when in FRL mode

        @param self the TLqdInstrument object
        @param vic Video ID code
        @param bitDepth Bit depth, 8, 10, 12 or 16
        @param callbackforSS Callback function to do source setup
        @param testParameters TLqdTestParameters
        @return TLqdResult"""

        cmd = 'ct HFR1-35 -n ' + str(bitDepth) + ' -v ' + str(vic)
        return self.runRequireHpTest(cmd, testParameters, callbackforSS)

    def runHfr1_36(self, stepNumber, callbackforSS=False, testParameters=None):

        """Execute FRL source test HFR1-36

        This test verifies that the Source DUT transmits 3D Audio (L-PCM) using
        a valid packet format while in FRL Mode.

        There are two parts to this test:
            - Step 1: Verify that the DUT follows the EDID and does not send 3D
                audio
            - Step 2: Verify that the DUT follows the EDID and sends 3D audio

        @param self the TLqdInstrument object
        @param stepNumber Test step number, 1 or 2
        @param callbackforSS Callback function to do source setup
        @param testParameters TLqdTestParameters
        @return TLqdResult"""

        cmd = 'ct HFR1-36 -i' + str(stepNumber)
        return self.runRequireHpTest(cmd, testParameters, callbackforSS)

    def runHfr1_37(self, callbackforSS=False, testParameters=None):

        """Execute FRL source test HFR1-37

        This test verifies that the Source DUT transmits 3D Audio (One Bit)
        using a valid packet format while in FRL Mode.

        @param self the TLqdInstrument object
        @param callbackforSS Callback function to do source setup
        @param testParameters TLqdTestParameters
        @return TLqdResult"""

        return self.runRequireHpTest('ct HFR1-37', testParameters, callbackforSS)

    def runHfr1_38(self, callbackforSS=False, testParameters=None):

        """Execute FRL source test HFR1-38

        This test verifies that the Source DUT transmits Multi Stream Audio
        using a valid packet format while in FRL Mode.

        @param self the TLqdInstrument object
        @param callbackforSS Callback function to do source setup
        @param testParameters TLqdTestParameters
        @return TLqdResult"""

        return self.runRequireHpTest('ct HFR1-38', testParameters, callbackforSS)

    def runHfr1_39(self, callbackforSS=False, testParameters=None):

        """Execute FRL source test HFR1-39

        This test verifies that the Source DUT transmits One Bit Multi Stream
        Audio using a valid packet format while in FRL Mode.

        @param self the TLqdInstrument object
        @param callbackforSS Callback function to do source setup
        @param testParameters TLqdTestParameters
        @return TLqdResult"""

        return self.runRequireHpTest('ct HFR1-39', testParameters, callbackforSS)

    def runHfr1_40(self, callbackforSS=False, testParameters=None):

        """Execute FRL source test HFR1-40

        This test verifies that the Source DUT, whenever transmitting a
        supported audio format, sends a properly formatted audio signal while
        in FRL Mode.

        @param self the TLqdInstrument object
        @param callbackforSS Callback function to do source setup
        @param testParameters TLqdTestParameters
        @return TLqdResult"""

        return self.runRequireHpTest('ct HFR1-40', testParameters, callbackforSS)

    def runHfr1_41(self, callbackforSS=False, testParameters=None):

        """Execute FRL source test HFR1-41

        This test verifies all fields within the 3D Audio Sample Packet from
        the Source DUT follows the corresponding rules specified in the
        IEC 60958 specifications while in FRL Mode.

        @param self the TLqdInstrument object
        @param callbackforSS Callback function to do source setup
        @param testParameters TLqdTestParameters
        @return TLqdResult"""

        return self.runRequireHpTest('ct HFR1-41', testParameters, callbackforSS)

    def runHfr1_43(self, callbackforSS=False, testParameters=None):

        """Execute FRL source test HFR1-43

        This test verifies that the behavior of all fields within the HBR Audio
        Sample Packet follows the corresponding rules specified in the
        IEC 60958 or IEC 61937 specifications while in FRL Mode

        @param self the TLqdInstrument object
        @param callbackforSS Callback function to do source setup
        @param testParameters TLqdTestParameters
        @return TLqdResult"""

        return self.runRequireHpTest('ct HFR1-43', testParameters, callbackforSS)

    def runHfr1_45(self, sampling, layout, callbackforSS=False, testParameters=None):

        """Execute FRL source test HFR1-45

        This test verifies that the Audio Sample Packet is transmitted with the
        supported sample frequency while in FRL Mode

        @param self the TLqdInstrument object
        @param sampling Audio sampling rate in Hz
        @param layout (0=2-channel, 1=multi-channel)
        @param callbackforSS Callback function to do source setup
        @param testParameters TLqdTestParameters
        @return TLqdResult"""

        cmd = 'ct HFR1-45 -s ' + str(sampling) + ' -l ' + str(layout)
        return self.runRequireHpTest(cmd, testParameters, callbackforSS)

    def runHfr1_46(self, callbackforSS=False, testParameters=None):

        """Execute FRL source test HFR1-46

        This test verifies that the Audio Sample Packet is transmitted with the
        supported sample frequency while in FRL Mode

        @param self the TLqdInstrument object
        @param callbackforSS Callback function to do source setup
        @param testParameters TLqdTestParameters
        @return TLqdResult"""

        return self.runRequireHpTest('ct HFR1-46', testParameters, callbackforSS)

    def runHfr1_50(self, vic, callbackforSS=False, testParameters=None):

        """Execute FRL source test HFR1-50

        This test verifies that the Source DUT supports 24-bit Color Depth
        4320p Video Formats when in FRL mode

        @param self the TLqdInstrument object
        @param vic Video ID code
        @param callbackforSS Callback function to do source setup
        @param testParameters TLqdTestParameters
        @return TLqdResult"""

        cmd = 'ct HFR1-50 -v ' + str(vic)
        return self.runRequireHpTest(cmd, testParameters, callbackforSS)

    def runHfr1_51(self, vic, stepNumber, callbackforSS, testParameters=None):

        """Execute FRL source test HFR1-51

        This test verifies that the YCbCr 4:2:0 signaling information in the
        AVI InfoFrame is correct while in FRL Mode

        There are four parts to this test:
            - Step 1: Verify that the DUT follows the EDID Y420 Video Data Block
            - Step 2: Verify that the DUT follows the EDID YCbCr 4:2:0
                Capabilites Map Data Block
            - Step 3: Verify that the DUT follows the EDID with an empty
                YCbCr 4:2:0 Capabilites Map Data Block
            - Step 4: Verify that the DUT does not transmit YCbCr 4:2:0 based
                on the EDID data

        The test requires a 2160p VIC: 96, 97, 101, 102, 106 or 107

        @param self the TLqdInstrument object
        @param vic Video identification code
        @param stepNumber Test step number, 1 - 4
        @param callbackforSS Callback function to do source setup
        @param testParameters TLqdTestParameters
        @return TLqdResult"""

        cmd = 'ct HFR1-51 -v' + str(vic) + ' -i' + str(stepNumber)
        return self.runRequireHpTest(cmd, testParameters, callbackforSS)

    def runHfr1_52(self, stepNumber, callbackforSS=False, testParameters=None):

        """Execute FRL source test HFR1-52

        This test verifies that the YCbCr 4:2:0 signaling information in the
        AVI InfoFrame is correct while in FRL Mode

        There are four parts to this test:
            - Step 1: Verify that the DUT supports BT.2020 YCC
            - Step 2: Verify that the DUT follows the EDID and does not send
                BT.2020 YCC
            - Step 3: Verify that the DUT supports BT.2020 cYCC
            - Step 4: Verify that the DUT follows the EDID and does not send
                BT.2020 cYCC

        The test requires a 2160p VIC: 96, 97, 101, 102, 106 or 107

        @param self the TLqdInstrument object
        @param stepNumber Test step number, 1 - 4
        @param callbackforSS Callback function to do source setup
        @param testParameters TLqdTestParameters
        @return TLqdResult"""

        cmd = 'ct HFR1-52' + ' -i' + str(stepNumber)
        return self.runRequireHpTest(cmd, testParameters, callbackforSS)

    def runHfr1_58(self, vic, stepNumber, bitDepth=None, bt2020=None,
                   callbackforSS=False, testParameters=None):

        """Execute FRL source test HFR1-58

        This test verifies that the Source, whenever transmitting any
        video formats with an 861G pixel frequencey above 600MHz
        while in FRL mode, transmits an accurate AVI InfoFrame
        at least once per every two video fields and appropriate
        color depth as indicated by GCP.

        This test can verify:

        - 8-bit formats, such as given VIC
            - Required arguments:
                - vic: The expected VIC
        - ITU-R BT.2020 cYCC and RGB/YCC colorimetry.
            - Required arguments:
                - vic: The expected VIC
                - bitDepth: 10 or 12
                - bt2020:
                    - 0: No BT.2020 colorimetry permitted
                    - 1: BT.2020 cYCC colorimetry expected
                    - 2: BT.2020 RGB or YCC colorimetry expected

        @param self the TLqdInstrument object
        @param vic Video identification code
        @param stepNumber Test step number, 1 - 24
        @param bitDepth Bit depth, None, 10 or 12
        @param bt2020 BT.2020 option, None, 0, 1 or 2
        @param callbackforSS Callback function to do source setup
        @param testParameters TLqdTestParameters
        @return TLqdResult"""

        cmd = 'ct HFR1-58 -v' + str(vic) + ' -i' + str(stepNumber)
        if bitDepth:
            cmd = cmd + ' -n' + str(bitDepth)
        if 21 <= stepNumber <= 24 :
            cmd = cmd + ' -B' + str(bt2020)
        return self.runRequireHpTest(cmd, testParameters, callbackforSS)

    def runHfr1_65(self, stepNumber, callbackforSS=False, testParameters=None):

        """Execute FRL source test HFR1-65

        This test verifies that the source correctly implements the transport
        of Compressed Video Transport Extended Metadata

        There are three parts to this test:
            - Step 1: Verify no CVTEM is sent when the EDID DSC_1p2=0
            - Step 2: Verify CVTEM is sent when the EDID DSC_1p2=1,
                FAPA_start_location=0
            - Step 3: Verify CVTEM is sent when the EDID DSC_1p2=1,
                FAPA_start_location=1

        @param self the TLqdInstrument object
        @param stepNumber Test step number, 1 - 3
        @param callbackforSS Callback function to do source setup
        @param testParameters TLqdTestParameters
        @return TLqdResult"""

        cmd = 'ct HFR1-65 -i' + str(stepNumber)
        return self.runRequireHpTest(cmd, testParameters, callbackforSS)

    def runHfr1_67(self, stepNumber, testParameters=None):

        """Execute FRL source test HFR1-65

        This test verifies that the source CDF parameters

        @param self the TLqdInstrument object
        @param stepNumber Test step number, 1 - 8
        @param testParameters TLqdTestParameters
        @return TLqdResult"""

        cmd = 'ct HFR1-67 -i' + str(stepNumber)
        return self.runTest(cmd, testParameters)

    def runHfr1_68(self, callbackforSS=False, testParameters=None):

        """Execute FRL source test HFR1-68

        This test verifies that the source DUT polls
        update flags and retrains when requested by the sink

        @param self the TLqdInstrument object
        @param callbackforSS Callback function to do source setup
        @param testParameters TLqdTestParameters
        @return TLqdResult"""

        return self.runRequireHpTest('ct HFR1-68', testParameters, callbackforSS)

    def runHfr1_69(self, vic, stepNumber, callbackforSS=False, testParameters=None):

        """Execute FRL source test HFR1-69

        @param self the TLqdInstrument object
        @param vic Video identification code
        @param stepNumber Test step number, 1 - 4
        @param callbackforSS Callback function to do source setup
        @param testParameters TLqdTestParameters
        @return TLqdResult"""

        ret = TLqdResult(TLqdStatus.FAIL, [], [])

        cmd = 'ct HFR1-69 -i' + str(stepNumber) + ' -v' + str(vic)
        ret = self.runTest(cmd, testParameters, callbackforSS)
        return ret

    def runHfr1_80(self, vic, stepNumber, callback, supportsTestImage=False,
                   callbackforSS=False, testParameters=None):

        """Execute FRL source test HFR1-80

        This test verifies that the Source DUT supports 2160p 8 bpc RGB
        Compressed Formats when in FRL mode

        There are two parts to this test:
            - Step 1: Verify with the maximum FRL rate
            - Step 2: Verify with the minimum FRL rate and HF-SCDB EDID

        The test requires a 2160p VIC: 96, 97, 101, 102, 106, 107, 114-120,
        124-127, 193, 218-219

        @param self the TLqdInstrument object
        @param vic Video identification code
        @param stepNumber Test step number, 1 - 2
        @param callback Callback function to verify bitmap image
        @param supportsTestImage Indicates the DUT supports the DSC test image
        @param callbackforSS Callback function to do source setup
        @param testParameters TLqdTestParameters
        @return TLqdResult"""

        cmd = 'ct HFR1-80' + ' -v ' + str(vic) + ' -i' + str(stepNumber)
        if supportsTestImage:
            cmd = cmd + ' -T'
        ret = self.runRequireHpTest(cmd, testParameters, callbackforSS)
        if callback:
            ret = self.imageCallback(callback, ret)
        return ret

    def runHfr1_81(self, vic, stepNumber, callback, supportsTestImage=False,
                   callbackforSS=False, testParameters=None):

        """Execute FRL source test HFR1-81

        This test verifies that the Source DUT supports 4320p 8 bpc RGB
        Compressed Formats when in FRL mode

        There are two parts to this test:
            - Step 1: Verify with the maximum FRL rate
            - Step 2: Verify with the minimum FRL rate and HF-SCDB EDID

        The test requires a 4320p VIC: 194-215

        @param self the TLqdInstrument object
        @param vic Video identification code
        @param stepNumber Test step number, 1 - 2
        @param callback Callback function to verify bitmap image
        @param supportsTestImage Indicates the DUT supports the DSC test image
        @param callbackforSS Callback function to do source setup
        @param testParameters TLqdTestParameters
        @return TLqdResult"""

        cmd = 'ct HFR1-81' + ' -v ' + str(vic) + ' -i' + str(stepNumber)
        if supportsTestImage:
            cmd = cmd + ' -T'
        ret = self.runRequireHpTest(cmd, testParameters, callbackforSS)
        if callback:
            ret = self.imageCallback(callback, ret)
        return ret

    def runHfr1_82(self, vic, bitDepth, stepNumber, callback,
                   supportsTestImage=False, callbackforSS=False,
                   testParameters=None):

        """Execute FRL source test HFR1-82

        This test verifies that the Source DUT supports <=2160p 10 bpc and/or
        12 bpc RGB Primary Compressed Formats when in FRL mode

        There are two parts to this test:
            - Step 1: Verify with the maximum FRL rate
            - Step 2: Verify with the minimum FRL rate and HF-SCDB EDID

        The test requires a <=2160p VIC: 63, 64, 77, 78, 93-107, 114-127, 193,
        218-219

        @param self the TLqdInstrument object
        @param vic Video identification code
        @param bitDepth Bit depth, 10 or 12
        @param stepNumber Test step number, 1 - 2
        @param callback Callback function to verify bitmap image
        @param supportsTestImage Indicates the DUT supports the DSC test image
        @param callbackforSS Callback function to do source setup
        @param testParameters TLqdTestParameters
        @return TLqdResult"""

        cmd = 'ct HFR1-82' + ' -v' + str(vic) + ' -n' + str(bitDepth)
        cmd = cmd + ' -i' + str(stepNumber)
        if supportsTestImage:
            cmd = cmd + ' -T'
        ret = self.runRequireHpTest(cmd, testParameters, callbackforSS)
        if callback:
            ret = self.imageCallback(callback, ret)
        return ret

    def runHfr1_83(self, vic, bitDepth, stepNumber, callback,
                   supportsTestImage=False, callbackforSS=False,
                   testParameters=None):

        """Execute FRL source test HFR1-83

        This test verifies that the Source DUT supports 4320p 10 bpc and/or
        12 bpc RGB Primary Compressed Formats when in FRL mode

        There are two parts to this test:
            - Step 1: Verify with the maximum FRL rate
            - Step 2: Verify with the minimum FRL rate and HF-SCDB EDID

        The test requires a 4320p VIC: 194-215

        @param self the TLqdInstrument object
        @param vic Video identification code
        @param bitDepth Bit depth, 10 or 12
        @param stepNumber Test step number, 1 - 2
        @param callback Callback function to verify bitmap image
        @param supportsTestImage Indicates the DUT supports the DSC test image
        @param callbackforSS Callback function to do source setup
        @param testParameters TLqdTestParameters
        @return TLqdResult"""

        cmd = 'ct HFR1-83' + ' -v' + str(vic) + ' -n' + str(bitDepth)
        cmd = cmd + ' -i' + str(stepNumber)
        if supportsTestImage:
            cmd = cmd + ' -T'
        ret = self.runRequireHpTest(cmd, testParameters, callbackforSS)
        if callback:
            ret = self.imageCallback(callback, ret)
        return ret

    def runHfr1_84(self, vic, subSampling, stepNumber, callback,
                   supportsTestImage=False, callbackforSS=False,
                   testParameters=None):

        """Execute FRL source test HFR1-84

        This test verifies that the Source DUT supports <= 2160p YCbCr 4:4:4,
        4:2:2 and/or 4:2:0 Primary Compressed Formats indicated in the EDID
        when in FRL mode

        There are two parts to this test:
            - Step 1: Verify with the maximum FRL rate
            - Step 2: Verify with the minimum FRL rate and HF-SCDB EDID

        The test for 4:4:4 subsampling requires a VIC: 63, 64, 77, 78, 93-107,
            114-127, 193, 218-219
        The test for 4:2:2 subsampling requires a VIC: 93-107, 114-127, 193,
            218-219
        The test for 4:2:0 subsampling requires a VIC: 96, 97, 101, 102, 106,
            107, 114-120, 124-127, 193, 218-219

        @param self the TLqdInstrument object
        @param vic Video identification code
        @param subSampling TLqdSubsampling
        @param stepNumber Test step number, 1 - 2
        @param callback Callback function to verify bitmap image
        @param supportsTestImage Indicates the DUT supports the DSC test image
        @param callbackforSS Callback function to do source setup
        @param testParameters TLqdTestParameters
        @return TLqdResult"""

        cmd = 'ct HFR1-84' + ' -v' + str(vic) + ' -c' + str(subSampling)
        cmd = cmd + ' -i' + str(stepNumber)
        if supportsTestImage:
            cmd = cmd + ' -T'
        ret = self.runRequireHpTest(cmd, testParameters, callbackforSS)
        if callback:
            ret = self.imageCallback(callback, ret)
        return ret

    def runHfr1_85(self, vic, subSampling, stepNumber, callback,
                   supportsTestImage=False, callbackforSS=False,
                   testParameters=None):

        """Execute FRL source test HFR1-85

        This test verifies that the Source DUT supports transmitting at least
        one 4320p YCbCr 4:4:4, 4:2:2, or 4:2:0 Primary Compressed Video Format

        There are two parts to this test:
            - Step 1: Verify with the maximum FRL rate
            - Step 2: Verify with the minimum FRL rate and HF-SCDB EDID

        The test for 4:4:4/4:2:2 subsampling requires a VIC: 194-215
        The test for 4:2:0 subsampling requires a VIC: 194-217

        @param self the TLqdInstrument object
        @param vic Video identification code
        @param subSampling TLqdSubsampling
        @param stepNumber Test step number, 1 - 2
        @param callback Callback function to verify bitmap image
        @param supportsTestImage Indicates the DUT supports the DSC test image
        @param callbackforSS Callback function to do source setup
        @param testParameters TLqdTestParameters
        @return TLqdResult"""

        cmd = 'ct HFR1-85' + ' -v' + str(vic) + ' -c' + str(subSampling)
        cmd = cmd + ' -i' + str(stepNumber)
        if supportsTestImage:
            cmd = cmd + ' -T'
        ret = self.runRequireHpTest(cmd, testParameters, callbackforSS)
        if callback:
            ret = self.imageCallback(callback, ret)
        return ret

    def runHfr5_1_20(self, testParameters=None):

        """Execute eARC source test HFR5-1-20

        This test verifies that the eARC Tx achieves discovery with COMMA width
        margining

        @param self the TLqdInstrument object
        @param testParameters TLqdTestParameters
        @return TLqdResult"""

        return self.runEarcTest('ct HFR5-1-20', testParameters)

    def runHfr5_1_21(self, testParameters=None):

        """Execute eARC source test HFR5-1-21

        This test verifies that the eARC Tx achieves discovery with Bit Time
        margining

        @param self the TLqdInstrument object
        @param testParameters TLqdTestParameters
        @return TLqdResult"""

        return self.runEarcTest('ct HFR5-1-21', testParameters)

    def runHfr5_1_22(self, testParameters=None):

        """Execute eARC source test HFR5-1-22

        This test verifies that the eARC Tx gets <NACK> indicating eARC RX Busy

        @param self the TLqdInstrument object
        @param testParameters TLqdTestParameters
        @return TLqdResult"""

        return self.runEarcTest('ct HFR5-1-22', testParameters)

    def runHfr5_1_23(self, testParameters=None):

        """Execute eARC source test HFR5-1-23

        This test verifies that the eARC Tx gets Common Mode Slow Response

        @param self the TLqdInstrument object
        @param testParameters TLqdTestParameters
        @return TLqdResult"""

        return self.runEarcTest('ct HFR5-1-23', testParameters)

    def runHfr5_1_24(self, testParameters=None):

        """Execute eARC source test HFR5-1-24

        This test verifies that the eARC Tx gets Timeout during Heartbeat

        @param self the TLqdInstrument object
        @param testParameters TLqdTestParameters
        @return TLqdResult"""

        return self.runEarcTest('ct HFR5-1-24', testParameters)

    def runHfr5_1_25(self, testParameters=None):

        """Execute eARC source test HFR5-1-25

        This test verifies that the eARC Tx gets Heartbeat Disconnect

        @param self the TLqdInstrument object
        @param testParameters TLqdTestParameters
        @return TLqdResult"""

        return self.runEarcTest('ct HFR5-1-25', testParameters)

    def runHfr5_1_26(self, testParameters=None):

        """Execute eARC source test HFR5-1-26

        This test verifies that the eARC Tx gets HPD LOW Disconnect

        @param self the TLqdInstrument object
        @param testParameters TLqdTestParameters
        @return TLqdResult"""

        return self.runEarcTest('ct HFR5-1-26', testParameters)

    def runHfr5_1_28(self, samplingRate, mute=None, bitDepth=None,
                     testParameters=None):

        """Execute eARC source test HFR5-1-28

        This test verifies that the eARC TX sends correctly structured 2-channel
        LPCM Audio Packets with 16-bit format Audio

        @param self the TLqdInstrument object
        @param samplingRate Audio sampling rate in kHz (48, 44.1, etc.)
        @param mute If not None, tests MUTE=1 (or 0)
        @param bitDepth Audio sample size (16, 20 or 24)
        @param testParameters TLqdTestParameters
        @return TLqdResult"""

        cmd = 'ct HFR5-1-28 -r' + str(samplingRate)
        if mute is not None:
            cmd = cmd + ' -m' + str(mute)
        if bitDepth is not None:
            cmd = cmd + ' -b' + str(bitDepth)
        return self.runEarcTest(cmd, testParameters)

    def runHfr5_1_29(self, samplingRate, mute=None, bitDepth=None,
                     testParameters=None):

        """Execute eARC source test HFR5-1-29

        This test verifies that the eARC TX sends correctly structured multi-
        channel 2-channel LPCM Audio Packets with 16-bit format Audio

        @param self the TLqdInstrument object
        @param samplingRate Audio sampling rate in kHz (48, 44.1, etc.)
        @param mute If not None, tests MUTE=1 (or 0)
        @param bitDepth Audio sample size (16, 20 or 24)
        @param testParameters TLqdTestParameters
        @return TLqdResult"""

        cmd = 'ct HFR5-1-29 -r' + str(samplingRate)
        if mute is not None:
            cmd = cmd + ' -m' + str(mute)
        if bitDepth is not None:
            cmd = cmd + ' -b' + str(bitDepth)
        return self.runEarcTest(cmd, testParameters)

    def runHfr5_1_32(self, samplingRate, callback, testParameters=None):

        """Execute eARC source test HFR5-1-32

        This test verifies that the eARC Tx sends 2-channel LPCM Audio at the
        highest Basic Rate and the highest bit-rate it is capable of

        @param self the TLqdInstrument object
        @param samplingRate Audio sampling rate in kHz (48, 44.1, etc.)
        @param callback Callback function to verify received audio
        @param testParameters TLqdTestParameters
        @return TLqdResult"""

        cmd = 'ct HFR5-1-32 -r' + str(samplingRate)
        ret = self.runEarcTest(cmd, testParameters)
        if callback:
            ret = self.testCallback(callback, ret)
        return ret

    def runHfr5_1_33(self, samplingRate, callback, testParameters=None):

        """Execute eARC source test HFR5-1-33

        This test verifies that the eARC Tx sends multi-channel 2-channel
        LPCM Audio at the highest Basic Rate and the highest bit-rate it is
        capable of

        @param self the TLqdInstrument object
        @param samplingRate Audio sampling rate in kHz (48, 44.1, etc.)
        @param callback Callback function to verify received audio
        @param testParameters TLqdTestParameters
        @return TLqdResult"""

        cmd = 'ct HFR5-1-33 -r' + str(samplingRate)
        ret = self.runEarcTest(cmd, testParameters)
        if callback:
            ret = self.testCallback(callback, ret)
        return ret

    def runHfr5_1_34(self, samplingRate, chanAlloc, callback,
                     testParameters=None):

        """Execute eARC source test HFR5-1-34

        This test verifies that the eARC Tx sends a valid Channel Allocation
        Field in the Channel Status Bits when 8-channel layout LPCM data is sent

        @param self the TLqdInstrument object
        @param samplingRate Audio sampling rate in kHz (48, 44.1, etc.)
        @param chanAlloc Channel allocation value
        @param callback Callback function to verify received audio
        @param testParameters TLqdTestParameters
        @return TLqdResult"""

        cmd = 'ct HFR5-1-34 -r' + str(samplingRate) + ' -C' + str(chanAlloc)
        ret = self.runEarcTest(cmd, testParameters)
        if callback:
            ret = self.testCallback(callback, ret)
        return ret

    def runHfr5_1_35(self, testParameters=None):

        """Execute eARC source test HFR5-1-35

        This test verifies that the eARC Tx Reads Capabilities Data Structure at
        startup

        @param self the TLqdInstrument object
        @param testParameters TLqdTestParameters
        @return TLqdResult"""

        return self.runEarcTest('ct HFR5-1-35', testParameters)

    def runHfr5_1_36(self, testParameters=None):

        """Execute eARC source test HFR5-1-36

        This test verifies that the eARC Tx Re-reads Capabilities Data Structure
        when CAP_CHNG->1

        @param self the TLqdInstrument object
        @param testParameters TLqdTestParameters
        @return TLqdResult"""

        return self.runEarcTest('ct HFR5-1-36', testParameters)

    def runHfr5_1_37(self, testParameters=None):

        """Execute eARC source test HFR5-1-37

        This test verifies that the eARC Tx Re-reads ERX_LATENCY when
        STAT_CHNG->1

        @param self the TLqdInstrument object
        @param testParameters TLqdTestParameters
        @return TLqdResult"""

        return self.runEarcTest('ct HFR5-1-37', testParameters)

    def runHfr5_1_38(self, stepNumber, testParameters=None):

        """Execute eARC source test HFR5-1-38

        This test verifies that the eARC Tx signals that it is leaving Standby
        by temporarily dropping the HPD signal. This HPD signal change is needed
        to cause the eARC RX to start signaling with an eARC COMMA sequence

        There are two steps for this test:
            - stepNumber=1: The test initializes eARC and waits for the DUT to
                signal HPD=1
            - stepNumber=2: The DUT should enter and exit Standby, set HPD=0
                for at least 100ms, then set HPD=1

        @param self the TLqdInstrument object
        @param stepNumber Test step number, 1 - 2
        @param testParameters TLqdTestParameters
        @return TLqdResult"""

        cmd = 'ct HFR5-1-38 -i' + str(stepNumber)
        return self.runEarcTest(cmd, testParameters)

    def runHfr5_1_39(self, testParameters=None):

        """Execute eARC source test HFR5-1-39

        This test verifies that the eARC Tx uses the HDMI_HPD bit in its
        EARC_TX_STAT register to signal that its EDID has changed on its
        eARC port

        @param self the TLqdInstrument object
        @param testParameters TLqdTestParameters
        @return TLqdResult"""

        return self.runEarcTest('ct HFR5-1-39', testParameters)

    def runHfr5_1_50(self, testParameters=None):

        """Execute eARC source test HFR5-1-50

        This test verifies that the eARC Tx Responds <RETRY> to Read Data
        Packet With Uncorrectable ECC Error

        @param self the TLqdInstrument object
        @param testParameters TLqdTestParameters
        @return TLqdResult"""

        return self.runEarcTest('ct HFR5-1-50', testParameters)

    def runHfr5_1_51(self, testParameters=None):

        """Execute eARC source test HFR5-1-51

        This test verifies that the eARC Tx EDID Update and HPD on CDS Change

        @param self the TLqdInstrument object
        @param testParameters TLqdTestParameters
        @return TLqdResult"""

        return self.runEarcTest('ct HFR5-1-51', testParameters)

    def runHfr5_1_52(self, testParameters=None):

        """Execute eARC source test HFR5-1-52

        This test verifies that an ARC-capable DUT can abandon eARC Discovery
        and fall back to ARC if needed

        @param self the TLqdInstrument object
        @param testParameters TLqdTestParameters
        @return TLqdResult"""

        return self.runEarcTest('ct HFR5-1-52', testParameters)

    def runHfr5_1_55(self, testParameters=None):

        """Execute eARC source test HFR5-1-55

        This test verifies that the eARC Tx gets Heartbeat Failure during
        Discovery

        @param self the TLqdInstrument object
        @param testParameters TLqdTestParameters
        @return TLqdResult"""

        return self.runEarcTest('ct HFR5-1-55', testParameters)

    def runHfr5_1_56(self, samplingRate, mute=None, bitDepth=None,
                     testParameters=None):

        """Execute eARC source test HFR5-1-56

        This test verifies that the eARC TX sends correctly structured multi-
        channel 8-channel LPCM Audio Packets with 16-bit format Audio

        @param self the TLqdInstrument object
        @param samplingRate Audio sampling rate in kHz (48, 44.1, etc.)
        @param mute If not None, tests MUTE=1 (or 0)
        @param bitDepth Audio sample size (16, 20 or 24)
        @param testParameters TLqdTestParameters
        @return TLqdResult"""

        cmd = 'ct HFR5-1-56 -r' + str(samplingRate)
        if mute is not None:
            cmd = cmd + ' -m' + str(mute)
        if bitDepth is not None:
            cmd = cmd + ' -b' + str(bitDepth)
        return self.runEarcTest(cmd, testParameters)

    def runHfr5_1_58(self, samplingRate, speakers, mute=None,
                     testParameters=None):

        """Execute eARC source test HFR5-1-58

        This test verifies that the eARC TX sends correctly structured multi-
        channel 16-channel LPCM Audio Packets with 16-bit format Audio

        @param self the TLqdInstrument object
        @param samplingRate Audio sampling rate in kHz (48, 44.1, etc.)
        @param speakers List of speaker descriptors
        @param mute If not None, tests MUTE=1 (or 0)
        @param testParameters TLqdTestParameters
        @return TLqdResult"""

        cmd = 'ct HFR5-1-58 -r' + str(samplingRate)
        if mute is not None:
            cmd = cmd + ' -m' + str(mute)
        cmd = cmd + ' -S"' + str(speakers) + '"'
        return self.runEarcTest(cmd, testParameters)

    def runHfr5_1_59(self, samplingRate, speakers, mute=None,
                     testParameters=None):

        """Execute eARC source test HFR5-1-59

        This test verifies that the eARC TX sends correctly structured multi-
        channel 32-channel LPCM Audio Packets with 16-bit format Audio

        @param self the TLqdInstrument object
        @param samplingRate Audio sampling rate in kHz (48, 44.1, etc.)
        @param speakers List of speaker descriptors
        @param mute If not None, tests MUTE=1 (or 0)
        @param testParameters TLqdTestParameters
        @return TLqdResult"""

        cmd = 'ct HFR5-1-59 -r' + str(samplingRate)
        if mute is not None:
            cmd = cmd + ' -m' + str(mute)
        cmd = cmd + ' -S"' + str(speakers) + '"'
        return self.runEarcTest(cmd, testParameters)

    def runHfr5_2_20(self, testParameters=None):

        """Execute eARC sink test HFR5-2-20

        This test verifies that the eARC Rx meets the spec for eARC discovery

        @param self the TLqdInstrument object
        @param testParameters TLqdTestParameters
        @return TLqdResult"""

        return self.runEarcTest('ct HFR5-2-20', testParameters)

    def runHfr5_2_21(self, testParameters=None):

        """Execute eARC sink test HFR5-2-21

        This test verifies that the eARC Rx responds to Heartbeat after eARC is
        connected

        @param self the TLqdInstrument object
        @param testParameters TLqdTestParameters
        @return TLqdResult"""

        return self.runEarcTest('ct HFR5-2-21', testParameters)

    def runHfr5_2_22(self, testParameters=None):

        """Execute eARC sink test HFR5-2-22

        This test verifies that the eARC Rx stops sending COMMAs when no eARC
        heartbeat is detected

        @param self the TLqdInstrument object
        @param testParameters TLqdTestParameters
        @return TLqdResult"""

        return self.runEarcTest('ct HFR5-2-22', testParameters)

    def runHfr5_2_23(self, testParameters=None):

        """Execute eARC sink test HFR5-2-23

        This test verifies that the eARC Rx responds with <NACK> when it gets a
        Common Mode Data Packet containing an unexpected Device ID

        @param self the TLqdInstrument object
        @param testParameters TLqdTestParameters
        @return TLqdResult"""

        return self.runEarcTest('ct HFR5-2-23', testParameters)

    def runHfr5_2_24(self, testParameters=None):

        """Execute eARC sink test HFR5-2-24

        This test verifies that the eARC Rx restarts a command when it gets an
        <eARC_READ> or <eARC_WRITE> command in the middle of a previous command

        @param self the TLqdInstrument object
        @param testParameters TLqdTestParameters
        @return TLqdResult"""

        return self.runEarcTest('ct HFR5-2-24', testParameters)

    def runHfr5_2_25(self, testParameters=None):

        """Execute eARC sink test HFR5-2-25

        This test verifies that the eARC Rx disconnects when it detects a
        sustained TX Heartbeat Timeout

        @param self the TLqdInstrument object
        @param testParameters TLqdTestParameters
        @return TLqdResult"""

        return self.runEarcTest('ct HFR5-2-25', testParameters)

    ## @cond
    def testCallback(self, callback, results):

        """Process results to verify test results via callback

        @param self the TLqdInstrument object
        @param callback Callback function to verify bitmap image
        @param results TLqdResult
        @return TLqdResult"""

        # See if there is a step file information
        stepsFile = self.getStepsFileName(results)
        if not callback or not stepsFile:
            return results

        import tempfile
        from os import close

        localFile = tempfile.mkstemp('.log', 'tlqdapisteps')
        close(localFile[0])
        localFile = localFile[1]

        self.getFile(stepsFile, localFile)
        tag = 'text:'
        info = ''
        foundTag = False
        lFile = open(localFile, "r")
        for line in lFile:
            if foundTag:
                info = info + line
            else:
                foundTag = line.find(tag) == 0
        lFile.close()

        ret = str(callback(info)).upper()
        info = "Callback returned: " + ret
        if ret == "SKIPPED" or ret == "PASS":
            results.info.append(info)
        elif ret == "FAIL":
            results.status = ret
            results.errors.append(info)
        else:
            info = 'Unexpected return value from callback: "' + ret + '"'
            results.errors.append(info)

        return results
    ## @endcond

    ## @cond
    def runHdmiSinkTest(self, cmd, callback, cdf):
        """Run an HDMI Sink test

        @param self the TLqdInstrument object
        @param cmd Command to execute
        @param callback Callback function
        @param cdf CDF file to use
        @return TLqdResult"""

        if cdf: # Gave a CDF file?
            self.putFile(cdf, RemoteCdfFile)
            cmd = cmd + ' -C' + RemoteCdfFile

        result = self.command(TLqdApiTag + cmd)
        results = self.compileTestResults(result)
        return self.testCallback(callback, results)
    ## @endcond

    def runHf2_5(self, callback, vic=None, cdf=None):

        """Execute HDMI sink test HF2-5

        This test verifies that the Sink DUT supports any Video Format/color
        mode for TMDS Character Rate above 340 Mcsc up to 600 Mcsc

        @param self the TLqdInstrument object
        @param callback Callback function
        @param vic Optional VIC to use
        @param cdf Optional CDF file to use
        @return TLqdResult"""

        cmd = 'ct HF2-5'
        if vic:
            cmd = cmd + ' -v' + str(vic)
        return self.runHdmiSinkTest(cmd, callback, cdf)

    def runHf2_6(self, callback, vic, minOrMax, cdf=None):

        """Execute HDMI sink test HF2-6

        This test verifies that the Sink DUT supports 24-bit Color Depth 2160p
        Video Format for TMDS Character Rate above 340 Mcsc up to 600 Mcsc
        indicated in the EDID

        @param self the TLqdInstrument object
        @param callback Callback function
        @param vic VIC to use (96, 97, 101 or 102)
        @param minOrMax if True minimum rate, maximum otherwise
        @param cdf Optional CDF file to use
        @return TLqdResult"""

        cmd = 'ct HF2-6' + ' -v' + str(vic)
        if minOrMax:
            cmd = cmd + ' -m'
        return self.runHdmiSinkTest(cmd, callback, cdf)

    def runHf2_7(self, callback, vic, bitDepth, minOrMax, yCbCr, cdf=None):

        """Execute HDMI sink test HF2-7

        This test verifies that the Sink DUT supports any Deep Color Video
        2160p Video Format for TMDS Character Rate above 340 Mcsc up to 600 Mcsc

        @param self the TLqdInstrument object
        @param callback Callback function
        @param vic VIC to use (93, 94, 95, 98, 99 or 100)
        @param bitDepth Number of bits/pixel - 10, 12 or 16
        @param minOrMax If True minimum rate, maximum otherwise
        @param yCbCr If True indicates YCbCr 4:4:4 signalling
        @param cdf Optional CDF file to use
        @return TLqdResult"""

        cmd = 'ct HF2-7' + ' -v' + str(vic) + ' -n' + str(bitDepth)
        if minOrMax:
            cmd = cmd + ' -m'
        if yCbCr:
            cmd = cmd + ' -y'
        return self.runHdmiSinkTest(cmd, callback, cdf)

    def runHf2_8(self, callback, vic, threeD, minOrMax, cdf=None):

        """Execute HDMI sink test HF2-8

        This test verifies the Sink DUT supports 2160p 3D 2160p Video Formats
        for TMDS Character Rate above 340 Mcsc up to 600 Mcsc

        The test requires a VIC in the range from 93-102 (inclusive)

        The test also requires a 3D format to be specified, one of:
            - F for Frame packing
            - T for Top/bottom
            - S for Side-by-side (half)

        @param self the TLqdInstrument object
        @param callback Callback function
        @param vic VIC to use (93-102)
        @param threeD 3D option (F, T or S)
        @param minOrMax If True minimum rate, maximum otherwise
        @param cdf Optional CDF file to use
        @return TLqdResult"""

        cmd = 'ct HF2-8' + ' -v' + str(vic) + ' -3' + str(threeD)
        if minOrMax:
            cmd = cmd + ' -m'
        return self.runHdmiSinkTest(cmd, callback, cdf)

    def runHf2_9(self, callback, stepNumber, cdf=None):

        """Execute HDMI sink test HF2-9

        This test verifies that the Sink properly supports scrambling for TMDS
        Character Rates at or below 340Mcsc

        @param self the TLqdInstrument object
        @param callback Callback function
        @param stepNumber Test step number, 1 or 2
        @param cdf Optional CDF file to use
        @return TLqdResult"""

        cmd = 'ct HF2-9 -i' + str(stepNumber)
        return self.runHdmiSinkTest(cmd, callback, cdf)

    def runHf2_10(self, version=TLqdEdidComplianceTestVersion.Version2_0,
                  cdf=None):

        """Execute HDMI sink test HF2-10

        This test verifies that the sink's EDID has a valid HDMI Forum
        Vendor Specific Data Block

        @param self the TLqdInstrument object
        @param version Optional TLqdEdidComplianceTestVersion, defaults to 2.0
        @param cdf Optional CDF file to use
        @return TLqdResult"""

        cmd = 'ct HF2-10 -V' + str(version)
        return self.runHdmiSinkTest(cmd, None, cdf)

    def runHf2_23(self, callback, vic, stepNumber, cdf=None):

        """Execute HDMI sink test HF2-23

        This test verifies that the Sink properly supports YCbCr 4:2:0 Pixel
        decoding and signaling

        @param self the TLqdInstrument object
        @param callback Callback function
        @param vic Video Identification Code (96, 97, 101, 102, 106, or 106)
        @param stepNumber Test step number, 1 or 2
        @param cdf Optional CDF file to use
        @return TLqdResult"""

        cmd = 'ct HF2-23 -v' + str(vic) + ' -i' + str(stepNumber)
        return self.runHdmiSinkTest(cmd, callback, cdf)

    def runHf2_24(self, callback, vic, bitDepth, cdf=None):

        """Execute HDMI sink test HF2-24

        This test verifies that the Sink properly supports YCbCr 4:2:0 Deep
        Color Pixel decoding and signaling

        @param self the TLqdInstrument object
        @param callback Callback function
        @param vic Video Identification Code (96, 97, 101, 102, 106, or 106)
        @param bitDepth Number of bits/pixel (10, 12 or 16)
        @param cdf Optional CDF file to use
        @return TLqdResult"""

        cmd = 'ct HF2-24 -v' + str(vic) + ' -n' + str(bitDepth)
        return self.runHdmiSinkTest(cmd, callback, cdf)

    def runHf2_25(self, callback, vic, checkEdid, checkEquiv, nominalRate,
                  minOrMax, cdf=None):

        """Execute HDMI sink test HF2-25

        This test verifies that a "21:9" (64:27)-capable Sink DUT, whenever it
        receives any supported "21:9" (64:27) Video Format, correctly decodes
        and displays it

        @param self the TLqdInstrument object
        @param callback Callback function
        @param vic Video Identification Code (65-92 or 103-107)
        @param checkEdid Perform EDID checks
        @param checkEquiv Check the equivalent aspect ratio per CTA-861-G
        @param nominalRate Check the format at the nominal rate
        @param minOrMax if True minimum rate, maximum otherwise
        @param cdf Optional CDF file to use
        @return TLqdResult"""

        cmd = 'ct HF2-25 -v' + str(vic)
        if checkEdid:
            cmd = cmd + ' -E'
        if checkEquiv:
            cmd = cmd + ' -e'
        elif nominalRate:
            cmd = cmd + ' -N'
        elif minOrMax:
            cmd = cmd + ' -m'
        return self.runHdmiSinkTest(cmd, callback, cdf)

    def runHf2_26(self, vics, above340Mcsc, cdf=None):

        """Execute HDMI sink test HF2-26

        This test verifies that the Sink DUT correctly declares support for
        Video Formats in its EDID

        @param self the TLqdInstrument object
        @param vics List of 21x9 aspect ratio VICs
        @param above340Mcsc Indicates DUT support >= 340Mcsc
        @param cdf Optional CDF file to use
        @return TLqdResult"""

        cmd = 'ct HF2-26 -v' + self.stringify(vics)
        if above340Mcsc:
            cmd = cmd + ' -3'
        return self.runHdmiSinkTest(cmd, None, cdf)

    def runHf2_30(self, callback, stream=1, flat=False, vic=0, cdf=None):

        """Execute HDMI sink test HF2-30

        This test verifies that a Multi-stream Audio capable Sink supports
        Multi-stream Audio Sample Packets and signaling

        @param self the TLqdInstrument object
        @param callback Callback function to verify the multi-stream audio
        @param stream Stream number to verify
        @param flat Test the stream_flat bits in the audio sample packets
        @param vic Optional video information code to use
        @param cdf Optional CDF file to use
        @return TLqdResult"""

        cmd = 'ct HF2-30'
        if stream > 0:
            cmd = cmd + ' -s' + str(stream)
        if flat:
            cmd = cmd + ' -f'
        return self.runHdmiSinkTest(cmd, callback, cdf)

    def runHf2_31(self, vics, cdf=None):

        """Execute HDMI sink test HF2-31

        This test verifies that a YCbCr 4:2:0 capable Sink DUT EDID contains a
        valid Video Data Block and/or YCbCr 4:2:0 Capability Map Data Block

        @param self the TLqdInstrument object
        @param vics List of 4K 4:2:0 VICs (96, 97, 101, 102, 106 and/or 107)
        @param cdf Optional CDF file to use
        @return TLqdResult"""

        return self.runHdmiSinkTest('ct HF2-31 -v' + self.stringify(vics),
                                    None, cdf)

    def runHf2_32(self, bt2020Ycc, bt2020cYcc, cdf=None):

        """Execute HDMI sink test HF2-32

        This test verifies that a YCbCr 4:2:0 BT.2020 capable Sink DUT EDID
        contains a valid Colorimetry Data Block

        @param self the TLqdInstrument object
        @param bt2020Ycc Indicates support for BT.2020 YCC
        @param bt2020cYcc Indicates support for BT.2020 cYCC
        @param cdf Optional CDF file to use
        @return TLqdResult"""

        cmd = 'ct HF2-32'
        if bt2020Ycc:
            cmd = cmd + ' -y'
        if bt2020cYcc:
            cmd = cmd + ' -c'
        return self.runHdmiSinkTest(cmd, None, cdf)

    def runHf2_35(self, vics, dc10, dc12, dc16, cdf=None):

        """Execute HDMI sink test HF2-35

        This test verifies that a YCbCr 4:2:0 Deep Color Pixel encoding-capable
        Sink DUT EDID contains a valid HF-VSDB

        @param self the TLqdInstrument object
        @param vics List of 4K 4:2:0 VICs (96, 97, 101, 102, 106 and/or 107)
        @param dc10 Indicates support for 10-bit deep color
        @param dc12 Indicates support for 12-bit deep color
        @param dc16 Indicates support for 16-bit deep color
        @param cdf Optional CDF file to use
        @return TLqdResult"""

        cmd = 'ct HF2-35 -v' + self.stringify(vics)
        if dc10:
            cmd = cmd + ' -0'
        if dc12:
            cmd = cmd + ' -2'
        if dc16:
            cmd = cmd + ' -6'
        return self.runHdmiSinkTest(cmd, None, cdf)

    def runHf2_39(self, msAudio=False, threeDAudio=False, msOneBit=False,
                  threeDOneBit=False, msMixed=False, cdf=None):

        """Execute HDMI sink test HF2-39

        This test verifies that the structure of the HDMI Audio Data Block in
        the EDID is valid

        @param self the TLqdInstrument object
        @param msAudio Indicates support for multi-stream audio
        @param threeDAudio Indicates support for 3D audio
        @param msOneBit Indicates support for multi-stream One Bit audio
        @param threeDOneBit Indicates support for 3D One Bit audio
        @param msMixed Indicates support for multi-stream audio mixed
        @param cdf Optional CDF file to use
        @return TLqdResult"""

        cmd = 'ct HF2-39'
        if msAudio:
            cmd = cmd + ' -m'
        if threeDAudio:
            cmd = cmd + ' -3'
        if msOneBit:
            cmd = cmd + ' -O'
        if threeDOneBit:
            cmd = cmd + ' -T'
        if msMixed:
            cmd = cmd + ' -x'
        return self.runHdmiSinkTest(cmd, None, cdf)

    def runHf2_40(self, callback, vic, threeD, stepNumber, cdf=None):

        """Execute HDMI sink test HF2-40

        This test verifies that the Sink DUT correctly decodes and uses the
        information in the Vendor Specific InfoFrame, whenever it receives
        "Dual View"

        @param self the TLqdInstrument object
        @param callback Callback function
        @param vic Video identification code
        @param threeD 3D option, F, T or S
        @param stepNumber Test step number, 1 - 4
        @param cdf Optional CDF file to use
        @return TLqdResult"""

        cmd = 'ct HF2-40 -v' + str(vic) + ' -3' + str(threeD) + \
              ' -i' + str(stepNumber)
        return self.runHdmiSinkTest(cmd, callback, cdf)

    def runHf2_41(self, independentView=True, cdf=None):

        """Execute HDMI sink test HF2-41

        This test verifies that the Sink DUT has the correct content in the
        HF-VSDB for the independent view feature

        @param self the TLqdInstrument object
        @param independentView Indicates support for independent view
        @param cdf Optional CDF file to use
        @return TLqdResult"""

        cmd = 'ct HF2-41'
        if independentView:
            cmd = cmd + ' -i'
        return self.runHdmiSinkTest(cmd, None, cdf)

    def runHf2_43(self, callback, vic, threeD, option, stepNumber,
                  supportsOsd=True, cdf=None):

        """Execute HDMI sink test HF2-43

        This test verifies that whenever the Sink DUT receives "3D OSD
        Disparity" data, it correctly decodes and uses the information in the
        HF-VSIF

        The test has 4 options: a-d:
            a: Send HF-VSIF 3D_DisparityData version 1
            b: Send HF-VSIF 3D_DisparityData version 2,
                3D_DisparityData_length 3
            c: Send HF-VSIF 3D_DisparityData version 2,
                3D_DisparityData_length 11
            d: Send HF-VSIF 3D_DisparityData version 3

        Each option has 4 steps:
            1: Send a normal HF-VSIF
            2: Send a VSIF that is not an HDMI Forum (IEEE OUI 0xC45ED8)
            3: Set 3D_valid=0 in HF-VSIF
            4: Do not send an HF-VSIF

        For options 2-4, the DUT should not use OSD Disparity

        @param self the TLqdInstrument object
        @param callback Callback function
        @param vic Video Identification Code
        @param threeD 3D option, F, T or S
        @param option Test option a - d
        @param stepNumber Test step number, 1 - 4
        @param supportsOsd Indicates OSD support (defaults to True)
        @param cdf Optional CDF file to use
        @return TLqdResult"""

        cmd = 'ct HF2-43 -v' + str(vic) + ' -3' + str(threeD) + ' -O' + \
            str(option) + ' -i' + str(stepNumber)
        if supportsOsd:
            cmd = cmd + ' -o'
        return self.runHdmiSinkTest(cmd, callback, cdf)

    def runHf2_53(self, scdc=False, readRequests=False, lte340=False,
                  indView=False, dualView=False, osd=False, dc10=False,
                  dc12=False, dc16=False, above340=False, cdf=None):

        """Execute HDMI sink test HF2-53

        This test verifies that a Sink DUT EDID contains a valid HF-VSDB when
        required by any feature

        @param self the TLqdInstrument object
        @param scdc Indicates support for SCDC
        @param readRequests Indicates support for read requests
        @param lte340 Indicates support for scrambling <= 340Mcsc
        @param indView Indicates support for independent view
        @param dualView Indicates support for dual view
        @param osd Indicates support for on-screen display
        @param dc10 Indicates support for 4:2:0 10-bit deep color
        @param dc12 Indicates support for 4:2:0 12-bit deep color
        @param dc16 Indicates support for 4:2:0 16-bit deep color
        @param above340 Indicates support for rates > 340Mcsc
        @param cdf Optional CDF file to use
        @return TLqdResult"""

        cmd = 'ct HF2-53'
        if scdc:
            cmd = cmd + ' -s'
        if readRequests:
            cmd = cmd + ' -r'
        if lte340:
            cmd = cmd + ' -l'
        if indView:
            cmd = cmd + ' -i'
        if dualView:
            cmd = cmd + ' -d'
        if osd:
            cmd = cmd + ' -o'
        if dc10:
            cmd = cmd + ' -0'
        if dc12:
            cmd = cmd + ' -2'
        if dc16:
            cmd = cmd + ' -6'
        if above340:
            cmd = cmd + ' -a'
        return self.runHdmiSinkTest(cmd, None, cdf)

    def runHf2_54(self, callback, checkEdid, sdr=False, hdr=False, smpte=False,
                  hlg=False, smpteOption=0, cdf=None):

        """Execute HDMI sink test HF2-54

        This test verifies that the Sink DUT contains a valid HDR Static
        Metadata Data Block

        @param self the TLqdInstrument object
        @param callback Callback function
        @param checkEdid Perform EDID checks
        @param sdr Indicates support for HDR Traditional SDR
        @param hdr Indicates support for HDR Traditional HDR
        @param smpte Indicates support for HDR SMPTE ST.2084
        @param hlg Indicates support for HDR Hybrid Log Gamma
        @param smpteOption R/G/B option number for the SMPTE test (1-6)
        @param cdf Optional CDF file to use
        @return TLqdResult"""

        cmd = 'ct HF2-54'
        if checkEdid:
            cmd = cmd + ' -e'
            callback = None
        if sdr:
            cmd = cmd + ' -s'
        if hdr:
            cmd = cmd + ' -h'
        if smpte:
            cmd = cmd + ' -S' + ' -O' + str(smpteOption)
        if hlg:
            cmd = cmd + ' -H'
        return self.runHdmiSinkTest(cmd, callback, cdf)

    def runHf2_71(self, callback, vic, stepNumber, cdf=None):

        """Execute HDMI sink test HF2-71

        This test verifies that the Sink properly supports YCbCr 4:2:0 Pixel
        decoding and signaling for CTA-861-G VICs

        @param self the TLqdInstrument object
        @param callback Callback function
        @param vic Video Identification Code (114, 115, 116, 117, 118, 119, 120,
            124, 125, 126, 194, 195, 196, 202, 203, 204, 218, 219)
        @param stepNumber Test step number, 1 or 2
        @param cdf Optional CDF file to use
        @return TLqdResult"""

        cmd = 'ct HF2-71 -v' + str(vic) + ' -i' + str(stepNumber)
        return self.runHdmiSinkTest(cmd, callback, cdf)

    def runHf2_72(self, callback, vic, bitDepth, cdf=None):

        """Execute HDMI sink test HF2-72

        This test verifies that the Sink properly supports YCbCr 4:2:0 Deep
        Color Pixel decoding and signaling for CTA-861-G VICs

        @param self the TLqdInstrument object
        @param callback Callback function
        @param vic Video Identification Code (114, 115, 116, 117, 118, 119, 120,
            124, 125, 126, 194, 195, 196, 202, 203, 204, 218, 219)
        @param bitDepth Number of bits/pixel (10, 12 or 16)
        @param cdf Optional CDF file to use
        @return TLqdResult"""

        cmd = 'ct HF2-72 -v' + str(vic) + ' -n' + str(bitDepth)
        return self.runHdmiSinkTest(cmd, callback, cdf)

    def runHf2_94(self, callback, audioRate, nOption, cdf=None):

        """Execute HDMI sink test HF2-94

        This test verifies that whenever the Sink DUT receives a supported
        audio format, it properly decodes and renders it

        @param self the TLqdInstrument object
        @param callback Callback function to verify the multi-stream audio
        @param audioRate Audio sampling rate in kHz (32, 44.1 or 48)
        @param nOption N option ("nominal", "minimum" or "maximum")
        @param cdf Optional CDF file to use
        @return TLqdResult"""

        cmd = 'ct HF2-94 -s' + str(audioRate) + ' -n' + str(nOption)
        return self.runHdmiSinkTest(cmd, callback, cdf)

    def runHfr2_17(self, callback, cdf=None):

        """Execute FRL sink test HFR2-17

        This test verifies that the FRL Lock bits are set and reset correctly
        based on video input

        @param self the TLqdInstrument object
        @param callback Callback function
        @param cdf Optional CDF file to use
        @return TLqdResult"""

        cmd = 'ct HFR2-17'
        return self.runHdmiSinkTest(cmd, None, cdf)

    def runHfr2_18(self, callback, cdf=None):

        """Execute FRL sink test HFR2-18

        This test verifies that each FRL Character Error Counter operates
        correctly in the presence of a specific series of injected errors when
        the counters are being read periodically

        @param self the TLqdInstrument object
        @param callback Callback function
        @param cdf Optional CDF file to use
        @return TLqdResult"""

        cmd = 'ct HFR2-18'
        return self.runHdmiSinkTest(cmd, None, cdf)

    def runHfr2_19(self, callback, cdf=None):

        """Execute FRL sink test HFR2-19

        This test verifies that each FRL Character Error Counter operates
        correctly in the presence of a specific series of injected errors

        @param self the TLqdInstrument object
        @param callback Callback function
        @param cdf Optional CDF file to use
        @return TLqdResult"""

        cmd = 'ct HFR2-19'
        return self.runHdmiSinkTest(cmd, None, cdf)

    def runHfr2_20(self, callback, cdf=None):

        """Execute FRL sink test HFR2-20

        This test verifies that each FRL Character Error Counter operates
        correctly in the presence of a series of injected errors that exceed
        the maximum values of the counters

        @param self the TLqdInstrument object
        @param callback Callback function
        @param cdf Optional CDF file to use
        @return TLqdResult"""

        cmd = 'ct HFR2-20'
        return self.runHdmiSinkTest(cmd, None, cdf)

    def runHfr2_21(self, callback, cdf=None):

        """Execute FRL sink test HFR2-21

        This test verifies that each FRL CED_Update Flag operates correctly
        when a specific series of injected errors is presented

        @param self the TLqdInstrument object
        @param callback Callback function
        @param cdf Optional CDF file to use
        @return TLqdResult"""

        cmd = 'ct HFR2-21'
        return self.runHdmiSinkTest(cmd, None, cdf)

    def runHfr2_22(self, callback, cdf=None):

        """Execute FRL sink test HFR2-22

        This test verifies that each FRL CED_Update Flag operates correctly
        when a series of injected errors is presented that exceed the maximum
        value of the counter

        @param self the TLqdInstrument object
        @param callback Callback function
        @param cdf Optional CDF file to use
        @return TLqdResult"""

        cmd = 'ct HFR2-22'
        return self.runHdmiSinkTest(cmd, None, cdf)

    def runHfr2_48(self, callback, cdf=None):

        """Execute FRL sink test HFR2-48

        This test verifies the basic operation of Reed-Solomon Valid flag and
        Corrections Counter

        @param self the TLqdInstrument object
        @param callback Callback function
        @param cdf Optional CDF file to use
        @return TLqdResult"""

        cmd = 'ct HFR2-48'
        return self.runHdmiSinkTest(cmd, None, cdf)

    def runHfr2_49(self, callback, cdf=None):

        """Execute FRL sink test HFR2-49

        This test verifies that the FRL Reed-Solomon Corrections Counter
        operates correctly in the presence of a specific series of symbol
        errors when the counters are being read periodically

        @param self the TLqdInstrument object
        @param callback Callback function
        @param cdf Optional CDF file to use
        @return TLqdResult"""

        cmd = 'ct HFR2-49'
        return self.runHdmiSinkTest(cmd, None, cdf)

    def runHfr2_50(self, callback, cdf=None):

        """Execute FRL sink test HFR2-50

        This test verifies that the FRL RS Correction Counter operates
        correctly in the presence of a series of symbol errors that exceed the
        maximum value of the counter

        @param self the TLqdInstrument object
        @param callback Callback function
        @param cdf Optional CDF file to use
        @return TLqdResult"""

        cmd = 'ct HFR2-50'
        return self.runHdmiSinkTest(cmd, None, cdf)

    def runHfr2_51(self, callback, cdf=None):

        """Execute FRL sink test HFR2-51

        This test verifies that the FRL RSED_Update Flag operates correctly in
        the presence of a specific series of symbol errors

        @param self the TLqdInstrument object
        @param callback Callback function
        @param cdf Optional CDF file to use
        @return TLqdResult"""

        cmd = 'ct HFR2-51'
        return self.runHdmiSinkTest(cmd, None, cdf)

    def runHfr2_52(self, callback, cdf=None):

        """Execute FRL sink test HFR2-52

        This test verifies that the FRL RSED_Update Flag operates correctly in
        the presence of a super-maximum number of symbol errors

        @param self the TLqdInstrument object
        @param callback Callback function
        @param cdf Optional CDF file to use
        @return TLqdResult"""

        cmd = 'ct HFR2-52'
        return self.runHdmiSinkTest(cmd, None, cdf)

    def runHfr2_53(self, fva=False, allm=False, qms=False, vrr=False,
                   fapa=False, dsc=False, above340=False, ccbpci=False,
                   nmvrr=False, eightk50=False, eightk60=False, vrrHigh=None,
                   maxFrl=None, dscMaxFrl=None, cdf=None):

        """Execute HDMI sink test HFR2-53

        This test verifies that a Sink DUT EDID contains a valid HF-VSDB when
        required by any features introduced in the HDMI 2.1 specification

        @param self the TLqdInstrument object
        @param fva Indicates support for FVA
        @param allm Indicates support for ALLM
        @param qms Indicates support for QMS beyond VRR range
        @param vrr Indicates support for VRR
        @param fapa Indicates support for FAPA start location
        @param dsc Indicates support for DSC
        @param above340 Indicates support for rates > 340Mcsc
        @param ccbpci Indicates support for CCBPCI
        @param nmvrr Indicates support for Negative Mvrr
        @param eightk50 Indicates support for 8K50
        @param eightk60 Indicates support for 8K60
        @param vrrHigh Indicates VRR high range
        @param maxFrl Indicates the maximum FRL rate
        @param dscMaxFrl Indicates the maximum FRL rate for DSC
        @param cdf Optional CDF file to use
        @return TLqdResult"""

        cmd = 'ct HFR2-53'
        if fva:
            cmd = cmd + ' -f'
        if allm:
            cmd = cmd + ' -a'
        if qms:
            cmd = cmd + ' -q'
        if vrr:
            cmd = cmd + ' -v'
        if fapa:
            cmd = cmd + ' -F'
        if dsc:
            cmd = cmd + ' -d'
        if above340:
            cmd = cmd + ' -A'
        if ccbpci:
            cmd = cmd + ' -c'
        if nmvrr:
            cmd = cmd + ' -n'
        if eightk50:
            cmd = cmd + ' -5'
        if eightk60:
            cmd = cmd + ' -6'
        if vrrHigh is not None:
            cmd = cmd + ' -r' + str(vrrHigh)
        if maxFrl is not None:
            cmd = cmd + ' -l' + str(maxFrl)
        if dscMaxFrl is not None:
            cmd = cmd + ' -D' + str(dscMaxFrl)
        return self.runHdmiSinkTest(cmd, None, cdf)

    def runHfr2_70(self, cdf=None):

        """Execute HDMI sink test HFR2-70

        This test verifies that a Sink DUT EDID sets all reserved bits in the
        SCDS to 0

        @param self the TLqdInstrument object
        @param cdf Optional CDF file to use
        @return TLqdResult"""

        return self.runHdmiSinkTest('ct HFR2-70', None, cdf)

    def runHfr2_80(self, callback, vic, testRgb, minPixRate, maxFrlRate,
                   cdf=None):

        """Execute DSC sink test HFR2-80

        This test verifies that the Sink DUT supports 2160p RGB 8 bpc Compressed
        Formats indicated in the EDID when in FRL mode

        @param self the TLqdInstrument object
        @param callback Callback function to verify DSC video
        @param vic Video identification code for a 2160p format
        @param testRgb Indicates testing RGB, YCbCr 4:4:4 otherwise
        @param minPixRate Indicates minimum (99.5%) pixel rate,
            max (100.5%) otherwise
        @param maxFrlRate Indicates the highest FRL rate supported by the DUT
        @param cdf Optional CDF file to use
        @return TLqdResult"""

        cmd = 'ct HFR2-80 -v' + str(vic)
        if testRgb:
            cmd = cmd + ' -R'
        else:
            cmd = cmd + ' -Y'
        if minPixRate:
            cmd = cmd + ' -C'
        if maxFrlRate:
            cmd = cmd + ' -F'
        return self.runHdmiSinkTest(cmd, callback, cdf)

    def runHfr2_81(self, callback, vic, testRgb, minPixRate, maxFrlRate,
                   cdf=None):

        """Execute DSC sink test HFR2-81

        This test verifies that the Sink DUT supports 4320p RGB 8 bpc Primary
        Compressed Formats indicated in the EDID when in FRL mode

        @param self the TLqdInstrument object
        @param callback Callback function to verify DSC video
        @param vic Video identification code for a 4320p format
        @param testRgb Indicates testing RGB, YCbCr 4:4:4 otherwise
        @param minPixRate Indicates minimum (99.5%) pixel rate,
            max (100.5%) otherwise
        @param maxFrlRate Indicates the highest FRL rate supported by the DUT
        @param cdf Optional CDF file to use
        @return TLqdResult"""

        cmd = 'ct HFR2-81 -v' + str(vic)
        if testRgb:
            cmd = cmd + ' -R'
        else:
            cmd = cmd + ' -Y'
        if minPixRate:
            cmd = cmd + ' -C'
        if maxFrlRate:
            cmd = cmd + ' -F'
        return self.runHdmiSinkTest(cmd, callback, cdf)

    def runHfr2_82(self, callback, vic, test10, minPixRate, maxFrlRate,
                   cdf=None):

        """Execute DSC sink test HFR2-82

        This test verifies that the Sink DUT supports 2160p 10 bpc and/or
        12 bpc RGB Primary Compressed Formats indicated in the EDID when in
        FRL mode

        @param self the TLqdInstrument object
        @param callback Callback function to verify DSC video
        @param vic Video identification code for a 2160p format
        @param test10 Indicates testing 10-bit RGB, 12-bit otherwise
        @param minPixRate Indicates minimum (99.5%) pixel rate,
            max (100.5%) otherwise
        @param maxFrlRate Indicates the highest FRL rate supported by the DUT
        @param cdf Optional CDF file to use
        @return TLqdResult"""

        cmd = 'ct HFR2-82 -v' + str(vic)
        if test10:
            cmd = cmd + ' -0'
        else:
            cmd = cmd + ' -2'
        if minPixRate:
            cmd = cmd + ' -C'
        if maxFrlRate:
            cmd = cmd + ' -F'
        return self.runHdmiSinkTest(cmd, callback, cdf)

    def runHfr2_83(self, callback, vic, test10, minPixRate, maxFrlRate,
                   cdf=None):

        """Execute DSC sink test HFR2-83

        This test verifies that the Sink DUT supports 4320p 10 bpc and/or 12 bpc
        RGB Primary Compressed Formats indicated in the EDID when in FRL mode

        @param self the TLqdInstrument object
        @param callback Callback function to verify DSC video
        @param vic Video identification code for a 4320p format
        @param test10 Indicates testing 10-bit RGB, 12-bit otherwise
        @param minPixRate Indicates minimum (99.5%) pixel rate,
            max (100.5%) otherwise
        @param maxFrlRate Indicates the highest FRL rate supported by the DUT
        @param cdf Optional CDF file to use
        @return TLqdResult"""

        cmd = 'ct HFR2-83 -v' + str(vic)
        if test10:
            cmd = cmd + ' -0'
        else:
            cmd = cmd + ' -2'
        if minPixRate:
            cmd = cmd + ' -C'
        if maxFrlRate:
            cmd = cmd + ' -F'
        return self.runHdmiSinkTest(cmd, callback, cdf)

    def runHfr2_84(self, callback, vic, ycc420, minPixRate, maxFrlRate,
                   cdf=None):

        """Execute DSC sink test HFR2-84

        This test verifies that the Sink DUT supports 2160p 4:2:2 and/or 4:2:0
        Primary Compressed Formats indicated in the EDID when in FRL mode

        @param self the TLqdInstrument object
        @param callback Callback function to verify DSC video
        @param vic Video identification code for a 2160p format
        @param ycc420 Indicates testing YCbCr 4:2:0, 4:2:2 otherwise
        @param minPixRate Indicates minimum (99.5%) pixel rate,
            max (100.5%) otherwise
        @param maxFrlRate Indicates the highest FRL rate supported by the DUT
        @param cdf Optional CDF file to use
        @return TLqdResult"""

        cmd = 'ct HFR2-84 -v' + str(vic)
        if ycc420:
            cmd = cmd + ' -0'
        else:
            cmd = cmd + ' -2'
        if minPixRate:
            cmd = cmd + ' -C'
        if maxFrlRate:
            cmd = cmd + ' -F'
        return self.runHdmiSinkTest(cmd, callback, cdf)

    def runHfr2_85(self, callback, vic, ycc420, minPixRate, maxFrlRate,
                   cdf=None):

        """Execute DSC sink test HFR2-85

        This test verifies that the Sink DUT supports 4320p 4:2:2 and/or 4:2:0
        Primary Compressed Formats indicated in the EDID when in FRL mode

        @param self the TLqdInstrument object
        @param callback Callback function to verify DSC video
        @param vic Video identification code for a 4320p format
        @param ycc420 Indicates testing YCbCr 4:2:0, 4:2:2 otherwise
        @param minPixRate Indicates minimum (99.5%) pixel rate,
            max (100.5%) otherwise
        @param maxFrlRate Indicates the highest FRL rate supported by the DUT
        @param cdf Optional CDF file to use
        @return TLqdResult"""

        cmd = 'ct HFR2-85 -v' + str(vic)
        if ycc420:
            cmd = cmd + ' -0'
        else:
            cmd = cmd + ' -2'
        if minPixRate:
            cmd = cmd + ' -C'
        if maxFrlRate:
            cmd = cmd + ' -F'
        return self.runHdmiSinkTest(cmd, callback, cdf)

    def runHfr2_94(self, callback, rateInkHz, nOption, cdf=None):

        """Execute HDMI sink test HFR2-94

        This test verifies that whenever the Sink DUT receives a supported
        audio format, it properly decodes and renders it

        @param self the TLqdInstrument object
        @param callback Callback function to verify audio
        @param rateInkHz Audio sampling rate in kHz
        @param nOption N option ()
        @param cdf Optional CDF file to use
        @return TLqdResult"""

        cmd = 'ct HFR2-94 -s' + str(rateInkHz) + ' -n' + str(nOption)
        return self.runHdmiSinkTest(cmd, callback, cdf)

    def capture(self, type, sizePct, localDirectory=None, qdDirectory=None,
                triggerMode=None, triggerType=None, position=None,
                hotplugDuration=None, videoCheck=False, getVideo=False,
                timing=False, interpret=False, interpretScambling=False,
                triggerData=None, triggerMask=None, triggerLaneMask=None,
                triggerDpcdAddress=None, captureTimeLimit=None,
                getDsc=False, getAca=False):
        """Perform a capture

        @param self the TLqdInstrument object
        @param type TLqdCaptureType Type of capture
        @param sizePct Amount of memory in percent to use
        @param localDirectory Folder path to store capture artifacts
        @param qdDirectory instrument directory path to capture artifacts
        @param triggerMode TLqdTriggerMode Trigger mode
        @param triggerType TLqdTriggerType Type of trigger
        @param position Trigger position
        @param hotplugDuration Duration of hot-plug in milliseconds
        @param videoCheck Perform a video check
        @param getVideo Extract video frames
        @param timing Perform timing analysis
        @param interpret Interpret data islands
        @param interpretScambling Interpret scrambling
        @param triggerData trigger based on this data value
        @param triggerMask trigger based on mask for data value
        @param triggerLaneMask trigger based on mask for lanes
        @param triggerDpcdAddress trigger based on this dpcd address
        @param captureTimeLimit capture until this time limit in milliseconds
        @param getDsc Extract and uncompress Dsc frames
        @param getAca Collect ACA logs during capture
        @return TLqdResult"""

        cmd = 'capture -t' + str(type) + ' -s' + str(sizePct)
        if triggerMode is not None:
            cmd = cmd + ' -m' + str(triggerMode)
        if triggerType is not None:
            cmd = cmd + ' -g' + str(triggerType)
        if position is not None:
            cmd = cmd + ' -p' + str(position)
        if hotplugDuration is not None:
            cmd = cmd + ' -h' + str(hotplugDuration)
        if videoCheck:
            cmd = cmd + ' -v'
        if getVideo:
            cmd = cmd + ' -i'
        if timing:
            cmd = cmd + ' -T'
        if interpret:
            cmd = cmd + ' -I'
        if interpretScambling:
            cmd = cmd + ' -S'
        if triggerData is not None:
            cmd = cmd + ' -b' + str(triggerData)
        if triggerMask is not None:
            cmd = cmd + ' -M' + str(triggerMask)
        if triggerLaneMask is not None:
            cmd = cmd + ' -l' + str(triggerLaneMask)
        if triggerDpcdAddress is not None:
            cmd = cmd + ' -a' + str(triggerDpcdAddress)
        if captureTimeLimit is not None:
            cmd = cmd + ' -C' + str(captureTimeLimit)
        if getDsc:
            cmd = cmd + ' -D'
        if getAca:
            cmd = cmd + ' -A'

        deleteRemote = qdDirectory is None
        if (localDirectory is not None or
            qdDirectory is not None):
            qdDirectory = self.prepareDirectories(localDirectory, qdDirectory)
            cmd = cmd + ' -d' + qdDirectory

        result = self.command(TLqdApiTag + cmd)
        self.transferResults(localDirectory, qdDirectory)

        # Clean up the directory on the quantumdata instrument
        if deleteRemote and qdDirectory is not None:
            self.command('exec rm -fr ' + qdDirectory)

        return self.compileCommandResult(result)

    ## @cond
    def parseDpcd(self, input):
        ret = []
        for i in range(0, len(input), 2):
            ret.append(int(input[i:i+2], 16))
        return ret
    ## @endcond

    def readCapabilityRegisters(self, register, quantity=1):

        """Read DisplayPort capability register(s) from the sink

        Reading capability registers is a source function.

        @param self the TLqdInstrument object
        @param register First register to read
        @return collection of register values"""

        if self.cardUsed is None:
            return []

        prefix = 'OUT' + str(self.cardUsed) + '0:'
        if isinstance(register, str):
            register = int(register, 16)
        register = "%X" % (register, ) # Value is in hex
        cmd = prefix + 'DPTX:DPCD? ' + register + ' ' + str(quantity)
        return self.parseDpcd(self.command(cmd))

    def getCapabilityRegisters(self, register, quantity=1):

        """Get the current DisplayPort capability register(s) from the sink

        The capability registers are set in the quantumdata DP sink

        @param self the TLqdInstrument object
        @param register First register to return
        @return collection of register values"""

        if self.cardUsed is None:
            return []

        prefix = 'OUT' + str(self.cardUsed) + '0:'
        if isinstance(register, str):
            register = int(register, 16)
        register = "%X" % (register, ) # Value is in hex
        cmd = prefix + 'rxcapr ' + register + ' ' + str(quantity)
        return self.parseDpcd(self.command(cmd))

    def setCapabilityRegisters(self, firstRegister, values):

        """Set new DisplayPort capability register(s) on the sink

        The capability registers are set in the quantumdata DP sink

        @param self the TLqdInstrument object
        @param register First register to set
        @param values collection of register values"""

        if self.cardUsed is None:
            return

        prefix = 'OUT' + str(self.cardUsed) + '0:'
        if isinstance(firstRegister, str):
            firstRegister = int(firstRegister, 16)
        firstRegister = "%X" % (firstRegister, ) # Value is in hex
        cmd = prefix + 'rxcapw ' + firstRegister
        for value in values:
            if isinstance(value, str):
                value = int(value, 16)
            value = "%X" % (value, ) # Value is in hex
            cmd = cmd + ' ' + value
        self.command(cmd)

    def getTestAutoRegister(self, register):

        """Get the current Test Auto register from the sink

        The Test Auto registers are set in the quantumdata DP sink

        @param self the TLqdInstrument object
        @param register register address to read
        @return register value in hex"""

        if self.cardUsed is None:
            return 0

        prefix = 'OUT' + str(self.cardUsed) + '0:'
        if isinstance(register, str):
            register = int(register, 16)
        register = "%X" % (register, ) # Value is in hex
        cmd = prefix + 'rxtestautor ' + register
        return hex(self.command(cmd))

    def setTestAutoRegister(self, register, value):

        """Set new Test Auto register on the sink

        The Test Auto register is set in the quantumdata DP sink

        @param self the TLqdInstrument object
        @param register register address to write
        @param value register value
        @return String empty string for success or ERROR for failure"""

        if self.cardUsed is None:
            return

        prefix = 'IN' + str(self.cardUsed) + '0:'
        if isinstance(register, str):
            register = int(register, 16)
        register = "%X" % (register, ) # Address is in hex

        cmd = prefix + 'rxtestautow ' + register

        if isinstance(value, str):
            value = int(value, 16)
        value = "%X" % (value, ) # Value is in hex

        cmd = cmd + ' ' + str(value)
        return self.command(cmd)

    def setAudio(self, audio):

        """Set audio LPCM

        @param self the TLqdInstrument object
        @param audio TLqdAudio object
        @return TLqdResult"""

        cmd = TLqdApiTag + 'set_audio'
        if audio.sampling:
            cmd = cmd + ' -r ' + str(audio.sampling)
        if audio.bitSize:
            cmd = cmd + ' -b ' + str(audio.bitSize)
        if audio.channels:
            delim = ''
            freqs = ' -f'
            amps = ' -a'
            for channel in audio.channels:
                freqs = freqs + delim + str(channel.frequency)
                amps = amps + delim + str(channel.amplitude)
                delim = ','
            cmd = cmd + freqs + amps
        return self.compileCommandResult(self.command(cmd))

    ## @cond
    def parseAudioData(self, output):
        freq = 0
        bits = 0
        channels = []
        tag = 'Rate:'
        pos = output.find(tag)
        if pos >= 0:
            output = output[pos+len(tag):]
            tag = 'Hz, bits:'
            pos = output.find(tag)
            if pos >= 0:
                freq = output[:pos]
                output = output[pos+len(tag):]
                tag = ', channels:'
                pos = output.find(tag)
                if pos >= 0:
                    bits = output[:pos]
                    output = output[pos+len(tag):]
                    if output[0] == '[': # List of channel data?
                        output = output[1:]
                    else: # A count of channels, not a list
                        channels = int(output)
                        output = ''
                    done = len(output) <= 0
                    while not done:
                        endFreq = 'Hz,'
                        endAmp = 'dB'
                        posFreq = output.find(endFreq)
                        posAmp = output.find(endAmp)
                        if posFreq >= 0 and posAmp >= 0:
                            chan = TLqdAudioChannel(0, 0)
                            chan.frequency = output[:posFreq]
                            output = output[posFreq+len(endFreq):]
                            posAmp = output.find(endAmp)
                            chan.amplitude = output[:posAmp]
                            output = output[posAmp+len(endAmp)+1:]
                            channels.append(chan)
                        else:
                            done = True;
                else:
                    bits = output
            else:
                freq = output
        return TLqdAudio(freq, bits, channels)

    ## @endcond

    def getAudio(self):

        """Get the audio LPCM metrics in use

        @param self the TLqdInstrument object
        @return TLqdAudio object"""

        cmd = TLqdApiTag + 'get_audio'
        output = self.command(cmd)
        return self.parseAudioData(output)

    ## @cond
    def parseCompEntry(self, entry):

        # entry is in the format:
        # "name", X(X), channel or subtype, sampling, layoutB
        # Channel or subtype, sampling and layoutB may not be present
        name = ''
        type = ''
        sampling = None
        channels = None
        layoutB = False
        pos = entry.find(', layoutB')
        if pos > 0:
            layoutB = True
            entry = entry[:pos]
        end = entry.find('", ')
        if end > 0 and entry[0] == '"':
            name = entry[1:end]
            entry = entry[end+3:]
            end = entry.find(', ')
            if end > 0:
                type = entry[:end]
                entry = entry[end+2:]
                tag = ', Sampling: '
                end = entry.find(tag)
                if end > 0:
                    channels = entry[:end]
                    sampling = entry[end+len(tag):]
                else:
                    channels = entry
            else:
                type = entry
        if channels:
            tag = 'Channels: '
            pos = channels.find(tag)
            if pos >= 0:
                channels = channels[len(tag):]
        return TLqdCompressedAudio(name, type, channels, sampling, layoutB)
    ## @endcond

    ## @cond
    def parseRxAudioData(self, output):
        lpcm = None
        comp = None
        pos = output.find("LPCM: ")
        if pos == 0:
            lpcm = self.parseAudioData(output[6:])
        else:
            pos = output.find("Compressed: ")
            if pos == 0:
                comp = self.parseCompEntry('"1", ' + output[12:])
        return TLqdReceivedAudio(lpcm, comp)

    ## @endcond

    def listCompressedAudio(self):

        """Get a list of compressed audio formats

        @param self the TLqdInstrument object
        @return Collection of TLqdCompressedAudio objects"""

        ret = []
        cmd = TLqdApiTag + 'list_comp_audio'
        output = self.command(cmd)
        for line in output.split('\n'):
            ret.append(self.parseCompEntry(line))
        return ret

    def setCompressedAudio(self, name):

        """Set a compressed audio format

        @param self the TLqdInstrument object
        @param name Name of the compressed audio format
        @return TLqdResult"""

        cmd = TLqdApiTag + 'set_comp_audio ' + str(name)
        return self.compileCommandResult(self.command(cmd))

    def getCompressedAudio(self):

        """Get the compressed audio format in use

        @param self the TLqdInstrument object
        @return TLqdCompressedAudio object"""

        entry = self.command(TLqdApiTag + 'get_comp_audio')
        return self.parseCompEntry(entry)

    def setEarcAudio(self, audio):

        """Set eARC audio LPCM

        @param self the TLqdInstrument object
        @param audio TLqdAudio object
        @return TLqdResult"""

        cmd = TLqdApiTag + 'set_earc_audio'
        if audio.sampling:
            cmd = cmd + ' -r ' + str(audio.sampling)
        if audio.bitSize:
            cmd = cmd + ' -b ' + str(audio.bitSize)
        if audio.channels:
            delim = ''
            freqs = ' -f'
            amps = ' -a'
            for channel in audio.channels:
                freqs = freqs + delim + str(channel.frequency)
                amps = amps + delim + str(channel.amplitude)
                delim = ','
            cmd = cmd + freqs + amps
        return self.compileCommandResult(self.command(cmd))

    def getEarcAudio(self):

        """Get the eARC audio LPCM metrics in use

        @param self the TLqdInstrument object
        @return TLqdAudio object"""

        cmd = TLqdApiTag + 'get_earc_audio'
        output = self.command(cmd)
        return self.parseAudioData(output)

    def listEarcCompressedAudio(self):

        """Get a list of eARC compressed audio formats

        @param self the TLqdInstrument object
        @return Collection of TLqdCompressedAudio objects"""

        ret = []
        cmd = TLqdApiTag + 'list_earc_comp_audio'
        output = self.command(cmd)
        for line in output.split('\n'):
            ret.append(self.parseCompEntry(line))
        return ret

    def setEarcCompressedAudio(self, name, layoutB=False):

        """Set an eARC compressed audio format

        @param self the TLqdInstrument object
        @param name Name of the compressed audio format
        @param layoutB Indicates layout B is used
        @return TLqdResult"""

        cmd = TLqdApiTag + 'set_earc_comp_audio '
        if layoutB:
            cmd = cmd + '-B '
        cmd = cmd + str(name)
        return self.compileCommandResult(self.command(cmd))

    def getEarcCompressedAudio(self):

        """Get the eARC compressed audio format in use

        @param self the TLqdInstrument object
        @return TLqdCompressedAudio object"""

        entry = self.command(TLqdApiTag + 'get_earc_comp_audio')
        return self.parseCompEntry(entry)

    def getReceivedEarcAudio(self):

        """Get the eARC audio being received

        @param self the TLqdInstrument object
        @return TLqdReceivedAudio object"""

        cmd = TLqdApiTag + 'get_earc_rx_audio'
        output = self.command(cmd)
        return self.parseRxAudioData(output)

    def setEdidFile(self, edidFile, hpDurationInMs=100):
        """Set the EDID file on the device

        @param self the TLqdInstrument object
        @param edidFile Local file in XML format to load
        @param hpDurationInMs Hot-plug duration in milliseconds (0=no HP)
        @return TLqdResult"""

        self.saveEdidFile(edidFile)
        cmd = TLqdApiTag + 'edid ' + RemoteEdidFile + ' ' + str(hpDurationInMs)
        return self.compileCommandResult(self.command(cmd))

    def setEdidData(self, edidData, hpDurationInMs=100):
        """Set the EDID data on the device

        @param self the TLqdInstrument object
        @param edidData String of EDID data ("00FFFFFFFFFFFF00...")
        @param hpDurationInMs Hot-plug duration in milliseconds (0=no HP)
        @return TLqdResult"""

        self.saveEdidData(edidData)
        cmd = TLqdApiTag + 'edid ' + RemoteEdidFile + ' ' + str(hpDurationInMs)
        return self.compileCommandResult(self.command(cmd))

    def i2cVerbs(self, read=None, write=None):
        """ Set the verbs for I2C read/write

        @param self the Qd980 object
        @param read Verb for I2C read
        @param write Verb for I2C write"""

        if read:
            self.i2crVerb = read
        if write:
            self.i2cwVerb = write

    def i2cr(self, addr, reg, qty=None, system=None):
        """ Read the given I2C register values

        @param self the TLqdInstrument object
        @param addr I2C address
        @param reg I2C register
        @param qty Optional quantity
        @param system Optional I2C system ID"""

        i2cCmd = self.i2crVerb
        if system is not None:
            i2cCmd = i2cCmd + " " + str(system)
        i2cCmd = i2cCmd + " " + format(addr, 'x') + " " + format(reg, 'x')
        if qty:
            i2cCmd = i2cCmd + " " + format(qty, 'x')
        return self.command(i2cCmd)

    def i2cw(self, addr, reg, value, system=None):
        """ Write the given value to the I2C register

        @param self the TLqdInstrument object
        @param addr I2C address
        @param reg I2C register
        @param value Value to write
        @param system Optional I2C system ID"""

        i2cCmd = self.i2cwVerb
        if system is not None:
            i2cCmd = i2cCmd + " " + str(system)
        i2cCmd = i2cCmd + " " + format(addr, 'x') + " " + format(reg, 'x') + \
            " " + format(value, 'x')
        self.command(i2cCmd)

    def enableOutput(self, enabled):
        """ Enable/disable output

        @param self the TLqdInstrument object
        @param enabled Indicates if output is enabled or disabled"""

        opt = '0'
        if enabled:
            opt = '1'
        self.command(TLqdApiTag + 'output ' + opt)

    def isOutputEnabled(self):
        """ Is output enabled/disabled

        @param self the TLqdInstrument object
        @return True if output is enabled"""

        return int(self.command(TLqdApiTag + 'output')) != 0

def TLqdConnectTelnet(ip, user='qd', passwd='qd', port=None):

    """Connect to a quantumdata instrument via telnet

    *NOTE* If the connection cannot be established, this method will still
    return a TLqdInstrument. The connection status can be checked
    by examining @ref TLqdInstrument.connected

    @param ip Internet address or host name
    @param user User ID - defaults to "qd"
    @param passwd Password - defaults to "qd"
    @param port Port number for telnet - defaults to None
    @return TLqdInstrument object"""

    qdDev = TLqdInstrument(ip, user, passwd, False, port)
    return qdDev

def TLqdConnectSsh(ip, user='qd', passwd='qd', port=None):

    """Connect to a quantumdata instrument via ssh

    *NOTE* If the connection cannot be established, this method will still
    return a TLqdInstrument. The connection status can be checked
    by examining @ref TLqdInstrument.connected

    @param ip Internet address or host name
    @param user User ID - defaults to "qd"
    @param passwd Password - defaults to "qd"
    @param port Port number for ssh - defaults to None
    @return TLqdInstrument object"""

    qdDev = TLqdInstrument(ip, user, passwd, True, port)
    return qdDev

def TLqdCommand(qdDev, cmd):

    """Execute a command

    See @ref TLqdInstrument.command for details

    @param qdDev Interface to quantumdata instrument
    @param cmd Command to send (newline isn't needed)
    @return String output from command"""

    return qdDev.command(cmd)

def TLqdVersion(qdDev):

    """Obtain version data about the quantumdata instrument

    @param qdDev Interface to quantumdata instrument
    @return String with version information"""

    return qdDev.getVersion()

def TLqdDiscover(qdDev):

    """Obtain data about what is installed on the quantumdata instrument

    @param qdDev Interface to quantumdata instrument
    @return list of installed cards"""

    return qdDev.getDiscover()

def TLqdLicenses(qdDev):

    """Obtain data about what is licensed on the quantumdata instrument

    @param qdDev Interface to quantumdata instrument
    @return list of licenses"""

    return qdDev.getLicenses()

def TLqdUse(qdDev, cardNumber):

    """Select a card for use

    @param qdDev Interface to quantumdata instrument
    @param cardNumber Installed card number to use"""

    qdDev.setCardUsed(cardNumber)

def TLqdSetFormat(qdDev, name, colorSpace=None, subsampling=None,
                   bitDepth=None, vic=None):

    """Set a video format

    @param qdDev Interface to quantumdata instrument
    @param name Format name
    @param colorSpace TLqdColorSpace
    @param subsampling TLqdSubsampling
    @param vic Video identification code
    @param bitDepth Number of bits/pixel
    @return TLqdResult"""

    return qdDev.setFormat(name, colorSpace, subsampling, bitDepth, vic)

def TLqdUpdateVtem(qdDev, vrrEn=None, mConst=None, reducedBlanking=None,
                   fvaFactorM1=None, baseVfront=None, baseRefreshRate=None):
    """Update Video Timing Extended Metadata

    @param qdDev Interface to quantumdata instrument
    @param vrrEn Vrr enable
    @param mConst mConst value
    @param reducedBlanking Reduced blanking value
    @param fvaFactorM1 Fast vactive factor minus 1
    @param baseVfront Base vfront
    @param baseRefreshRate Base refresh rate
    @return TLqdResult"""

    return qdDev.updateVtem(vrrEn, mConst, reducedBlanking, fvaFactorM1, baseVfront, baseRefreshRate)

def TLqdSet3dFormat(qdDev, threeDformat, name=""):

    """Set a 3D video format

    @param qdDev Interface to quantumdata instrument
    @param threeDformat the TLqd3dData object
    @param name Optional format name
    @return TLqdResult"""

    return qdDev.set3dFormat(threeDformat, name)

## @cond
class InputType(object):
    def __init__(self, type):
        self.type = type

    def __str__(self):
        return str(self.type)

    def __eq__(self, other):
        # Check for another InputType
        if isinstance(other, InputType):
            return self.type == other.type
        # Check for a number
        if isinstance(other, self.type.__class__):
            return self.type == other
        # Who knows what we were given
        return self.type == int(type)

    def __ne__(self, other):
        return not self.__eq__(other)
## @endcond

class TLqdLinkTrainingType(InputType):
    """@brief Link Training Type

    Used to specify Link Training Type"""

    def __init__(self, type):

        """Specify a Link Training Type

        @param self the TLqdLinkTrainingType object
        @param linkTrainingType Link Training Type"""

        InputType.__init__(self, type)

    ## Link Training Type Adaptive
    LinkTrainingTypeAdaptive = InputType(1)
    ## Link Training Type non Adaptive
    LinkTrainingTypeNonAdaptive = InputType(2)

class TLqdLinkTrainingMethod(InputType):
    """@brief DP Link Training Method

    Used to specify a DP Link Training Method"""

    def __init__(self, type):

        """Specify a DP Link Training Method

        @param self the TLqdLinkTrainingMethod object
        @param linkTrainingMethod Link Training Method"""

        InputType.__init__(self, type)

    ## Link Training Method Legacy
    LinkTrainingMethodLegacy = InputType(1)
    ## Link Training Method UHBR
    LinkTrainingMethodUHBR = InputType(2)

class TLqdLttpr8b10bMethod(InputType):
    """@brief DP Lttpr 8b10b Link training Method

    Used to specify a DP Lttpr 8b10b Link Training Method"""

    def __init__(self, type):

        """Specify a DP Lttpr 8b10b Link Training Method

        @param self the TLqdLttpr8b10bMethod object
        @param lttpr8b10bMethod Lttpr 8b10b Link Training Method"""

        InputType.__init__(self, type)

    ## 8b10b Link Training Method Transparent
    LinkTrainingMethodTransparent = InputType(1)
    ## 8b10b Link Training Method Non Transparent
    LinkTrainingMethodNonTransparent = InputType(2)

class TLqdLinkRate(InputType):
    """@brief Link Rate

    Used to specify a Link Rate"""

    def __init__(self, type):

        """Specify Link Rate

        @param self the TLqdLinkRate object
        @param linkRate Link Rate"""

        InputType.__init__(self, type)

    ## Link Rate RBR
    LinkRateRBR = InputType(0x6)
    ## Link Rate HBR
    LinkRateHBR = InputType(0xA)
    ## Link Rate HBR2
    LinkRateHBR2 = InputType(0x14)
    ## Link Rate HBR3
    LinkRateHBR3 = InputType(0x1E)
    ## Link Rate UHBR10
    LinkRateUHBR10 = InputType(0x21)
    ## Link Rate UHBR135
    LinkRateUHBR135 = InputType(0x24)
    ## Link Rate UHBR20
    LinkRateUHBR20 = InputType(0x22)

def TLqdSetLinkTraining(qdDev,
    linkTrainingType=TLqdLinkTrainingType.LinkTrainingTypeAdaptive,
    linkTrainingMethod=None, lttpr8b10bMethod=None, laneCount=None,
    linkRate=None, vsLevel=None, peLevel=None, ffe=None, retry=True,
    fec=False, synchronousClock=True, spreadSpectrum=False):
    """Set link training

    @param qdDev Interface to quantumdata instrument
    @param linkTrainingType Optional TLqdLinkTrainingType, defaults to adaptive
    @param linkTrainingMethod Optional TLqdLinkTrainingMethod
    @param lttpr8b10bMethod Optional TLqdLttpr8b10bMethod
    @param laneCount Lane Count [1,2,4]
    @param linkRate Optional TLqdLinkRate
    @param vsLevel volatage Swing level [0-3]
    @param peLevel preEmphasis level [0-3]
    @param ffe ffe preset value [0-15]
    @param retry retry during link training
    @param fec fec enable/disable
    @param synchronousClock synchronousClock enable/disable
    @param spreadSpectrum spreadSpectrum enable/disable
    @return TLqdResult"""

    return qdDev.setLinkTraining(linkTrainingType, linkTrainingMethod,
                                 lttpr8b10bMethod, laneCount, linkRate, vsLevel,
                                 peLevel, ffe, retry, fec, synchronousClock,
                                 spreadSpectrum)

class TLqdHotPlugMode(InputType):
    """@brief Hot Plug Mode

    Used to specify a Hot Plug Mode"""

    def __init__(self, type):

        """Specify a hot plug mode

        @param self the TLqdHotPlugMode object
        @param mode Hot Plug Mode"""

        InputType.__init__(self, type)

    ## Hotplug line in low mode.
    HotPlugModeLow = InputType(1)
    ## Hotplug line in high mode.
    HotPlugModeHigh = InputType(2)

def TlqdSetHotPlug(qdDev, duration=None, mode=None):

    """ Set Hot Plug

    @param qdDev Interface to quantumdata instrument
    @param duration Hot Plug duration in milli second
    @param mode Optional TLqdHotPlugMode
    @return TLqdResult"""

    return qdDev.setHotPlug(duration, mode)

def TlqdGetSinkTestCrc(qdDev):

    """Get Sink Test CRC Info
    @param qdDev Interface to quantumdata instrument
    @return TLqdCrcParameters"""

    return qdDev.getSinkTestCrc()

def TlqdGetRxLinkTrainingStatus(qdDev):

    """Get Rx Link Training Status

    @param qdDev Interface to quantumdata instrument
    @return TLqdRxLinkTrainingStatus"""

    return qdDev.getRxLinkTrainingStatus()

def TlqdGetErrorInfo(qdDev):

    """Get Error Info
    @param qdDev Interface to quantumdata instrument
    @return TLqdDpErrorInfoParameters"""

    return qdDev.getErrorInfo()

def TlqdGetCrc(qdDev, port, dsc):

    """Get CRC Info
    @param qdDev Interface to quantumdata instrument
    @param port TLqdPort
    @param dsc optional to parameter to collect dsc crc
    @return TLqdCrcParameters"""

    return qdDev.getCrc(port, dsc)

class TLqdDisplayPortCtsType(InputType):
    """@brief display port CTS type

    Used to specify a display port CTS type"""

    def __init__(self, type):

        """Specify a display port CTS type

        @param self the TLqdDisplayPortCtsType object
        @param type display port CTS type"""

        InputType.__init__(self, type)

    ## DP Source CTS 1.2 Core
    Dp12SourceCore = InputType(1)
    ## DP Sink CTS 1.2 Core
    Dp12SinkCore = InputType(2)
    ## DP 1.4a Source CTS Core
    Dp14aSourceCore = InputType(3)
    ## DP 1.4a Sink CTS Core
    Dp14aSinkCore = InputType(4)
    ## DP 1.4a DSC Source CTS
    Dp14aDscSource = InputType(5)
    ## DP 1.4a DSC Sink CTS
    Dp14aDscSink = InputType(6)
    ## DP Adaptive-Sync Source CTS
    DpAdaptiveSyncSource = InputType(7)
    ## DP Adaptive-Sync Sink CTS
    DpAdaptiveSyncSource = InputType(8)
    ## DP Edid Source CTS
    DpEdidSource = InputType(9)
    ## DP Edid Sink CTS
    DpEdidSink = InputType(10)
    ## DP 2.0 Source CTS Core
    Dp20SourceCore = InputType(11)
    ## DP 2.0 Sink CTS Core
    Dp20SinkCore = InputType(12)
    ## DP 2.0 LTTPR Device CTS Core
    Dp20LttprDeviceCore = InputType(13)

def TLqdGetDpTestDescr(qdDev, type=TLqdDisplayPortCtsType.Dp14aSourceCore, testId='4.3.1.1'):
    """Get DP compliance test description for the given test

    @param qdDev Interface to quantumdata instrument
    @param type Optional TLqdDisplayPortCtsType, defaults to DP 1.4a Source CTS Core
    @param testId Optional Test ID, defaults to 4.3.1.1
    @return String containing test description"""

    return qdDev.getDpTestDescr(type, testId)

def TlqdGetTxLinkTrainingStatus(qdDev):

    """Get Tx Link Training Status

    @param qdDev Interface to quantumdata instrument
    @return TLqdTxLinkTrainingStatus"""

    return qdDev.getTxLinkTrainingStatus()

def TLqdGetSinkStatus(qdDev):

    """Get Sink Status

    @param qdDev Interface to quantumdata instrument
    @return TLqdMsaParameters, TLqdVstatParameters"""

    return qdDev.getSinkStatus()

def TLqdGetLinkTrainingTime(qdDev):

    """Get Link Training Time

    @param qdDev Interface to quantumdata instrument
    @return TLqdLinkTrainingTime"""

    return qdDev.getLinkTrainingTime()

def TLqdGetTimingReport(qdDev, type, reportTime=None, localDirectory=None, qdDirectory=None):

    """Get a Timing report

    @param qdDev Interface to quantumdata instrument
    @param type Type of timing report
    @param reportTime Optional Time to capture timing report in milliseconds
    @param localDirectory Optional Folder path to store timing report
    @param qdDirectory Optional Instrument directory path to timing report
    @return TLqdResult"""

    return qdDev.getTimingReport(type, reportTime, localDirectory, qdDirectory)

def TLqdGenerateTestPattern(qdDev, testPatternType=None, linkRate=None, testPatternSet=None,
                            vsLevel=None, peLevel=None, selectiveInterval=None,
                            rfbInterval=None, minRefreshRate=None, maxRefreshRate=None,
                            totalChangePeriod=None, incrementStep=None, decrementStep=None,
                            splitOption=None, sdpLocation=None, sdpClockCycles=None):
    """Generate Test pattern

    @param qdDev Interface to quantumdata instrument
    @param testPatternType Optional TLqdTestPatterType
    @param linkRate Optional TLqdLinkRate [RBR | HBR | HBR2 | HBR3]
    @param testPatternSet Optional Test pattern Set [TPS1 | TPS2| TPS3]
    @param vsLevel volatage Swing level [0-3]
    @param peLevel preEmphasis level [0-3]
    @param selectiveInterval Optional Selective Updates interval in frames
    @param rfbInterval Optional full frame RFB update interval in frames
    @param minRefreshRate Optional Minimum refresh rate, floating point number
    @param maxRefreshRate Optional Maximum refresh rate, floating point number
    @param totalChangePeriod Optional Total change period in frames
    @param incrementStep Optional Increment step in miliseconds
    @param decrementStep Optional Decrement step in miliseconds
    @param splitOption Optional Split SDP Options
    @param sdpLocation Optional SDP Clock Cycles
    @param sdpClockCycles Optional SDP location
    @return TLqdResult"""

    return qdDev.generateTestPattern(testPatternType, linkRate, testPatternSet,
                            vsLevel, peLevel, selectiveInterval,
                            rfbInterval, minRefreshRate, maxRefreshRate,
                            totalChangePeriod, incrementStep, decrementStep,
                            splitOption, sdpLocation, sdpClockCycles)

class TLqdTestPatterType(InputType):
    """@brief Test Pattern Type

    Used to specify a Test Pattern Type"""

    def __init__(self, type):

        """Specify a Test Pattern Type

        @param self the TLqdTestPatterType object
        @param mode Color Mode"""

        InputType.__init__(self, type)

    ## Test Pattern Training
    TestPatternTraining = InputType(1)
    ## Test Pattern Panel Replay
    TestPatternPanelReplay = InputType(2)
    ## Test Pattern Square
    TestPatternSquare = InputType(3)
    ## Test Pattern Zig-Zag
    TestPatternZigZag = InputType(4)
    ## Test Pattern Split SDP
    TestPatternSplitSdp= InputType(5)
    ## Test Pattern Stop
    TestPatternStop = InputType(6)

class TLqdDscColorMode(InputType):
    """@brief DSC Color Mode

    Used to specify a DSC Color Mode"""

    def __init__(self, type):

        """Specify a DSC Color Mode

        @param self the TLqdDscColorMode object
        @param mode Color Mode"""

        InputType.__init__(self, type)

    ## Color Mode RGB
    ColorModeRgb = InputType(0)
    ## Color Mode 4:4:4
    ColorMode444 = InputType(1)
    ## Color Mode 422Simple
    ColorMode422Simple = InputType(2)
    ## Color Mode 422Native
    ColorMode422Native = InputType(3)
    ## Color Mode 420Native
    ColorMode420Native = InputType(4)

def TLqdSetDsc(qdDev, image, format=None, colorMode=None,
                 bitsPerCompoment=None, bitsPerPixel=None, sliceWidth=None,
                 sliceHeight=None, blockPredictionDisable=False,
                 lineBuffer=None):
    """Set DSC paramters

    @param qdDev Interface to quantumdata instrument
    @param image image name
    @param format DSC timing format
    @param colorMode Optional TLqdDscColorMode
    @param bitsPerCompoment bits per compoments
    @param bitsPerPixel bits per pixel
    @param sliceWidth Dsc slice Width
    @param sliceHeight Dsc slice Height
    @param blockPredictionDisable block prediction disable
    @param lineBuffer line buffer depth
    @return TLqdResult"""

    return qdDev.setDsc(image, format, colorMode, bitsPerCompoment,
                          bitsPerPixel, sliceWidth, sliceHeight,
                          blockPredictionDisable, lineBuffer)

class TLqdLttprRevision(InputType):
     """@brief LTTPR Revision

     Used to specify a LTTPR Revision"""

     def __init__(self, type):

         """Specify a Lttpr Revision

         @param self the TLqdLttprRevision object
         @param revision Revision"""

         InputType.__init__(self, type)

     ## LTTPR Revision 14
     Revision14 = InputType(14)
     ## LTTPR Revision 20
     Revision20 = InputType(20)

def TlqdSetLttpr(qdDev, revision=None, eqInterlaneAlign=None,
                 cdsInterlaneAlign=None, eqDone=None, count=None):
    """Set LTTPR emulation

    @param qdDev Interface to quantumdata instrument
    @param revision Optional TLqdLttprRevision
    @param eqInterlaneAlign delay during EQ interlane Alignment
    @param cdsInterlaneAlign delay during CDS interlane Alignment
    @param eqDone return value of F0008 for EQ done status per LTTPR
    @param count number of LTTPR emulated
    @return TLqdResult"""

    return qdDev.setLttpr(revision, eqInterlaneAlign, cdsInterlaneAlign,
                          eqDone, count)

def TlqdHdcp2xTest(qdDev, testId, testParameters):
    """Execute HDCP 2.x compliance test

    @param qdDev Interface to quantumdata instrument
    @param testId Test ID to execute
    @param testParameters TLqdTestParameters
    @return TLqdResult"""

    return qdDev.runHdcp2xTest(testId, testParameters)

def TlqdHdcp1xTest(qdDev, testId, testParameters):
    """Execute HDCP 1.x compliance test

    @param qdDev Interface to quantumdata instrument
    @param testId Test ID to execute
    @param testParameters TLqdTestParameters
    @return TLqdResult"""

    return qdDev.runHdcp1xTest(testId, testParameters)

def TlqdEdidSinkTest(qdDev, testId, testParameters):
    """Execute EDID sink compliance test

    @param qdDev Interface to quantumdata instrument
    @param testId Test ID to execute
    @param testParameters TLqdTestParameters
    @return TLqdResult"""

    return qdDev.runEdidSinkTest(testId, testParameters)

def TlqdDp14SourceTest(qdDev, testName, callback, testParameters):
    """Execute DP 1.4 source compliance test

    @param qdDev Interface to quantumdata instrument
    @param testName Testname to execute Source test case
    @param callback Callback function to verify step file information
    @param testParameters TLqdTestParameters
    @return TLqdResult"""

    return qdDev.runDp14SourceTest(testName, callback, testParameters)

def TlqdDp14SinkTest(qdDev, testName, callback, testParameters):
    """Execute DP 1.4 sink compliance test

    @param qdDev Interface to quantumdata instrument
    @param testName Testname to execute Sink test case
    @param callback Callback function to verify step file information
    @param testParameters TLqdTestParameters
    @return TLqdResult"""

    return qdDev.runDp14SinkTest(testName, callback, testParameters)

def TlqdDp12SourceTest(qdDev, testName, callback, testParameters):
    """Execute DP 1.2 source compliance test

    @param qdDev Interface to quantumdata instrument
    @param testName Testname to execute Source test case
    @param callback Callback function to verify step file information
    @param testParameters TLqdTestParameters
    @return TLqdResult"""

    return qdDev.runDp12SourceTest(testName, callback, testParameters)

def TlqdDp12SinkTest(qdDev, testName, callback, testParameters):
    """Execute DP 1.2 sink compliance test

    @param qdDev Interface to quantumdata instrument
    @param testName Testname to execute Sink test case
    @param callback Callback function to verify step file information
    @param testParameters TLqdTestParameters
    @return TLqdResult"""

    return qdDev.runDp12SinkTest(testName, callback, testParameters)

def TlqdDp20SourceTest(qdDev, testName, callback, testParameters):
    """Execute DP 2.0 source compliance test

    @param qdDev Interface to quantumdata instrument
    @param testName Testname to execute Source test case
    @param callback Callback function to verify step file information
    @param testParameters TLqdTestParameters
    @return TLqdResult"""

    return qdDev.runDp20SourceTest(testName, callback, testParameters)

def TlqdDp20SinkTest(qdDev, testName, callback, testParameters):
    """Execute DP 2.0 sink compliance test

    @param qdDev Interface to quantumdata instrument
    @param testName Testname to execute Sink test case
    @param callback Callback function to verify step file information
    @param testParameters TLqdTestParameters
    @return TLqdResult"""

    return qdDev.runDp20SinkTest(testName, callback, testParameters)

def TlqdDpEdidSourceTest(qdDev, testName, callback, testParameters):
    """Execute DP edid source compliance test

    @param qdDev Interface to quantumdata instrument
    @param testName Testname to execute Source test case
    @param callback Callback function to verify step file information
    @param testParameters TLqdTestParameters
    @return TLqdResult"""

    return qdDev.runDpEdidSourceTest(testName, callback, testParameters)

def TlqdDpEdidSinkTest(qdDev, testName, callback, testParameters):
    """Execute DP edid sink compliance test

    @param qdDev Interface to quantumdata instrument
    @param testName Testname to execute Sink test case
    @param callback Callback function to verify step file information
    @param testParameters TLqdTestParameters
    @return TLqdResult"""

    return qdDev.runDpEdidSinkTest(testName, callback, testParameters)

class TLqdExportMode(InputType):
    """@brief export mode

    Used to specify a export mode"""

    def __init__(self, mode):

        """Specify a export mode

        @param self the TLqdExportMode object
        @param mode export Mode"""

        InputType.__init__(self, mode)

    ## Export Mode Text
    ExportModeText = InputType(1)
    ## Export Mode Bitmap
    ExportModeBitmap = InputType(2)

def TlqdCreateBitmaporText(qdDev, frame, mode=None, localDirectory=None, qdDirectory=None):
    """Create Video frame Bitmap or Text file

    @param qdDev Interface to quantumdata instrument
    @param frame frame number to render,
    @param mode Optional TLqdExportMode
    @param localDirectory Optional Folder path to store generated files
    @param qdDirectory Optional Instrument directory path to store files
    @return TLqdResult"""

    return qdDev.createBitmaporText(frame, mode, localDirectory, qdDirectory)

class TLqdPort(InputType):
    """@brief Port

    Used to specify a Port"""

    def __init__(self, type):

        """Specify a Port

        @param self the TLqdPort object
        @param port Port Rx or Tx"""

        InputType.__init__(self, type)

    ## port Rx
    PortRx = InputType(1)
    ## Port Tx
    PortTx = InputType(2)

class TLqdMstMode(InputType):
    """@brief MST Mode

    Used to specify a MST Mode"""

    def __init__(self, type):

        """Specify a MST Mode

        @param self the TLqdMstMode object
        @param mode Mode SST or Mode MST"""

        InputType.__init__(self, type)

    ## mode SST
    SSTMode = InputType(1)
    ## Mode MST
    MSTMode = InputType(2)

def TlqdSetMst(qdDev, port=None, mode=None, channelToShow=None,
               channelCount=None):
    """Set MST

    @param qdDev Interface to quantumdata instrument
    @param port Optional TLqdPort
    @param mode Optional TLqdMstMode
    @param channelToShow virtual channel to show [1-4]
    @param channelCount number of virtual channel to configure [1-4]
    @return TLqdResult"""

    return qdDev.setMst(port, mode, channelToShow, channelCount)

def TlqdSetSpdif(qdDev, enableSpdifOutput=None, enableTriggerOutput=None):
    """Set SPDIF

    @param qdDev Interface to quantumdata instrument
    @param enableSpdifOutput spdif output enable
    @param enableTriggerOutput trigger output enable
    @return TLqdResult"""

    return qdDev.setSpdif(enableSpdifOutput, enableTriggerOutput)

class TLqdPinAssignmentMode(InputType):
    """@brief Pin Assignment Mode

    Used to specify a Pin Assignment Mode"""

    def __init__(self, type):

        """Specify a Pin Assignment Mode

        @param self the TLqdPinAssignmentMode object
        @param mode Pin Assignment Mode D or CE"""

        InputType.__init__(self, type)

    ## Pin Assignment Mode D
    PinAssignmentModeD = InputType(1)
    ## Pin Assignment Mode CE
    PinAssignmentModeCE = InputType(2)

def TlqdSetUsb(qdDev, port=None, pinAssignment=None, powerRoleSwap=None):
    """set Usb

    @param qdDev Interface to quantumdata instrument
    @param port Optional TLqdPort
    @param pinAssignment Optional TLqdPinAssignmentMode
    @param powerRoleSwap power role swap
    @return TLqdResult"""

    return qdDev.setUsb(port, pinAssignment, powerRoleSwap)

class TLqdHdcpMode(InputType):
    """@brief HDCP Mode

    Used to specify a HDCP Mode"""

    def __init__(self, type):

        """Specify a HDCP Mode

        @param self the TLqdHdcpMode object
        @param mode Mode Hdcp13 or Mode Hdcp23 or HdcpNone to disable"""

        InputType.__init__(self, type)

    ## mode HDCP13
    HDCP13Mode = InputType(1)
    ## Mode HDCP23
    HDCP23Mode = InputType(2)
    ## Mode HDCPNone
    HDCPNone = InputType(3)

def TlqdSetHdcp(qdDev, port, mode, key=None, repeater=None, repDepth=None, repDeviceCount=None):
    """Set HDCP

    @param port TLqdPort
    @param mode TLqdHdcpMode
    @param key Optional HDCP Key (1:prod, 2:facsimile1, 3:facsimile2)
    @param repeater Optional Repeater config value
    @param repDepth Optional Repeater Depth value
    @param repDeviceCount Optional Repeater Device Count value
    @return TLqdResult"""

    return qdDev.setHdcp(port, mode, key, repeater, repDepth, repDeviceCount)

def TlqdGetHdcp(qdDev, port, mode):
    """Get HDCP

    @param port TLqdPort
    @param mode TLqdHdcpMode
    @return TLqdHdcpParameters"""

    return qdDev.getHdcp(port, mode)

def TLqdGetFormat(qdDev):

    """Get the current video format data

    @param qdDev Interface to quantumdata instrument
    @return string describing the current format"""

    return qdDev.getFormat()

def TLqdGetFormatParameters(qdDev, all=False):

    """Get the current video format data parameters

    @param qdDev Interface to quantumdata instrument
    @param all Optional indicator to get *all* format parameters instead of
    the essential ones
    @return TLqdVideoFormatParameters"""

    return qdDev.getFormatParameters(all)

def TLqdUpdateFormatParameters(qdDev, params):

    """Update video format parameters

    @param qdDev Interface to quantumdata instrument
    @param params TLqdVideoFormatParameters
    @return TLqdResult"""

    return qdDev.updateFormatParameters(params)

def TLqdUseFormatParameters(qdDev, params):

    """Set a new video format using parameters

    @param qdDev Interface to quantumdata instrument
    @param params TLqdVideoFormatParameters
    @return TLqdResult"""

    return qdDev.useFormatParameters(params)

def TLqdListFormats(qdDev):

    """Get the list of video format names

    @param qdDev Interface to quantumdata instrument
    @return list of format names"""

    return qdDev.listFormats()

def TLqdGet3dFormat(qdDev):

    """Get the current 3D video format data

    @param qdDev Interface to quantumdata instrument
    @return TLqd3dData"""

    return qdDev.get3dFormat()

def TLqdSetImage(qdDev, name):

    """Set a video image

    @param qdDev Interface to quantumdata instrument
    @param name Image name
    @return TLqdResult"""

    return qdDev.setImage(name)

def TLqdGetImage(qdDev):

    """Get the current video image name

    @param qdDev Interface to quantumdata instrument
    @return Current image name"""

    return qdDev.getImage()

def TLqdUpdateImage(qdDev):

    """Update a video image

    @param qdDev Interface to quantumdata instrument"""

    return qdDev.updateImage()

class InfoFrame(IntValue):
    def __init__(self, value):
        IntValue.__init__(self, value)

    def __str__(self):
        if int(self.value) == 0:
            return 'GIF_IF'
        if int(self.value) == 1:
            return 'AVI_IF'
        if int(self.value) == 2:
            return 'SPD_IF'
        if int(self.value) == 3:
            return 'AUD_IF'
        if int(self.value) == 4:
            return 'MPEG_IF'
        if int(self.value) == 5:
            return 'GIF2_IF'
        if int(self.value) == 6:
            return 'XVYCC_GBD_PACKET'
        if int(self.value) == 7:
            return 'HDMI_VS_IF'
        if int(self.value) == 8:
            return 'HDMI_FORUM_VS_IF'
        if int(self.value) == 9:
            return 'AUDIO_METADATA'
        if int(self.value) == 10:
            return 'HDR_IF'
        if int(self.value) == 11:
            return 'ACP_PACKET'
        if int(self.value) == 12:
            return 'ISRC1_PACKET'
        if int(self.value) == 13:
            return 'ISRC2_PACKET'
        if int(self.value) == 14:
            return 'VTEM_PACKET'
        if int(self.value) == 15:
            return 'CVTEM_PACKET'
        if int(self.value) == 16:
            return 'HDR_EM_PACKET'
        if int(self.value) == 17:
            return 'EMDS_PACKET'
        if int(self.value) == 18:
            return 'DOLBY_VS_IF'

        return str(self.value)

class TLqdInfoFrameType(InfoFrame):

    """@brief Info Frame type

    Used to specify a Info Frame packet type"""

    def __init__(self, type):

        """Specify a Info Frame packet type

        @param self the TLqdInfoFrameType object
        @param type InfoFrame index"""

        InputType.__init__(self, type)

    ## GIF
    GifInfoFrame     = InfoFrame(0)
    ## AVI
    AviInfoFrame     = InfoFrame(1)
    ## SPD
    SpdInfoFrame     = InfoFrame(2)
    ## AUDIO
    AudInfoFrame     = InfoFrame(3)
    ## MPEG
    MpegInfoFrame    = InfoFrame(4)
    ## GIF2
    Gif2InfoFrame    = InfoFrame(5)
    ## XVYCC_GBD
    XvyccGbdPacket   = InfoFrame(6)
    ## HDMI_VSI
    HdmiVSInfoFrame  = InfoFrame(7)
    ## HDMI_FORUM_VS
    HdmiforumVInfoFrame = InfoFrame(8)
    ## AUDIO_METADATA
    AudioMetaData    = InfoFrame(9)
    ## HDR
    HDRInfoFrame     = InfoFrame(10)
    ## ACP
    ACPPacket        = InfoFrame(11)
    ## ISRC1
    ISRC1Packet      = InfoFrame(12)
    ## ISRC2
    ISRC2Packet      = InfoFrame(13)
    ## VTEM
    VTEMPacket       = InfoFrame(14)
    ## CVTEM
    CVTEMPacket      = InfoFrame(15)
    ## HDREM
    HDREMPacket      = InfoFrame(16)
    ## EMDS
    EMDSPacket       = InfoFrame(17)
    ## DOLBY_VS
    DOLBYVSInfoFrame = InfoFrame(18)

def TLqdConfigInfoFrame(qdDev, type=None, enable=False):

    """Enable/Disable the Info frame packets

    @param type TLqdInfoFrameType
    @param enable bool to enable/disable InfoFrame packets
    @return TLqdResult"""

    return qdDev.configInfoFrame(type, enable)

def TLqSetInfoFrame(qdDev, count=None, valid=None, status=None,
                  isrc1Data=None, isrc2Data=None, acpType=None,
                  acpData=None):

    """Set the the Info Frame Packet data(ISRC1, ISRC2 and ACP)

    @param count Isrc1 count value
    @param valid Isrc1 valid value
    @param status Isrc1 status value
    @param isrc1Data Isrc1 data value
    @param isrc2Data Isrc2 data value
    @param acpType Acp type value
    @param acpData Acp data value
    @return TLqdResult"""

    return qdDev.setInfoFrameData(count, valid, status, isrc1Data,
                                  isrc2Data, acpType, acpData)

def TLqdGetInfoFrameData(qdDev):

    """Get the Info Frame Packet data(ISRC1, ISRC2 and ACP)

    @param qdDev Interface to quantumdata instrument
    @return string describing the Info Frame packets data"""

    return qdDev.getInfoFrameData()

def TLqdListImages(qdDev):

    """Get the list of video format images

    @param qdDev Interface to quantumdata instrument
    @return list of image names"""

    return qdDev.listImages()

def TLqdGetImageParameters(qdDev, name=None):

    """Get the video image parameters

    @param qdDev Interface to quantumdata instrument
    @param name Optional image name, default is current image in use
    @return list of image parameters"""

    return qdDev.getImageParameters(name)

def TLqdGetImageParameter(qdDev, name, parameter):

    """Get the video image parameter value

    @param qdDev Interface to quantumdata instrument
    @param name Image name
    @param parameter Parameter name
    @return image parameter value"""

    return qdDev.getImageParameter(name, parameter)

def TLqdSetImageParameter(qdDev, name, parameter, value):

    """Set a video image parameter value

    @param qdDev Interface to quantumdata instrument
    @param name Image name
    @param parameter Parameter name
    @param value image parameter value"""

    qdDev.setImageParameter(name, parameter, value)

def TLqdGetImageRenditions(qdDev):

    """Get the number of video image renditions

    @param qdDev Interface to quantumdata instrument
    @return number of image renditions"""

    return qdDev.getImageRenditions()

def TLqdGetImageRendition(qdDev):

    """Get the video image parameter value

    @param qdDev Interface to quantumdata instrument
    @return current image rendition"""

    return qdDev.getImageRendition()

def TLqdSetImageRendition(qdDev, value):

    """Set the video image rendition

    @param qdDev Interface to quantumdata instrument
    @param image parameter value"""

    qdDev.setImageRendition(value)

def TLqdSetScrambling(qdDev, is_scrambled):

    """Set scrambling mode

    @param qdDev Interface to quantumdata instrument
    @param is_scrambled Indicates new scrambling
    @return TLqdResult"""

    return qdDev.setScrambling(is_scrambled)

def TLqdGetScrambling(qdDev):

    """Get the current scrambling mode

    @param qdDev Interface to quantumdata instrument
    @return True if scrambling"""

    return qdDev.getScrambling()

def TLqdGetVideoFrame(qdDev, fileName):

    """Get a frame of video

    @param qdDev Interface to quantumdata instrument
    @param fileName Fully qualified output bitmap file name
    @return TLqdResult"""

    return qdDev.getVideoFrame(fileName)

def TLqdGetPixel(qdDev, x, y):

    """Get one pixel

    @param qdDev Interface to quantumdata instrument
    @param x X coordinate
    @param y Y coordinate
    @return TLqdPixel"""

    return qdDev.getPixel(x, y)

def TLqdGetAudioInfoframe(qdDev):

    """Get an audio infoframe

    @param qdDev Interface to quantumdata instrument
    @return tuple of (result, error or decoded infoframe, infoframe octets)"""

    return qdDev.getAudioInfoframe()

def TLqdGetAviInfoframe(qdDev):

    """Get an AVI infoframe

    @param qdDev Interface to quantumdata instrument
    @return tuple of (result, error or decoded infoframe, infoframe octets)"""

    return qdDev.getAviInfoframe()

def TLqdGetDrmInfoframe(qdDev):

    """Get a dynamic range and mastering infoframe

    @param qdDev Interface to quantumdata instrument
    @return tuple of (result, error or decoded infoframe, infoframe octets)"""

    return qdDev.getDrmInfoframe()

def TLqdGetGcp(qdDev):

    """Get a general control packet

    @param qdDev Interface to quantumdata instrument
    @return tuple of (result, error or decoded infoframe, infoframe octets)"""

    return qdDev.getGcp()

def TLqdGetVendorSpecificInfoframe(qdDev):

    """Get a vendor specific infoframe

    @param qdDev Interface to quantumdata instrument
    @return tuple of (result, error or decoded infoframe, infoframe octets)"""

    return qdDev.getVendorSpecificInfoframe()

def TLqdGetReceivedFormat(qdDev):

    """Get the video format parameters being received

    @param qdDev Interface to quantumdata instrument
    @return TLqdVideoFormatParameters"""

    return qdDev.getReceivedFormat()

def TLqdTestAudio(qdDev):

    """Evaluate incoming audio

    @param qdDev Interface to quantumdata instrument
    @return audio test report"""

    return qdDev.testAudio()

def TLqdIsArcSupported(qdDev):

    """Is ARC audio supported?

    @param qdDev Interface to quantumdata instrument
    @return True if ARC is supported"""

    return qdDev.isArcSupported()

def TLqdIsEarcSupported(qdDev):

    """Is eARC audio supported?

    @param qdDev Interface to quantumdata instrument
    @return True if eARC is supported"""

    return qdDev.isEarcSupported()

def TLqd7_16(qdDev, vic, callbackforSS=False, testParameters=None):

    """Run HDMI 1.4 source test 7-16

    See @ref TLqdInstrument.run7_16 for details

    @param qdDev Interface to quantumdata instrument
    @param vic Video identification code
    @param callbackforSS Callback function to do source setup
    @param testParameters TLqdTestParameters
    @return TLqdResult"""

    return qdDev.run7_16(vic, callbackforSS, testParameters)

def TLqd7_17(qdDev, vic, callbackforSS=False, testParameters=None):

    """Run HDMI 1.4 source test 7-17

    See @ref TLqdInstrument.run7_17 for details

    @param qdDev Interface to quantumdata instrument
    @param vic Video identification code
    @param callbackforSS Callback function to do source setup
    @param testParameters TLqdTestParameters
    @return TLqdResult"""

    return qdDev.run7_17(vic, callbackforSS, testParameters)

def TLqd7_18(qdDev, vic, callbackforSS=False, testParameters=None):

    """Run HDMI 1.4 source test 7-18

    See @ref TLqdInstrument.run7_18 for details

    @param qdDev Interface to quantumdata instrument
    @param vic Video identification code
    @param callbackforSS Callback function to do source setup
    @param testParameters TLqdTestParameters
    @return TLqdResult"""

    return qdDev.run7_18(vic, callbackforSS, testParameters)

def TLqd7_19(qdDev, vic,  stepNumber, callbackforSS=False, testParameters=None):

    """Run HDMI 1.4 source test 7-19

    See @ref TLqdInstrument.run7_19 for details

    @param qdDev Interface to quantumdata instrument
    @param vic Video identification code
    @param stepNumber Test step number, 1 or 2
    @param callbackforSS Callback function to do source setup
    @param testParameters TLqdTestParameters
    @return TLqdResult"""

    return qdDev.run7_19(vic, stepNumber, callbackforSS, testParameters)

def TLqd7_23(qdDev, vic, callback, callbackforSS=False, testParameters=None):

    """Run HDMI 1.4 source test 7-23

    See @ref TLqdInstrument.run7_23 for details

    @param qdDev Interface to quantumdata instrument
    @param vic Video identification code
    @param callback Callback function to verify bitmap image
    @param callbackforSS Callback function to do source setup
    @param testParameters TLqdTestParameters
    @return TLqdResult"""

    return qdDev.run7_23(vic, callback, callbackforSS, testParameters)

def TLqd7_24(qdDev, vic, callback, callbackforSS=False, testParameters=None):

    """Run HDMI 1.4 source test 7-24

    See @ref TLqdInstrument.run7_24 for details

    @param qdDev Interface to quantumdata instrument
    @param vic Video identification code
    @param callback Callback function to verify bitmap image
    @param callbackforSS Callback function to do source setup
    @param testParameters TLqdTestParameters
    @return TLqdResult"""

    return qdDev.run7_24(vic, callback, callbackforSS, testParameters)

def TLqd7_25(qdDev, vic, callbackforSS=False, testParameters=None):

    """Run HDMI 1.4 source test 7-25

    See @ref TLqdInstrument.run7_25 for details

    @param qdDev Interface to quantumdata instrument
    @param vic Video identification code
    @param callbackforSS Callback function to do source setup
    @param testParameters TLqdTestParameters
    @return TLqdResult"""

    return qdDev.run7_25(vic, callbackforSS, testParameters)

def TLqd7_26(qdDev, vic, callbackforSS=False, testParameters=None):

    """Run HDMI 1.4 source test 7-26

    See @ref TLqdInstrument.run7_26 for details

    @param qdDev Interface to quantumdata instrument
    @param vic Video identification code
    @param callbackforSS Callback function to do source setup
    @param testParameters TLqdTestParameters
    @return TLqdResult"""

    return qdDev.run7_26(vic, callbackforSS, testParameters)

def TLqd7_27(qdDev, vic, callbackforSS=False, testParameters=None):

    """Run HDMI 1.4 source test 7-27

    See @ref TLqdInstrument.run7_27 for details

    @param qdDev Interface to quantumdata instrument
    @param vic Video identification code
    @param callbackforSS Callback function to do source setup
    @param testParameters TLqdTestParameters
    @return TLqdResult"""

    return qdDev.run7_27(vic, callbackforSS, testParameters)

def TLqd7_28(qdDev, stepNumber, callbackforSS=False, testParameters=None):

    """Run HDMI 1.4 source test 7-28

    See @ref TLqdInstrument.run7_28 for details

    @param qdDev Interface to quantumdata instrument
    @param stepNumber Test step number, 1, 2 or 3
    @param callbackforSS Callback function to do source setup
    @param testParameters TLqdTestParameters
    @return TLqdResult"""

    return qdDev.run7_28(stepNumber, callbackforSS, testParameters)

def TLqd7_29(qdDev, stepNumber, callbackforSS=False, testParameters=None):

    """Run HDMI 1.4 source test 7-29

    See @ref TLqdInstrument.run7_29 for details

    @param qdDev Interface to quantumdata instrument
    @param stepNumber Test step number, 1 or 2
    @param callbackforSS Callback function to do source setup
    @param testParameters TLqdTestParameters
    @return TLqdResult"""

    return qdDev.run7_29(stepNumber, callbackforSS, testParameters)

def TLqd7_30(qdDev, stepNumber, vic, samplingRate, maxChannels,
             callbackforSS=False, testParameters=None):

    """Run HDMI 1.4 source test 7-30

    See @ref TLqdInstrument.run7_30 for details

    @param qdDev Interface to quantumdata instrument
    @param stepNumber Test step number, 1 or 2
    @param vic Video identification code
    @param samplingRate L-PCM sampling rate in Hz
    @param maxChannels maximum number of audio channels
    @param callbackforSS Callback function to do source setup
    @param testParameters TLqdTestParameters
    @return TLqdResult"""

    return qdDev.run7_30(stepNumber, vic, samplingRate, maxChannels,
                         callbackforSS, testParameters)

def TLqd7_31(qdDev, stepNumber, vic, callbackforSS=False, testParameters=None):

    """Run HDMI 1.4 source test 7-31

    See @ref TLqdInstrument.run7_31 for details

    @param qdDev Interface to quantumdata instrument
    @param stepNumber Test step number, 1 or 2
    @param vic Video identification code
    @param callbackforSS Callback function to do source setup
    @param testParameters TLqdTestParameters
    @return TLqdResult"""

    return qdDev.run7_31(stepNumber, vic, callbackforSS, testParameters)

def TLqd7_32(qdDev, stepNumber, callbackforSS=False, testParameters=None):

    """Run HDMI 1.4 source test 7-32

    See @ref TLqdInstrument.run7_32 for details

    @param qdDev Interface to quantumdata instrument
    @param stepNumber Test step number, 1 or 2
    @param callbackforSS Callback function to do source setup
    @param testParameters TLqdTestParameters
    @return TLqdResult"""

    return qdDev.run7_32(stepNumber, callbackforSS, testParameters)

def TLqd7_33(qdDev, stepNumber, callbackforSS=False, testParameters=None):

    """Run HDMI 1.4 source test 7-33

    See @ref TLqdInstrument.run7_33 for details

    @param qdDev Interface to quantumdata instrument
    @param stepNumber Test step number, 1-5
    @param callbackforSS Callback function to do source setup
    @param testParameters TLqdTestParameters
    @return TLqdResult"""

    return qdDev.run7_33(stepNumber, callbackforSS, testParameters)

def TLqd7_33a(qdDev, callbackforSS=False, testParameters=None):

    """Run HDMI 1.4 source test 7-33a

    See @ref TLqdInstrument.run7_33a for details

    @param qdDev Interface to quantumdata instrument
    @param callbackforSS Callback function to do source setup
    @param testParameters TLqdTestParameters
    @return TLqdResult"""

    return qdDev.run7_33a(callbackforSS, testParameters)

def TLqd7_34(qdDev, vic, bitDepth, callbackforSS=False, testParameters=None):

    """Run HDMI 1.4 source test 7-34

    See @ref TLqdInstrument.run7_34 for details

    @param qdDev Interface to quantumdata instrument
    @param vic Video Identification code
    @param bitDepth Number of bits/color (only 12-bit is supported)
    @param callbackforSS Callback function to do source setup
    @param testParameters TLqdTestParameters
    @return TLqdResult"""

    return qdDev.run7_34(vic, bitDepth, callbackforSS, testParameters)

def TLqd7_35(qdDev, callbackforSS=False, testParameters=None):

    """Run HDMI 1.4 source test 7-35

    See @ref TLqdInstrument.run7_35 for details

    @param qdDev Interface to quantumdata instrument
    @param callbackforSS Callback function to do source setup
    @param testParameters TLqdTestParameters
    @return TLqdResult"""

    return qdDev.run7_35(callbackforSS, testParameters)

def TLqd7_36(qdDev, stepNumber, callbackforSS=False, testParameters=None):

    """Run HDMI 1.4 source test 7-36

    See @ref TLqdInstrument.run7_36 for details

    @param qdDev Interface to quantumdata instrument
    @param stepNumber Test step number, 1-2
    @param callbackforSS Callback function to do source setup
    @param testParameters TLqdTestParameters
    @return TLqdResult"""

    return qdDev.run7_36(stepNumber, callbackforSS, testParameters)

def TLqd7_37(qdDev, callbackforSS=False, testParameters=None):

    """Run HDMI 1.4 source test 7-37

    See @ref TLqdInstrument.run7_37 for details

    @param qdDev Interface to quantumdata instrument
    @param callbackforSS Callback function to do source setup
    @param testParameters TLqdTestParameters
    @return TLqdResult"""

    return qdDev.run7_37(callbackforSS, testParameters)

def TLqd7_38(qdDev, vic, threeD, callback, callbackforSS=False, testParameters=None):

    """Run HDMI 1.4 source test 7-38

    See @ref TLqdInstrument.run7_38 for details

    @param qdDev Interface to quantumdata instrument
    @param vic Video Identification Code
    @param threeD 3D option, None, 'F', 'T' or 'S'
    @param callback Optional callback function to verify bitmap image
    @param callbackforSS Callback function to do source setup
    @param testParameters TLqdTestParameters
    @return TLqdResult"""

    return qdDev.run7_38(vic, threeD, callback, callbackforSS, testParameters)

def TLqd7_39(qdDev, hdmiVic, callback, callbackforSS=False, testParameters=None):

    """Run HDMI 1.4 source test 7-39

    See @ref TLqdInstrument.run7_39 for details

    @param qdDev Interface to quantumdata instrument
    @param hdmiVic HDMI Video Identification Code
    @param callback Callback function to verify bitmap image
    @param callbackforSS Callback function to do source setup
    @param testParameters TLqdTestParameters
    @return TLqdResult"""

    return qdDev.run7_39(hdmiVic, callback, callbackforSS, testParameters)

def TLqd7_40(qdDev, stepNumber, callbackforSS=False, testParameters=None):

    """Run HDMI 1.4 source test 7-40

    See @ref TLqdInstrument.run7_40 for details

    @param qdDev Interface to quantumdata instrument
    @param stepNumber Test step number, 1-3
    @param callbackforSS Callback function to do source setup
    @param testParameters TLqdTestParameters
    @return TLqdResult"""

    return qdDev.run7_40(stepNumber, callbackforSS, testParameters)

def TLqdHF1_10(qdDev, stepNumber, callbackforSS=False, testParameters=None):

    """Run an iteration of HDMI source test HF1-10

    See @ref TLqdInstrument.runHf1_10 for details

    @param qdDev Interface to quantumdata instrument
    @param stepNumber Test step number, 1 or 2
    @param callbackforSS Callback function to do source setup
    @param testParameters TLqdTestParameters
    @return TLqdResult"""

    return qdDev.runHf1_10(stepNumber, callbackforSS, testParameters)

def TLqdHF1_11(qdDev, callbackforSS=False, testParameters=None):

    """Run an iteration of HDMI source test HF1-11

    See @ref TLqdInstrument.runHf1_11 for details

    @param qdDev Interface to quantumdata instrument
    @param callbackforSS Callback function to do source setup
    @param testParameters TLqdTestParameters
    @return TLqdResult"""

    return qdDev.runHf1_11(callbackforSS, testParameters)

def TLqdHF1_12(qdDev, callbackforSS=False, testParameters=None):

    """Run an iteration of HDMI source test HF1-12

    See @ref TLqdInstrument.runHf1_12 for details

    @param qdDev Interface to quantumdata instrument
    @param callbackforSS Callback function to do source setup
    @param testParameters TLqdTestParameters
    @return TLqdResult"""

    return qdDev.runHf1_12(callbackforSS, testParameters)

def TLqdHF1_13(qdDev, stepNumber, callbackforSS=False, testParameters=None):

    """Run an iteration of HDMI source test HF1-13

    See @ref TLqdInstrument.runHf1_13 for details

    @param qdDev Interface to quantumdata instrument
    @param stepNumber Test step number, 1 or 2
    @param callbackforSS Callback function to do source setup
    @param testParameters TLqdTestParameters
    @return TLqdResult"""

    return qdDev.runHf1_13(stepNumber, callbackforSS, testParameters)

def TLqdHF1_14(qdDev, vic, callbackforSS=False, testParameters=None):

    """Run an iteration of HDMI source test HF1-14

    See @ref TLqdInstrument.runHf1_14 for details

    @param qdDev Interface to quantumdata instrument
    @param vic Video identification code
    @param callbackforSS Callback function to do source setup
    @param testParameters TLqdTestParameters
    @return TLqdResult"""

    return qdDev.runHf1_14(vic, callbackforSS, testParameters)

def TLqdHF1_15(qdDev, vic, bitDepth, stepNumber, callbackforSS=False, testParameters=None):

    """Run an iteration of HDMI source test HF1-15

    See @ref TLqdInstrument.runHf1_15 for details

    @param qdDev Interface to quantumdata instrument
    @param vic Video identification code
    @param bitDepth Bit depth, 10 or 12
    @param stepNumber Test step number, 1 or 2
    @param callbackforSS Callback function to do source setup
    @param testParameters TLqdTestParameters
    @return TLqdResult"""

    return qdDev.runHf1_15(vic, bitDepth, stepNumber, callbackforSS, testParameters)

def TLqdHF1_16(qdDev, vic, threeD, callbackforSS=False, testParameters=None):

    """Run an iteration of HDMI source test HF1-16

    See @ref TLqdInstrument.runHf1_16 for details

    @param qdDev Interface to quantumdata instrument
    @param vic Video identification code
    @param threeD 3D option, F, T or S
    @param callbackforSS Callback function to do source setup
    @param testParameters TLqdTestParameters
    @return TLqdResult"""

    return qdDev.runHf1_16(vic, threeD, callbackforSS, testParameters)

def TLqdHF1_17(qdDev, callbackforSS=False, testParameters=None):

    """Run an iteration of HDMI source test HF1-17

    See @ref TLqdInstrument.runHf1_17 for details

    @param qdDev Interface to quantumdata instrument
    @param callbackforSS Callback function to do source setup
    @param testParameters TLqdTestParameters
    @return TLqdResult"""

    return qdDev.runHf1_17(callbackforSS, testParameters)

def TLqdHF1_18(qdDev, vic, bitDepth=None, threeD=None, bt2020=None,
               callbackforSS=False, testParameters=None):

    """Run an iteration of HDMI source test HF1-18

    See @ref TLqdInstrument.runHf1_18 for details

    @param qdDev Interface to quantumdata instrument
    @param vic Video identification code
    @param bitDepth Bit depth, None, 10 or 12
    @param threeD 3D option, None, F, T or S
    @param bt2020 BT.2020 option, None, 0, 1 or 2
    @param callbackforSS Callback function to do source setup
    @param testParameters TLqdTestParameters
    @return TLqdResult"""

    return qdDev.runHf1_18(vic, bitDepth, threeD, bt2020, callbackforSS, testParameters)

def TLqdHF1_20(qdDev, callbackforSS=False, testParameters=None):

    """Run an iteration of HDMI source test HF1-20

    See @ref TLqdInstrument.runHf1_20 for details

    @param qdDev Interface to quantumdata instrument
    @param callbackforSS Callback function to do source setup
    @param testParameters TLqdTestParameters
    @return TLqdResult"""

    return qdDev.runHf1_20(callbackforSS, testParameters)

def TLqdHF1_21(qdDev, callbackforSS=False, testParameters=None):

    """Run an iteration of HDMI source test HF1-21

    See @ref TLqdInstrument.runHf1_21 for details

    @param qdDev Interface to quantumdata instrument
    @param callbackforSS Callback function to do source setup
    @param testParameters TLqdTestParameters
    @return TLqdResult"""

    return qdDev.runHf1_21(callbackforSS, testParameters)

def TLqdHF1_22(qdDev, callbackforSS=False, testParameters=None):

    """Run an iteration of HDMI source test HF1-22

    See @ref TLqdInstrument.runHf1_22 for details

    @param qdDev Interface to quantumdata instrument
    @param callbackforSS Callback function to do source setup
    @param testParameters TLqdTestParameters
    @return TLqdResult"""

    return qdDev.runHf1_22(callbackforSS, testParameters)

def TLqdHF1_23(qdDev, callbackforSS=False, testParameters=None):

    """Run an iteration of HDMI source test HF1-23

    See @ref TLqdInstrument.runHf1_23 for details

    @param qdDev Interface to quantumdata instrument
    @param callbackforSS Callback function to do source setup
    @param testParameters TLqdTestParameters
    @return TLqdResult"""

    return qdDev.runHf1_23(callbackforSS, testParameters)

def TLqdHF1_24(qdDev, vic, callbackforSS=False, testParameters=None):

    """Run an iteration of HDMI source test HF1-24

    See @ref TLqdInstrument.runHf1_24 for details

    @param qdDev Interface to quantumdata instrument
    @param vic Video identification code
    @param callbackforSS Callback function to do source setup
    @param testParameters TLqdTestParameters
    @return TLqdResult"""

    return qdDev.runHf1_24(vic, callbackforSS, testParameters)

def TLqdHF1_25(qdDev, vic, stepNumber, bitDepth, callbackforSS=False, testParameters=None):

    """Run an iteration of HDMI source test HF1-25

    See @ref TLqdInstrument.runHf1_25 for details

    @param qdDev Interface to quantumdata instrument
    @param vic Video identification code
    @param stepNumber Test step number, 1 or 2
    @param bitDepth Bit depth, 10 or 12
    @param callbackforSS Callback function to do source setup
    @param testParameters TLqdTestParameters
    @return TLqdResult"""

    return qdDev.runHf1_25(vic, stepNumber, bitDepth, callbackforSS, testParameters)

def TLqdHF1_26(qdDev, vic, threeD, callbackforSS=False, testParameters=None):

    """Run an iteration of HDMI source test HF1-26

    See @ref TLqdInstrument.runHf1_26 for details

    @param qdDev Interface to quantumdata instrument
    @param vic Video identification code
    @param threeD 3D option, F, T or S
    @param callbackforSS Callback function to do source setup
    @param testParameters TLqdTestParameters
    @return TLqdResult"""

    return qdDev.runHf1_26(vic, threeD, callbackforSS, testParameters)

def TLqdHF1_27(qdDev, callbackforSS=False, testParameters=None):

    """Run an iteration of HDMI source test HF1-27

    See @ref TLqdInstrument.runHf1_27 for details

    @param qdDev Interface to quantumdata instrument
    @param callbackforSS Callback function to do source setup
    @param testParameters TLqdTestParameters
    @return TLqdResult"""

    return qdDev.runHf1_27(callbackforSS, testParameters)

def TLqdHF1_28(qdDev, vic, bitDepth=None, threeD=None, bt2020=None,
               callbackforSS=False, testParameters=None):

    """Run an iteration of HDMI source test HF1-28

    See @ref TLqdInstrument.runHf1_28 for details

    @param qdDev Interface to quantumdata instrument
    @param vic Video identification code
    @param bitDepth Bit depth, None, 10 or 12
    @param threeD 3D option, None, F, T or S
    @param bt2020 BT.2020 option, None, 0, 1 or 2
    @param callbackforSS Callback function to do source setup
    @param testParameters TLqdTestParameters
    @return TLqdResult"""

    return qdDev.runHf1_28(vic, bitDepth, threeD, bt2020, callbackforSS, testParameters)

def TLqdHF1_29(qdDev, callbackforSS=False, testParameters=None):

    """Run an iteration of HDMI source test HF1-29

    See @ref TLqdInstrument.runHf1_29 for details

    @param qdDev Interface to quantumdata instrument
    @param callbackforSS Callback function to do source setup
    @param testParameters TLqdTestParameters
    @return TLqdResult"""

    return qdDev.runHf1_29(callbackforSS, testParameters)

def TLqdHF1_31v(qdDev, vic, callback, supportsTestImage=False,
                callbackforSS=False, testParameters=None):

    """Run HDMI source test HF1-31 with a visual check

    See @ref TLqdInstrument.runHfr1_31v for details

    @param qdDev Interface to quantumdata instrument
    @param vic Video ID code
    @param callback Callback function to verify bitmap image
    @param supportsTestImage Indicates the DUT supports the test image
    @param callbackforSS Callback function to do source setup
    @param testParameters TLqdTestParameters
    @return TLqdResult"""

    return qdDev.runHf1_31v(vic, callback, supportsTestImage, callbackforSS, testParameters)

def TLqdHF1_31(qdDev, vic, stepNumber, callbackforSS=False, testParameters=None):

    """Run an iteration of HDMI source test HF1-31

    See @ref TLqdInstrument.runHf1_31 for details

    @param qdDev Interface to quantumdata instrument
    @param vic Video identification code
    @param stepNumber Test step number, 1 or 2
    @param callbackforSS Callback function to do source setup
    @param testParameters TLqdTestParameters
    @return TLqdResult"""

    return qdDev.runHf1_31(vic, stepNumber, callbackforSS, testParameters)

def TLqdHF1_32v(qdDev, vic, bitDepth, callback, supportsTestImage,
                callbackforSS=False, testParameters=None):
    """Run HDMI source test HF1-32 with a visual check

    See @ref TLqdInstrument.runHf1_32v for details

    @param qdDev Interface to quantumdata instrument
    @param vic Video identification code
    @param bitDepth Bit depth, 10, 12 or 16
    @param callback Callback function to verify bitmap image
    @param supportsTestImage Indicates the DUT supports the test image
    @param callbackforSS Callback function to do source setup
    @param testParameters TLqdTestParameters
    @return TLqdResult"""

    return qdDev.runHf1_32v(vic, bitDepth, callback, supportsTestImage,
                            callbackforSS, testParameters)

def TLqdHF1_32(qdDev, vic, stepNumber, bitDepth, callbackforSS=False,
               testParameters=None):

    """Run an iteration of HDMI source test HF1-32

    See @ref TLqdInstrument.runHf1_32 for details

    @param qdDev Interface to quantumdata instrument
    @param vic Video identification code
    @param stepNumber Test step number, 1 or 2
    @param bitDepth Bit depth, 10, 12 or 16
    @param callbackforSS Callback function to do source setup
    @param testParameters TLqdTestParameters
    @return TLqdResult"""

    return qdDev.runHf1_32(vic, stepNumber, bitDepth, callbackforSS,
                           testParameters)

def TLqdHF1_33(qdDev, vic, callbackforSS=False, testParameters=None):

    """Run an iteration of HDMI source test HF1-33

    See @ref TLqdInstrument.runHf1_33 for details

    @param qdDev Interface to quantumdata instrument
    @param vic Video identification code
    @param callbackforSS Callback function to do source setup
    @param testParameters TLqdTestParameters
    @return TLqdResult"""

    return qdDev.runHf1_33(vic, callbackforSS, testParameters)

def TLqdHF1_34(qdDev, vic, bitDepth, callbackforSS=False, testParameters=None):

    """Run an iteration of HDMI source test HF1-34

    See @ref TLqdInstrument.runHf1_34 for details

    @param qdDev Interface to quantumdata instrument
    @param vic Video identification code
    @param bitDepth Bit depth, 10 or 12
    @param callbackforSS Callback function to do source setup
    @param testParameters TLqdTestParameters
    @return TLqdResult"""

    return qdDev.runHf1_34(vic, bitDepth, callbackforSS, testParameters)

def TLqdHF1_35v(qdDev, vic, callback, callbackforSS=False, testParameters=None):

    """Run an iteration of HDMI source test HF1-35 with a visual check

    See @ref TLqdInstrument.runHf1_35v for details

    @param qdDev Interface to quantumdata instrument
    @param vic Video identification code
    @param callback Callback function to verify bitmap image
    @param callbackforSS Callback function to do source setup
    @param testParameters TLqdTestParameters
    @return TLqdResult"""

    return qdDev.runHf1_35v(vic, callback, callbackforSS, testParameters)

def TLqdHF1_35(qdDev, vic, callbackforSS=False, testParameters=None):

    """Run an iteration of HDMI source test HF1-35

    See @ref TLqdInstrument.runHf1_35 for details

    @param qdDev Interface to quantumdata instrument
    @param vic Video identification code
    @param callbackforSS Callback function to do source setup
    @param testParameters TLqdTestParameters
    @return TLqdResult"""

    return qdDev.runHf1_35(vic, callbackforSS, testParameters)

def TLqdHF1_41(qdDev, callbackforSS=False, testParameters=None):

    """Run HDMI source test HF1-41

    See @ref TLqdInstrument.runHf1_41 for details

    @param qdDev Interface to quantumdata instrument
    @param callbackforSS Callback function to do source setup
    @param testParameters TLqdTestParameters
    @return TLqdResult"""

    return qdDev.runHf1_41(callbackforSS, testParameters)

def TLqdHF1_43(qdDev, callbackforSS=False, testParameters=None):

    """Run HDMI source test HF1-43

    See @ref TLqdInstrument.runHf1_43 for details

    @param qdDev Interface to quantumdata instrument
    @param callbackforSS Callback function to do source setup
    @param testParameters TLqdTestParameters
    @return TLqdResult"""

    return qdDev.runHf1_43(callbackforSS, testParameters)

def TLqdHF1_44(qdDev, callbackforSS=False, testParameters=None):

    """Run HDMI source test HF1-44

    See @ref TLqdInstrument.runHf1_44 for details

    @param qdDev Interface to quantumdata instrument
    @param callbackforSS Callback function to do source setup
    @param testParameters TLqdTestParameters
    @return TLqdResult"""

    return qdDev.runHf1_44(callbackforSS, testParameters)

def TLqdHF1_45(qdDev, callbackforSS=False, testParameters=None):

    """Run HDMI source test HF1-44

    See @ref TLqdInstrument.runHf1_45 for details

    @param qdDev Interface to quantumdata instrument
    @param callbackforSS Callback function to do source setup
    @param testParameters TLqdTestParameters
    @return TLqdResult"""

    return qdDev.runHf1_45(callbackforSS, testParameters)

def TLqdHF1_47(qdDev, stepNumber, callbackforSS=False, testParameters=None):

    """Run an iteration of HDMI source test HF1-47

    See @ref TLqdInstrument.runHf1_47 for details

    @param qdDev Interface to quantumdata instrument
    @param stepNumber Test step number, 1 - 3
    @param callbackforSS Callback function to do source setup
    @param testParameters TLqdTestParameters
    @return TLqdResult"""

    return qdDev.runHf1_47(stepNumber, callbackforSS, testParameters)

def TLqdHF1_48(qdDev, stepNumber, callbackforSS=False, testParameters=None):

    """Run an iteration of HDMI source test HF1-48

    See @ref TLqdInstrument.runHf1_48 for details

    @param qdDev Interface to quantumdata instrument
    @param stepNumber Test step number, 1 - 2
    @param callbackforSS Callback function to do source setup
    @param testParameters TLqdTestParameters
    @return TLqdResult"""

    return qdDev.runHf1_48(stepNumber, callbackforSS, testParameters)

def TLqdHF1_49(qdDev, stepNumber, callbackforSS=False, testParameters=None):

    """Run an iteration of HDMI source test HF1-49

    See @ref TLqdInstrument.runHf1_49 for details

    @param qdDev Interface to quantumdata instrument
    @param stepNumber Test step number, 1 - 2
    @param callbackforSS Callback function to do source setup
    @param testParameters TLqdTestParameters
    @return TLqdResult"""

    return qdDev.runHf1_49(stepNumber, callbackforSS, testParameters)

def TLqdHF1_51(qdDev, vic, stepNumber, callbackforSS=False, testParameters=None):

    """Run an iteration of HDMI source test HF1-51

    See @ref TLqdInstrument.runHf1_51 for details

    @param qdDev Interface to quantumdata instrument
    @param vic Video identification code
    @param stepNumber Test step number, 1 - 4
    @param callbackforSS Callback function to do source setup
    @param testParameters TLqdTestParameters
    @return TLqdResult"""

    return qdDev.runHf1_51(vic, stepNumber, callbackforSS, testParameters)

def TLqdHF1_52(qdDev, stepNumber, callbackforSS=False, testParameters=None):

    """Run an iteration of HDMI source test HF1-52

    See @ref TLqdInstrument.runHf1_52 for details

    @param qdDev Interface to quantumdata instrument
    @param stepNumber Test step number, 1 - 4
    @param callbackforSS Callback function to do source setup
    @param testParameters TLqdTestParameters
    @return TLqdResult"""

    return qdDev.runHf1_52(stepNumber, callbackforSS, testParameters)

def TLqdHF1_53(qdDev, stepNumber, callbackforSS=False, testParameters=None):

    """Run an iteration of HDMI source test HF1-53

    See @ref TLqdInstrument.runHf1_53 for details

    @param qdDev Interface to quantumdata instrument
    @param stepNumber Test step number, 1 - 11
    @param callbackforSS Callback function to do source setup
    @param testParameters TLqdTestParameters
    @return TLqdResult"""

    return qdDev.runHf1_53(stepNumber, callbackforSS, testParameters)

def TLqdHF1_57(qdDev, stepNumber, fvaTiming=None, callbackforSS=False,
               testParameters=None):

    """Run an iteration of HDMI source test HF1-57

    See @ref TLqdInstrument.runHf1_57 for details

    @param qdDev Interface to quantumdata instrument
    @param stepNumber Test step number, 1 - 6
    @param fvaTiming Fva timing structure.
        "HorizontalxVertical-BRR*Range"
        where Range can be 2FFMAX (all), FF#, or FF#-#.
        example: 1920x1080-60*2FFMAX
    @param callbackforSS Callback function to do source setup
    @param testParameters TLqdTestParameters
    @return TLqdResult"""

    return qdDev.runHf1_57(stepNumber, fvaTiming,
                           callbackforSS, testParameters)

def TLqdHF1_58(qdDev, stepNumber, itFormat=None,
               callbackforSS=False, testParameters=None):

    """Run an iteration of HDMI source test HF1-58

    See @ref TLqdInstrument.runHf1_58 for details

    @param qdDev Interface to quantumdata instrument
    @param stepNumber Test step number, 1 - 33
    @param itFormat IT format timing structure
        "HorizontalxVertical-RefreshRate-Blanking",
        with Blanking being 0-Standard, 1-Reduced Ver1, 2- Reduced Ver2.
        example: 2560x1440-60-1
    @param callbackforSS Callback function to do source setup
    @param testParameters TLqdTestParameters
    @return TLqdResult"""

    return qdDev.runHf1_58(stepNumber, itFormat,
                           callbackforSS, testParameters)

def TLqdHF1_60(qdDev, stepNumber, fvaTiming=None,
               itFormat=None, callbackforSS=False, testParameters=None):

    """Run an iteration of HDMI source test HF1-60

    See @ref TLqdInstrument.runHf1_60 for details

    @param qdDev Interface to quantumdata instrument
    @param stepNumber Test step number, 1 - 34
    @param fvaTiming Fva timing structure.
        "HorizontalxVertical-BRR*Range"
        where Range can be 2FFMAX (all), FF#, or FF#-#.
        example: 1920x1080-60*2FFMAX
    @param itFormat IT format timing structure
        "HorizontalxVertical-RefreshRate-Blanking",
        with Blanking being 0-Standard, 1-Reduced Ver1, 2- Reduced Ver2.
        example: 2560x1440-60-1
    @param callbackforSS Callback function to do source setup
    @param testParameters TLqdTestParameters
    @return TLqdResult"""

    return qdDev.runHf1_60(stepNumber, fvaTiming, itFormat,
                           callbackforSS, testParameters)

def TLqdHF1_66(qdDev, stepNumber, vic=None,
               callbackforSS=False, testParameters=None):

    """Run an iteration of HDMI source test HF1-66

    See @ref TLqdInstrument.runHf1_66 for details

    @param qdDev Interface to quantumdata instrument
    @param stepNumber Test step number, 1 - 6
    @param vic Video identification code
    @param callbackforSS Callback function to do source setup
    @param testParameters TLqdTestParameters
    @return TLqdResult"""

    return qdDev.runHf1_66(stepNumber, vic, callbackforSS, testParameters)

def TLqdHF1_71(qdDev, vic, callbackforSS=False, testParameters=None):

    """Run an iteration of HDMI source test HF1-71

    See @ref TLqdInstrument.runHf1_71 for details

    @param qdDev Interface to quantumdata instrument
    @param vic The CTA-861-G 4:2:0 Video ID code
    @param callbackforSS Callback function to do source setup
    @param testParameters TLqdTestParameters
    @return TLqdResult"""

    return qdDev.runHf1_71(vic, callbackforSS, testParameters)

def TLqdHF1_72(qdDev, vic, bitDepth, callbackforSS=False, testParameters=None):

    """Run an iteration of HDMI source test HF1-72

    See @ref TLqdInstrument.runHf1_72 for details

    @param qdDev Interface to quantumdata instrument
    @param vic The CTA-861-G 4:2:0 Video ID code
    @param bitDepth Bit depth, 10 or 12
    @param callbackforSS Callback function to do source setup
    @param testParameters TLqdTestParameters
    @return TLqdResult"""

    return qdDev.runHf1_72(vic, bitDepth, callbackforSS, testParameters)

def TLqdHF1_74(qdDev, vic, bitDepth, stepNumber=None, callbackforSS=False, testParameters=None):

    """Run an iteration of HDMI source test HF1-74

    See @ref TLqdInstrument.runHf1_74 for details

    @param qdDev Interface to quantumdata instrument
    @param vic Video identification code
    @param bitDepth Bit depth, 10
    @param stepNumber Test step number, 1 - 9
    @param callbackforSS Callback function to do source setup
    @param testParameters TLqdTestParameters
    @return TLqdResult"""

    return qdDev.runHf1_74(vic, bitDepth, stepNumber, callbackforSS, testParameters)

def TLqdHF1_75(qdDev, vic, stepNumber=None, callbackforSS=False, testParameters=None):

    """Run an iteration of HDMI source test HF1-75

    See @ref TLqdInstrument.runHf1_75 for details

    @param qdDev Interface to quantumdata instrument
    @param vic Video identification code
    @param stepNumber Test step number, 1 - 12
    @param callbackforSS Callback function to do source setup
    @param testParameters TLqdTestParameters
    @return TLqdResult"""

    return qdDev.runHf1_75(vic, stepNumber, callbackforSS, testParameters)

def TLqdHFR1_10(qdDev, callbackforSS=False, testParameters=None):

    """Run FRL source test HFR1-10

    See @ref TLqdInstrument.runHfr1_10 for details

    @param qdDev Interface to quantumdata instrument
    @param callbackforSS Callback function to do source setup
    @param testParameters TLqdTestParameters
    @return TLqdResult"""

    return qdDev.runHfr1_10(callbackforSS, testParameters)

def TLqdHFR1_11(qdDev, stepNumber, callbackforSS=False, testParameters=None):

    """Run FRL source test HFR1-11

    See @ref TLqdInstrument.runHfr1_11 for details

    @param qdDev Interface to quantumdata instrument
    @param stepNumber Test step number, 1 - 2
    @param callbackforSS Callback function to do source setup
    @param testParameters TLqdTestParameters
    @return TLqdResult"""

    return qdDev.runHfr1_11(stepNumber, callbackforSS, testParameters)

def TLqdHFR1_12(qdDev, callbackforSS=False, testParameters=None):

    """Run FRL source test HFR1-12

    See @ref TLqdInstrument.runHfr1_12 for details

    @param qdDev Interface to quantumdata instrument
    @param callbackforSS Callback function to do source setup
    @param testParameters TLqdTestParameters
    @return TLqdResult"""

    return qdDev.runHfr1_12(callbackforSS, testParameters)

def TLqdHFR1_13(qdDev, maxFrlRate=6, callbackforSS=False, testParameters=None):

    """Run FRL source test HFR1-13

    See @ref TLqdInstrument.runHfr1_13 for details

    @param qdDev Interface to quantumdata instrument
    @param maxFrlRate Maximum FRL rate - 0-6
    @param callbackforSS Callback function to do source setup
    @param testParameters TLqdTestParameters
    @return TLqdResult"""

    return qdDev.runHfr1_13(maxFrlRate, callbackforSS, testParameters)

def TLqdHFR1_14(qdDev, vic, callbackforSS=False, testParameters=None):

    """Run FRL source test HFR1-14

    See @ref TLqdInstrument.runHfr1_14 for details

    @param qdDev Interface to quantumdata instrument
    @param vic Video ID code
    @param callbackforSS Callback function to do source setup
    @param testParameters TLqdTestParameters
    @return TLqdResult"""

    return qdDev.runHfr1_14(vic, callbackforSS, testParameters)

def TLqdHFR1_15(qdDev, vic, bitDepth=8, callbackforSS=False, testParameters=None):

    """Run FRL source test HFR1-15

    See @ref TLqdInstrument.runHfr1_15 for details

    @param qdDev Interface to quantumdata instrument
    @param vic Video ID code
    @param bitDepth Bit depth, 8, 10, 12 or 16
    @param callbackforSS Callback function to do source setup
    @param testParameters TLqdTestParameters
    @return TLqdResult"""

    return qdDev.runHfr1_15(vic, bitDepth, callbackforSS, testParameters)

def TLqdHFR1_16(qdDev, vic, threeD, callbackforSS=False, testParameters=None):

    """Run FRL source test HFR1-16

    See @ref TLqdInstrument.runHfr1_16 for details

    @param qdDev Interface to quantumdata instrument
    @param vic Video ID code for a 2160p format
    @param threeD 3D option, F, T or S
    @param callbackforSS Callback function to do source setup
    @param testParameters TLqdTestParameters
    @return TLqdResult"""

    return qdDev.runHfr1_16(vic, threeD, callbackforSS, testParameters)

def TLqdHFR1_17(qdDev, callbackforSS=False, testParameters=None):

    """Run FRL source test HFR1-17

    See @ref TLqdInstrument.runHfr1_17 for details

    @param qdDev Interface to quantumdata instrument
    @param callbackforSS Callback function to do source setup
    @param testParameters TLqdTestParameters
    @return TLqdResult"""

    return qdDev.runHfr1_17(callbackforSS, testParameters)

def TLqdHFR1_18(qdDev, vic, bitDepth=None, threeD=None, bt2020=None,
                callbackforSS=False, testParameters=None):

    """Run FRL source test HFR1-18

    See @ref TLqdInstrument.runHfr1_18 for details

    @param qdDev Interface to quantumdata instrument
    @param vic Video identification code
    @param bitDepth Bit depth, None, 10 or 12
    @param threeD 3D option, None, F, T or S
    @param bt2020 BT.2020 option, None, 0, 1 or 2
    @param callbackforSS Callback function to do source setup
    @param testParameters TLqdTestParameters
    @return TLqdResult"""

    return qdDev.runHfr1_18(vic, bitDepth, threeD, bt2020,
                            callbackforSS, testParameters)

def TLqdHFR1_19(qdDev, stepNumber, callbackforSS=False, testParameters=None):

    """Run FRL source test HFR1-19

    See @ref TLqdInstrument.runHfr1_19 for details

    @param qdDev Interface to quantumdata instrument
    @param stepNumber Test step number, 1 - 2
    @param callbackforSS Callback function to do source setup
    @param testParameters TLqdTestParameters
    @return TLqdResult"""

    return qdDev.runHfr1_19(stepNumber, callbackforSS, testParameters)

def TLqdHFR1_20(qdDev, stepNumber, callbackforSS=False, testParameters=None):

    """Run FRL source test HFR1-20

    See @ref TLqdInstrument.runHfr1_20 for details

    @param qdDev Interface to quantumdata instrument
    @param stepNumber Test step number, 1 - 2
    @param callbackforSS Callback function to do source setup
    @param testParameters TLqdTestParameters
    @return TLqdResult"""

    return qdDev.runHfr1_20(stepNumber, callbackforSS, testParameters)

def TLqdHFR1_21(qdDev, stepNumber, callbackforSS=False, testParameters=None):

    """Run FRL source test HFR1-21

    See @ref TLqdInstrument.runHfr1_21 for details

    @param qdDev Interface to quantumdata instrument
    @param stepNumber Test step number, 1 - 2
    @param callbackforSS Callback function to do source setup
    @param testParameters TLqdTestParameters
    @return TLqdResult"""

    return qdDev.runHfr1_21(stepNumber, callbackforSS, testParameters)

def TLqdHFR1_22(qdDev, stepNumber, bitDepth=None, callbackforSS=False, testParameters=None):

    """Run FRL source test HFR1-22

    See @ref TLqdInstrument.runHfr1_22 for details

    @param qdDev Interface to quantumdata instrument
    @param stepNumber Test step number, 1 - 2
    @param bitDepth Bit depth, 8, 10, 12 or 16
    @param callbackforSS Callback function to do source setup
    @param testParameters TLqdTestParameters
    @return TLqdResult"""

    return qdDev.runHfr1_22(stepNumber, bitDepth, callbackforSS, testParameters)

def TLqdHFR1_23(qdDev, callbackforSS=False, testParameters=None):

    """Run FRL source test HFR1-23

    See @ref TLqdInstrument.runHfr1_23 for details

    @param qdDev Interface to quantumdata instrument
    @param callbackforSS Callback function to do source setup
    @param testParameters TLqdTestParameters
    @return TLqdResult"""

    return qdDev.runHfr1_23(callbackforSS, testParameters)

def TLqdHFR1_24(qdDev, vic, callbackforSS=False, testParameters=None):

    """Run FRL source test HFR1-24

    See @ref TLqdInstrument.runHfr1_24 for details

    @param qdDev Interface to quantumdata instrument
    @param vic Video ID code
    @param callbackforSS Callback function to do source setup
    @param testParameters TLqdTestParameters
    @return TLqdResult"""

    return qdDev.runHfr1_24(vic, callbackforSS, testParameters)

def TLqdHFR1_25(qdDev, vic, bitDepth=8, callbackforSS=False, testParameters=None):

    """Run FRL source test HFR1-25

    See @ref TLqdInstrument.runHfr1_25 for details

    @param qdDev Interface to quantumdata instrument
    @param vic Video ID code
    @param bitDepth Bit depth, 8, 10, 12 or 16
    @param callbackforSS Callback function to do source setup
    @param testParameters TLqdTestParameters
    @return TLqdResult"""

    return qdDev.runHfr1_25(vic, bitDepth, callbackforSS, testParameters)

def TLqdHFR1_26(qdDev, vic, threeD, callbackforSS=False, testParameters=None):

    """Run FRL source test HFR1-26

    See @ref TLqdInstrument.runHfr1_26 for details

    @param qdDev Interface to quantumdata instrument
    @param vic Video ID code for a non-2160p format
    @param threeD 3D option, F, T or S
    @param callbackforSS Callback function to do source setup
    @param testParameters TLqdTestParameters
    @return TLqdResult"""

    return qdDev.runHfr1_26(vic, threeD, callbackforSS, testParameters)

def TLqdHFR1_27(qdDev, callback, supportsTestImage=False, bitDepth=8,
                 callbackforSS=False, testParameters=None):

    """Run FRL source test HFR1-27

    See @ref TLqdInstrument.runHfr1_27 for details

    @param qdDev Interface to quantumdata instrument
    @param callback Callback function to verify bitmap image
    @param supportsTestImage Indicates the DUT supports the test image
    @param bitDepth Bit depth, 8, 10, 12 or 16
    @param callbackforSS Callback function to do source setup
    @param testParameters TLqdTestParameters
    @return TLqdResult"""

    return qdDev.runHfr1_27(callback, supportsTestImage, bitDepth,
                            callbackforSS, testParameters)

def TLqdHFR1_28(qdDev, vic, bitDepth=None, threeD=None, bt2020=None,
                 callbackforSS=False, testParameters=None):

    """Run FRL source test HFR1-28

    See @ref TLqdInstrument.runHfr1_28 for details

    @param qdDev Interface to quantumdata instrument
    @param vic Video identification code
    @param bitDepth Bit depth, None, 10 or 12
    @param threeD 3D option, None, F, T or S
    @param bt2020 BT.2020 option, None, 0, 1 or 2
    @param callbackforSS Callback function to do source setup
    @param testParameters TLqdTestParameters
    @return TLqdResult"""

    return qdDev.runHfr1_28(vic, bitDepth, threeD, bt2020,
                            callbackforSS, testParameters)

def TLqdHFR1_29(qdDev, callback, supportsTestImage=False,
                callbackforSS=False, testParameters=None):

    """Run FRL source test HFR1-29

    See @ref TLqdInstrument.runHfr1_29 for details

    @param qdDev Interface to quantumdata instrument
    @param callback Callback function to verify bitmap image
    @param supportsTestImage Indicates the DUT supports the test image
    @param callbackforSS Callback function to do source setup
    @param testParameters TLqdTestParameters
    @return TLqdResult"""

    return qdDev.runHfr1_29(callback, supportsTestImage,
                            callbackforSS, testParameters)

def TLqdHFR1_30(qdDev, callback, subSampling, supportsTestImage=False,
                 callbackforSS=False, testParameters=None):

    """Run FRL source test HFR1-30

    See @ref TLqdInstrument.runHfr1_30 for details

    @param qdDev Interface to quantumdata instrument
    @param callback Callback function to verify bitmap image
    @param subSampling TLqdSubsampling
    @param supportsTestImage Indicates the DUT supports the test image
    @param callbackforSS Callback function to do source setup
    @param testParameters TLqdTestParameters
    @return TLqdResult"""

    return qdDev.runHfr1_30(callback, subSampling, supportsTestImage,
                            callbackforSS, testParameters)

def TLqdHFR1_31(qdDev, callback, callbackforSS, vic, supportsTestImage=False,
                 testParameters=None):

    """Run FRL source test HFR1-31

    See @ref TLqdInstrument.runHfr1_31 for details

    @param qdDev Interface to quantumdata instrument
    @param callback Callback function to verify bitmap image
    @param callbackforSS Callback function to do source setup
    @param vic Video ID code
    @param supportsTestImage Indicates the DUT supports the test image
    @param callbackforSS Callback function to do source setup
    @param testParameters TLqdTestParameters
    @return TLqdResult"""

    return qdDev.runHfr1_31(callback, callbackforSS, vic, supportsTestImage, testParameters)

def TLqdHFR1_32(qdDev, callback, vic, supportsTestImage=False, bitDepth=8,
                callbackforSS=False, testParameters=None):

    """Run FRL source test HFR1-32

    See @ref TLqdInstrument.runHfr1_32 for details

    @param qdDev Interface to quantumdata instrument
    @param callback Callback function to verify bitmap image
    @param vic Video ID code
    @param supportsTestImage Indicates the DUT supports the test image
    @param bitDepth Bit depth, 8, 10, 12 or 16
    @param callbackforSS Callback function to do source setup
    @param testParameters TLqdTestParameters
    @return TLqdResult"""

    return qdDev.runHfr1_32(callback, vic, supportsTestImage, bitDepth,
                            callbackforSS, testParameters)

def TLqdHFR1_33(qdDev, vic, callbackforSS, testParameters=None):

    """Run FRL source test HFR1-33

    See @ref TLqdInstrument.runHfr1_33 for details

    @param qdDev Interface to quantumdata instrument
    @param vic Video ID code
    @param callbackforSS Callback function to do source setup
    @param testParameters TLqdTestParameters
    @return TLqdResult"""

    return qdDev.runHfr1_33(vic, callbackforSS, testParameters)

def TLqdHFR1_34(qdDev, vic, bitDepth=8, callbackforSS=False, testParameters=None):

    """Run FRL source test HFR1-34

    See @ref TLqdInstrument.runHfr1_34 for details

    @param qdDev Interface to quantumdata instrument
    @param vic Video ID code
    @param bitDepth Bit depth, 8, 10, 12 or 16
    @param callbackforSS Callback function to do source setup
    @param testParameters TLqdTestParameters
    @return TLqdResult"""

    return qdDev.runHfr1_34(vic, bitDepth, callbackforSS, testParameters)

def TLqdHFR1_35(qdDev, vic, bitDepth=8, callbackforSS=False, testParameters=None):

    """Run FRL source test HFR1-35

    See @ref TLqdInstrument.runHfr1_35 for details

    @param qdDev Interface to quantumdata instrument
    @param vic Video ID code
    @param bitDepth Bit depth, 8, 10, 12 or 16
    @param callbackforSS Callback function to do source setup
    @param testParameters TLqdTestParameters
    @return TLqdResult"""

    return qdDev.runHfr1_35(vic, bitDepth, callbackforSS, testParameters)

def TLqdHFR1_36(qdDev, stepNumber, callbackforSS=False, testParameters=None):

    """Run FRL source test HFR1-36

    See @ref TLqdInstrument.runHfr1_36 for details

    @param qdDev Interface to quantumdata instrument
    @param stepNumber Test step number, 1 or 2
    @param callbackforSS Callback function to do source setup
    @param testParameters TLqdTestParameters
    @return TLqdResult"""

    return qdDev.runHfr1_36(stepNumber, callbackforSS, testParameters)

def TLqdHFR1_37(qdDev, callbackforSS=False, testParameters=None):

    """Run FRL source test HFR1-37

    See @ref TLqdInstrument.runHfr1_37 for details

    @param qdDev Interface to quantumdata instrument
    @param callbackforSS Callback function to do source setup
    @param testParameters TLqdTestParameters
    @return TLqdResult"""

    return qdDev.runHfr1_37(callbackforSS, testParameters)

def TLqdHFR1_38(qdDev, callbackforSS=False, testParameters=None):

    """Run FRL source test HFR1-38

    See @ref TLqdInstrument.runHfr1_38 for details

    @param qdDev Interface to quantumdata instrument
    @param callbackforSS Callback function to do source setup
    @param testParameters TLqdTestParameters
    @return TLqdResult"""

    return qdDev.runHfr1_38(callbackforSS, testParameters)

def TLqdHFR1_39(qdDev, callbackforSS=False, testParameters=None):

    """Run FRL source test HFR1-39

    See @ref TLqdInstrument.runHfr1_39 for details

    @param qdDev Interface to quantumdata instrument
    @param callbackforSS Callback function to do source setup
    @param testParameters TLqdTestParameters
    @return TLqdResult"""

    return qdDev.runHfr1_39(callbackforSS, testParameters)

def TLqdHFR1_40(qdDev, callbackforSS=False, testParameters=None):

    """Run FRL source test HFR1-40

    See @ref TLqdInstrument.runHfr1_40 for details

    @param qdDev Interface to quantumdata instrument
    @param callbackforSS Callback function to do source setup
    @param testParameters TLqdTestParameters
    @return TLqdResult"""

    return qdDev.runHfr1_40(callbackforSS, testParameters)

def TLqdHFR1_41(qdDev, callbackforSS=False, testParameters=None):

    """Run FRL source test HFR1-41

    See @ref TLqdInstrument.runHfr1_41 for details

    @param qdDev Interface to quantumdata instrument
    @param callbackforSS Callback function to do source setup
    @param testParameters TLqdTestParameters
    @return TLqdResult"""

    return qdDev.runHfr1_41(callbackforSS, testParameters)

def TLqdHFR1_43(qdDev, callbackforSS=False, testParameters=None):

    """Run FRL source test HFR1-43

    See @ref TLqdInstrument.runHfr1_43 for details

    @param qdDev Interface to quantumdata instrument
    @param callbackforSS Callback function to do source setup
    @param testParameters TLqdTestParameters
    @return TLqdResult"""

    return qdDev.runHfr1_43(callbackforSS, testParameters)

def TLqdHFR1_45(qdDev, sampling, layout, callbackforSS=False, testParameters=None):

    """Run FRL source test HFR1-45

    See @ref TLqdInstrument.runHfr1_45 for details

    @param qdDev Interface to quantumdata instrument
    @param sampling Audio sampling rate in Hz
    @param layout (0=2-channel, 1=multi-channel)
    @param callbackforSS Callback function to do source setup
    @param testParameters TLqdTestParameters
    @return TLqdResult"""

    return qdDev.runHfr1_45(sampling, layout, callbackforSS, testParameters)

def TLqdHFR1_46(qdDev, callbackforSS=False, testParameters=None):

    """Run FRL source test HFR1-46

    See @ref TLqdInstrument.runHfr1_46 for details

    @param qdDev Interface to quantumdata instrument
    @param callbackforSS Callback function to do source setup
    @param testParameters TLqdTestParameters
    @return TLqdResult"""

    return qdDev.runHfr1_46(callbackforSS, testParameters)

def TLqdHFR1_50(qdDev, vic, callbackforSS=False, testParameters=None):

    """Run FRL source test HFR1-50

    See @ref TLqdInstrument.runHfr1_50 for details

    @param qdDev Interface to quantumdata instrument
    @param vic Video ID code
    @param callbackforSS Callback function to do source setup
    @param testParameters TLqdTestParameters
    @return TLqdResult"""

    return qdDev.runHfr1_50(vic, callbackforSS, testParameters)

def TLqdHFR1_51(qdDev, vic, stepNumber, callbackforSS=False, testParameters=None):

    """Run FRL source test HFR1-51

    See @ref TLqdInstrument.runHfr1_51 for details

    @param qdDev Interface to quantumdata instrument
    @param vic Video ID code
    @param stepNumber Test step number, 1 - 4
    @param callbackforSS Callback function to do source setup
    @param testParameters TLqdTestParameters
    @return TLqdResult"""

    return qdDev.runHfr1_51(vic, stepNumber, callbackforSS, testParameters)

def TLqdHFR1_52(qdDev, stepNumber, callbackforSS=False, testParameters=None):

    """Run FRL source test HFR1-52

    See @ref TLqdInstrument.runHfr1_52 for details

    @param qdDev Interface to quantumdata instrument
    @param stepNumber Test step number, 1 - 4
    @param callbackforSS Callback function to do source setup
    @param testParameters TLqdTestParameters
    @return TLqdResult"""

    return qdDev.runHfr1_52(callbackforSS, testParameters)

def TLqdHFR1_58(qdDev, vic, stepNumber, bitDepth=None, bt2020=None,
               callbackforSS=False, testParameters=None):

    """Run FRL source test HFR1-58

    See @ref TLqdInstrument.runHfr1_58 for details

    @param qdDev Interface to quantumdata instrument
    @param vic Video identification code
    @param stepNumber Test step number, 1 - 24
    @param bitDepth Bit depth, None, 10 or 12
    @param bt2020 BT.2020 option, None, 0, 1 or 2
    @param callbackforSS Callback function to do source setup
    @param testParameters TLqdTestParameters
    @return TLqdResult"""

    return qdDev.runHfr1_58(vic, stepNumber, bitDepth, bt2020,
                            callbackforSS, testParameters)

def TLqdHFR1_65(qdDev, stepNumber, callbackforSS=False, testParameters=None):

    """Run FRL source test HFR1-65

    See @ref TLqdInstrument.runHfr1_65 for details

    @param qdDev Interface to quantumdata instrument
    @param stepNumber Test step number, 1 - 3
    @param callbackforSS Callback function to do source setup
    @param testParameters TLqdTestParameters
    @return TLqdResult"""

    return qdDev.runHfr1_65(stepNumber, callbackforSS, testParameters)

def TLqdHFR1_67(qdDev, stepNumber, testParameters=None):

    """Run FRL source test HFR1-67

    See @ref TLqdInstrument.runHfr1_67 for details

    @param qdDev Interface to quantumdata instrument
    @param stepNumber Test step number, 1 - 8
    @param testParameters TLqdTestParameters
    @return TLqdResult"""

    return qdDev.runHfr1_67(stepNumber, testParameters)

def TLqdHFR1_68(qdDev, callbackforSS=False, testParameters=None):

    """Run FRL source test HFR1-68

    See @ref TLqdInstrument.runHfr1_68 for details

    @param qdDev Interface to quantumdata instrument
    @param callbackforSS Callback function to do source setup
    @param testParameters TLqdTestParameters
    @return TLqdResult"""

    return qdDev.runHfr1_68(callbackforSS, testParameters)

def TLqdHFR1_69(qdDev, vic, stepNumber, callbackforSS=False, testParameters=None):

    """Run FRL source test HFR1-69

    See @ref TLqdInstrument.runHfr1_69 for details

    @param qdDev Interface to quantumdata instrument
    @param vic Video identification code
    @param stepNumber Test step number, 1 - 4
    @param callbackforSS Callback function to do source setup
    @param testParameters TLqdTestParameters
    @return TLqdResult"""

    return qdDev.runHfr1_69(vic, stepNumber, callbackforSS, testParameters)

def TLqdHFR1_80(qdDev, vic, stepNumber, callback, supportsTestImage=False,
                callbackforSS=False, testParameters=None):

    """Run FRL source test HFR1-80

    See @ref TLqdInstrument.runHfr1_80 for details

    @param qdDev Interface to quantumdata instrument
    @param vic Video identification code
    @param stepNumber Test step number, 1 - 2
    @param callback Callback function to verify bitmap image
    @param supportsTestImage Indicates the DUT supports the test image
    @param callbackforSS Callback function to do source setup
    @param testParameters TLqdTestParameters
    @return TLqdResult"""

    return qdDev.runHfr1_80(vic, stepNumber, callback, supportsTestImage,
                            callbackforSS, testParameters)

def TLqdHFR1_81(qdDev, vic, stepNumber, callback, supportsTestImage=False,
               callbackforSS=False, testParameters=None):

    """Run FRL source test HFR1-81

    See @ref TLqdInstrument.runHfr1_81 for details

    @param qdDev Interface to quantumdata instrument
    @param vic Video identification code
    @param stepNumber Test step number, 1 - 2
    @param callback Callback function to verify bitmap image
    @param supportsTestImage Indicates the DUT supports the DSC test image
    @param callbackforSS Callback function to do source setup
    @param testParameters TLqdTestParameters
    @return TLqdResult"""

    return qdDev.runHfr1_81(vic, stepNumber, callback, supportsTestImage,
                            callbackforSS, testParameters)

def TLqdHFR1_82(qdDev, vic, bitDepth, stepNumber, callback,
               supportsTestImage=False, callbackforSS=False, testParameters=None):

    """Run FRL source test HFR1-82

    See @ref TLqdInstrument.runHfr1_82 for details

    @param qdDev Interface to quantumdata instrument
    @param vic Video identification code
    @param bitDepth Bit depth, 10 or 12
    @param stepNumber Test step number, 1 - 2
    @param callback Callback function to verify bitmap image
    @param supportsTestImage Indicates the DUT supports the DSC test image
    @param callbackforSS Callback function to do source setup
    @param testParameters TLqdTestParameters
    @return TLqdResult"""

    return qdDev.runHfr1_82(vic, bitDepth, stepNumber, callback,
                             supportsTestImage, callbackforSS, testParameters)

def TLqdHFR1_83(qdDev, vic, bitDepth, stepNumber, callback,
               supportsTestImage=False, callbackforSS=False, testParameters=None):

    """Run FRL source test HFR1-83

    See @ref TLqdInstrument.runHfr1_83 for details

    @param qdDev Interface to quantumdata instrument
    @param vic Video identification code
    @param bitDepth Bit depth, 10 or 12
    @param stepNumber Test step number, 1 - 2
    @param callback Callback function to verify bitmap image
    @param supportsTestImage Indicates the DUT supports the DSC test image
    @param callbackforSS Callback function to do source setup
    @param testParameters TLqdTestParameters
    @return TLqdResult"""

    return qdDev.runHfr1_83(vic, bitDepth, stepNumber, callback,
                            supportsTestImage, callbackforSS, testParameters)

def TLqdHFR1_84(qdDev, vic, subSampling, stepNumber, callback,
               supportsTestImage=False, callbackforSS=False, testParameters=None):

    """Run FRL source test HFR1-84

    See @ref TLqdInstrument.runHfr1_84 for details

    @param qdDev Interface to quantumdata instrument
    @param vic Video identification code
    @param subSampling TLqdSubsampling
    @param stepNumber Test step number, 1 - 2
    @param callback Callback function to verify bitmap image
    @param supportsTestImage Indicates the DUT supports the DSC test image
    @param callbackforSS Callback function to do source setup
    @param testParameters TLqdTestParameters
    @return TLqdResult"""

    return qdDev.runHfr1_84(vic, subSampling, stepNumber, callback,
                            supportsTestImage, callbackforSS, testParameters)

def TLqdHFR1_85(qdDev, vic, subSampling, stepNumber, callback,
               supportsTestImage=False, callbackforSS=False, testParameters=None):

    """Run FRL source test HFR1-85

    See @ref TLqdInstrument.runHfr1_85 for details

    @param qdDev Interface to quantumdata instrument
    @param vic Video identification code
    @param subSampling TLqdSubsampling
    @param stepNumber Test step number, 1 - 2
    @param callback Callback function to verify bitmap image
    @param supportsTestImage Indicates the DUT supports the DSC test image
    @param callbackforSS Callback function to do source setup
    @param testParameters TLqdTestParameters
    @return TLqdResult"""

    return qdDev.runHfr1_85(vic, subSampling, stepNumber, callback,
                            supportsTestImage, callbackforSS, testParameters)

def TLqdHFR5_1_20(qdDev, testParameters=None):

    """Run eARC source test HFR5-1-20

    See @ref TLqdInstrument.runHfr5_1_20 for details

    @param qdDev Interface to quantumdata instrument
    @param testParameters TLqdTestParameters
    @return TLqdResult"""

    return qdDev.runHfr5_1_20(testParameters)

def TLqdHFR5_1_21(qdDev, testParameters=None):

    """Run eARC source test HFR5-1-21

    See @ref TLqdInstrument.runHfr5_1_21 for details

    @param qdDev Interface to quantumdata instrument
    @param testParameters TLqdTestParameters
    @return TLqdResult"""

    return qdDev.runHfr5_1_21(testParameters)

def TLqdHFR5_1_22(qdDev, testParameters=None):

    """Run eARC source test HFR5-1-22

    See @ref TLqdInstrument.runHfr5_1_22 for details

    @param qdDev Interface to quantumdata instrument
    @param testParameters TLqdTestParameters
    @return TLqdResult"""

    return qdDev.runHfr5_1_22(testParameters)

def TLqdHFR5_1_23(qdDev, testParameters=None):

    """Run eARC source test HFR5-1-23

    See @ref TLqdInstrument.runHfr5_1_23 for details

    @param qdDev Interface to quantumdata instrument
    @param testParameters TLqdTestParameters
    @return TLqdResult"""

    return qdDev.runHfr5_1_23(testParameters)

def TLqdHFR5_1_24(qdDev, testParameters=None):

    """Run eARC source test HFR5-1-24

    See @ref TLqdInstrument.runHfr5_1_24 for details

    @param qdDev Interface to quantumdata instrument
    @param testParameters TLqdTestParameters
    @return TLqdResult"""

    return qdDev.runHfr5_1_24(testParameters)

def TLqdHFR5_1_25(qdDev, testParameters=None):

    """Run eARC source test HFR5-1-25

    See @ref TLqdInstrument.runHfr5_1_25 for details

    @param qdDev Interface to quantumdata instrument
    @param testParameters TLqdTestParameters
    @return TLqdResult"""

    return qdDev.runHfr5_1_25(testParameters)

def TLqdHFR5_1_26(qdDev, testParameters=None):

    """Run eARC source test HFR5-1-26

    See @ref TLqdInstrument.runHfr5_1_26 for details

    @param qdDev Interface to quantumdata instrument
    @param testParameters TLqdTestParameters
    @return TLqdResult"""

    return qdDev.runHfr5_1_26(testParameters)

def TLqdHFR5_1_28(qdDev, samplingRate, mute=None, bitDepth=None,
                  testParameters=None):

    """Run eARC source test HFR5-1-28

    See @ref TLqdInstrument.runHfr5_1_28 for details

    @param qdDev Interface to quantumdata instrument
    @param samplingRate Audio sampling rate in kHz (48, 44.1, etc.)
    @param mute If not None, tests MUTE=1 (or 0)
    @param bitDepth Audio sample size (16, 20 or 24)
    @param testParameters TLqdTestParameters
    @return TLqdResult"""

    return qdDev.runHfr5_1_28(samplingRate, mute, bitDepth, testParameters)

def TLqdHFR5_1_29(qdDev, samplingRate, mute=None, bitDepth=None,
                  testParameters=None):

    """Run eARC source test HFR5-1-29

    See @ref TLqdInstrument.runHfr5_1_29 for details

    @param qdDev Interface to quantumdata instrument
    @param samplingRate Audio sampling rate in kHz (48, 44.1, etc.)
    @param mute If not None, tests MUTE=1 (or 0)
    @param bitDepth Audio sample size (16, 20 or 24)
    @param testParameters TLqdTestParameters
    @return TLqdResult"""

    return qdDev.runHfr5_1_29(samplingRate, mute, bitDepth, testParameters)

def TLqdHFR5_1_32(qdDev, samplingRate, callback, testParameters=None):

    """Run eARC source test HFR5-1-32

    See @ref TLqdInstrument.runHfr5_1_32 for details

    @param qdDev Interface to quantumdata instrument
    @param samplingRate Audio sampling rate in kHz (48, 44.1, etc.)
    @param callback Callback function to verify received audio
    @param testParameters TLqdTestParameters
    @return TLqdResult"""

    return qdDev.runHfr5_1_32(samplingRate, callback, testParameters)

def TLqdHFR5_1_33(qdDev, samplingRate, callback, testParameters=None):

    """Run eARC source test HFR5-1-33

    See @ref TLqdInstrument.runHfr5_1_33 for details

    @param qdDev Interface to quantumdata instrument
    @param samplingRate Audio sampling rate in kHz (48, 44.1, etc.)
    @param callback Callback function to verify received audio
    @param testParameters TLqdTestParameters
    @return TLqdResult"""

    return qdDev.runHfr5_1_33(samplingRate, callback, testParameters)

def TLqdHFR5_1_34(qdDev, samplingRate, chanAlloc, callback,
                  testParameters=None):

    """Run eARC source test HFR5-1-34

    See @ref TLqdInstrument.runHfr5_1_34 for details

    @param qdDev Interface to quantumdata instrument
    @param samplingRate Audio sampling rate in kHz (48, 44.1, etc.)
    @param chanAlloc Channel allocation value
    @param callback Callback function to verify received audio
    @param testParameters TLqdTestParameters
    @return TLqdResult"""

    return qdDev.runHfr5_1_34(samplingRate, chanAlloc, callback, testParameters)

def TLqdHFR5_1_35(qdDev, testParameters=None):

    """Run eARC source test HFR5-1-35

    See @ref TLqdInstrument.runHfr5_1_35 for details

    @param qdDev Interface to quantumdata instrument
    @param testParameters TLqdTestParameters
    @return TLqdResult"""

    return qdDev.runHfr5_1_35(testParameters)

def TLqdHFR5_1_36(qdDev, testParameters=None):

    """Run eARC source test HFR5-1-36

    See @ref TLqdInstrument.runHfr5_1_36 for details

    @param qdDev Interface to quantumdata instrument
    @param testParameters TLqdTestParameters
    @return TLqdResult"""

    return qdDev.runHfr5_1_36(testParameters)

def TLqdHFR5_1_37(qdDev, testParameters=None):

    """Run eARC source test HFR5-1-37

    See @ref TLqdInstrument.runHfr5_1_37 for details

    @param qdDev Interface to quantumdata instrument
    @param testParameters TLqdTestParameters
    @return TLqdResult"""

    return qdDev.runHfr5_1_37(testParameters)

def TLqdHFR5_1_38(qdDev, stepNumber, testParameters=None):

    """Run eARC source test HFR5-1-38

    See @ref TLqdInstrument.runHfr5_1_38 for details

    @param qdDev Interface to quantumdata instrument
    @param stepNumber Test step number, 1 - 2
    @param testParameters TLqdTestParameters
    @return TLqdResult"""

    return qdDev.runHfr5_1_38(stepNumber, testParameters)

def TLqdHFR5_1_39(qdDev, testParameters=None):

    """Run eARC source test HFR5-1-39

    See @ref TLqdInstrument.runHfr5_1_39 for details

    @param qdDev Interface to quantumdata instrument
    @param testParameters TLqdTestParameters
    @return TLqdResult"""

    return qdDev.runHfr5_1_39(testParameters)

def TLqdHFR5_1_50(qdDev, testParameters=None):

    """Run eARC source test HFR5-1-50

    See @ref TLqdInstrument.runHfr5_1_50 for details

    @param qdDev Interface to quantumdata instrument
    @param testParameters TLqdTestParameters
    @return TLqdResult"""

    return qdDev.runHfr5_1_50(testParameters)

def TLqdHFR5_1_51(qdDev, testParameters=None):

    """Run eARC source test HFR5-1-51

    See @ref TLqdInstrument.runHfr5_1_51 for details

    @param qdDev Interface to quantumdata instrument
    @param testParameters TLqdTestParameters
    @return TLqdResult"""

    return qdDev.runHfr5_1_51(testParameters)

def TLqdHFR5_1_52(qdDev, testParameters=None):

    """Run eARC source test HFR5-1-52

    See @ref TLqdInstrument.runHfr5_1_52 for details

    @param qdDev Interface to quantumdata instrument
    @param testParameters TLqdTestParameters
    @return TLqdResult"""

    return qdDev.runHfr5_1_52(testParameters)

def TLqdHFR5_1_55(qdDev, testParameters=None):

    """Run eARC source test HFR5-1-55

    See @ref TLqdInstrument.runHfr5_1_55 for details

    @param qdDev Interface to quantumdata instrument
    @param testParameters TLqdTestParameters
    @return TLqdResult"""

    return qdDev.runHfr5_1_55(testParameters)

def TLqdHFR5_1_56(qdDev, samplingRate, mute=None, bitDepth=None,
                  testParameters=None):

    """Run eARC source test HFR5-1-56

    See @ref TLqdInstrument.runHfr5_1_56 for details

    @param qdDev Interface to quantumdata instrument
    @param samplingRate Audio sampling rate in kHz (48, 44.1, etc.)
    @param mute If not None, tests MUTE=1 (or 0)
    @param bitDepth Audio sample size (16, 20 or 24)
    @param testParameters TLqdTestParameters
    @return TLqdResult"""

    return qdDev.runHfr5_1_56(samplingRate, mute, bitDepth, testParameters)

def TLqdHFR5_1_58(qdDev, samplingRate, speakers, mute=None,
                  testParameters=None):

    """Run eARC source test HFR5-1-58

    See @ref TLqdInstrument.runHfr5_1_58 for details

    @param qdDev Interface to quantumdata instrument
    @param samplingRate Audio sampling rate in kHz (48, 44.1, etc.)
    @param speakers List of speaker descriptors
    @param mute If not None, tests MUTE=1 (or 0)
    @param testParameters TLqdTestParameters
    @return TLqdResult"""

    return qdDev.runHfr5_1_58(samplingRate, speakers, mute, testParameters)

def TLqdHFR5_1_59(qdDev, samplingRate, speakers, mute=None,
                  testParameters=None):

    """Run eARC source test HFR5-1-59

    See @ref TLqdInstrument.runHfr5_1_59 for details

    @param qdDev Interface to quantumdata instrument
    @param samplingRate Audio sampling rate in kHz (48, 44.1, etc.)
    @param speakers List of speaker descriptors
    @param mute If not None, tests MUTE=1 (or 0)
    @param testParameters TLqdTestParameters
    @return TLqdResult"""

    return qdDev.runHfr5_1_59(samplingRate, speakers, mute, testParameters)

def TLqdHFR5_2_20(qdDev, testParameters=None):

    """Run eARC sink test HFR5-2-20

    See @ref TLqdInstrument.runHfr5_2_20 for details

    @param qdDev Interface to quantumdata instrument
    @param testParameters TLqdTestParameters
    @return TLqdResult"""

    return qdDev.runHfr5_2_20(testParameters)

def TLqdHFR5_2_21(qdDev, testParameters=None):

    """Run eARC sink test HFR5-2-21

    See @ref TLqdInstrument.runHfr5_2_21 for details

    @param qdDev Interface to quantumdata instrument
    @param testParameters TLqdTestParameters
    @return TLqdResult"""

    return qdDev.runHfr5_2_21(testParameters)

def TLqdHFR5_2_22(qdDev, testParameters=None):

    """Run eARC sink test HFR5-2-22

    See @ref TLqdInstrument.runHfr5_2_22 for details

    @param qdDev Interface to quantumdata instrument
    @param testParameters TLqdTestParameters
    @return TLqdResult"""

    return qdDev.runHfr5_2_22(testParameters)

def TLqdHFR5_2_23(qdDev, testParameters=None):

    """Run eARC sink test HFR5-2-23

    See @ref TLqdInstrument.runHfr5_2_23 for details

    @param qdDev Interface to quantumdata instrument
    @param testParameters TLqdTestParameters
    @return TLqdResult"""

    return qdDev.runHfr5_2_23(testParameters)

def TLqdHFR5_2_24(qdDev, testParameters=None):

    """Run eARC sink test HFR5-2-24

    See @ref TLqdInstrument.runHfr5_2_24 for details

    @param qdDev Interface to quantumdata instrument
    @param testParameters TLqdTestParameters
    @return TLqdResult"""

    return qdDev.runHfr5_2_24(testParameters)

def TLqdHFR5_2_25(qdDev, testParameters=None):

    """Run eARC sink test HFR5-2-25

    See @ref TLqdInstrument.runHfr5_2_25 for details

    @param qdDev Interface to quantumdata instrument
    @param testParameters TLqdTestParameters
    @return TLqdResult"""

    return qdDev.runHfr5_2_25(testParameters)

def TLqdHF2_5(qdDev, callback, vic=None, cdf=None):

    """Run HDMI sink test HF2-5

    See @ref TLqdInstrument.runHf2_5 for details

    @param qdDev Interface to quantumdata instrument
    @param callback Callback function
    @param vic Optional VIC to use
    @param cdf Optional CDF file to use
    @return TLqdResult"""

    return qdDev.runHf2_5(callback, vic, cdf)

def TLqdHF2_6(qdDev, callback, vic, minOrMax, cdf=None):

    """Run HDMI sink test HF2-6

    See @ref TLqdInstrument.runHf2_6 for details

    @param qdDev Interface to quantumdata instrument
    @param callback Callback function
    @param vic VIC to use (96, 97, 101 or 102)
    @param minOrMax if True minimum rate, maximum otherwise
    @param cdf Optional CDF file to use
    @return TLqdResult"""

    return qdDev.runHf2_6(callback, vic, minOrMax, cdf)

def TLqdHF2_7(qdDev, callback, vic, bitDepth, minOrMax, yCbCr, cdf=None):

    """Run HDMI sink test HF2-7

    See @ref TLqdInstrument.runHf2_7 for details

    @param qdDev Interface to quantumdata instrument
    @param callback Callback function
    @param vic VIC to use (93, 94, 95, 98, 99 or 100)
    @param bitDepth Number of bits/pixel - 10, 12 or 16
    @param minOrMax If True minimum rate, maximum otherwise
    @param yCbCr If True indicates YCbCr 4:4:4 signalling
    @param cdf Optional CDF file to use
    @return TLqdResult"""

    return qdDev.runHf2_7(callback, vic, bitDepth, minOrMax, yCbCr, cdf)

def TLqdHF2_8(qdDev, callback, vic, threeD, minOrMax, cdf=None):

    """Run HDMI sink test HF2-8

    See @ref TLqdInstrument.runHf2_8 for details

    @param qdDev Interface to quantumdata instrument
    @param callback Callback function
    @param vic VIC to use (93-102)
    @param threeD 3D option (F, T or S)
    @param minOrMax If True minimum rate, maximum otherwise
    @param yCbCr If True indicates YCbCr 4:4:4 signalling
    @return TLqdResult"""

    return qdDev.runHf2_8(callback, vic, threeD, minOrMax, cdf)

def TLqdHF2_9(qdDev, callback, stepNumber, cdf=None):

    """Run HDMI sink test HF2-9

    See @ref TLqdInstrument.runHf2_9 for details

    @param qdDev Interface to quantumdata instrument
    @param callback Callback function
    @param stepNumber Test step number, 1 or 2
    @param cdf Optional CDF file to use
    @return TLqdResult"""

    return qdDev.runHf2_9(callback, stepNumber, cdf)

def TLqdHF2_10(qdDev, version=TLqdEdidComplianceTestVersion.Version2_0,
               cdf=None):

    """Run HDMI sink test HF2-10

    See @ref TLqdInstrument.runHf2_10 for details

    @param qdDev Interface to quantumdata instrument
    @param version Optional TLqdEdidComplianceTestVersion, defaults to 2.0
    @param cdf Optional CDF file to use
    @return TLqdResult"""

    return qdDev.runHf2_10(version, cdf)

def TLqdHF2_23(qdDev, callback, vic, stepNumber, cdf=None):

    """Run HDMI sink test HF2-23

    See @ref TLqdInstrument.runHf2_23 for details

    @param qdDev Interface to quantumdata instrument
    @param callback Callback function
    @param vic Video Identification Code (96, 97, 101, 102, 106, or 106)
    @param stepNumber Test step number, 1 or 2
    @param cdf Optional CDF file to use
    @return TLqdResult"""

    return qdDev.runHf2_23(callback, vic, stepNumber, cdf)

def TLqdHF2_24(qdDev, callback, vic, bitDepth, cdf=None):

    """Run HDMI sink test HF2-24

    See @ref TLqdInstrument.runHf2_24 for details

    @param qdDev Interface to quantumdata instrument
    @param callback Callback function
    @param vic Video Identification Code (96, 97, 101, 102, 106, or 106)
    @param bitDepth Number of bits/pixel (10, 12 or 16)
    @param cdf Optional CDF file to use
    @return TLqdResult"""

    return qdDev.runHf2_24(callback, vic, bitDepth, cdf)

def TLqdHF2_25(qdDev, callback, vic, checkEdid, checkEquiv, nominalRate,
               minOrMax, cdf=None):

    """Run HDMI sink test HF2-25

    See @ref TLqdInstrument.runHf2_25 for details

    @param qdDev Interface to quantumdata instrument
    @param callback Callback function
    @param vic Video Identification Code (65-92 or 103-107)
    @param checkEdid Perform EDID checks
    @param checkEquiv Check the equivalent aspect ratio per CTA-861-G
    @param nominalRate Check the format at the nominal rate
    @param minOrMax if True minimum rate, maximum otherwise
    @param cdf Optional CDF file to use
    @return TLqdResult"""

    return qdDev.runHf2_25(callback, vic, checkEdid, checkEquiv, nominalRate,
                           minOrMax, cdf)

def TLqdHF2_26(qdDev, vics, above340Mcsc, cdf=None):

    """Run HDMI sink test HF2-26

    See @ref TLqdInstrument.runHf2_26 for details

    @param qdDev Interface to quantumdata instrument
    @param vics List of 21x9 ascpect ratio VICs
    @param above340Mcsc Indicates DUT support >= 340Mcsc
    @param cdf Optional CDF file to use
    @return TLqdResult"""

    return qdDev.runHf2_26(vics, above340Mcsc, cdf)

def TLqdHF2_30(qdDev, callback, stream=1, flat=False, vic=0, cdf=None):

    """Run HDMI sink test HF2-30

    See @ref TLqdInstrument.runHf2_30 for details

    @param qdDev Interface to quantumdata instrument
    @param callback Callback function to verify the multi-stream audio
    @param stream Stream number to verify
    @param flat Test the stream_flat bits in the audio sample packets
    @param vic Video identification code
    @param cdf Optional CDF file to use
    @return TLqdResult"""

    return qdDev.runHf2_30(callback, stream, flat, vic, cdf)

def TLqdHF2_31(qdDev, vics, cdf=None):

    """Run HDMI sink test HF2-31

    See @ref TLqdInstrument.runHf2_31 for details

    @param qdDev Interface to quantumdata instrument
    @param vics List of 4K 4:2:0 VICs (96, 97, 101, 102, 106 and/or 107)
    @param cdf Optional CDF file to use
    @return TLqdResult"""

    return qdDev.runHf2_31(vics, cdf)

def TLqdHF2_32(qdDev, bt2020Ycc, bt2020cYcc, cdf=None):

    """Run HDMI sink test HF2-32

    See @ref TLqdInstrument.runHf2_32 for details

    @param qdDev Interface to quantumdata instrument
    @param bt2020Ycc Indicates support for BT.2020 YCC
    @param bt2020cYcc Indicates support for BT.2020 cYCC
    @param cdf Optional CDF file to use
    @return TLqdResult"""

    return qdDev.runHf2_32(bt2020Ycc, bt2020cYcc, cdf)

def TLqdHF2_35(qdDev, vics, dc10, dc12, dc16, cdf=None):

    """Run HDMI sink test HF2-35

    See @ref TLqdInstrument.runHf2_35 for details

    @param qdDev Interface to quantumdata instrument
    @param vics List of 4K 4:2:0 VICs (96, 97, 101, 102, 106 and/or 107)
    @param dc10 Indicates support for 10-bit deep color
    @param dc12 Indicates support for 12-bit deep color
    @param dc16 Indicates support for 16-bit deep color
    @param cdf Optional CDF file to use
    @return TLqdResult"""

    return qdDev.runHf2_35(vics, dc10, dc12, dc16, cdf)

def TLqdHF2_39(qdDev, msAudio=False, threeDAudio=False, msOneBit=False,
               threeDOneBit=False, msMixed=False, cdf=None):

    """Run HDMI sink test HF2-39

    See @ref TLqdInstrument.runHf2_39 for details

    @param qdDev Interface to quantumdata instrument
    @param msAudio Indicates support for multi-stream audio
    @param threeDAudio Indicates support for 3D audio
    @param msOneBit Indicates support for multi-stream One Bit audio
    @param threeDOneBit Indicates support for 3D One Bit audio
    @param msMixed Indicates support for multi-stream audio mixed
    @param cdf Optional CDF file to use
    @return TLqdResult"""

    return qdDev.runHf2_39(msAudio, threeDAudio, msOneBit, threeDOneBit,
                           msMixed, cdf)

def TLqdHF2_40(qdDev, callback, vic, threeD, stepNumber, cdf=None):

    """Run HDMI sink test HF2-40

    See @ref TLqdInstrument.runHf2_40 for details

    @param qdDev Interface to quantumdata instrument
    @param callback Callback function to verify bitmap image
    @param vic Video identification code
    @param threeD 3D option, F, T or S
    @param stepNumber Test step number, 1 - 4
    @param cdf Optional CDF file to use
    @return TLqdResult"""

    return qdDev.runHf2_40(callback, vic, threeD, stepNumber, cdf)

def TLqdHF2_41(qdDev, independentView=True, cdf=None):

    """Run HDMI sink test HF2-41

    See @ref TLqdInstrument.runHf2_41 for details

    @param qdDev Interface to quantumdata instrument
    @param independentView Indicates support for independent view
    @param cdf Optional CDF file to use
    @return TLqdResult"""

    return qdDev.runHf2_41(independentView, cdf)

def TLqdHF2_43(qdDev, callback, vic, threeD, option, stepNumber,
               supportsOsd=True, cdf=None):

    """Run HDMI sink test HF2-43

    See @ref TLqdInstrument.runHf2_43 for details

    @param qdDev Interface to quantumdata instrument
    @param callback Callback function to verify OSD disparity behavior
    @param vic Video Identification Code
    @param threeD 3D option, F, T or S
    @param option Test option a - d
    @param stepNumber Test step number, 1 - 4
    @param supportsOsd Indicates OSD support (defaults to True)
    @param cdf Optional CDF file to use
    @return TLqdResult"""

    return qdDev.runHf2_43(callback, vic, threeD, option, stepNumber,
                           supportsOsd, cdf)

def TLqdHF2_53(qdDev, scdc=False, readRequests=False, lte340=False,
               indView=False, dualView=False, osd=False, dc10=False,
               dc12=False, dc16=False, above340=False, cdf=None):

    """Run HDMI sink test HF2-53

    See @ref TLqdInstrument.runHf2_53 for details

    @param qdDev Interface to quantumdata instrument
    @param scdc Indicates support for SCDC
    @param readRequests Indicates support for read requests
    @param lte340 Indicates support for scrambling <= 340Mcsc
    @param indView Indicates support for independent view
    @param dualView Indicates support for dual view
    @param osd Indicates support for on-screen display
    @param dc10 Indicates support for 4:2:0 10-bit deep color
    @param dc12 Indicates support for 4:2:0 12-bit deep color
    @param dc16 Indicates support for 4:2:0 16-bit deep color
    @param above340 Indicates support for rates > 340Mcsc
    @param cdf Optional CDF file to use
    @return TLqdResult"""

    return qdDev.runHf2_53(scdc, readRequests, lte340, indView, dualView, osd,
                           dc10, dc12, dc16, above340, cdf)

def TLqdHF2_54(qdDev, callback, checkEdid, sdr=False, hdr=False, smpte=False,
               hlg=False, smpteOption=0, cdf=None):

    """Run HDMI sink test HF2-54

    See @ref TLqdInstrument.runHf2_54 for details

    @param qdDev Interface to quantumdata instrument
    @param callback Callback function
    @param checkEdid Perform EDID checks
    @param sdr Indicates support for HDR Traditional SDR
    @param hdr Indicates support for HDR Traditional HDR
    @param smpte Indicates support for HDR SMPTE ST.2084
    @param hlg Indicates support for HDR Hybrid Log Gamma
    @param smpteOption R/G/B option number for the SMPTE test (1-6)
    @param cdf Optional CDF file to use
    @return TLqdResult"""

    return qdDev.runHf2_54(checkEdid, sdr, hdr, smpte, hlg, cdf)

def TLqdHF2_71(qdDev, callback, vic, stepNumber, cdf=None):

    """Run HDMI sink test HF2-71

    See @ref TLqdInstrument.runHf2_71 for details

    @param qdDev Interface to quantumdata instrument
    @param callback Callback function
    @param vic Video Identification Code (114, 115, 116, 117, 118, 119, 120,
        124, 125, 126, 194, 195, 196, 202, 203, 204, 218, 219)
    @param stepNumber Test step number, 1 or 2
    @param cdf Optional CDF file to use
    @return TLqdResult"""

    return qdDev.runHf2_71(callback, vic, stepNumber, cdf)

def TLqdHF2_72(qdDev, callback, vic, bitDepth, cdf=None):

    """Run HDMI sink test HF2-72

    See @ref TLqdInstrument.runHf2_72 for details

    @param qdDev Interface to quantumdata instrument
    @param callback Callback function
    @param vic Video Identification Code (114, 115, 116, 117, 118, 119, 120,
        124, 125, 126, 194, 195, 196, 202, 203, 204, 218, 219)
    @param bitDepth Number of bits/pixel (10, 12 or 16)
    @param cdf Optional CDF file to use
    @return TLqdResult"""

    return qdDev.runHf2_72(callback, vic, bitDepth, cdf)

def TLqdHF2_94(qdDev, callback, audioRate, nOption, cdf=None):

    """Run HDMI sink test HF2-94

    See @ref TLqdInstrument.runHf2_94 for details

    @param qdDev Interface to quantumdata instrument
    @param callback Callback function
    @param audioRate Audio sampling rate in kHz (32, 44.1 or 48)
    @param nOption N option ("nominal", "minimum" or "maximum")
    @param cdf Optional CDF file to use
    @return TLqdResult"""

    return qdDev.runHf2_94(callback, audioRate, nOption, cdf)

def TLqdHFR2_17(qdDev, callback, cdf=None):

    """Run HDMI sink test HFR2-17

    See @ref TLqdInstrument.runHfr2_17 for details

    @param qdDev Interface to quantumdata instrument
    @param callback Callback function
    @param cdf Optional CDF file to use
    @return TLqdResult"""

    return qdDev.runHfr2_17(callback, cdf)

def TLqdHFR2_18(qdDev, callback, cdf=None):

    """Run HDMI sink test HFR2-18

    See @ref TLqdInstrument.runHfr2_18 for details

    @param qdDev Interface to quantumdata instrument
    @param callback Callback function
    @param cdf Optional CDF file to use
    @return TLqdResult"""

    return qdDev.runHfr2_18(callback, cdf)

def TLqdHFR2_19(qdDev, callback, cdf=None):

    """Run HDMI sink test HFR2-19

    See @ref TLqdInstrument.runHfr2_19 for details

    @param qdDev Interface to quantumdata instrument
    @param callback Callback function
    @param cdf Optional CDF file to use
    @return TLqdResult"""

    return qdDev.runHfr2_19(callback, cdf)

def TLqdHFR2_20(qdDev, callback, cdf=None):

    """Run HDMI sink test HFR2-20

    See @ref TLqdInstrument.runHfr2_20 for details

    @param qdDev Interface to quantumdata instrument
    @param callback Callback function
    @param cdf Optional CDF file to use
    @return TLqdResult"""

    return qdDev.runHfr2_20(callback, cdf)

def TLqdHFR2_21(qdDev, callback, cdf=None):

    """Run HDMI sink test HFR2-21

    See @ref TLqdInstrument.runHfr2_21 for details

    @param qdDev Interface to quantumdata instrument
    @param callback Callback function
    @param cdf Optional CDF file to use
    @return TLqdResult"""

    return qdDev.runHfr2_21(callback, cdf)

def TLqdHFR2_22(qdDev, callback, cdf=None):

    """Run HDMI sink test HFR2-22

    See @ref TLqdInstrument.runHfr2_22 for details

    @param qdDev Interface to quantumdata instrument
    @param callback Callback function
    @param cdf Optional CDF file to use
    @return TLqdResult"""

    return qdDev.runHfr2_22(callback, cdf)

def TLqdHFR2_48(qdDev, callback, cdf=None):

    """Run HDMI sink test HFR2-48

    See @ref TLqdInstrument.runHfr2_48 for details

    @param qdDev Interface to quantumdata instrument
    @param callback Callback function
    @param cdf Optional CDF file to use
    @return TLqdResult"""

    return qdDev.runHfr2_48(callback, cdf)

def TLqdHFR2_49(qdDev, callback, cdf=None):

    """Run HDMI sink test HFR2-49

    See @ref TLqdInstrument.runHfr2_49 for details

    @param qdDev Interface to quantumdata instrument
    @param callback Callback function
    @param cdf Optional CDF file to use
    @return TLqdResult"""

    return qdDev.runHfr2_49(callback, cdf)

def TLqdHFR2_50(qdDev, callback, cdf=None):

    """Run HDMI sink test HFR2-50

    See @ref TLqdInstrument.runHfr2_50 for details

    @param qdDev Interface to quantumdata instrument
    @param callback Callback function
    @param cdf Optional CDF file to use
    @return TLqdResult"""

    return qdDev.runHfr2_50(callback, cdf)

def TLqdHFR2_51(qdDev, callback, cdf=None):

    """Run HDMI sink test HFR2-51

    See @ref TLqdInstrument.runHfr2_51 for details

    @param qdDev Interface to quantumdata instrument
    @param callback Callback function
    @param cdf Optional CDF file to use
    @return TLqdResult"""

    return qdDev.runHfr2_51(callback, cdf)

def TLqdHFR2_52(qdDev, callback, cdf=None):

    """Run HDMI sink test HFR2-52

    See @ref TLqdInstrument.runHfr2_52 for details

    @param qdDev Interface to quantumdata instrument
    @param callback Callback function
    @param cdf Optional CDF file to use
    @return TLqdResult"""

    return qdDev.runHfr2_52(callback, cdf)

def TLqdHFR2_53(qdDev, fva=False, allm=False, qms=False, vrr=False, fapa=False,
                dsc=False, above340=False, ccbpci=False, nmvrr=False,
                eightk50=False, eightk60=False, vrrHigh=None, maxFrl=None,
                dscMaxFrl=None, cdf=None):

    """Run HDMI sink test HFR2-53

    See @ref TLqdInstrument.runHfr2_53 for details

    @param qdDev Interface to quantumdata instrument
    @param fva Indicates support for FVA
    @param allm Indicates support for ALLM
    @param qms Indicates support for QMS beyond VRR range
    @param vrr Indicates support for VRR
    @param fapa Indicates support for FAPA start location
    @param dsc Indicates support for DSC
    @param above340 Indicates support for rates > 340Mcsc
    @param ccbpci Indicates support for CCBPCI
    @param nmvrr Indicates support for Negative Mvrr
    @param eightk50 Indicates support for 8K50
    @param eightk60 Indicates support for 8K60
    @param vrrHigh Indicates VRR high range
    @param maxFrl Indicates the maximum FRL rate
    @param dscMaxFrl Indicates the maximum FRL rate for DSC
    @param cdf Optional CDF file to use
    @return TLqdResult"""

    return qdDev.runHfr2_53(fva, allm, qms, vrr, fapa, dsc, above340, ccbpci,
                            nmvrr, eightk50, eightk60, vrrHigh, maxFrl,
                            dscMaxFrl, cdf)

def TLqdHFR2_70(qdDev, cdf=None):

    """Run HDMI sink test HFR2-70

    See @ref TLqdInstrument.runHfr2_70 for details

    @param qdDev Interface to quantumdata instrument
    @param cdf Optional CDF file to use
    @return TLqdResult"""

    return qdDev.runHfr2_70(cdf)

def TLqdHFR2_80(qdDev, callback, vic, testRgb, minPixRate, maxFrlRate,cdf=None):

    """Run DSC sink test HFR2-80

    See @ref TLqdInstrument.runHfr2_80 for details

    @param qdDev Interface to quantumdata instrument
    @param callback Callback function to verify DSC video
    @param vic Video identification code for a 2160p format
    @param testRgb Indicates testing RGB, YCbCr 4:4:4 otherwise
    @param minPixRate Indicates minimum (99.5%) pixel rate,
        max (100.5%) otherwise
    @param maxFrlRate Indicates the highest FRL rate supported by the DUT
    @param cdf Optional CDF file to use
    @return TLqdResult"""

    return qdDev.runHfr2_80(callback, vic, testRgb, minPixRate, maxFrlRate, cdf)

def TLqdHFR2_81(qdDev, callback, vic, testRgb, minPixRate, maxFrlRate,cdf=None):

    """Run DSC sink test HFR2-81

    See @ref TLqdInstrument.runHfr2_81 for details

    @param qdDev Interface to quantumdata instrument
    @param callback Callback function to verify DSC video
    @param vic Video identification code for a 4320p format
    @param testRgb Indicates testing RGB, YCbCr 4:4:4 otherwise
    @param minPixRate Indicates minimum (99.5%) pixel rate,
        max (100.5%) otherwise
    @param maxFrlRate Indicates the highest FRL rate supported by the DUT
    @param cdf Optional CDF file to use
    @return TLqdResult"""

    return qdDev.runHfr2_81(callback, vic, testRgb, minPixRate, maxFrlRate, cdf)

def TLqdHFR2_82(qdDev, callback, vic, test10, minPixRate, maxFrlRate,cdf=None):

    """Run DSC sink test HFR2-82

    See @ref TLqdInstrument.runHfr2_82 for details

    @param qdDev Interface to quantumdata instrument
    @param callback Callback function to verify DSC video
    @param vic Video identification code for a 2160p format
    @param test10 Indicates testing 10-bit RGB, 12-bit otherwise
    @param minPixRate Indicates minimum (99.5%) pixel rate,
        max (100.5%) otherwise
    @param maxFrlRate Indicates the highest FRL rate supported by the DUT
    @param cdf Optional CDF file to use
    @return TLqdResult"""

    return qdDev.runHfr2_82(callback, vic, test10, minPixRate, maxFrlRate, cdf)

def TLqdHFR2_83(qdDev, callback, vic, test10, minPixRate, maxFrlRate,cdf=None):

    """Run DSC sink test HFR2-83

    See @ref TLqdInstrument.runHfr2_83 for details

    @param qdDev Interface to quantumdata instrument
    @param callback Callback function to verify DSC video
    @param vic Video identification code for a 4320p format
    @param test10 Indicates testing 10-bit RGB, 12-bit otherwise
    @param minPixRate Indicates minimum (99.5%) pixel rate,
        max (100.5%) otherwise
    @param maxFrlRate Indicates the highest FRL rate supported by the DUT
    @param cdf Optional CDF file to use
    @return TLqdResult"""

    return qdDev.runHfr2_83(callback, vic, test10, minPixRate, maxFrlRate, cdf)

def TLqdHFR2_84(qdDev, callback, vic, ycc420, minPixRate, maxFrlRate,cdf=None):

    """Run DSC sink test HFR2-84

    See @ref TLqdInstrument.runHfr2_84 for details

    @param qdDev Interface to quantumdata instrument
    @param callback Callback function to verify DSC video
    @param vic Video identification code for a 2160p format
    @param ycc420 Indicates testing YCbCr 4:2:0, 4:2:2 otherwise
    @param minPixRate Indicates minimum (99.5%) pixel rate,
        max (100.5%) otherwise
    @param maxFrlRate Indicates the highest FRL rate supported by the DUT
    @param cdf Optional CDF file to use
    @return TLqdResult"""

    return qdDev.runHfr2_84(callback, vic, ycc420, minPixRate, maxFrlRate, cdf)

def TLqdHFR2_85(qdDev, callback, vic, ycc420, minPixRate, maxFrlRate,cdf=None):

    """Run DSC sink test HFR2-85

    See @ref TLqdInstrument.runHfr2_85 for details

    @param qdDev Interface to quantumdata instrument
    @param callback Callback function to verify DSC video
    @param vic Video identification code for a 4320p format
    @param ycc420 Indicates testing YCbCr 4:2:0, 4:2:2 otherwise
    @param minPixRate Indicates minimum (99.5%) pixel rate,
        max (100.5%) otherwise
    @param maxFrlRate Indicates the highest FRL rate supported by the DUT
    @param cdf Optional CDF file to use
    @return TLqdResult"""

    return qdDev.runHfr2_85(callback, vic, ycc420, minPixRate, maxFrlRate, cdf)

def TLqdReadCapabilityRegisters(qdDev, register, quantity=1):

    """Read DisplayPort capability register(s) from the sink

    See @ref TLqdInstrument.readCapabilityRegisters for details

    @param qdDev Interface to quantumdata instrument
    @param register First register to read
    @return collection of register values"""

    return qdDev.readCapabilityRegisters(register, quantity)

def TLqdGetCapabilityRegisters(qdDev, register, quantity=1):

    """Get the current DisplayPort capability register(s) from the sink

    See @ref TLqdInstrument.getCapabilityRegisters for details

    @param qdDev Interface to quantumdata instrument
    @param register First register to return
    @return collection of register values"""

    return qdDev.getCapabilityRegisters(register, quantity)

def TLqdSetCapabilityRegisters(qdDev, firstRegister, values):

    """Set new DisplayPort capability register(s) on the sink

    See @ref TLqdInstrument.setCapabilityRegisters for details

    @param qdDev Interface to quantumdata instrument
    @param register First register to set
    @param values collection of register values"""

    return qdDev.setCapabilityRegisters(firstRegister, values)

def TLqdGetTestAutoRegister(qdDev, register):

    """Get the current Test Auto register from the sink

    See @ref TLqdInstrument.getTestAutoRegister for details

    @param qdDev Interface to quantumdata instrument
    @param register register address to read
    @return register value in hex"""

    return qdDev.getTestAutoRegister(register)

def TLqdSetTestAutoRegister(qdDev, register, value):

    """Set new Test Auto register on the sink

    See @ref TLqdInstrument.setTestAutoRegister for details

    @param qdDev Interface to quantumdata instrument
    @param register register address to write
    @param value register value
    @return String empty string for success or ERROR for failure"""

    return qdDev.setTestAutoRegister(register, value)

class TLqdStatus(StatusValue):
    """@brief Status of operation

    Supported statuses"""

    def __init__(self, value):

        """Create a status

        @param self The new TLqdStatus object
        @param value String"""

        StatusValue.__init__(self, value)

    ## The operation passed or succeeded
    PASS = StatusValue('Pass')
    ## The operation failed
    FAIL = StatusValue('Fail')
    ## The operation was skipped
    SKIPPED = StatusValue('Skipped')

class TLqdStepStatus(StatusValue):
    """@brief Status of operation

    Supported statuses"""

    def __init__(self, value):

        """Create a status

        @param self The new TLqdStepStatus object
        @param value String"""

        StatusValue.__init__(self, value)

    ## The button have PASS option
    PASS = StatusValue('Pass')

    ## The button have FAIL option
    FAIL = StatusValue('Fail')

    ## The button have OK option
    OK = StatusValue('Ok')

    ## The button have NO option
    NO = StatusValue('No')

    ## The button have Replay option
    REPLAY = StatusValue('Replay')

class TLqdStep(object):
    """@brief Test Step information

       used to provide step info to user"""

    description = ''
    okOption = False
    noOption = False
    passOption = False
    failOption = False
    replayOption = False

class TLqdResult(object):
    """@brief Test result

    Results of running a test or command"""

    def __init__(self, status, info, errors):

        """Create a result

        @param self The new TLqdResult object
        @param status Status from the operation
        @param info Collection of information from operation
        @param errors Collection of errors detected during the operation"""

        self.status = status
        self.info = info
        self.errors = errors

    def __str__(self):
        """Get a string representation

        @param self The TLqdResult object
        @return string representation"""

        return str(self.status)

class TLqdColorSpace(ColorSpaceValue):
    """@brief Color space

    Supported color spaces"""

    def __init__(self, name, key, needsSubsampling):

        """Create a color space

        @param self The new TLqdColorSpace object
        @param name String identifying the color space
        @param key Color space ID used by the quantumdata instrument
        @param needsSubsampling Indicates subsampling must be specified"""

        # No name?
        if name is None or name == '':
            # Find one and use it
            for cs in TLqdColorSpace.All:
                if cs.key == key:
                    name = cs.name
                    needsSubsampling = cs.needsSubsampling
                    break

        ColorSpaceValue.__init__(self, name, key, needsSubsampling)

    ## RGB
    RGB = ColorSpaceValue('RGB', 10, False)
    ## YCbCr601
    YCbCr601 = ColorSpaceValue('YCbCr601', 14, True)
    ## YCbCr709
    YCbCr709 = ColorSpaceValue('YCbCr709', 15, True)
    ## xvYCbCr601
    xvYCbCr601 = ColorSpaceValue('xvYCbCr601', 17, True)
    ## xvYCbCr709
    xvYCbCr709 = ColorSpaceValue('xvYCbCr709', 18, True)
    ## sYCC601
    sYCC601 = ColorSpaceValue('sYCC601', 19, True)
    ## opYCC601
    opYCC601 = ColorSpaceValue('opYCC601', 20, True)
    ## opRGB
    opRGB = ColorSpaceValue('opRGB', 21, False)
    ## BT2020cYCC
    BT2020cYCC = ColorSpaceValue('BT2020cYCC', 22, True)
    ## BT2020YCbCr
    BT2020YCbCr = ColorSpaceValue('BT2020YCbCr', 23, True)
    ## BT2020RGB
    BT2020RGB = ColorSpaceValue('BT2020RGB', 24, False)
    ## DCIP3RGB
    DCIP3RGB = ColorSpaceValue('DCIP3RGB', 25, False)

    ## All defined color spaces
    All = [RGB, YCbCr601, YCbCr709, xvYCbCr601, xvYCbCr709, sYCC601, opYCC601,
           opRGB, BT2020cYCC, BT2020YCbCr, BT2020RGB, DCIP3RGB]

class TLqdSubsampling(SubsamplingValue):
    """@brief Subsampling

    Supported sub-sampling"""

    def __init__(self, name, key):

        """Create a sub-sampling entry

        @param self The new TLqdSubsampling object
        @param name String identifying the subsampling
        @param key Subsampling ID used by the quantumdata instrument"""

        # No name?
        if name is None or name == '':
            # Find one and use it
            for cs in TLqdSubsampling.All:
                if cs.key == key:
                    name = cs.name
                    break

        SubsamplingValue.__init__(self, name, key)

    ## RGB 4:4:4
    RGB444 = SubsamplingValue('RGB 4:4:4', 0)
    ## 4:4:4
    SS444 = SubsamplingValue('4:4:4', 4)
    ## 4:2:2
    SS422 = SubsamplingValue('4:2:2', 2)
    ## 4:2:0
    SS420 = SubsamplingValue('4:2:0', 3)

    ## All defined sub-sampling
    All = [RGB444, SS444, SS422, SS420]

## @cond
class CaptureType(object):
    def __init__(self, type):
        self.type = type

    def __str__(self):
        return str(self.type)

    def __eq__(self, other):
        # Check for another CaptureType
        if isinstance(other, CaptureType):
            return self.type == other.type
        # Check for a number
        if isinstance(other, self.type.__class__):
            return self.type == other
        # Who knows what we were given
        return self.type == int(type)

    def __ne__(self, other):
        return not self.__eq__(other)
## @endcond

class TLqdCaptureType(CaptureType):
    """@brief Capture type

    Used to specify a capture type"""

    def __init__(self, type):

        """Specify a type of capture

        @param self the TLqdCaptureParameters object
        @param type Type of capture"""

        CaptureType.__init__(self, type)

    ## TmdsAnalysis TMDS Raw Byte analysis
    TmdsAnalysis = CaptureType(0)
    ## TmdsDataIsland TMDS data island only
    TmdsDataIsland = CaptureType(1)
    ## FrlDecode FRL decode
    FrlDecode = CaptureType(2)
    ## DpData DisplayPort data
    DpData = CaptureType(3)
    ## DpDscFec DisplayPort DSC/FEC
    DpDscFec = CaptureType(4)
    ## DpSDP DisplayPort SDP only
    DpSdp = CaptureType(5)
    ## DP Raw 10B data capture
    DpRaw10b = CaptureType(6)
    ## Dp Raw UHBR capture
    DpRawUHBR = CaptureType(7)
    ## TmdsDataAnalysis TMDS data analysis (audio, video, data island)
    TmdsDataAnalysis = CaptureType(8)
    ## FrlDataIsland Frl data island only
    FrlDataIsland = CaptureType(9)

class TLqdTriggerMode(CaptureType):
    """@brief Capture mode

    Used to specify a trigger mode"""

    def __init__(self, mode):

        """Specify a trigger mode

        @param self the TLqdTriggerMode object
        @param mode Trigger mode"""

        CaptureType.__init__(self, mode)

    ## No trigger
    NoTriggerMode = CaptureType(0)
    ## First event
    FirstEvent = CaptureType(1)
    ## After position
    AfterPosition = CaptureType(2)
    ## Immediate capture
    Immediate = CaptureType(3)
    ## Start of Frame
    StartOfFrame = CaptureType(4)
    ## Dp Specified Symbol
    DpSpecifiedSymbol = CaptureType(5)
    ## Dp data value
    DpDataValue = CaptureType(6)
    ## Dp Sdp type Received
    DpSdpTypeReceived = CaptureType(7)
    ## Dp Sdp type Not Received
    DpSdpTypeNotReceived = CaptureType(8)
    ## Dp Vbid Received
    DpVbidReceived = CaptureType(9)
    ## Dp Vbid Not Received
    DpVbidNotReceived = CaptureType(10)
    ## Dp Aux Read or Write
    DpAuxRw = CaptureType(11)
    ## Dp 8b10b Symbol Error
    DpSymbolError = CaptureType(12)
    ## Dp 8b10b Disparity Error
    DpDisparityError = CaptureType(13)
    ## Dp Tps2 Start
    DpTps2Start = CaptureType(14)
    ## Dp Tps3 Start
    DpTps3Start = CaptureType(15)
    ## Dp Tps4 Start
    DpTps4Start = CaptureType(16)
    ## Dp Hdcp13 Start
    DpHdcp13Start = CaptureType(17)
    ## Dp Hdcp22 Start
    DpHdcp22Start = CaptureType(18)
    ## Dp Mst Start
    DpMstStart = CaptureType(19)
    ## Dp Tps2 Exit
    DpTps2Exit = CaptureType(20)
    ## Dp Tps3 Exit
    DpTps3Exit = CaptureType(21)
    ## Dp Tps4 Exit
    DpTps4Exit = CaptureType(22)
    ## Dp Hdcp13 Exit
    DpHdcp13Exit = CaptureType(23)
    ## Dp Hdcp22 Exit
    DpHdcp22Exit = CaptureType(24)
    ## Dp Mst Exit
    DpMstExit = CaptureType(25)
    ## Dp Byte 10B
    DpByte10B = CaptureType(26)
    ## Dp Fec Decode Enable
    DpFecDecodeEnable = CaptureType(27)
    ## Dp FEC Decode Disable
    DpFECDecodeDisable = CaptureType(28)
    ## Dp Ml Phy Standby
    DpMlPhyStandby = CaptureType(29)
    ## Dp Ml Phy Sleep
    DpMlPhySleep = CaptureType(30)
    ## Dp Aux Phy Wake
    DpAuxPhyWake = CaptureType(31)
    ## Dp Uhbr Control Symbol Received
    DpUhbrCtlSybReceived = CaptureType(32)
    ## Dp PanelReplay Vsc Received
    DpVscRecevied = CaptureType(33)

class TLqdTriggerType(CaptureType):
    """@brief Capture trigger type

    Used to specify a capture trigger type"""

    def __init__(self, type):

        """Specify a capture trigger type

        @param self the TLqdTriggerType object
        @param mode Trigger type"""

        CaptureType.__init__(self, type)

    ## No trigger type
    NoTriggerType = CaptureType(0)
    ## VSYNC assert
    VsyncAssertTriggerType = CaptureType(1)
    ## Encryption enabled
    EncryptionEnabledTriggerType = CaptureType(2)
    ## Encryption disabled
    EncryptionDisabledTriggerType = CaptureType(3)
    ## External input
    ExternalInputTriggerType = CaptureType(4)
    ## Manual
    ManualTriggerType = CaptureType(5)
    ## TMDS clock change
    TmdsClockChangeTriggerType = CaptureType(6)
    ## FRL start
    FrlStartTriggerType = CaptureType(7)
    ## HDDCP2.3 Encrypted Frame Detected
    HDDCP23EncryptedFrameDetectTriggerType = CaptureType(8)
    ## Horizontal Total Change
    HTotalChangeTriggerType = CaptureType(9)
    ## Horizontal Active Change
    HActiveTriggerType = CaptureType(10)
    ## Horizontal Sync Change
    HSyncChangeTriggerType = CaptureType(11)
    ## Horizontal Front Change
    HFrontChangeTriggerType = CaptureType(12)
    ## Vertical Total Change
    VTotalChangeTriggerType = CaptureType(13)
    ## Vertical Active Change
    VActiveChangeTriggerType = CaptureType(14)
    ## Vertical Sync Change
    VSynceChangeTriggerType = CaptureType(15)
    ## Vertical Front Change
    VfrontChangeTriggerType = CaptureType(16)
    ## Partial Data Island Match 1
    PartialDataIslandMatch1TriggerType = CaptureType(17)

def TLqdCapture(qdDev, type, sizePct, localDirectory=None, qdDirectory=None,
                triggerMode=None, triggerType=None, position=None,
                hotplugDuration=None, videoCheck=False, getVideo=False,
                timing=False, interpret=False, interpretScambling=False,
                triggerData=None, triggerMask=None, triggerLaneMask=None,
                triggerDpcdAddress=None, captureTimeLimit=None,
                getDsc=False, getAca=False):
    """Perform a capture

    @param qdDev Interface to quantumdata instrument
    @param type TLqdCaptureType Type of capture
    @param sizePct Amount of memory in percent to use
    @param localDirectory Folder path to store capture artifacts
    @param qdDirectory instrument directory path to capture artifacts
    @param triggerMode TLqdTriggerMode Trigger mode
    @param triggerType TLqdTriggerType Type of trigger
    @param position Trigger position
    @param hotplugDuration Duration of hot-plug in milliseconds
    @param videoCheck Perform a video check
    @param getVideo Extract video frames
    @param timing Perform timing analysis
    @param interpret Interpret data islands
    @param interpretScambling Interpret scrambling
    @param triggerData trigger based on this data value
    @param triggerMask trigger based on mask for data value
    @param triggerLaneMask trigger based on mask for lanes
    @param triggerDpcdAddress trigger based on this dpcd address
    @param captureTimeLimit capture until this time limit in milliseconds
    @param getDsc Extract and uncompress Dsc frames
    @param getAca Collect ACA logs during capture
    @return TLqdResult"""

    return qdDev.capture(type, sizePct, localDirectory, qdDirectory,
                         triggerMode, triggerType, position, hotplugDuration,
                         videoCheck, getVideo, timing, interpret,
                         interpretScambling, triggerData, triggerMask,
                         triggerLaneMask, triggerDpcdAddress, captureTimeLimit,
                         getDsc, getAca)

def TLqdSetAudio(qdDev, audio):

    """Set audio LPCM

    @param qdDev Interface to quantumdata instrument
    @param audio TLqdAudio object
    @return TLqdResult"""

    return qdDev.setAudio(audio)

def TLqdGetAudio(qdDev):

    """Get audio LPCM

    @param qdDev Interface to quantumdata instrument
    @return TLqdAudio object"""

    return qdDev.getAudio()

def TLqdListCompressedAudio(qdDev):

    """Get a list of compressed audio formats

    @param qdDev Interface to quantumdata instrument
    @return Collection of TLqdCompressedAudio objects"""

    return qdDev.listCompressedAudio()

def TLqdSetCompressedAudio(qdDev, name):

    """Set a compressed audio format

    @param qdDev Interface to quantumdata instrument
    @param name Name of the compressed audio format
    @return TLqdResult"""

    return qdDev.setCompressedAudio(name)

def TLqdGetCompressedAudio(qdDev):

    """Get the compressed audio format in use

    @param qdDev Interface to quantumdata instrument
    @return TLqdCompressedAudio object"""

    return qdDev.getCompressedAudio()

def TLqdSetEarcAudio(qdDev, audio):

    """Set eARC audio LPCM

    @param qdDev Interface to quantumdata instrument
    @param audio TLqdAudio object
    @return TLqdResult"""

    return qdDev.setEarcAudio(audio)

def TLqdGetEarcAudio(qdDev):

    """Get eARC audio LPCM

    @param qdDev Interface to quantumdata instrument
    @return TLqdAudio object"""

    return qdDev.getEarcAudio()

def TLqdListEarcCompressedAudio(qdDev):

    """Get a list of eARC compressed audio formats

    @param qdDev Interface to quantumdata instrument
    @return Collection of TLqdCompressedAudio objects"""

    return qdDev.listEarcCompressedAudio()

def TLqdSetEarcCompressedAudio(qdDev, name, layoutB=False):

    """Set an eARC compressed audio format

    @param qdDev Interface to quantumdata instrument
    @param name Name of the compressed audio format
    @param layoutB Indicates layout B is used
    @return TLqdResult"""

    return qdDev.setEarcCompressedAudio(name, layoutB)

def TLqdGetEarcCompressedAudio(qdDev):

    """Get the eARC compressed audio format in use

    @param qdDev Interface to quantumdata instrument
    @return TLqdCompressedAudio object"""

    return qdDev.getEarcCompressedAudio()

def TLqdGetReceivedEarcAudio(qdDev):

    """Get the eARC audio being received

    @param qdDev Interface to quantumdata instrument
    @return TLqdReceivedAudio object"""

    return qdDev.getReceivedEarcAudio()

def TLqdSetEdidFile(qdDev, edidFile, hpDurationInMs=100):

    """Set the EDID file on the device

    @param qdDev Interface to quantumdata instrument
    @param edidFile Local file in XML format to load
    @param hpDurationInMs Hot-plug duration in milliseconds (0=no HP)
    @return TLqdResult"""

    return qdDev.setEdidFile(edidFile, hpDurationInMs)

def TLqdSetEdidData(qdDev, edidData, hpDurationInMs=100):

    """Set the EDID data on the device

    @param qdDev Interface to quantumdata instrument
    @param edidData String of EDID data ("00FFFFFFFFFFFF00...")
    @param hpDurationInMs Hot-plug duration in milliseconds (0=no HP)
    @return TLqdResult"""

    return qdDev.setEdidData(edidData, hpDurationInMs)

def TLqdEnableOutput(qdDev, enabled):
    """ Enable/disable output

    @param qdDev the TLqdInstrument object
    @param enabled Indicates if output is enabled or disabled"""

    qdDev.enableOutput(enabled)

def TLqdIsOutputEnabled(qdDev):
    """ Is output enabled/disabled

    @param qdDev the TLqdInstrument object
    @return True if output is enabled"""

    return qdDev.isOutputEnabled()

class TLqdCaptureOption(CaptureOption):
    """@brief Options for capture data

    Capture data option"""

    def __init__(self, value):
        """Create a capture option

        @param self the TLqdCaptureOption object
        @param value CaptureOption index"""

        CaptureOption.__init__(self, value)

    ## Nothing - no capture data
    Nothing = CaptureOption(0)

    ## All - all capture data
    All = CaptureOption(1)

    ## Failures - all capture data only for failures
    Failures = CaptureOption(2)

class TLqd3dOption(ThreeDoption):
    """@brief 3D options"""

    def __init__(self, value):
        """Create a 3D option

        @param self the TLqd3dOption object
        @param value ThreeDoption index"""

        ThreeDoption.__init__(self, value)

    ## Off - no 3D
    Off = ThreeDoption(-1)

    ## FramePacking - Frame packing
    FramePacking = ThreeDoption(0)

    ## LineAlt - Alternate lines
    LineAlt = ThreeDoption(2)

    ## SideFull - Full side-by-side
    SideFull = ThreeDoption(3)

    ## LplusDepth - L + depth
    LplusDepth = ThreeDoption(4)

    ## TopBottom - Top and bottom
    TopBottom = ThreeDoption(6)

    ## SideHalf - Half side-by-side
    SideHalf = ThreeDoption(8)

class TLqd3dExtOption(ThreeDextOption):
    """@brief 3D options"""

    def __init__(self, value):
        """Create a 3D extension option

        @param self the TLqd3dExtOption object
        @param value ThreeDextOption index"""

        ThreeDextOption.__init__(self, value)

    ## NoExt - no 3D extension
    NoExt = ThreeDextOption(-1)

    ## HorizontalSubSampling - Horizontal sub-sampling
    HorizontalSubSampling = ThreeDextOption(0)

    ## QuincunxOddOdd - Quincunx odd/odd
    QuincunxOddOdd = ThreeDextOption(1)

    ## QuincunxOddEven - Quincunx odd/even
    QuincunxOddEven = ThreeDextOption(2)

    ## QuincunxEvenOdd - Quincunx even/odd
    QuincunxEvenOdd = ThreeDextOption(3)

    ## QuincunxEvenEven - Quincunx even/even
    QuincunxEvenEven = ThreeDextOption(4)

class TLqd3dData(object):
    """@brief 3D data"""

    def __init__(self, option=TLqd3dOption.Off, ext=TLqd3dExtOption.NoExt):
        """Create 3D data

        @param self the TLqd3dData object
        @param option TLqd3dOption
        @param ext TLqd3dExtOption"""

        ## @param option 3D option
        self.option = option
        ## @param ext 3D extension
        self.ext = ext

    def __str__(self):
        """String representation

        @param self the TLqd3dData object"""

        ret = "3D: " + str(self.option)
        if self.option != TLqd3dOption.Off and \
            self.ext != TLqd3dExtOption.NoExt:
            ret = ret + ", extension: " + str(self.ext)

        return ret;

class TLqdTestParameters(object):
    """@brief Options to control a test or specify the results location

    Used to provide a test with results directory paths or control data.

    Be advised that specifying captureSizeFrames cannot guarantee the
    exact number of frames captured. Using this parameter will only result
    in a rough number of frames +/- 50%"""

    def __init__(self, localDirectory=None, qdDirectory=None, omitHp=None,
                 edidData=None, edidFile=None, captureSizePct=None,
                 durationMs=None, maxFrl=None, cdf=None,
                 saveCaptures=TLqdCaptureOption.All, captureSizeFrames=None,
                 collectAca=False, collectResult=False, collectEdid=False,
                 collectSyslog=False, collectAlllogs=False, callbackSrcSet=False):

        """Create test parameters

        @param self the TLqdTestParameters object
        @param localDirectory Folder path to store test result artifacts
        @param qdDirectory instrument directory path to store test result
            artifacts
        @param omitHp Hot-plug should be skipped
        @param edidData EDID data string
        @param edidFile local file with EDID XML data
        @param captureSizePct Capture size in percent
        @param durationMs Test duration in milliseconds
        @param maxFrl Maximum FRL rate 0-6
        @param cdf Optional CDF file
        @param saveCaptures Option for capture data, default is all, ignored if
            localDirectory is not specified
        @param captureSizeFrames Capture size in number of frames
        @param collectACA to capture ACA log
        @param collectResult to capture Result log
        @param collectEdid to capture Edid log
        @param collectSyslog to capture syslog
        @param collectAlllogs to capture all logs
        @param callbackSrcSet for source setup"""

        self.localDirectory = localDirectory
        self.qdDirectory = qdDirectory
        self.omitHp = omitHp
        self.edidData = edidData
        self.edidFile = edidFile
        self.captureSizePct = captureSizePct
        self.captureSizeFrames = captureSizeFrames
        self.durationMs = durationMs
        self.maxFrl = maxFrl
        self.cdf = cdf
        self.saveCaptures = saveCaptures
        self.collectAca = collectAca
        self.collectResult = collectResult
        self.collectEdid = collectEdid
        self.collectSyslog = collectSyslog
        self.collectAlllogs = collectAlllogs
        self.callbackSrcSet = callbackSrcSet

class TLqdScanType(ScanType):
    """@brief Type of frame transmission

    Scan type"""

    def __init__(self, value):
        """Create a scan type

        @param self the TLqdScanType object
        @param value Scan type index"""

        ScanType.__init__(self, value)

    ## Progressive
    Progressive = ScanType(1)

    ## Interlaced
    Interlaced = ScanType(2)

class TLqdPolarity(Polarity):
    """@brief Type of signal polarity

    Signal polarity"""

    def __init__(self, value):
        """Create a polarity

        @param self the TLqdPolarity object
        @param value Polarity index"""

        Polarity.__init__(self, value)

    ## Positive
    Positive = Polarity(1)

    ## Negative
    Negative = Polarity(0)

class InputColorSpace(TLqdColorSpace):
    def __init__(self, key):
        TLqdColorSpace.__init__(self, None, int(key), False)

class InputSubsampling(TLqdSubsampling):
    def __init__(self, key):
        TLqdSubsampling.__init__(self, None, int(key))

class TLqdAudioChannel(object):
    """@brief Audio channel data"""

    def __init__(self, frequency, amplitude):
        """Create a TLqdAudioChannel

        @param self the TLqdAudioChannel object
        @param frequency Sine wave frequency in Hz
        @param amplitude Sine wave amplitude in dB (<= 0)"""

        self.frequency = frequency
        self.amplitude = amplitude

class TLqdAudio(object):
    """@brief Audio data"""

    def __init__(self, sampling, bitSize=16, channels=[]):
        """Create a TLqdAudio

        @param self the TLqdAudio object
        @param sampling Sampling rate in Hz
        @param bitSize Number of bits per sample (16, 20 or 24)
        @param channels Optional collection of TLqdAudioChannel objects"""

        self.sampling = sampling
        self.bitSize = bitSize
        self.channels = channels

class TLqdCompressedAudio(object):
    """@brief Compressed audio data"""

    def __init__(self, name, type, channels=None, sampling=None, layoutB=False):
        """Create a TLqdCompressedAudio

        @param self the TLqdCompressedAudio object
        @param name Name of the compressed format
        @param type Compressed format type
        @param channels Optional channel information
        @param sampling Optional sampling information
        @param layoutB Optional layout B (for eARC only)"""

        self.name = name
        self.type = type
        self.sampling = sampling
        self.channels = channels
        self.layoutB = layoutB

class TLqdReceivedAudio(object):
    """@brief Received audio data"""

    def __init__(self, lpcm, compressed):
        """Create a TLqdReceivedAudio

        @param self the TLqdReceivedAudio object
        @param lpcm TLqdAudio
        @param compressed TLqdCompressedAudio"""

        self.lpcm = lpcm
        self.compressed = compressed

class TLqdDpErrorInfoParameters(object):
    """@brief Error Information"""

    def __init__(self, fec, unCorrectedErrors, correctedErrors, bitErrors,
        parityBlockErrors, bitEightTenTraining, symbolError, disparityError):
        """Create an Error Information

        @param self the TLqdDpErrorInfoParameters object
        @param fec the Forward error correction
        @param unCorrectedErrors the Uncorrected errors
        @param correctedErrors the Corrected errors
        @param bitErrors"""

        self.fec = fec
        self.unCorrectedErrors = unCorrectedErrors
        self.correctedErrors = correctedErrors
        self.bitErrors = bitErrors
        self.parityBlockErrors = parityBlockErrors
        self.bitEightTenTraining = bitEightTenTraining
        self.symbolError = symbolError
        self.disparityError = disparityError


class TLqdDpLaneStatus(object):
    """@brief Lane status"""

    def __init__(self, crStatus, ceqStatus, slckStatus, volSwing, preEmp, ffe):
        """Create a Lane status

        @param self the TLqdDpLaneStatus object
        @param crStatus Clock recovery status
        @param ceqStatus Channel equalization status
        @param slckStatus Symbol lock status
        @param volSwing Voltage swing level
        @param preEmp Lane Pre Emphasis Level
        @param ffe the FFE Level"""

        self.crStatus = crStatus
        self.ceqStatus = ceqStatus
        self.slckStatus = slckStatus
        self.volSwing = volSwing
        self.preEmp = preEmp
        self.ffe = ffe

class TLqdRxLinkTrainingStatus(object):
    """@brief Rx link training status

        Used to provide Rx link training status"""

    def __init__(self, activeLanes, bandWidth, dpLaneStatus):
        """Create a Rx link training status

        @param self the TLqdRxLinkTrainingStatus object
        @param activeLanes the Number of active lanes
        @param bandWidth the Link bandwidth in Gbps
        @param dpLaneStatus the Lane status"""

        self.activeLanes = activeLanes
        self.bandWidth = bandWidth
        self.dpLaneStatus = dpLaneStatus

class TLqdTxLinkTrainingStatus(object):
    """@brief Tx link training status

        Used to provide Tx link training status"""

    def __init__(self, mainStream='', activeLanes=None, bandWidth='',
                 dpLaneStatus=None, interLaneAlign=''):

        """Create a Tx link training status

        @param self the TLqdTxLinkTrainingStatus object
        @param mainStream the Status of main stream
        @param activeLanes the Number of active lanes
        @param bandWidth the Link bandwidth in Gbps
        @param dpLaneStatus the Lane status
        @param interLaneAlign the Inter lane alignment status"""

        self.mainStream = mainStream
        self.activeLanes = activeLanes
        self.bandWidth = bandWidth
        self.dpLaneStatus = dpLaneStatus
        self.interLaneAlign = interLaneAlign

class TLqdCrcParameters(object):
    """@brief Crc Parameters

        Used to provide crc status and values"""

    def __init__(self, option, crc0, crc1, crc2, crcRCr, crcGY, crcBCb,
                 dscStatus):
        """Create Crc parameters

        @param self the TLqdCrcParameters object
        @param option Option of crc info
        @param crc0 Dsc crc engine 0
        @param crc1 Dsc crc engine 1
        @param crc2 Dsc crc engine 2
        @param crcRCr the R or Cr components crc value
        @param crcGY the G or Y components crc value
        @param crcBCb the B or Cb components crc value
        @param dscStatus DSC video crc status """

        self.option = option
        self.crc0 = crc0
        self.crc1 = crc1
        self.crc2 = crc2
        self.crcRCr = crcRCr
        self.crcGY = crcGY
        self.crcBCb = crcBCb
        self.dscStatus = dscStatus

class TLqdHdcpParameters(object):
    """@brief HDCP Parameters

        Used to provide HDCP status and Key Type"""

    def __init__(self, hdcpStatus, key):
        """Create HDCP parameters

        @param self the TLqdHdcpParameters object
        @param hdcpStatus HDCP status
        @param key HDCP key type"""

        self.hdcpStatus = hdcpStatus
        self.key = key

class TLqdVstatParameters(object):
    """@brief Vstat Parameters

        Used to provide Vstat Parameters"""

    def __init__(self, link, laneCount, bandWidth, horizontalResolution, horizontalTotal, verticalResolution, verticalTotal,
                scan, numberBitsPerChannel, color, digtalVideoSignalMode, hdcpEncrption, verticalRate, downSpread):
        """Create vstat parameters

        @param self the TLqdVstatParameters object
        @param link
        @param laneCount the Number of active lanes
        @param bandWidth Link bandwidth in Gbps
        @param horizontalResolution Horizontal resolution of transmitted main video stream
        @param horizontalTotal Horizontal total of transmitted main video stream
        @param verticalResolution Vertical resolution of transmitted main video stream
        @param verticalTotal Vertical total of transmitted main video stream
        @param scan
        @param numberBitsPerChannel Number of bits per channel
        @param color
        @param digtalVideoSignalMode Digital video sampling mode
        @param hdcpEncrption Hdcp encrption indicator value
        @param verticalRate Vertical rate
        @param downSpread Downspread"""

        self.link = link
        self.laneCount = laneCount
        self.bandWidth = bandWidth
        self.horizontalResolution = horizontalResolution
        self.horizontalTotal = horizontalTotal
        self.verticalResolution = verticalResolution
        self.verticalTotal = verticalTotal
        self.scan = scan
        self.numberBitsPerChannel = numberBitsPerChannel
        self.color = color
        self.digtalVideoSignalMode = digtalVideoSignalMode
        self.hdcpEncrption = hdcpEncrption
        self.verticalRate = verticalRate
        self.downSpread = downSpread

class TLqdMsaParameters(object):
    """@brief Msa Parameters

        Used to provide Main stream attributes"""

    def __init__(self, horizontalTotal, horizontalSyncPolarity, verticalTotal, verticalSyncPolarity,
                horizontalSyncWidth, verticalSyncWidth, horizontalResolution, verticalResolution,
                horizontalStart, verticalStart, misc0, misc1, verticalFrequency, streamClock, vbId, aFrequency):
        """Create Msa parameters

        @param self the TLqdMsaParameters object
        @param horizontalTotal Horizontal total of transmitted main video stream
        @param horizontalSyncPolarity Horizontal sync pulse polarity in pixel count
        @param verticalTotal Vertical total of transmitted main video stream
        @param verticalSyncPolarity Vertical sync pulse polarity in pixel count
        @param horizontalSyncWidth Horizontal sync pulse width in pixel count
        @param verticalSyncWidth Horizontal sync pulse width in pixel count
        @param horizontalResolution Horizontal resolution of transmitted main video stream
        @param verticalResolution Vertical resolution of transmitted main video stream
        @param horizontalStart Horizontal start from leading edge of HSync
        @param verticalStart Vertical start from leading edge of VSync
        @param misc0
        @param misc1
        @param verticalFrequency Vertical frequency
        @param streamClock Synchronous clock
        @param vbId VB-id
        @param aFrequency Audio frequency"""

        self.horizontalTotal = horizontalTotal
        self.horizontalSyncPolarity = horizontalSyncPolarity
        self.verticalTotal = verticalTotal
        self.verticalSyncPolarity = verticalSyncPolarity
        self.horizontalSyncWidth = horizontalSyncWidth
        self.verticalSyncWidth = verticalSyncWidth
        self.horizontalResolution = horizontalResolution
        self.verticalResolution = verticalResolution
        self.horizontalStart = horizontalStart
        self.verticalStart = verticalStart
        self.misc0 = misc0
        self.misc1 = misc1
        self.verticalFrequency = verticalFrequency
        self.streamClock = streamClock
        self.vbId = vbId
        self.aFrequency = aFrequency

class TLqdLinkTrainingTime(object):
    """@brief Link Training Time Info

        Used to provide Link Training Time Info"""

    def __init__(self, rxPhyLocked, tps2Detected, tps3Detected, tps4Detected,
                lane0Trained, lane1Trained, lane2Trained, lane3Trained,
                noTpDetected,ltComplete, vstreamDetect,
                lane0ClkLock, lane1ClkLock, lane2ClkLock, lane3ClkLock):
        """Create Link Training Time Info

        @param self the TLqdLinkTrainingTime object
        @param rxPhyLocked  Rx phy locked time
        @param tps2Detected Tps2 detected time
        @param tps3Detected Tps3 detected time
        @param tps4Detected Tps4 detected time
        @param lane0Trained Lane0 trained time
        @param lane1Trained Lane1 trained time
        @param lane2Trained Lane2 trained time
        @param lane3Trained Lane3 trained time
        @param NoTpDetected No tp detected time
        @param ltComplete Link training complete time
        @param vstreamDetect Vstream detect time
        @param lane0ClkLock Lane0 clock lock time
        @param lane1ClkLock Lane1 clock lock time
        @param lane2ClkLock Lane2 clock lock time
        @param lane3ClkLock Lane3 clock lock time"""

        self.rxPhyLocked = rxPhyLocked
        self.tps2Detected = tps2Detected
        self.tps3Detected = tps3Detected
        self.tps4Detected = tps4Detected
        self.lane0Trained = lane0Trained
        self.lane1Trained = lane1Trained
        self.lane2Trained = lane2Trained
        self.lane3Trained = lane3Trained
        self.noTpDetected = noTpDetected
        self.ltComplete = ltComplete
        self.vstreamDetect = vstreamDetect
        self.lane0ClkLock = lane0ClkLock
        self.lane1ClkLock = lane1ClkLock
        self.lane2ClkLock = lane2ClkLock
        self.lane3ClkLock = lane3ClkLock

class TLqdVideoFormatParameters(object):
    """@brief Video format parameters

    Settings for outputting video

    @param HorizontalRate <SUP>*</SUP> Line frequency
    @param HorizontalResolution <SUP>*</SUP> Number of pixels in a line
    @param HorizontalSyncPulseDelay <SUP>*</SUP> Horizontal sync pulse delay
    @param HorizontalSyncPulsePolarity <SUP>*</SUP> Horizontal sync pulse
        polarity
    @param HorizontalSyncPulseWidth <SUP>*</SUP> Horizontal sync pulse width
    @param HorizontalTotal <SUP>*</SUP> Total horizontal width
    @param NumberClocksPerPixel <SUP>*</SUP> Number of clocks/pixel for low
        frequency formats
    @param ScanType <SUP>*</SUP> Frame scan type: Interlaced or Progressive
    @param VerticalResolution <SUP>*</SUP> Number of lines in a frame
    @param VerticalSyncPulseDelay <SUP>*</SUP> Vertical sync pulse delay
    @param VerticalSyncPulsePolarity <SUP>*</SUP> Vertical sync pulse polarity
    @param VerticalSyncPulseWidth <SUP>*</SUP> Vertical sync pulse width
    @param VerticalTotal <SUP>*</SUP> Total vertical height
    @param CompositeSyncPulsePolarity Composite sync pulse polarity
    @param NumberBitsPerColor Pixel depth
    @param SignalType Signal type
    @param QuantizationMode Quantization mode
    @param SamplingMode Sampling mode
    @param VideoIdentificationCode CTA VIC
    @param HdmiVideoIdentificationCode HDMI VIC
    @param TuneFactor 1 or 1.001 for NTSC
    @param SignalPolarity Signal polarity
    @param ContentAspectRatio Content aspect ratio
    @param SignalAspectRatio Signal aspect ratio
    @param ExtendedAspectRatio Extended aspect ratio
    @param NumberPixelsPerPixel Number of pixel/pixel
    @param ProtocolType DVI or HDMI
    @param GammaCorrectionFactor Gamma correction factor
    @param GammaCorrectionMode Gamma correction mode
    @param HorizontalSize Horizontal size units
    @param VerticalSize Vertical size units
    @param EqualizationBeforeVerticalSyncPulse Equalization before vertical
        sync pulse
    @param EqualizationAfterVerticalSyncPulse Equalization after vertical sync
        pulse
    @param SizeUnit Size of a unit
    @param SelectSyncSignalType Select sync signal type
    @param DigitalSyncCompositeType Digital sync composite type
    @param DigitalSyncSeparateType Digital sync separate type
    @param DisplayCodeBitMask Display code bitmask
    @param DisplayCodeExpected Display code expected
    @param HorizontalSyncPulseGate Horizontal sync pulse gate
    @param VerticalSyncPulseGate Vertical sync pulse gate
    @param CompositeSyncPulseGate Composite sync pulse gate
    @param RedGate Red color gate
    @param GreenGate Green color gate
    @param BlueGate Blue color gate
    @param RepeatField Repeat field
    @param PixelClockPulseGate Pixel clock pulse gate
    @param TriLevelSyncPulseGate Tri-level sync pulse gate
    @param PixelElementDepth Pixel element depth
    @param HorizontalVerticalSyncAdjustment Horizontal vertical sync adjustment
    @param DcBalancingGate DC balancing gate
    @param PreemphasisGate Preemphasis gate
    @param NumberLinks Number of links
    @param HorizontalVerticalPulseDelay Horizontal vertical pulse delay
    @param NumberAudioBits Number of audio bits
    @param AudioRate Audio rate in Hz
    @param NumberDigitalAudioStreams Number of audio streams
    @param NumberDigitalAudioChannels Number of audio channels
    @param AudioSignalType Audio signal type
    @param AudioSignalInterface Audio signal interface
    @param AudioContentAvailable Audio content available
    @param AudioContentGate Audio content gate
    @param AudioChannelsAvailable Audio channels available
    @param AudioChannelGate Audio channel gate
    @param AudioLevelShift Audio level shift
    @param AudioDownmixingGate Audio downmixing gate
    @param SignalFromExtendedApertureMap Signal from extended aperture map
    @param ExtendedFromContentApertureMap Extended from content aperture map
    @param ArbitraryLeftBorderWidth Arbitrary left border width
    @param ArbitraryRightBorderWidth Arbitrary right border width
    @param ArbitraryTopBorderHeight Arbitrary top border height
    @param ArbitraryBottomBorderHeight Arbitrary bottom border height
    @param SignalSwing Signal swing level
    @param * Required parameter
    """

    ## @private
    tags = [
        VideoFormatParameter("DVIC", "VideoIdentificationCode", False),
        VideoFormatParameter("HRAT", "HorizontalRate", True, float),
        VideoFormatParameter("HRES", "HorizontalResolution", True),
        VideoFormatParameter("HSPD", "HorizontalSyncPulseDelay", True),
        VideoFormatParameter("HSPP", "HorizontalSyncPulsePolarity", True,
            TLqdPolarity),
        VideoFormatParameter("HSPW", "HorizontalSyncPulseWidth", True),
        VideoFormatParameter("HTOT", "HorizontalTotal", True),
        VideoFormatParameter("NCPP", "NumberClocksPerPixel", True),
        VideoFormatParameter("SCAN", "ScanType", True, TLqdScanType),
        VideoFormatParameter("VRES", "VerticalResolution", True),
        VideoFormatParameter("VSPD", "VerticalSyncPulseDelay", True),
        VideoFormatParameter("VSPP", "VerticalSyncPulsePolarity", True,
            TLqdPolarity),
        VideoFormatParameter("VSPW", "VerticalSyncPulseWidth", True),
        VideoFormatParameter("VTOT", "VerticalTotal", True),
        VideoFormatParameter("CSPP", "CompositeSyncPulsePolarity", False,
            TLqdPolarity),
        VideoFormatParameter("NBPC", "NumberBitsPerColor"),
        VideoFormatParameter("DVST", "SignalType", True, InputColorSpace),
        VideoFormatParameter("DVQM", "QuantizationMode"),
        VideoFormatParameter("DVSM", "SamplingMode", True, InputSubsampling),
        VideoFormatParameter("HVIC", "HdmiVideoIdentificationCode"),
        VideoFormatParameter("TUNE", "TuneFactor", False, float),
        VideoFormatParameter("DVSP", "SignalPolarity", False, TLqdPolarity),
        VideoFormatParameter("CXAR", "ContentAspectRatio", False, float),
        VideoFormatParameter("SXAR", "SignalAspectRatio", False, float),
        VideoFormatParameter("EXAR", "ExtendedAspectRatio", False, float),
        VideoFormatParameter("NPPP", "NumberPixelsPerPixel"),
        VideoFormatParameter("DVPT", "ProtocolType"),
        VideoFormatParameter("GAMA", "GammaCorrectionFactor", False, float),
        VideoFormatParameter("GAMC", "GammaCorrectionMode"),
        VideoFormatParameter("HSIZ", "HorizontalSize", False, float),
        VideoFormatParameter("VSIZ", "VerticalSize", False, float),
        VideoFormatParameter("EQUB", "EqualizationBeforeVerticalSyncPulse"),
        VideoFormatParameter("EQUA", "EqualizationAfterVerticalSyncPulse"),
        VideoFormatParameter("USIZ", "SizeUnit"),
        VideoFormatParameter("SSST", "SelectSyncSignalType"),
        VideoFormatParameter("DSCT", "DigitalSyncCompositeType"),
        VideoFormatParameter("DSST", "DigitalSyncSeparateType"),
        VideoFormatParameter("DCBM", "DisplayCodeBitMask"),
        VideoFormatParameter("DCEX", "DisplayCodeExpected"),
        VideoFormatParameter("HSPG", "HorizontalSyncPulseGate"),
        VideoFormatParameter("VSPG", "VerticalSyncPulseGate"),
        VideoFormatParameter("CSPG", "CompositeSyncPulseGate"),
        VideoFormatParameter("REDG", "RedGate"),
        VideoFormatParameter("GRNG", "GreenGate"),
        VideoFormatParameter("BLUG", "BlueGate"),
        VideoFormatParameter("RFLD", "RepeatField"),
        VideoFormatParameter("PCPG", "PixelClockPulseGate"),
        VideoFormatParameter("TSPG", "TriLevelSyncPulseGate"),
        VideoFormatParameter("PELD", "PixelElementDepth"),
        VideoFormatParameter("HVSA", "HorizontalVerticalSyncAdjustment"),
        VideoFormatParameter("BALG", "DcBalancingGate"),
        VideoFormatParameter("PREG", "PreemphasisGate"),
        VideoFormatParameter("NLNK", "NumberLinks"),
        VideoFormatParameter("HVPD", "HorizontalVerticalPulseDelay"),
        VideoFormatParameter("NBPA", "NumberAudioBits"),
        VideoFormatParameter("ARAT", "AudioRate", False, float),
        VideoFormatParameter("NDAS", "NumberDigitalAudioStreams"),
        VideoFormatParameter("NDAC", "NumberDigitalAudioChannels"),
        VideoFormatParameter("DAST", "AudioSignalType"),
        VideoFormatParameter("DASI", "AudioSignalInterface"),
        VideoFormatParameter("DAXA", "AudioContentAvailable"),
        VideoFormatParameter("DAXG", "AudioContentGate"),
        VideoFormatParameter("DACA", "AudioChannelsAvailable"),
        VideoFormatParameter("DACG", "AudioChannelGate"),
        VideoFormatParameter("DALS", "AudioLevelShift"),
        VideoFormatParameter("DADG", "AudioDownmixingGate"),
        VideoFormatParameter("SXEX", "SignalFromExtendedApertureMap"),
        VideoFormatParameter("EXCX", "ExtendedFromContentApertureMap"),
        VideoFormatParameter("XLBW", "ArbitraryLeftBorderWidth"),
        VideoFormatParameter("XRBW", "ArbitraryRightBorderWidth"),
        VideoFormatParameter("XTBH", "ArbitraryTopBorderHeight"),
        VideoFormatParameter("XBBH", "ArbitraryBottomBorderHeight"),
        VideoFormatParameter("DVSS", "SignalSwing", False, float),
        VideoFormatParameter("PRAT", "PixelRate", False, float),
        VideoFormatParameter("FRAT", "FrameRate", False, float),
        VideoFormatParameter("LANES", "NumberLanes"),
        VideoFormatParameter("LRAT", "LaneRate", False, float),
        ]

    def __init__(self):
        """Create video parameters

        @param self the TLqdVideoFormatParameters object"""

        # Create the member dictionary
        for tag in TLqdVideoFormatParameters.tags:
            self.__dict__[tag.longTag] = None

    def __str__(self):
        """Represent video parameters as a string

        @param self the TLqdVideoFormatParameters object"""

        ret = []
        comma = ''
        for tag in TLqdVideoFormatParameters.tags:
            if tag.manditory or self.__dict__[tag.longTag] is not None:
                value = ''
                if self.__dict__[tag.longTag] is not None:
                    value = self.__dict__[tag.longTag]
                ret.append(comma + tag.longTag + ":" + str(value))
                comma = ', '
        return ''.join(ret)

    ## @cond

    def isSub(self, type, value):
        if type is object:
            # Since everything is an object, fail
            return False
        if isinstance(value, type):
            return True
        for sc in type.__bases__:
            if self.isSub(sc, value):
                return True
        return False

    def getCode(self, type, value):
        if type == int or type == float:
            return type(value)
        # Make sure the types match
        if self.isSub(type, value):
            if type == TLqdPolarity or type == TLqdScanType:
                return value.value
            if type == TLqdColorSpace or type == InputColorSpace or \
                type == TLqdSubsampling or type == InputSubsampling:
                return value.key
        if self.isSub(int, value):
            return value
        return None

    ## @endcond
