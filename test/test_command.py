import bootstrap

import sys
import unittest

from pesky.settings.command import CommandRoot

class TestCommand(unittest.TestCase):

    def test_run_command(self):
        root = CommandRoot('fooprogram', 'fooutils', '0.0.1', 'do foo things', 'fooprogram [OPTIONS...]')
        root.add_arg_longoption('foo', 'fooprogram.option', 'foo')
        command = root.add_command('start', "start foo things", "fooprogram start [OPTIONS...]")
        command.add_arg_longoption('foo', 'fooprogram.start.option', 'foo')
        sys.argv = ['fooprogram', '--foo', 'bar', 'start', '--foo', 'baz']
        ns = root.parse()
        self.assertEqual(ns.get_str('fooprogram.option', 'foo'), 'bar')
        self.assertEqual(ns.get_str('fooprogram.start.option', 'foo'), 'baz')
