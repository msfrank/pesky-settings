# Copyright 2010-2014 Michael Frank <msfrank@syntaxjockey.com>
#
# This file is part of Pesky.  Pesky is BSD-licensed software;
# for copyright information see the LICENSE file.

import os

from pesky.settings.inifileparser import IniFileParser
from pesky.settings.argparser import ArgParser
from pesky.settings.environmentparser import EnvironmentParser
from pesky.settings.mergestrategy import MergeAccumulator, ReplaceStrategy
from pesky.settings.valuetree import ValueTree
from pesky.settings.namespace import Namespace

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
        # initialize the environment parser
        self.environmentparser = EnvironmentParser()
        self.environmentparser.add_env_var('CONFIG_FILE_PATH', 'pesky.config', 'file', required=False)
        # initialize the option parser
        self.argparser = ArgParser()
        self.argparser.set_appname(appname)
        self.argparser.set_version(version)
        self.argparser.set_description(description)
        self.argparser.set_usage(usage)
        self.argparser.add_option('c', 'config-file', 'pesky.config', 'file',
            help="Load configuration from FILE", metavar="FILE", recurring=False)
        # initialize the inifile parser
        self.inifileparser = IniFileParser()
        self.inifileparser.set_ini_path(os.path.join('/', 'etc', appgroup, appname + '.conf'))
        self.inifileparser.set_required(False)
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

    def parse(self):
        """
        Load configuration from environment, command-line arguments, and
        config file, and merge them together.

        :returns: A :class:`Namespace` object with the parsed settings
        :rtype: :class:`Namespace`
        """
        values = ValueTree()
        namespace = Namespace(values)
        # render options settings, then merge them
        proposed = self.argparser.render()
        values = self.accumulator.merge(values, proposed)
        # render environment settings, then merge them
        proposed = self.environmentparser.render()
        values = self.accumulator.merge(values, proposed)
        # if config file was specified by environ or options, then use it
        if namespace.contains_field('pesky.config', 'file'):
            config_path = values.get_field('pesky.config', 'file')
            self.inifileparser.set_ini_path(config_path)
            self.inifileparser.set_required(True)
        # render config file settings, then merge them
        proposed = self.inifileparser.render()
        values = self.accumulator.merge(values, proposed)
        # return the namespace containing the merged values
        return namespace
