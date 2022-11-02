"""
PalmSens Serial Port (UART) interface

This module implements the serial interface to the PalmSens instrument.

This module uses the "pyserial" module, which must be installed before running
this code. See https://pypi.org/project/pyserial/ for more information.

-------------------------------------------------------------------------------
Copyright (c) 2021 PalmSens BV
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

   - Redistributions of source code must retain the above copyright notice,
     this list of conditions and the following disclaimer.
   - Neither the name of PalmSens BV nor the names of its contributors
     may be used to endorse or promote products derived from this software
     without specific prior written permission.
   - This license does not release you from any requirement to obtain separate 
	  licenses from 3rd party patent holders to use this software.
   - Use of the software either in source or binary form must be connected to, 
	  run on or loaded to an PalmSens BV component.

DISCLAIMER: THIS SOFTWARE IS PROVIDED BY PALMSENS "AS IS" AND ANY EXPRESS OR
IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO
EVENT SHALL THE REGENTS AND CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA,
OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE,
EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

# Standard library imports
import logging

# Third-party imports
import serial
import serial.tools.list_ports


LOG = logging.getLogger(__name__)


def _is_mscript_device(port):
    """Check if the specified port is a known MethodSCRIPT device."""
    # NOTES:
    # - Since the EmStat Pico uses a generic FTDI USB-to-Serial chip,
    #   it is identified by Windows as "USB Serial Port". This is the
    #   text to look for when using the auto detection feature. Note
    #   that an EmStat Pico or Sensit BT cannot be auto-detected if
    #   there are also other devices connected that use this name.
    # - An EmStat4 device in bootloader mode would be identified as
    #   'EmStat4 Bootloader', but we only want to connect to devices
    #   that can run MethodSCRIPTs, so we do not include that here.
    return (port.description == 'EmStat4' or
            port.description.startswith('ESPicoDev') or
            port.description.startswith('SensitBT') or
            port.description.startswith('SensitSmart') or
            # ^ Above names are used in Linux
            # v Below names are used in Windows
            port.description.startswith('EmStat4 LR (COM') or
            port.description.startswith('EmStat4 HR (COM') or
            port.description.startswith('MultiEmStat4 LR (COM') or
            port.description.startswith('MultiEmStat4 HR (COM') or
            port.description.startswith('USB Serial Port'))


def auto_detect_port():
    """Auto detect serial communication port.

    This works by searching for an available port with the correct name.
    If exactly one port matches, this port will be returned. If there
    are either no or multiple matches, the auto detection fails and None
    is returned instead. In that case, the user must explicitly specify
    which port to connect to (or disconnect unneeded devices with the
    same port name).
    """
    LOG.info('Auto-detecting serial communication port.')
    # Get the available ports.
    ports = serial.tools.list_ports.comports(include_links=False)
    candidates = []
    for port in ports:
        LOG.debug('Found port: %s', port.description)
        if _is_mscript_device(port):
            candidates.append(port)

    if len(candidates) != 1:
        LOG.error('%d candidates found. Auto detect failed.', len(candidates))
        raise Exception('Auto detection of serial port failed.')

    LOG.info('Exactly one candidate found. Using %s.', port.device)
    return candidates[0].device


class Serial():
    """Serial communication interface for EmStat Pico."""

    def __init__(self, port, timeout):
        self.connection = serial.Serial(port=None, baudrate=230400, timeout=timeout)
        self.connection.port = port

    def __enter__(self):
        if not self.connection.is_open:
            self.open()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def open(self):
        self.connection.open()

    def close(self):
        self.connection.close()

    def write(self, data: bytes):
        self.connection.write(data)

    def readline(self) -> bytes:
        return self.connection.readline()
