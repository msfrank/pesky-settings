
import os, sys, unittest
from pesky.settings.configparser import ConfigParser
from pesky.settings import ConfigureError

tests_directory = os.path.dirname(os.path.abspath(__file__))

class TestConfigParser(unittest.TestCase):

    ini_path = os.path.join(tests_directory, 'config.ini')

    def test_config_section(self):
        "ConfigParser should parse a section"
        parser = ConfigParser()
        parser.set_path(self.ini_path)
        parser.set_required(True)
        parser.add_section('foo', 'fooprogram.ini.foo')
        store = parser.render()
        self.assertEqual(store.get('fooprogram.ini.foo.required'), ['foo'])
        self.assertEqual(store.get('fooprogram.ini.foo.optional'), ['bar'])
        self.assertEqual(store.get('fooprogram.ini.foo.spaces in key'), ['baz'])

    def test_optional_config_section(self):
        "ConfigParser should parse a missing optional section"
        parser = ConfigParser()
        parser.set_path(self.ini_path)
        parser.set_required(True)
        parser.add_section('missing', 'fooprogram.ini.foo', required=False)
        store = parser.render()
        self.assertEqual(store.get('fooprogram.ini.foo'), None)

    def test_required_config_section(self):
        "ConfigParser should raise ConfigureError if required section is missing"
        parser = ConfigParser()
        parser.set_path(self.ini_path)
        parser.set_required(True)
        parser.add_section('missing', 'fooprogram.ini.foo', required=True)
        self.assertRaises(ConfigureError, parser.render)

    def test_config_option(self):
        "ConfigParser should parse an option"
        parser = ConfigParser()
        parser.set_path(self.ini_path)
        parser.set_required(True)
        parser.add_option('foo', 'required', 'fooprogram.ini.foo.required')
        store = parser.render()
        self.assertEqual(store.get('fooprogram.ini.foo.required'), ['foo'])

    def test_optional_config_option(self):
        "ConfigParser should parse a missing optional option"
        parser = ConfigParser()
        parser.set_path(self.ini_path)
        parser.set_required(True)
        parser.add_option('foo', 'missing', 'fooprogram.ini.foo.optional', required=False)
        store = parser.render()
        self.assertEqual(store.get('fooprogram.ini.foo.optional'), None)

    def test_required_config_option(self):
        "ConfigParser should raise ConfigureError if required option is missing"
        parser = ConfigParser()
        parser.set_path(self.ini_path)
        parser.set_required(True)
        parser.add_option('foo', 'missing', 'fooprogram.ini.foo.missing', required=True)
        self.assertRaises(ConfigureError, parser.render)
