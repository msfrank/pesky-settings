import bootstrap

import os
import sys
import unittest

from pesky.settings.settings import Settings

tests_directory = os.path.dirname(os.path.abspath(__file__))

class TestSettings(unittest.TestCase):

    ini_path = os.path.join(tests_directory, 'config.ini')

    def test_parse_settings(self):
        "Settings should parse command options, environment, and config file"
        settings = Settings('fooprogram', 'fooutils', '0.0.1', 'do foo things', 'fooprogram [OPTIONS...]')
        settings.add_arg_longoption('foo', 'fooprogram.option', 'foo')
        settings.add_env_var('FOO', 'fooprogram.env', 'foo')
        settings.add_ini_section('foo', 'fooprogram.config')
        sys.argv = ['fooprogram','--config-file', self.ini_path, '--foo', 'bar']
        os.environ['FOO'] = 'bar'
        ns = settings.parse()
        self.assertEqual(ns.get_str('fooprogram.option', 'foo'), 'bar')
        self.assertEqual(ns.get_str('fooprogram.env', 'foo'), 'bar')
        self.assertEqual(ns.get_str('fooprogram.config', 'required'), 'foo')
        self.assertEqual(ns.get_str('fooprogram.config', 'optional'), 'bar')
        self.assertEqual(ns.get_str('fooprogram.config', 'spaces in key'), 'baz')

    # def test_parse_subcommand(self):
    #     settings = Settings('fooprogram', 'fooutils', '0.0.1', 'do foo things', 'fooprogram [OPTIONS...]')
    #     settings.add_arg_longoption('foo', 'fooprogram.option', 'foo')
    #     command = settings.add_command('start', "start foo things", "fooprogram start [OPTIONS...]")
    #     command.add_arg_longoption('foo', 'fooprogram.start.option', 'foo')
    #     sys.argv = ['fooprogram', '--foo', 'bar', 'start', '--foo', 'baz']
    #     ns = settings.parse()
    #     self.assertEqual(ns.get_str('fooprogram.option', 'foo'), 'bar')
    #     self.assertEqual(ns.get_str('fooprogram.start.option', 'foo'), 'baz')