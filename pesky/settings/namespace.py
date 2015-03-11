# Copyright 2010-2014 Michael Frank <msfrank@syntaxjockey.com>
#
# This file is part of Pesky.  Pesky is BSD-licensed software;
# for copyright information see the LICENSE file.

from pesky.settings.errors import ConfigureError

class Namespace(object):
    """
    """
    def __init__(self):
        self._store = Store()

    def merge(self, store):
        """
        """
        for name,values in store.iter():
            for value in values:
                self._store.append(name, values)

    def contains(self, name):
        """
        Returns True if the specified name exists, otherwise False.

        :param name: The name.
        :type name: str
        :returns: True or False.
        :rtype: [bool]
        """
        return self._store.contains(name)

    def get(self, name):
        """
        """
        return self._store.get(name, None)

    def iteritems(self):
        """
        Iterate all (name,value) pairs.
        """
        return self._store.iteritems()
