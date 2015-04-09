# Copyright 2010-2014 Michael Frank <msfrank@syntaxjockey.com>
#
# This file is part of Pesky.  Pesky is BSD-licensed software;
# for copyright information see the LICENSE file.

from pesky.settings.settings import Settings

class CommandRoot(Settings):
    """
    """
    def __init__(self, appname, appgroup, version, description, usage):
        super().__init__(appname, appgroup, version, description, usage)
        self.commands = {}

    def add_command(self, name, description, usage):
        options = self.options.add_subcommand(name)
        options.set_appname(name)
        options.set_description(description)
        options.set_usage(usage)
        return Command(options)

class Command(object):
    """
    """
    def __init__(self, options):
        self.options = options

    def add_arg_option(self, shortoption, longoption, path, name, help=None, metavar=None, recurring=False):
        self.options.add_option(shortoption, longoption, path, name, help, metavar, recurring)

    def add_arg_shortoption(self, shortoption, path, name, help=None, metavar=None, recurring=False):
        self.options.add_shortoption(shortoption, path, name, help, metavar, recurring)

    def add_arg_longoption(self, longoption, path, name, help=None, metavar=None, recurring=False):
        self.options.add_longoption(longoption, path, name, help, metavar, recurring)

    def add_arg_switch(self, shortswitch, longswitch, path, name, reverse=False, help=None, recurring=False):
        self.options.add_switch(shortswitch, longswitch, path, name, reverse, help, recurring)

    def add_arg_shortswitch(self, shortswitch, path, name, reverse=False, help=None, recurring=False):
        self.options.add_shortswitch(shortswitch, path, name, reverse, help, recurring)

    def add_arg_longswitch(self, longswitch, path, name, reverse=False, help=None, recurring=False):
        self.options.add_longswitch(longswitch, path, name, reverse, help, recurring)
