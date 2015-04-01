# Copyright 2010-2014 Michael Frank <msfrank@syntaxjockey.com>
#
# This file is part of Pesky.  Pesky is BSD-licensed software;
# for copyright information see the LICENSE file.

from configparser import ConfigParser

from pesky.settings.path import make_path
from pesky.settings.valuetree import ValueTree
from pesky.settings.errors import ConfigureError

class IniFileParser(object):
    """
    Contains configuration loaded from the specified configuration file.
    """
    def __init__(self):
        self._sections = {}
        self._options = {}
        self.ini_path = None
        self.required = False

    def set_ini_path(self, ini_path):
        """
        """
        self.ini_path = ini_path

    def set_required(self, required):
        """
        """
        self.required = required

    def add_section(self, section, path, required=False):
        """
        """
        self._sections[section] = (make_path(path),required)
 
    def add_option(self, section, option, path, name, required=False):
        """
        """
        self._options[(section,option)] = (make_path(path),name,required)

    def render(self):
        """
        :returns:
        :rtype: pesky.settings.valuetree.ValueTree
        """
        values = ValueTree()
        try:
            if self.ini_path is None:
                raise Exception("no configuration file was specified")
            with open(self.ini_path, 'r') as f:
                config = ConfigParser()
                config.read_file(f, self.ini_path)
                # parse sections
                for section,(path,required) in self._sections.items():
                    if config.has_section(section):
                        values.put_container(path)
                        for name,value in config.items(section):
                            values.put_field(path, name, value)
                    elif required:
                        raise ConfigureError("missing required section %s" % section)
                # parse items
                for (section,option),(path,name,required) in self._options.items():
                    if config.has_option(section, option):
                        values.put_container(path)
                        values.put_field(path, name, config.get(section, option))
                    elif required:
                        raise ConfigureError("missing required option %s => %s" % (section, option))
                return values
        except EnvironmentError as e:
            if self.required:
                raise ConfigureError("failed to read configuration: %s" % e.strerror)
            return values
