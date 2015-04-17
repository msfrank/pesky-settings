import bootstrap

import os, sys
import unittest
from pesky.settings.listparser import ListParser
from pesky.settings import ConfigureError

class TestListParser(unittest.TestCase):

    def test_single_arg_and_leftovers(self):
        "ListParser should parse a list of arguments and the leftovers"
        parser = ListParser()
        parser.add_arg('fooprogram.args', 'arg1')
        parser.put_leftover_args('fooprogram.args', 'leftover')
        args = ['foo', 'bar', 'baz']
        values = parser.render(args)
        self.assertEqual(values.get_field('fooprogram.args', 'arg1'), 'foo')
        self.assertListEqual(values.get_field_list('fooprogram.args', 'leftover'), ['bar', 'baz'])

    def test_required_args(self):
        "ListParser should raise ConfigureError if required argument is missing"
        parser = ListParser()
        parser.add_arg('fooprogram.args', 'arg1')
        args = []
        self.assertRaises(ConfigureError, parser.render, args)

    def test_required_minimum_leftover_args(self):
        "ListParser should raise ConfigureError if leftover arguments are less than the minimum"
        parser = ListParser()
        parser.put_leftover_args('fooprogram.args', 'leftover', minimum=2)
        args = ['foo']
        self.assertRaises(ConfigureError, parser.render, args)

    def test_required_maximum_leftover_args(self):
        "ListParser should raise ConfigureError if leftover arguments are greater than the maximum"
        parser = ListParser()
        parser.put_leftover_args('fooprogram.args', 'leftover', maximum=2)
        args = ['foo', 'bar', 'baz']
        self.assertRaises(ConfigureError, parser.render, args)
