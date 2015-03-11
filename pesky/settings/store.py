# Copyright 2010-2014 Michael Frank <msfrank@syntaxjockey.com>
#
# This file is part of Pesky.  Pesky is BSD-licensed software;
# for copyright information see the LICENSE file.

class Store(object):
    """
    """
    def __init__(self):
        self._values = {}

    def append(self, name, value):
        """
        Appends the value to the specified name.
        """
        curr = self._values.get(name, [])
        curr.append(value)
        self._values[name] = curr

    def contains(self, name):
        """
        Returns True if the specified name exists, otherwise False.
        """
        return name in self._values

    def get(self, name):
        """
        """
        return self._values.get(name, None)

    def iteritems(self):
        """
        Iterate all (name,value) pairs.
        """
        return self._values.iteritems()
