# Copyright 2010-2014 Michael Frank <msfrank@syntaxjockey.com>
#
# This file is part of Pesky.  Pesky is BSD-licensed software;
# for copyright information see the LICENSE file.

import os

from pesky.settings.path import make_path
from pesky.settings.valuetree import ValueTree
from pesky.settings.errors import ConfigureError

class EnvironmentParser(object):
    """
    Contains configuration loaded from environment variables.
    """
    def __init__(self):
        self._envvars = {}

    def add_env_var(self, envvar, path, name, required=False):
        """
        """
        self._envvars[envvar] = (make_path(path),name,required)
 
    def render(self, environ):
        """
        :returns:
        :rtype: pesky.settings.valuetree.ValueTree
        """
        environ = environ.copy()
        values = ValueTree()
        # parse sections
        for envvar,(path,name,required) in self._envvars.items():
            if envvar in environ:
                values.put_container(path)
                values.put_field(path, name, environ[envvar])
            elif required:
                raise ConfigureError("missing required environment variable %s" % envvar)
        return values
