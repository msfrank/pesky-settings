
import sys
import unittest
from pesky.settings.optionparser import OptionParser, ProgramUsage, ProgramVersion

class TestOptionParser(unittest.TestCase):

    def test_short_option(self):
        "OptionParser should parse a short option"
        parser = OptionParser()
        parser.set_appname("fooprogram")
        parser.set_version("0.0.1")
        parser.set_usage("use fooprogram")
        parser.set_description("fooprogram is great!")
        parser.add_shortoption('s', 'fooprogram.shortoption', 's')
        sys.argv = ['program', '-s', 'foo']
        values = parser.render()
        self.assertEqual(values.get_field('fooprogram.shortoption', 's'), 'foo')

    def test_long_option(self):
        "OptionParser should parse a long option"
        parser = OptionParser()
        parser.set_appname("fooprogram")
        parser.set_version("0.0.1")
        parser.set_usage("use fooprogram")
        parser.set_description("fooprogram is great!")
        parser.add_longoption('long', 'fooprogram.longoption', 'long')
        sys.argv = ['program', '--long', 'foo']
        values = parser.render()
        self.assertEqual(values.get_field('fooprogram.longoption', 'long'), 'foo')

    def test_long_and_short_option(self):
        "OptionParser should parse a long and short option"
        parser = OptionParser()
        parser.set_appname("fooprogram")
        parser.set_version("0.0.1")
        parser.set_usage("use fooprogram")
        parser.set_description("fooprogram is great!")
        parser.add_option('s', 'long', 'fooprogram.option', 'long_and_short')
        sys.argv = ['program', '--long', 'foo']
        values = parser.render()
        self.assertEqual(values.get_field('fooprogram.option', 'long_and_short'), 'foo')
        sys.argv = ['program', '-s', 'bar']
        values = parser.render()
        self.assertEqual(values.get_field('fooprogram.option', 'long_and_short'), 'bar')

    def test_recurring_option(self):
        "OptionParser should parse a recurring option"
        parser = OptionParser()
        parser.set_appname("fooprogram")
        parser.set_version("0.0.1")
        parser.set_usage("use fooprogram")
        parser.set_description("fooprogram is great!")
        parser.add_shortoption('s', 'fooprogram.shortoption', 's', recurring=True)
        sys.argv = ['program', '-s', 'foo', '-s', 'bar', '-s', 'baz']
        values = parser.render()
        self.assertListEqual(values.get_field_list('fooprogram.shortoption', 's'), ['foo', 'bar', 'baz'])

    def test_short_switch(self):
        "OptionParser should parse a short switch"
        parser = OptionParser()
        parser.set_appname("fooprogram")
        parser.set_version("0.0.1")
        parser.set_usage("use fooprogram")
        parser.set_description("fooprogram is great!")
        parser.add_shortswitch('s', 'fooprogram.shortswitch', 's')
        sys.argv = ['program', '-s']
        values = parser.render()
        self.assertEqual(values.get_field('fooprogram.shortswitch', 's'), 'true')

    def test_long_switch(self):
        "OptionParser should parse a long switch"
        parser = OptionParser()
        parser.set_appname("fooprogram")
        parser.set_version("0.0.1")
        parser.set_usage("use fooprogram")
        parser.set_description("fooprogram is great!")
        parser.add_longswitch('long', 'fooprogram.longswitch', 'long')
        sys.argv = ['program', '--long']
        values = parser.render()
        self.assertEqual(values.get_field('fooprogram.longswitch', 'long'), 'true')

    def test_long_and_short_switch(self):
        "OptionParser should parse a long and short switch"
        parser = OptionParser()
        parser.set_appname("fooprogram")
        parser.set_version("0.0.1")
        parser.set_usage("use fooprogram")
        parser.set_description("fooprogram is great!")
        parser.add_switch('s', 'long', 'fooprogram.switch', 'long_and_short')
        sys.argv = ['program', '--long']
        values = parser.render()
        self.assertEqual(values.get_field('fooprogram.switch', 'long_and_short'), 'true')
        sys.argv = ['program', '-s']
        values = parser.render()
        self.assertEqual(values.get_field('fooprogram.switch', 'long_and_short'), 'true')

    def test_recurring_switch(self):
        "OptionParser should parse a recurring switch"
        parser = OptionParser()
        parser.set_appname("fooprogram")
        parser.set_version("0.0.1")
        parser.set_usage("use fooprogram")
        parser.set_description("fooprogram is great!")
        parser.add_shortswitch('s', 'fooprogram.shortswitch', 's', recurring=True)
        sys.argv = ['program', '-s', '-s', '-s']
        values = parser.render()
        self.assertListEqual(values.get_field_list('fooprogram.shortswitch', 's'), ['true', 'true', 'true'])
        sys.argv = ['program', '-sss']
        values = parser.render()
        self.assertListEqual(values.get_field_list('fooprogram.shortswitch', 's'), ['true', 'true', 'true'])

    def test_sub_command(self):
        "OptionParser should parse a subcommand"
        parser = OptionParser()
        parser.set_appname("fooprogram")
        parser.set_version("0.0.1")
        parser.set_usage("use fooprogram")
        parser.set_description("fooprogram is great!")
        parser.add_shortoption('s', 'fooprogram.option', 's')
        subparser = parser.add_subcommand("dosub")
        subparser.add_shortoption('s', 'fooprogram.dosub.option', 's')
        sys.argv = ['program', '-s', 'foo', 'dosub', '-s', 'bar']
        values = parser.render()
        self.assertEqual(values.get_field('fooprogram.option', 's'), 'foo')
        self.assertEqual(values.get_field('fooprogram.dosub.option', 's'), 'bar')

    def test_usage(self):
        "OptionParser should raise ProgramUsage when --help is specified"
        parser = OptionParser()
        parser.set_appname("fooprogram")
        parser.set_version("0.0.1")
        parser.set_usage("use fooprogram")
        parser.set_description("fooprogram is great!")
        sys.argv = ['program', '--help']
        self.assertRaises(ProgramUsage, parser.render)

    def test_version(self):
        "OptionParser should raise ProgramVersion when --version is specified"
        parser = OptionParser()
        parser.set_appname("fooprogram")
        parser.set_version("0.0.1")
        parser.set_usage("use fooprogram")
        parser.set_description("fooprogram is great!")
        sys.argv = ['program', '--version']
        self.assertRaises(ProgramVersion, parser.render)
