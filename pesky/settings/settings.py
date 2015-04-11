# Copyright 2010-2014 Michael Frank <msfrank@syntaxjockey.com>
#
# This file is part of Pesky.  Pesky is BSD-licensed software;
# for copyright information see the LICENSE file.

import os, sys

from pesky.settings.inifileparser import IniFileParser
from pesky.settings.argparser import ArgParser
from pesky.settings.environmentparser import EnvironmentParser
from pesky.settings.mergestrategy import MergeAccumulator, ReplaceStrategy
from pesky.settings.valuetree import ValueTree
from pesky.settings.namespace import Namespace
from pesky.settings.errors import ConfigureError

class Parser(object):
    """
    """
    def __init__(self):
        pass


class Settings(object):
    """
    High-level settings configurator, which merges settings from command
    line arguments, environment variables, and INI-style configuration files.
    """
    def __init__(self, appname, appgroup, version, description, usage):
        self.appname = appname
        self.appgroup = appgroup
        self.version = version
        self.description = description
        self.usage = usage
        self.subusage = 'Available subcommands:'
        # initialize the environment parser
        self.environmentparser = EnvironmentParser()
        self.environmentparser.add_env_var('CONFIG_FILE_PATH', 'pesky.settings', 'config_file', required=False)
        # initialize the arg parser
        self.argparser = ArgParser()
        self.argparser.add_option('c', 'config-file', 'pesky.settings', 'config_file',
            help="Load configuration from FILE", metavar="FILE", recurring=False)
        self.argparser.add_switch('h', 'help', 'pesky.settings', 'display_help',
            help="Display usage message", recurring=False)
        self.argparser.add_switch('V', 'version', 'pesky.settings', 'display_version',
            help="Display version message", recurring=False)
        # initialize the command parser
        self.subcommands = {}
        # initialize the inifile parser
        self.inifileparser = IniFileParser()
        # initialize the merge accumulator
        self.accumulator = MergeAccumulator(ReplaceStrategy())

    def add_env_var(self, envvar, path, name, required=False):
        self.environmentparser.add_env_var(envvar, path, name, required)

    def add_arg_option(self, shortoption, longoption, path, name, help=None, metavar=None, recurring=False):
        self.argparser.add_option(shortoption, longoption, path, name, help, metavar, recurring)

    def add_arg_shortoption(self, shortoption, path, name, help=None, metavar=None, recurring=False):
        self.argparser.add_shortoption(shortoption, path, name, help, metavar, recurring)

    def add_arg_longoption(self, longoption, path, name, help=None, metavar=None, recurring=False):
        self.argparser.add_longoption(longoption, path, name, help, metavar, recurring)

    def add_arg_switch(self, shortswitch, longswitch, path, name, reverse=False, help=None, recurring=False):
        self.argparser.add_switch(shortswitch, longswitch, path, name, reverse, help, recurring)

    def add_arg_shortswitch(self, shortswitch, path, name, reverse=False, help=None, recurring=False):
        self.argparser.add_shortswitch(shortswitch, path, name, reverse, help, recurring)

    def add_arg_longswitch(self, longswitch, path, name, reverse=False, help=None, recurring=False):
        self.argparser.add_longswitch(longswitch, path, name, reverse, help, recurring)

    def add_ini_section(self, section, path, required=False):
        self.inifileparser.add_section(section, path, required)

    def add_ini_option(self, section, option, path, name, required=False):
        self.inifileparser.add_option(section, option, path, name, required)

    # def add_command(self, name, description, usage):
    #     """
    #     :param name:
    #     :param description:
    #     :param usage:
    #     :return:
    #     """
    #     if name in self.subcommands:
    #         raise ConfigureError("command '%s' is already defined" % name)
    #     command = Command(name, description, usage)
    #     command.set_parent(self)
    #     return command

    def parse(self):
        """
        Load configuration from environment, command-line arguments, and
        config file, and merge them together.

        :returns: A :class:`Namespace` object with the parsed settings
        :rtype: :class:`Namespace`
        """
        values = ValueTree()
        values.put_container("pesky.settings")

        # store the program name
        values.put_field("pesky.settings", "program", sys.argv[0])

        # render program arguments, then merge them

        proposed = self.argparser.render(sys.argv[1:])
        self.accumulator.merge(values, proposed)

        # render environment variables, then merge them
        proposed = self.environmentparser.render(os.environ)
        self.accumulator.merge(values, proposed)

        # if config file was specified by environ or options, then use it
        ini_path = os.path.join('/', 'etc', self.appgroup, self.appname + '.conf')
        ini_required = False
        if values.contains('pesky.settings', 'config_file'):
            ini_path = values.get_field('pesky.settings', 'config_file')
            ini_required = True

        # render config file parameters, then merge them
        proposed = self.inifileparser.render(ini_path, ini_required)
        self.accumulator.merge(values, proposed)

        # return the namespace containing the merged values
        return Namespace(values)
