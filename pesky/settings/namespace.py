# Copyright 2010-2014 Michael Frank <msfrank@syntaxjockey.com>
#
# This file is part of Pesky.  Pesky is BSD-licensed software;
# for copyright information see the LICENSE file.

from pesky.settings.path import make_path
from pesky.settings.errors import ConfigureError

class Namespace(object):
    """
    """
    def __init__(self, values):
        """

        :param values:
        :type values: pesky.settings.valuetree.ValueTree
        :return:
        """
        self._values = values

    @classmethod
    def or_none(cls, fn, *args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except KeyError:
            return None

    def get_container(self, path):
        return self._values.get_container(path)

    def get_container_or_none(self, path):
        return Namespace.or_none(self.get_container, path)

    def contains_container(self, path):
        """
        """
        return self._values.contains_container(path)

    def get_raw(self, path, name):
        return self._values.get_field(path, name)

    def get_raw_or_none(self, path, name):
        return Namespace.or_none(self.get_raw, path, name)

    def get_raw_list(self, path, name):
        return self._values.get_field_list(path, name)

    def get_raw_list_or_none(self, path, name):
        return Namespace.or_none(self.get_raw_list, path, name)

    def get_str(self, path, name):
        return self._values.get_field(path, name).strip()

    def get_str_or_none(self, path, name):
        return Namespace.or_none(self.get_str, path, name)

    def get_str_list(self, path, name):
        return map(lambda x: x.strip(), self._values.get_field_list(path, name))

    def get_str_list_or_none(self, path, name):
        return Namespace.or_none(self.get_str_list, path, name)

    def get_flattened(self, path, name):
        return ' '.join(self._values.get_field(path, name).split())

    def get_flattened_or_none(self, path, name):
        return Namespace.or_none(self.get_str, path, name)

    def get_flattened_list(self, path, name):
        return map(lambda x: ' '.join(x.split()), self._values.get_field_list(path, name))

    def get_flattened_list_or_none(self, path, name):
        return Namespace.or_none(self.get_flattened_list, path, name)

    def get_int(self, path, name):
        return int(self.get_flattened(path, name))

    def get_int_or_none(self, path, name):
        return Namespace.or_none(self.get_int, path, name)

    def get_int_list(self, path, name):
        return map(lambda x: int(x), self.get_flattened_list(path, name))

    def get_int_list_or_none(self, path, name):
        return Namespace.or_none(self.get_int_list, path, name)

    def get_float(self, path, name):
        return float(self.get_flattened(path, name))

    def get_float_or_none(self, path, name):
        return Namespace.or_none(self.get_float, path, name)

    def get_float_list(self, path, name):
        return map(lambda x: float(x), self.get_flattened_list(path, name))

    def get_float_list_or_none(self, path, name):
        return Namespace.or_none(self.get_float_list, path, name)

    def contains_field(self, path, name):
        """
        Returns True if the specified name exists, otherwise False.

        :param name: The name.
        :type name: str
        :returns: True or False.
        :rtype: [bool]
        """
        return self._values.contains_field(path, name)

    def contains_field_list(self, path, name):
        """
        Returns True if the specified name exists, otherwise False.

        :param name: The name.
        :type name: str
        :returns: True or False.
        :rtype: [bool]
        """
        return self._values.contains_field_list(path, name)

    def contains(self, path, name):
        return self.contains_field(path, name) or self.contains_field_list(path, name)
