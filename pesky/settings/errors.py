# Copyright 2010-2014 Michael Frank <msfrank@syntaxjockey.com>
#
# This file is part of Pesky.  Pesky is BSD-licensed software;
# for copyright information see the LICENSE file.

class SettingsError(Exception):
    """
    Base exception class for pesky.settings.
    """
    pass

class ConfigureError(SettingsError):
    """
    Configuration parsing failed.
    """
    pass

class ConversionError(SettingsError):
    """
    Failed to convert to requested datatype.
    """
    pass
