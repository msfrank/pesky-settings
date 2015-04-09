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
    :param parent:
    :type parent: pesky.settings.argparser.ArgParser`
    :param name:
    :type name: str
    :param usage:
    :type usage: str
    :param description:
    :type description: str
    :param subusage:
    :type subusage: str
    """
    def __init__(self):
        self._parent = None
        self._command = None
        self._subcommands = {}
        self._options = {}
        self._optslist = []
        self.appname = sys.argv[0]
        self.version = None
        self.usage = ''
        self.description = ''
        self.subusage = 'Available subcommands:'

    def set_appname(self, appname):
        """
        """
        self.appname = appname

    def set_version(self, version):
        """
        """
        self.version = version

    def set_description(self, description):
        """
        """
        self.description = description

    def set_usage(self, usage):
        """
        """
        self.usage = usage

    def set_subusage(self, subusage):
        """
        """
        self.subusage = subusage

    def add_subcommand(self, name):
        """
        Add a subcommand to the parser.
        :param name:
        :type name: str
        """
        if name in self._subcommands:
            raise ConfigureError("subcommand '%s' is already defined" % name)
        subcommand = ArgParser()
        subcommand._command = name
        subcommand._parent = self
        self._subcommands[name] = subcommand
        return subcommand

    def _add(self, instance):
        """
        Add a command-line option or switch.

        :param o: o
        :type o: :class:`Option`
        """
        if instance.shortoption in self._options:
            raise RuntimeError("-%s is already defined" % instance.shortoption)
        if instance.longoption in self._options:
            raise RuntimeError("--%s is already defined" % instance.longoption)
        self._options["-%s" % instance.shortoption] = instance
        self._options["--%s" % instance.longoption] = instance
        self._optslist.append(instance)

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
        self._add(Option(shortoption, longoption, path, name, help, metavar, recurring))

    def add_shortoption(self, shortoption, path, name, help=None, metavar=None, recurring=False):
        self._add(ShortOption(shortoption, path, name, help, metavar, recurring))

    def add_longoption(self, longoption, path, name, help=None, metavar=None, recurring=False):
        self._add(LongOption(longoption, path, name, help, metavar, recurring))

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
        self._add(Switch(shortswitch, longswitch, path, name, reverse, help, recurring))

    def add_shortswitch(self, shortswitch, path, name, reverse=False, help=None, recurring=False):
        self._add(ShortSwitch(shortswitch, path, name, reverse, help, recurring))

    def add_longswitch(self, longswitch, path, name, reverse=False, help=None, recurring=False):
        self._add(LongSwitch(longswitch, path, name, reverse, help, recurring))

    def render(self, argv=None):
        """
        Parse the command line specified by argv.  If argv is None, then use sys.argv.

        :returns:
        :rtype: pesky.settings.valuetree.ValueTree
        """
        if argv is None:
            argv = sys.argv[:]
        else:
            argv = argv[:]
        values = ValueTree()
        values.put_container("pesky.option")
        values.put_field("pesky.option", "command", sys.argv[0])
        return self._render(argv[1:], values)

    def _render(self, argv, values):
        """
        """
        shortoptions = ''.join([o.shortident for o in self._optslist if o.shortoption != ''])
        longoptions = [o.longident for o in self._optslist if o.longoption != '']
        longoptions += ['help', 'version']
        if len(self._subcommands) == 0:
            options,args = getopt.gnu_getopt(argv, shortoptions, longoptions)
        else:
            options,args = getopt.getopt(argv, shortoptions, longoptions)
        for opt_name,opt_value in options:
            if opt_name == '--help':
                raise ProgramUsage(self)
            if opt_name == '--version':
                raise ProgramVersion(self)
            target = self._options[opt_name]
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
                raise ValueError("Unknown target type %s" % target.__class__.__name__)
        if len(self._subcommands) > 0:
            if len(args) == 0:
                raise ConfigureError("no subcommand specified")
            subcommand = args[0]
            args = args[1:]
            if not subcommand in self._subcommands:
                raise ConfigureError("no subcommand named '%s'" % subcommand)
            values.put_container('pesky.option')
            values.append_field('pesky.option', 'subcommand', subcommand)
            return self._subcommands[subcommand]._render(args, values)
        return values

class Option(object):
    """
    A command line option.
    """
    def __init__(self, shortoption, longoption, path, name, help, metavar, recurring):
        self.shortoption = shortoption
        self.shortident = "%s:" % shortoption
        self.longoption = longoption
        self.longident = "%s=" % longoption
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
        Option.__init__(self, shortoption, '', path, name, help, metavar, recurring)

class LongOption(Option):
    """
    A command line option with only a long name.
    """
    def __init__(self, longoption, path, name, help, metavar, recurring):
        Option.__init__(self, '', longoption, path, name, help, metavar, recurring)

class Switch(object):
    """
    A command line switch.
    """
    def __init__(self, shortoption, longoption, path, name, reverse, help, recurring):
        self.shortoption = shortoption
        self.shortident = shortoption
        self.longoption = longoption
        self.longident = longoption
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
        Switch.__init__(self, shortoption, '', path, name, reverse, help, recurring)

class LongSwitch(Switch):
    """
    A command line switch with only a long name.
    """
    def __init__(self, longoption, path, name, reverse, help, recurring):
        Switch.__init__(self, '', longoption, path, name, reverse, help, recurring)

class ProgramUsage(Exception):
    """
    Display a usage message and exit.
    """
    def __init__(self, parser):
        """
        :param parser:
        :type parser: pesky.settings.optionparser.ArgParser
        """
        self._parser = parser

    def __str__(self):
        string = ""
        commands = []
        parser = self._parser
        while parser != None:
            commands.insert(0, parser._command)
            parser = parser._parent
        string += "Usage: %s %s\n" % (' '.join(commands), self._parser.usage)
        string += "\n" 
        # display the description, if it was specified
        if self._parser.description != None and self._parser.description != '':
            string += self._parser.description + "\n"
            string += "\n"
        # display options
        if len(self._parser._optslist) > 0:
            options = []
            maxlength = 0
            for o in self._parser._optslist:
                spec = []
                if o.shortoption != '':
                    spec.append("-%s" % o.shortoption)
                if o.longoption != '':
                    spec.append("--%s" % o.longoption)
                if isinstance(o, Switch):
                    spec = ','.join(spec)
                elif isinstance(o, Option):
                    spec = ','.join(spec) + ' ' + o.metavar
                options.append((spec, o.help))
                if len(spec) > maxlength:
                    maxlength = len(spec)
            for spec,help in options: 
                string += " %s%s\n" % (spec.ljust(maxlength + 4), help)
            string += "\n"
        # display subcommands, if there are any
        if len(self._parser._subcommands) > 0:
            string += self._parser.subusage + "\n"
            string += "\n"
            for command,parser in sorted(self._parser._subcommands.items()):
                string += " %s\n" % command
            string += "\n"
        return string

class ProgramVersion(Exception):
    """
    Display the version and exit.
    """
    def __init__(self, parser):
        while parser._parent != None:
            parser = parser._parent
        self.appname = parser.appname
        self.version = parser.version

    def __str__(self):
        return "%s %s\n" % (self.appname, self.version)
