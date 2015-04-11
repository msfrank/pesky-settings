import bootstrap

import unittest
from pesky.settings.commandparser import CommandParser

class TestCommandParser(unittest.TestCase):

    def test_sub_command(self):
        "CommandParser should parse a subcommand"
        main = CommandParser('main', 'fooprogram', 'command', 'do foo things', 'foo [OPTIONS...]')
        main.add_shortoption('s', 'fooprogram.option', 's')
        dosub = main.add_subcommand('dosub', 'fooprogram', 'command', 'do foo sub things', 'foo dosub [OPTIONS...')
        dosub.add_shortoption('s', 'fooprogram.dosub.option', 's')
        argv = ['-s', 'foo', 'dosub', '-s', 'bar']
        values = main.render(argv)
        self.assertEqual(values.get_field('fooprogram.option', 's'), 'foo')
        self.assertEqual(values.get_field('fooprogram.dosub.option', 's'), 'bar')
        self.assertListEqual(values.get_field_list('fooprogram', 'command'), ['main', 'dosub'])
