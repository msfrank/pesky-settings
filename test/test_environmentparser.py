
import os, unittest
from pesky.settings.environmentparser import EnvironmentParser
from pesky.settings import ConfigureError

class TestEnvironmentParser(unittest.TestCase):

    def test_envvar(self):
        "EnvironmentParser should parse an environment variable"
        parser = EnvironmentParser()
        parser.add_env_var('HOME', 'fooprogram.env.home')
        os.environ = { 'HOME': '/tmp' }
        store = parser.render()
        self.assertEqual(store.get('fooprogram.env.home'), ['/tmp'])

    def test_optional_envvar(self):
        "EnvironmentParser should parse a missing environment variable"
        parser = EnvironmentParser()
        parser.add_env_var('HOME', 'fooprogram.env.home', required=False)
        os.environ = {}
        store = parser.render()
        self.assertEqual(store.get('fooprogram.env.home'), None)

    def test_missing_required_envvar(self):
        "EnvironmentParser should raise ConfigureError if required environment variable is missing"
        parser = EnvironmentParser()
        os.environ = {}
        parser.add_env_var('MISSING', 'fooprogram.env.missing', required=True)
        self.assertRaises(ConfigureError, parser.render)
