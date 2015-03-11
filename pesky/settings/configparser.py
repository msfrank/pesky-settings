# Copyright 2010-2014 Michael Frank <msfrank@syntaxjockey.com>
#
# This file is part of Pesky.  Pesky is BSD-licensed software;
# for copyright information see the LICENSE file.

import os, sys
from ConfigParser import RawConfigParser

from pesky.settings.store import Store
from pesky.settings.errors import ConfigureError

class ConfigParser(object):
    """
    Contains configuration loaded from the specified configuration file.
    """
    def __init__(self):
        self._sections = {}
        self._options = {}
        self.path = None
        self.required = False

    def set_path(self, path):
        """
        """
        self.path = path

    def set_required(self, required):
        """
        """
        self.required = required

    def add_section(self, section, path, required=False):
        """
        """
        self._sections[section] = (path,required)
 
    def add_option(self, section, option, path, required=False):
        """
        """
        self._options[(section,option)] = (path,required)

    def render(self):
        """
        """
        try:
            store = Store()
            with open(self.path, 'r') as f:
                config = RawConfigParser()
                config.readfp(f, self.path)
                # parse sections 
                for section,(path,required) in self._sections.iteritems():
                    if config.has_section(section):
                        for name,value in config.items(section):
                            store.append(path + '.' + name, value)
                    elif required:
                        raise ConfigureError("missing required section %s" % section)
                # parse items
                for (section,option),(path,required) in self._options.iteritems():
                    if config.has_option(section, option):
                        store.append(path, config.get(section, option))
                    elif required:
                        raise ConfigureError("missing required option %s => %s" % (section, option))
                return store
        except EnvironmentError as e:
            if self.required:
                raise ConfigureError("failed to read configuration: %s" % e.strerror)
            return Store()
