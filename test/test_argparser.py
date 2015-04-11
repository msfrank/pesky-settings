import bootstrap

import unittest
from pesky.settings.argparser import ArgParser

class TestArgParser(unittest.TestCase):

    def test_short_option(self):
        "ArgParser should parse a short option"
        parser = ArgParser()
        parser.add_shortoption('s', 'fooprogram.shortoption', 's')
        argv = ['-s', 'foo']
        values = parser.render(argv)
        self.assertEqual(values.get_field('fooprogram.shortoption', 's'), 'foo')

    def test_long_option(self):
        "ArgParser should parse a long option"
        parser = ArgParser()
        parser.add_longoption('long', 'fooprogram.longoption', 'long')
        argv = ['--long', 'foo']
        values = parser.render(argv)
        self.assertEqual(values.get_field('fooprogram.longoption', 'long'), 'foo')

    def test_long_and_short_option(self):
        "ArgParser should parse a long and short option"
        parser = ArgParser()
        parser.add_option('s', 'long', 'fooprogram.option', 'long_and_short')
        argv = ['--long', 'foo']
        values = parser.render(argv)
        self.assertEqual(values.get_field('fooprogram.option', 'long_and_short'), 'foo')
        argv = ['-s', 'bar']
        values = parser.render(argv)
        self.assertEqual(values.get_field('fooprogram.option', 'long_and_short'), 'bar')

    def test_recurring_option(self):
        "ArgParser should parse a recurring option"
        parser = ArgParser()
        parser.add_shortoption('s', 'fooprogram.shortoption', 's', recurring=True)
        argv = ['-s', 'foo', '-s', 'bar', '-s', 'baz']
        values = parser.render(argv)
        self.assertListEqual(values.get_field_list('fooprogram.shortoption', 's'), ['foo', 'bar', 'baz'])

    def test_short_switch(self):
        "ArgParser should parse a short switch"
        parser = ArgParser()
        parser.add_shortswitch('s', 'fooprogram.shortswitch', 's')
        argv = ['-s']
        values = parser.render(argv)
        self.assertEqual(values.get_field('fooprogram.shortswitch', 's'), 'true')

    def test_long_switch(self):
        "ArgParser should parse a long switch"
        parser = ArgParser()
        parser.add_longswitch('long', 'fooprogram.longswitch', 'long')
        argv = ['--long']
        values = parser.render(argv)
        self.assertEqual(values.get_field('fooprogram.longswitch', 'long'), 'true')

    def test_long_and_short_switch(self):
        "ArgParser should parse a long and short switch"
        parser = ArgParser()
        parser.add_switch('s', 'long', 'fooprogram.switch', 'long_and_short')
        argv = ['--long']
        values = parser.render(argv)
        self.assertEqual(values.get_field('fooprogram.switch', 'long_and_short'), 'true')
        argv = ['-s']
        values = parser.render(argv)
        self.assertEqual(values.get_field('fooprogram.switch', 'long_and_short'), 'true')

    def test_recurring_switch(self):
        "ArgParser should parse a recurring switch"
        parser = ArgParser()
        parser.add_shortswitch('s', 'fooprogram.shortswitch', 's', recurring=True)
        argv = ['-s', '-s', '-s']
        values = parser.render(argv)
        self.assertListEqual(values.get_field_list('fooprogram.shortswitch', 's'), ['true', 'true', 'true'])
        argv = ['-sss']
        values = parser.render(argv)
        self.assertListEqual(values.get_field_list('fooprogram.shortswitch', 's'), ['true', 'true', 'true'])

    # def test_sub_command(self):
    #     "ArgParser should parse a subcommand"
    #     parser = ArgParser()
    #     parser.add_shortoption('s', 'fooprogram.option', 's')
    #     subparser = parser.add_subcommand_parser("dosub")
    #     subparser.add_shortoption('s', 'fooprogram.dosub.option', 's')
    #     argv = ['program', '-s', 'foo', 'dosub', '-s', 'bar']
    #     values = parser.render(argv)
    #     self.assertEqual(values.get_field('fooprogram.option', 's'), 'foo')
    #     self.assertEqual(values.get_field('fooprogram.dosub.option', 's'), 'bar')
    #
    # def test_usage(self):
    #     "ArgParser should raise ProgramUsage when --help is specified"
    #     parser = ArgParser()
    #     sys.argv = ['program', '--help']
    #     self.assertRaises(ProgramUsage, parser.render)
    #
    # def test_version(self):
    #     "ArgParser should raise ProgramVersion when --version is specified"
    #     parser = ArgParser()
    #     sys.argv = ['program', '--version']
    #     self.assertRaises(ProgramVersion, parser.render)
