"""
PalmSens MethodSCRIPT module

This module provides functionality to translate and interpret the output of a
MethodSCRIPT (the measurement data).

The most relevant functions are:
  - parse_mscript_data_package(line)
  - parse_result_lines(lines)

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
import collections
import math
import warnings

# Third-party imports
import numpy as np


# Custom types
VarType = collections.namedtuple('VarType', ['id', 'name', 'unit'])
MScriptVar = collections.namedtuple('MScriptVar', ['type', 'value', 'value_string', 'metadata'])

# Dictionary for the conversion of the SI prefixes.
SI_PREFIX_FACTOR = {
    # supported SI prefixes:
    'a': 1e-18,  # atto
    'f': 1e-15,  # femto
    'p': 1e-12,  # pico
    'n': 1e-9,   # nano
    'u': 1e-6,   # micro
    'm': 1e-3,   # milli
    ' ': 1e0,
    'k': 1e3,    # kilo
    'M': 1e6,    # mega
    'G': 1e9,    # giga
    'T': 1e12,   # tera
    'P': 1e15,   # peta
    'E': 1e18,   # exa
    # special case:
    'i': 1e0,    # integer
}

# List of MethodSCRIPT variable types.
MSCRIPT_VAR_TYPES_LIST = [
    VarType('aa', 'unknown', ''),

    VarType('ab', 'WE vs RE potential', 'V'),
    VarType('ac', 'CE vs GND potential', 'V'),
    VarType('ad', 'SE vs GND potential', 'V'),
    VarType('ae', 'RE vs GND potential', 'V'),
    VarType('af', 'WE vs GND potential', 'V'),
    VarType('ag', 'WE vs CE potential', 'V'),

    VarType('as', 'AIN0 potential', 'V'),
    VarType('at', 'AIN1 potential', 'V'),
    VarType('au', 'AIN2 potential', 'V'),
    VarType('av', 'AIN3 potential', 'V'),
    VarType('aw', 'AIN4 potential', 'V'),
    VarType('ax', 'AIN5 potential', 'V'),
    VarType('ay', 'AIN6 potential', 'V'),
    VarType('az', 'AIN7 potential', 'V'),

    VarType('ba', 'WE current', 'A'),

    VarType('ca', 'Phase', 'degrees'),
    VarType('cb', 'Impedance', '\u2126'),  # NB: '\u2126' = ohm symbol
    VarType('cc', 'Z_real', '\u2126'),
    VarType('cd', 'Z_imag', '\u2126'),

    VarType('ce', 'EIS E TDD', 'V'),
    VarType('cf', 'EIS I TDD', 'A'),
    VarType('cg', 'EIS sampling frequency', 'Hz'),
    VarType('ch', 'EIS E AC', 'Vrms'),
    VarType('ci', 'EIS E DC', 'V'),
    VarType('cj', 'EIS I AC', 'Arms'),
    VarType('ck', 'EIS I DC', 'A'),

    VarType('da', 'Applied potential', 'V'),
    VarType('db', 'Applied current', 'A'),
    VarType('dc', 'Applied frequency', 'Hz'),
    VarType('dd', 'Applied AC amplitude', 'Vrms'),

    VarType('ea', 'Channel', ''),
    VarType('eb', 'Time', 's'),
    VarType('ec', 'Pin mask', ''),
    VarType('ed', 'Temperature', '\u00B0 Celsius'),  # NB: '\u00B0' = degrees symbol

    VarType('ha', 'Generic current 1', 'A'),
    VarType('hb', 'Generic current 2', 'A'),
    VarType('hc', 'Generic current 3', 'A'),
    VarType('hd', 'Generic current 4', 'A'),

    VarType('ia', 'Generic potential 1', 'V'),
    VarType('ib', 'Generic potential 2', 'V'),
    VarType('ic', 'Generic potential 3', 'V'),
    VarType('id', 'Generic potential 4', 'V'),

    VarType('ja', 'Misc. generic 1', ''),
    VarType('jb', 'Misc. generic 2', ''),
    VarType('jc', 'Misc. generic 3', ''),
    VarType('jd', 'Misc. generic 4', ''),
]

MSCRIPT_VAR_TYPES_DICT = {x.id: x for x in MSCRIPT_VAR_TYPES_LIST}

METADATA_STATUS_FLAGS = [
    (0x1, 'TIMING_ERROR'),
    (0x2, 'OVERLOAD'),
    (0x4, 'UNDERLOAD'),
    (0x8, 'OVERLOAD_WARNING'),
]

MSCRIPT_CURRENT_RANGES_EMSTAT_PICO = {
    0: '100 nA',
    1: '2 uA',
    2: '4 uA',
    3: '8 uA',
    4: '16 uA',
    5: '32 uA',
    6: '63 uA',
    7: '125 uA',
    8: '250 uA',
    9: '500 uA',
    10: '1 mA',
    11: '5 mA',
    128: '100 nA (High speed)',
    129: '1 uA (High speed)',
    130: '6 uA (High speed)',
    131: '13 uA (High speed)',
    132: '25 uA (High speed)',
    133: '50 uA (High speed)',
    134: '100 uA (High speed)',
    135: '200 uA (High speed)',
    136: '1 mA (High speed)',
    137: '5 mA (High speed)',
}

MSCRIPT_CURRENT_RANGES_EMSTAT4 = {
    # EmStat4 LR only:
    3: '1 nA',
    6: '10 nA',
    # EmStat4 LR/HR:
    9: '100 nA',
    12: '1 uA',
    15: '10 uA',
    18: '100 uA',
    21: '1 mA',
    24: '10 mA',
    # EmStat4 HR only:
    27: '100 mA',
}

MSCRIPT_POTENTIAL_RANGES_EMSTAT4 = {
    2:  "50 mV",
    3: "100 mV",
    4: "200 mV",
    5: "500 mV",
    6:   "1 V",
}


def get_variable_type(id):
    """Get the variable type with the specified id."""
    if id in MSCRIPT_VAR_TYPES_DICT:
        return MSCRIPT_VAR_TYPES_DICT[id]
    warnings.warn('Unsupported VarType id "%s"!' % id)
    return VarType(id, 'unknown', '')


def metadata_status_to_text(status):
    descriptions = []
    for mask, description in METADATA_STATUS_FLAGS:
        if status & mask:
            descriptions.append(description)
    if descriptions:
        return ' | '.join(descriptions)
    else:
        return 'OK'


def metadata_current_range_to_text(device_type, var_type, cr):
    cr_text = None
    if device_type == 'EmStat Pico':
        cr_text = MSCRIPT_CURRENT_RANGES_EMSTAT_PICO.get(cr)
    elif 'EmStat4' in device_type:
        # For EmStat4 series instruments, the range can be a current range or
        # potential range, depending on the variable type.
        if var_type.id in ['ab', 'cd']:
            cr_text = MSCRIPT_POTENTIAL_RANGES_EMSTAT4.get(cr)
        else:
            cr_text = MSCRIPT_CURRENT_RANGES_EMSTAT4.get(cr)
    return cr_text or 'UNKNOWN CURRENT RANGE'


class MScriptVar:
    """Class to store and parse a received MethodSCRIPT variable."""

    def __init__(self, data):
        assert len(data) >= 10
        self.data = data[:]
        # Parse the variable type.
        self.id = data[0:2]
        # Check for NaN.
        if data[2:10] == '     nan':
            self.raw_value = math.nan
            self.si_prefix = ' '
        else:
            # Parse the (raw) value,
            self.raw_value = self.decode_value(data[2:9])
            # Store the SI prefix.
            self.si_prefix = data[9]
        # Store the (raw) metadata.
        self.raw_metadata = data.split(',')[1:]
        # Parse the metadata.
        self.metadata = self.parse_metadata(self.raw_metadata)

    def __repr__(self):
        return 'MScriptVar(%r)' % self.data

    def __str__(self):
        return self.value_string

    @property
    def type(self):
        return get_variable_type(self.id)

    @property
    def si_prefix_factor(self):
        return SI_PREFIX_FACTOR[self.si_prefix]

    @property
    def value(self):
        return self.raw_value * self.si_prefix_factor

    @property
    def value_string(self):
        if self.type.unit:
            if self.si_prefix_factor == 1:
                if math.isnan(self.value):
                    return 'NaN %s' % (self.type.unit)
                else:
                    return '%d %s' % (self.raw_value, self.type.unit)
            else:
                return '%d %s%s' % (self.raw_value, self.si_prefix, self.type.unit)
        else:
            return '%.9g' % (self.value)

    @staticmethod
    def decode_value(var: str):
        """Decode the raw value of a MethodSCRIPT variable in a data package.

        The input is a 7-digit hexadecimal string (without the variable type
        and/or SI prefix). The output is the converted (signed) integer value.
        """
        assert len(var) == 7
        # Convert the 7 hexadecimal digits to an integer value and
        # subtract the offset.
        return int(var, 16) - (2 ** 27)

    @staticmethod
    def parse_metadata(tokens):
        """Parse the (optional) metadata."""
        metadata = {}
        for token in tokens:
            if (len(token) == 2) and (token[0] == '1'):
                value = int(token[1], 16)
                metadata['status'] = value
            if (len(token) == 3) and (token[0] == '2'):
                value = int(token[1:], 16)
                metadata['cr'] = value
        return metadata


def parse_mscript_data_package(line: str):
    """Parse a MethodSCRIPT data package.

    The format of a MethodSCRIPT data package is described in the
    MethodSCRIPT documentation. It starts with a 'P' and ends with a
    '\n' character. A package consists of an arbitrary number of
    variables. Each variable consists of a type (describing the
    variable), a value, and optionally one or more metadata values.

    This method returns a list of variables (of type `MScriptVar`)
    found in the line, if the line could successfully be decoded.
    If the line was not a MethodSCRIPT data package, `None` is
    returned.
    """
    if line.startswith('P') and line.endswith('\n'):
        return [MScriptVar(var) for var in line[1:-1].split(';')]


def parse_result_lines(lines):
    """Parse the result of a MethodSCRIPT and return a list of curves.

    This method returns a list of curves, where each curve is a list of
    measurement data (packages) seperated by an end-of-curve terminator
    such as '*', '+' or '-'. Each data package is a list of variables of
    type MScriptVar.

    So, the return type is a list of list of list of MScriptVars, and
    each variable can be accessed as `result[curve][row][col]`. For
    example, `result[1][2][3]` is the 4th variable of the 3th data point
    of the 2nd measurement loop.
    """
    curves = []
    current_curve = []
    for line in lines:
        # NOTE:
        # '+' = end of loop
        # '*' = end of measurement loop
        # '-' = end of scan, within measurement loop, in case nscans(>1)
        if line and line[0] in '+*-':
            # End of scan or (measurement) loop detected.
            # Store curve if not empty.
            if current_curve:
                curves.append(current_curve)
                current_curve = []
        else:
            # No end of scan. Try to parse as data package.
            package = parse_mscript_data_package(line)
            if package:
                # Line was a valid package.
                # Append the package to the current curve.
                current_curve.append(package)
    return curves


def get_values_by_column(curves, column, icurve=None):
    """Get all values from the specified column.

    `curves` is a list of list of list of variables of type `MScriptVar`, as
    returned by `parse_result_lines()`.

    `column` specifies which variable to return (i.e., the index within each
    data package).

    `icurve` specifies the index of the curve to use. If `None` (the default
    value), the data from all curves are used and concatenated into one list.

    This function returns a numpy array containing (only) the values of each
    variable in the specified column, so they can easily be used for further
    processing and/or plotting.
    """
    if icurve is None:
        values = []
        for curve in curves:
            values.extend(row[column].value for row in curve)
    else:
        values = [row[column].value for row in curves[icurve]]
    return np.asarray(values)
