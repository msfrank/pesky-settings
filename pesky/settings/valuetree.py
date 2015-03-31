# Copyright 2010-2014 Michael Frank <msfrank@syntaxjockey.com>
#
# This file is part of Pesky.  Pesky is BSD-licensed software;
# for copyright information see the LICENSE file.

from pesky.settings.path import Path, make_path

class ValueTree(object):
    """
    """
    def __init__(self):
        self._values = {}

    def put_container(self, path):
        """
        Creates a container at the specified path, creating any necessary
        intermediate containers.

        :param path:
        :type path:
        :raises ValueError: A component of path is a field name.
        """
        path = make_path(path)
        container = self
        for segment in path:
            try:
                container = container._values[segment]
                if not isinstance(container, ValueTree):
                    raise ValueError()
            except KeyError:
                valuetree = ValueTree()
                container._values[segment] = valuetree
                container = valuetree
            
    def remove_container(self, path):
        """
        Removes the container at the specified path.

        :param path:
        :type path:
        :raises ValueError: A component of path is a field name.
        :raises KeyError: A component of path doesn't exist.
        """
        path = make_path(path)
        container = self
        parent = None
        for segment in path:
            parent = container
            try:
                container = container._values[segment]
                if not isinstance(container, ValueTree):
                    raise ValueError()
            except KeyError:
                raise KeyError()
        del parent._values[path.segments[-1]]
 
    def get_container(self, path):
        """
        Retrieves the container at the specified path.

        :param path:
        :type path:
        :raises ValueError: A component of path is a field name.
        :raises KeyError: A component of path doesn't exist.
        """
        path = make_path(path)
        container = self
        for segment in path:
            try:
                container = container._values[segment]
                if not isinstance(container, ValueTree):
                    raise ValueError()
            except KeyError:
                raise KeyError()
        return container

    def contains_container(self, path):
        """
        Returns True if a container exists at the specified path,
        otherwise False.

        :param path:
        :type path:
        :raises ValueError: A component of path is a field name.
        """
        path = make_path(path)
        try:
            self.get_container(path)
            return True
        except KeyError:
            return False

    def put_field(self, path, name, value):
        """
        Creates a field with the specified name an value at path.  If the
        field already exists, it will be overwritten with the new value.
        """
        path = make_path(path)
        container = self.get_container(path)
        current = self._values.get(name)
        if current is not None and isinstance(current, ValueTree):
            raise TypeError()
        container._values[name] = value

    def append_field(self, path, name, value):
        """
        Appends the field to the container at the specified path.
        """
        path = make_path(path)
        container = self.get_container(path)
        current = container._values.get(name, None)
        if current is None:
            container._values[name] = value
        elif isinstance(current, ValueTree):
            raise TypeError()
        elif isinstance(current, list):
            container._values[name] = current + [value]
        else:
            container._values[name] = [current, value]

    def remove_field(self, path, name):
        """
        """
        path = make_path(path)
        container = self.get_container(path)
        try:
            value = container._values[name]
            if isinstance(value, ValueTree):
                raise TypeError()
            del container._values[name]
        except KeyError:
            pass

    def get(self, path, name):
        """
        :param path:
        :param name:
        :return:
        """
        container = self.get_container(path)
        try:
            return container._values[name]
        except KeyError:
            raise KeyError()

    def get_field(self, path, name):
        """
        Retrieves the value of the field at the specified path.

        :param path:
        :type path:
        :param name:
        :type name: str
        :raises ValueError: A component of path is a field name.
        :raises KeyError: A component of path doesn't exist.
        :raises TypeError: The field name is a component of a path.
        """
        try:
            value = self.get(path, name)
            if not isinstance(value, str):
                raise TypeError()
            return value
        except KeyError:
            raise KeyError()

    def get_field_list(self, path, name):
        """

        :param path:
        :param name:
        :raises ValueError: A component of path is a field name.
        :raises KeyError: A component of path doesn't exist.
        :raises TypeError: The field name is a component of a path.
        """
        try:
            value = self.get(path, name)
            if not isinstance(value, list):
                raise TypeError()
            return value
        except KeyError:
            raise KeyError()

    def contains_field(self, path, name):
        """
        Returns True if a field exists at the specified path, otherwise False.

        :param path:
        :type path:
        :param name:
        :type name: str
        :raises ValueError: A component of path is a field name.
        :raises TypeError: The field name is a component of a path.
        """
        try:
            self.get_field(path, name)
            return True
        except KeyError:
            return False

    def contains_field_list(self, path, name):
        """
        Returns True if a multi-valued field exists at the specified path, otherwise False.

        :param path:
        :type path:
        :param name:
        :type name: str
        :raises ValueError: A component of path is a field name.
        :raises TypeError: The field name is a component of a path.
        """
        try:
            self.get_field_list(path, name)
            return True
        except KeyError:
            return False

    def contains(self, path, name):
        """
        :param path:
        :param name:
        :return:
        """
        try:
            self.get(path, name)
            return True
        except KeyError:
            return False

    def iter_fields(self):
        """
        Iterate all fields as a sequence of (path,name,value) tuples.
        """
        def generator(path, values):
            for name,value in sorted(values.items()):
                if isinstance(value, ValueTree):
                    for inner in generator(path + name, value._values):
                        yield inner
                else:
                    yield (path, name, value)
        return generator(Path([]), self._values)
