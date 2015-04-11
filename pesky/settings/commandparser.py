import getopt

from pesky.settings.path import make_path
from pesky.settings.argparser import ArgParser, Option, Switch
from pesky.settings.valuetree import ValueTree
from pesky.settings.errors import ConfigureError

class CommandParser(ArgParser):
    """
    """
    def __init__(self, ident, path, name, description, usage):
        super().__init__()
        self.cmd_ident = ident
        self.cmd_path = path
        self.cmd_name = name
        self.cmd_description = description
        self.cmd_usage = usage
        self.subcommands = {}


    def add_subcommand(self, ident, path, name, description, usage):
        if ident is self.subcommands:
            raise KeyError()
        subcommand = CommandParser(ident, path, name, description, usage)
        self.subcommands[ident] = subcommand
        return subcommand

    def render(self, argv):
        return self._render(argv, ValueTree())

    def _render(self, argv, values):
        """
        """
        values.put_container(self.cmd_path)
        values.append_field(self.cmd_path, self.cmd_name, self.cmd_ident)

        argv = argv[:]
        if len(self.subcommands) == 0:
            options,args = getopt.gnu_getopt(argv, self.shortopts, self.longopts)
        else:
            options,args = getopt.getopt(argv, self.shortopts, self.longopts)

        for opt_name,opt_value in options:
            if not opt_name in self.option_instances:
                raise ConfigureError()
            target = self.option_instances[opt_name]
            if isinstance(target, Option):
                values.put_container(target.path)
                if values.contains(target.path, target.name) and not target.recurring:
                    raise ConfigureError("%s can only be specified once" % opt_name)
                values.append_field(target.path, target.name, opt_value)
            elif isinstance(target, Switch):
                values.put_container(target.path)
                if values.contains(target.path, target.name) and not target.recurring:
                    raise ConfigureError("%s can only be specified once" % opt_name)
                if target.reverse == True:
                    values.append_field(target.path, target.name, 'false')
                else:
                    values.append_field(target.path, target.name, 'true')
            else:
                raise RuntimeError("Unknown instance type %s" % target.__class__.__name__)

        # there is nothing remaining, so we're done
        if len(args) == 0:
            return values

        ident = args[0]
        argv = args[1:]

        # if there is no matching subcommand, then anything remaining is an arg
        if ident not in self.subcommands:
            if self.args_path and self.args_name:
                values.put_container(self.args_path)
                for arg_value in args:
                    values.append_field(self.args_path, self.args_name, arg_value)
            return values

        # otherwise render the subcommand
        return self.subcommands[ident]._render(argv, values)

class Command(object):
    """
    """
    def __init__(self, ident, path, name, description, usage):
        self.ident = ident
        self.path = path
        self.name = name
        self.description = description
        self.usage = usage
