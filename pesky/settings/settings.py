# Copyright 2010-2014 Michael Frank <msfrank@syntaxjockey.com>
#
# This file is part of Pesky.  Pesky is BSD-licensed software;
# for copyright information see the LICENSE file.

import os, sys, getopt, datetime
from ConfigParser import RawConfigParser

from pesky.settings.parser import Parser
from pesky.settings.namespace import Namespace
from pesky.settings.errors import ConfigureError

class Settings(object):
    """
    High-level settings configurator, which merges settings from command
    line arguments, environment variables, and INI-style configuration files.
    """
    def __init__(self, appname, appgroup, version, description, usage, subusage=None):
        self.appname = appname
        self.appgroup = appgroup
        self.version = version
        self.description = description
        self.usage = usage
        self.subusage = subusage
        # initialize the environment parser
        self.environ = EnvironmentParser()
        self.environ.add_env_var('CONFIG_FILE_PATH', 'pesky.config.file', required=False)
        # initialize the option parser
        self.options = OptionParser()
        self.options.set_appname(appname)
        self.options.set_version(version)
        self.options.set_description(description)
        self.options.set_usage(usage)
        if subusage is not None:
            self.options.set_subusage(subusage)
        self.options.add_option('c', 'config-file', 'pesky.config.file',
            help="Load configuration from FILE", metavar="FILE", recurring=False)
        # initialize the config parser
        self.config = ConfigParser()
        self.config.set_path(os.path.join('/', 'etc', appgroup, appname + '.conf'))
        self.config.set_required(False)

    def parse(self):
        """
        Load configuration from environment, command-line arguments, and
        config file, and merge them together.

        :returns: A :class:`Namespace` object with the parsed settings
        :rtype: :class:`Namespace`
        """
        ns = Namespace()
        strategy = AppendStrategy()
        # render options settings, then merge them into the namespace
        options = self.options.render()
        ns.merge_with(options, strategy)
        # render environment settings, then merge them into the namespace
        environ = self.environ.render()
        ns.merge_with(environ, strategy)
        # if config file was specified by environ or options, then use it
        config_path = ns.get_path('pesky.config.file')
        if config_path is not None:
            self.config.set_path(config_path)
            self.config.set_required(True)
        # render config file settings, then merge them into the namespace
        config = self.config.render()
        ns.merge_with(config, strategy)
        return ns
