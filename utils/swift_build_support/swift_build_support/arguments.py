# swift_build_support/arguments.py ------------------------------*- python -*-
#
# This source file is part of the Swift.org open source project
#
# Copyright (c) 2014 - 2016 Apple Inc. and the Swift project authors
# Licensed under Apache License v2.0 with Runtime Library Exception
#
# See http://swift.org/LICENSE.txt for license information
# See http://swift.org/CONTRIBUTORS.txt for the list of Swift project authors
#
# ----------------------------------------------------------------------------
"""
argparse suppliments
"""
# ----------------------------------------------------------------------------

from __future__ import absolute_import

import argparse
import os
import re
import shlex

__all__ = [
    "type"
]


class _Registry(object):
    pass


def _register(registry, name, value):
    setattr(registry, name, value)


type = _Registry()


def type_bool(string):
    """
    A strict parser for bools

    unlike Python's `bool()`, where `bool('False')` is `True`
    This function can be passed as `type=` argument to argparse to parse values
    passed to command line arguments.
    """
    if string in ['0', 'false', 'False']:
        return False
    if string in ['1', 'true', 'True']:
        return True
    raise argparse.ArgumentTypeError("%r is not a boolean value" % string)

_register(type, 'bool', type_bool)


def type_shell_split(string):
    """
    Parse and split shell arguments string into a list of shell arguments.

    Recognize `,` as a separator as well as white spaces.
    string: -BAR="foo bar" -BAZ='foo,bar',-QUX 42
    into
    ['-BAR=foo bar', '-BAZ=foo,bar', "-QUX", "42"]
    """
    lex = shlex.shlex(string, posix=True)
    lex.whitespace_split = True
    lex.whitespace += ','
    return list(lex)

_register(type, 'shell_split', type_shell_split)


def type_clang_compiler_version(string):
    """
    Parse version string and split into a tuple of strings
    (major, minor, patch)

    Support only "MAJOR.MINOR.PATCH" format.
    """
    m = re.match(r'^([0-9]+)\.([0-9]+)\.([0-9]+)$', string)
    if m is not None:
        return m.group(1, 2, 3)
    raise argparse.ArgumentTypeError(
        "%r is invalid version value. must be 'MAJOR.MINOR.PATCH'" % string)

_register(type, 'clang_compiler_version', type_clang_compiler_version)


def type_executable(string):
    """
    Check the string is executable path string.

    Convert it to absolute path.
    """
    if os.path.isfile(string) and os.access(string, os.X_OK):
        return os.path.abspath(string)
    raise argparse.ArgumentTypeError(
        "%r is not executable" % string)

_register(type, 'executable', type_executable)
