from pesky.settings.path import make_path
from pesky.settings.valuetree import ValueTree
from pesky.settings.errors import ConfigureError

class ListParser(object):
    """
    """
    def __init__(self):
        self.args = []
        self.leftover_path = None
        self.leftover_name = None
        self.leftover_help = None
        self.leftover_metavar = 'ARGS...'
        self.leftover_minimum = None
        self.leftover_maximum = None

    def put_leftover_args(self, path, name, help=None, metavar=None, minimum=None, maximum=None):
        """
        """
        self.leftover_path = make_path(path)
        self.leftover_name = name
        self.leftover_help = help
        if metavar is not None:
            self.leftover_metavar = metavar
        self.leftover_minimum = minimum
        self.leftover_maximum = maximum

    def add_arg(self, path, name, help=None, metavar=None):
        """
        """
        arg = Arg(path, name, help, metavar)
        self.args.append(arg)

    def render(self, args):
        """
        """
        values = ValueTree()
        items = args[:]
        for arg in self.args:
            try:
                item = items.pop(0)
                values.put_container(arg.path)
                values.put_field(arg.path, arg.name, item)
            except IndexError:
                raise ConfigureError()
        if self.leftover_minimum is not None and len(items) < self.leftover_minimum:
            raise ConfigureError()
        if self.leftover_maximum is not None and len(items) > self.leftover_maximum:
            raise ConfigureError()
        if self.leftover_path is not None and self.leftover_name is not None:
            values.put_container(self.leftover_path)
            values.put_field_list(self.leftover_path, self.leftover_name, items)
        return values

class Arg(object):
    """
    """
    def __init__(self, path, name, help, metavar):
        self.path = make_path(path)
        self.name = name
        self.help = help
        if metavar is not None:
            self.metavar = metavar
        else:
            self.metavar = 'ARG'
