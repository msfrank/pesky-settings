# Copyright 2010-2014 Michael Frank <msfrank@syntaxjockey.com>
#
# This file is part of Pesky.  Pesky is BSD-licensed software;
# for copyright information see the LICENSE file.

import os, sys, getopt

from pesky.settings.path import make_path
from pesky.settings.valuetree import ValueTree
from pesky.settings.errors import ConfigureError

class ArgParser(object):
    """
    """
    def __init__(self):
        self.option_instances = {}
        self.longopts = []
        self.shortopts = ''
        self.args_path = None
        self.args_name = None

    def add(self, instance):
        """
        Add a command-line option or switch.

        :param instance:
        :type instance:
        """
        if instance.shortoption in self.option_instances:
            raise RuntimeError("-%s is already defined" % instance.shortoption)
        if instance.longoption in self.option_instances:
            raise RuntimeError("--%s is already defined" % instance.longoption)
        if instance.shortoption is not None:
            self.shortopts += instance.shortident
            self.option_instances[instance.shortoption] = instance
        if instance.longoption is not None:
            self.longopts.append(instance.longident)
            self.option_instances[instance.longoption] = instance

    def add_option(self, shortoption, longoption, path, name, help=None, metavar=None, recurring=False):
        """
        Add a command-line option to be parsed.  An option (as opposed to a switch)
        is required to have an argument.

        :param shortoption: the one letter option name.
        :type shortoption: str
        :param longoption: the long option name.
        :type longoption: str
        :param path: Override the specified key.
        :type path: str
        :param help: The help string, displayed in --help output.
        :type help: str
        :param metavar: The variable displayed in the help string
        :type metavar: str
        """
        self.add(Option(shortoption, longoption, path, name, help, metavar, recurring))

    def add_shortoption(self, shortoption, path, name, help=None, metavar=None, recurring=False):
        self.add(ShortOption(shortoption, path, name, help, metavar, recurring))

    def add_longoption(self, longoption, path, name, help=None, metavar=None, recurring=False):
        self.add(LongOption(longoption, path, name, help, metavar, recurring))

    def add_switch(self, shortswitch, longswitch, path, name, reverse=False, help=None, recurring=False):
        """
        Add a command-line switch to be parsed.  A switch (as opposed to an option)
        has no argument.

        :param shortoption: the one letter option name.
        :type shortoption: str
        :param longoption: the long option name.
        :type longoption: str
        :param path: Override the specified key.
        :type path: str
        :param reverse: If True, then the meaning of the switch is reversed.
        :type reverse: bool
        :param help: The help string, displayed in --help output.
        :type help: str
        """
        self.add(Switch(shortswitch, longswitch, path, name, reverse, help, recurring))

    def add_shortswitch(self, shortswitch, path, name, reverse=False, help=None, recurring=False):
        self.add(ShortSwitch(shortswitch, path, name, reverse, help, recurring))

    def add_longswitch(self, longswitch, path, name, reverse=False, help=None, recurring=False):
        self.add(LongSwitch(longswitch, path, name, reverse, help, recurring))

    def put_args(self, path, name):
        self.args_path = make_path(path)
        self.args_name = name

    def render(self, argv):
        """
        Parse the command line specified by argv.

        :returns:
        :rtype: pesky.settings.valuetree.ValueTree
        """
        argv = argv[:]
        values = ValueTree()
        options,args = getopt.gnu_getopt(argv, self.shortopts, self.longopts)
        for opt_name,opt_value in options:
            if not opt_name in self.option_instances:
                raise ConfigureError()
            target = self.option_instances[opt_name]
            if isinstance(target, Option):
                values.put_container(target.path)
                if values.contains(target.path, target.name) and not target.recurring:
                    raise ConfigureError("%s can only be specified once" % opt_name)
                values.append_field(target.path, target.name, opt_value)
            elif isinstance(target, Switch):
                values.put_container(target.path)
                if values.contains(target.path, target.name) and not target.recurring:
                    raise ConfigureError("%s can only be specified once" % opt_name)
                if target.reverse == True:
                    values.append_field(target.path, target.name, 'false')
                else:
                    values.append_field(target.path, target.name, 'true')
            else:
                raise RuntimeError("Unknown instance type %s" % target.__class__.__name__)
        if self.args_path and self.args_name:
            values.put_container(self.args_path)
            for arg_value in args:
                values.append_field(self.args_path, self.args_name, arg_value)
        return values

class Option(object):
    """
    A command line option.
    """
    def __init__(self, shortoption, longoption, path, name, help, metavar, recurring):
        self.longoption = ('--' + longoption) if longoption is not None else None
        self.longident = (longoption + '=') if longoption is not None else None
        self.shortoption = ('-' + shortoption) if shortoption is not None else None
        self.shortident = (shortoption + ':') if shortoption is not None else None
        self.path = make_path(path)
        self.name = name
        self.help = help
        if metavar is not None:
            self.metavar = metavar
        else:
            self.metavar = 'VALUE'
        self.recurring = recurring

class ShortOption(Option):
    """
    A command line option with only a short name.
    """
    def __init__(self, shortoption, path, name, help, metavar, recurring):
        Option.__init__(self, shortoption, None, path, name, help, metavar, recurring)

class LongOption(Option):
    """
    A command line option with only a long name.
    """
    def __init__(self, longoption, path, name, help, metavar, recurring):
        Option.__init__(self, None, longoption, path, name, help, metavar, recurring)

class Switch(object):
    """
    A command line switch.
    """
    def __init__(self, shortoption, longoption, path, name, reverse, help, recurring):
        self.longoption = ('--' + longoption) if longoption is not None else None
        self.longident = longoption if longoption is not None else None
        self.shortoption = ('-' + shortoption) if shortoption is not None else None
        self.shortident = shortoption if shortoption is not None else None
        self.path = make_path(path)
        self.name = name
        self.reverse = reverse
        self.help = help
        self.recurring = recurring

class ShortSwitch(Switch):
    """
    A command line switch with only a short name.
    """
    def __init__(self, shortoption, path, name, reverse, help, recurring):
        Switch.__init__(self, shortoption, None, path, name, reverse, help, recurring)

class LongSwitch(Switch):
    """
    A command line switch with only a long name.
    """
    def __init__(self, longoption, path, name, reverse, help, recurring):
        Switch.__init__(self, None, longoption, path, name, reverse, help, recurring)
