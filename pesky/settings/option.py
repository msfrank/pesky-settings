# Copyright 2010-2014 Michael Frank <msfrank@syntaxjockey.com>
#
# This file is part of Pesky.  Pesky is BSD-licensed software;
# for copyright information see the LICENSE file.

import os, sys, getopt, datetime
from ConfigParser import RawConfigParser

class Option(object):
    """
    A command line option.
    """
    def __init__(self, shortname, longname, override, section=None, help=None, metavar=None):
        self.shortname = shortname
        self.shortident = "%s:" % shortname
        self.longname = longname
        self.longident = "%s=" % longname
        self.section = section
        self.override = override
        self.help = help
        if metavar is not None:
            self.metavar = metavar
        else:
            self.metavar = 'VALUE'

class ShortOption(Option):
    """
    A command line option with only a short name.
    """
    def __init__(self, shortname, override, section=None, help=None, metavar=None):
        Option.__init__(self, shortname, '', override, section, help, metavar)

class LongOption(Option):
    """
    A command line option with only a long name.
    """
    def __init__(self, longname, override, section=None, help=None, metavar=None):
        Option.__init__(self, '', longname, override, section, help, metavar)

class Switch(Option):
    """
    A command line switch.
    """
    def __init__(self, shortname, longname, override, section=None, reverse=False, help=None):
        Option.__init__(self, shortname, longname, override, section, help)
        self.shortident = shortname
        self.longident = longname
        self.reverse = reverse

class ShortSwitch(Switch):
    """
    A command line switch with only a short name.
    """
    def __init__(self, shortname, override, section=None, reverse=False, help=None):
        Switch.__init__(self, shortname, '', override, section, reverse, help)

class LongSwitch(Switch):
    """
    A command line switch with only a long name.
    """
    def __init__(self, longname, override, section=None, reverse=False, help=None):
        Switch.__init__(self, '', longname, override, section, reverse, help)
