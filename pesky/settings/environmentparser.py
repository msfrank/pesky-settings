# Copyright 2010-2014 Michael Frank <msfrank@syntaxjockey.com>
#
# This file is part of Pesky.  Pesky is BSD-licensed software;
# for copyright information see the LICENSE file.

import os

from pesky.settings.store import Store
from pesky.settings.errors import ConfigureError

class EnvironmentParser(object):
    """
    Contains configuration loaded from environment variables.
    """
    def __init__(self):
        self._envvars = {}

    def add_env_var(self, name, path, required=False):
        """
        """
        self._envvars[name] = (path,required)
 
    def render(self, environ=None):
        """
        """
        if environ is None:
            environ = os.environ.copy()
        else:
            environ = environ.copy()
        store = Store()
        # parse sections 
        for varname,(path,required) in self._envvars.iteritems():
            if varname in environ:
                store.append(path, environ[varname])
            elif required:
                raise ConfigureError("missing required environment variable %s" % varname)
        return store
