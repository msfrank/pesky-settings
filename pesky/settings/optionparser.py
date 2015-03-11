# Copyright 2010-2014 Michael Frank <msfrank@syntaxjockey.com>
#
# This file is part of Pesky.  Pesky is BSD-licensed software;
# for copyright information see the LICENSE file.

import os, sys, getopt

from pesky.settings.store import Store
from pesky.settings.errors import ConfigureError

class OptionParser(object):
    """
    :param parent:
    :type parent: :class:`BaseOptionParser`
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
        subcommand = OptionParser()
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
        if instance.shortname in self._options:
            raise RuntimeError("-%s is already defined" % instance.shortname)
        if instance.longname in self._options:
            raise RuntimeError("--%s is already defined" % instance.longname)
        self._options["-%s" % instance.shortname] = instance
        self._options["--%s" % instance.longname] = instance
        self._optslist.append(instance)

    def add_option(self, shortname, longname, path, help=None, metavar=None, recurring=False):
        """
        Add a command-line option to be parsed.  An option (as opposed to a switch)
        is required to have an argument.

        :param shortname: the one letter option name.
        :type shortname: str
        :param longname: the long option name.
        :type longname: str
        :param path: Override the specified key.
        :type path: str
        :param help: The help string, displayed in --help output.
        :type help: str
        :param metavar: The variable displayed in the help string
        :type metavar: str
        """
        self._add(Option(shortname, longname, path, help, metavar, recurring))

    def add_shortoption(self, shortname, path, help=None, metavar=None, recurring=False):
        self._add(ShortOption(shortname, path, help, metavar, recurring))

    def add_longoption(self, longname, path, help=None, metavar=None, recurring=False):
        self._add(LongOption(longname, path, help, metavar, recurring))

    def add_switch(self, shortname, longname, path, reverse=False, help=None, recurring=False):
        """
        Add a command-line switch to be parsed.  A switch (as opposed to an option)
        has no argument.

        :param shortname: the one letter option name.
        :type shortname: str
        :param longname: the long option name.
        :type longname: str
        :param path: Override the specified key.
        :type path: str
        :param reverse: If True, then the meaning of the switch is reversed.
        :type reverse: bool
        :param help: The help string, displayed in --help output.
        :type help: str
        """
        self._add(Switch(shortname, longname, path, reverse, help, recurring))

    def add_shortswitch(self, shortname, path, reverse=False, help=None, recurring=False):
        self._add(ShortSwitch(shortname, path, reverse, help, recurring))

    def add_longswitch(self, longname, path, reverse=False, help=None, recurring=False):
        self._add(LongSwitch(longname, path, reverse, help, recurring))

    def render(self, argv=None):
        """
        Parse the command line specified by argv.  If argv is None,
        then use sys.argv.
        """
        if argv is None:
            argv = sys.argv[:]
        else:
            argv = argv[:]
        store = Store()
        store.append("program.command", sys.argv[0])
        return self._render(argv[1:], store)

    def _render(self, argv, store):
        """
        """
        shortnames = ''.join([o.shortident for o in self._optslist if o.shortname != ''])
        longnames = [o.longident for o in self._optslist if o.longname != '']
        longnames += ['help', 'version']
        if len(self._subcommands) == 0:
            options,args = getopt.gnu_getopt(argv, shortnames, longnames)
        else:
            options,args = getopt.getopt(argv, shortnames, longnames)
        for opt_name,opt_value in options:
            if opt_name == '--help':
                raise ProgramUsage(self)
            if opt_name == '--version':
                raise ProgramVersion(self)
            target = self._options[opt_name]
            if isinstance(target, Option):
                if store.contains(target.path) and not target.recurring:
                    raise ConfigureError("%s can only be specified once" % opt_name)
                store.append(target.path, opt_value)
            elif isinstance(target, Switch):
                if store.contains(target.path) and not target.recurring:
                    raise ConfigureError("%s can only be specified once" % opt_name)
                if target.reverse == True:
                    store.append(target.path, 'false')
                else:
                    store.append(target.path, 'true')
            else:
                raise ValueError("Unknown target type %s" % target.__class__.__name__)
        if len(self._subcommands) > 0:
            if len(args) == 0:
                raise ConfigureError("no subcommand specified")
            subcommand = args[0]
            args = args[1:]
            if not subcommand in self._subcommands:
                raise ConfigureError("no subcommand named '%s'" % subcommand)
            store.append('pesky.option.command', subcommand)
            return self._subcommands[subcommand]._render(args, store)
        return store

class Option(object):
    """
    A command line option.
    """
    def __init__(self, shortname, longname, path, help, metavar, recurring):
        self.shortname = shortname
        self.shortident = "%s:" % shortname
        self.longname = longname
        self.longident = "%s=" % longname
        self.path = path
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
    def __init__(self, shortname, path, help, metavar, recurring):
        Option.__init__(self, shortname, '', path, help, metavar, recurring)

class LongOption(Option):
    """
    A command line option with only a long name.
    """
    def __init__(self, longname, path, help, metavar, recurring):
        Option.__init__(self, '', longname, path, help, metavar, recurring)

class Switch(object):
    """
    A command line switch.
    """
    def __init__(self, shortname, longname, path, reverse, help, recurring):
        self.shortname = shortname
        self.shortident = shortname
        self.longname = longname
        self.longident = longname
        self.path = path
        self.reverse = reverse
        self.help = help
        self.recurring = recurring

class ShortSwitch(Switch):
    """
    A command line switch with only a short name.
    """
    def __init__(self, shortname, path, reverse, help, recurring):
        Switch.__init__(self, shortname, '', path, reverse, help, recurring)

class LongSwitch(Switch):
    """
    A command line switch with only a long name.
    """
    def __init__(self, longname, path, reverse, help, recurring):
        Switch.__init__(self, '', longname, path, reverse, help, recurring)

class ProgramUsage(Exception):
    """
    Display a usage message and exit.
    """
    def __init__(self, parser):
        self._parser = parser
    def __str__(self):
        string = ""
        commands = []
        parser = self._parser
        while parser != None:
            commands.insert(0, parser._command)
            parser = parser._parent
        string += "Usage: %s %s\n" % (' '.join(commands), self.usage)
        string += "\n" 
        # display the description, if it was specified
        if self.description != None and self.description != '':
            string += self.description + "\n"
            string += "\n"
        # display options
        if len(self._optslist) > 0:
            options = []
            maxlength = 0
            for o in self._optslist:
                spec = []
                if o.shortname != '':
                    spec.append("-%s" % o.shortname)
                if o.longname != '':
                    spec.append("--%s" % o.longname)
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
        if len(self._subcommands) > 0:
            string += self.subusage + "\n"
            string += "\n"
            for command,parser in sorted(self._subcommands.items()):
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
