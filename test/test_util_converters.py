import bootstrap
import unittest
import datetime
import pesky.settings.util.converters
from pesky.settings.errors import ConversionError

class TestUtilConverters(unittest.TestCase):

    def test_convert_bool_true(self):
        "a valid truthy string should convert to bool"
        self.assertEquals(pesky.settings.util.converters.str_to_bool('true'), True)
        self.assertEquals(pesky.settings.util.converters.str_to_bool('yes'), True)
        self.assertEquals(pesky.settings.util.converters.str_to_bool('1'), True)

    def test_convert_bool_false(self):
        "a valid falsey string should convert to bool"
        self.assertEquals(pesky.settings.util.converters.str_to_bool('false'), False)
        self.assertEquals(pesky.settings.util.converters.str_to_bool('no'), False)
        self.assertEquals(pesky.settings.util.converters.str_to_bool('0'), False)

    def test_convert_bool_fails(self):
        "conversion of an invalid string to bool should raise ConversionError"
        self.assertRaises(ConversionError, pesky.settings.util.converters.str_to_bool, 'fails')

    def test_convert_int(self):
        "a valid string should convert to int"
        self.assertEqual(pesky.settings.util.converters.str_to_int('42'), 42)

    def test_convert_int_fails(self):
        "conversion of an invalid string to int should raise ConversionError"
        self.assertRaises(ConversionError, pesky.settings.util.converters.str_to_int, 'fails')

    def test_convert_float(self):
        "a valid string should convert to float"
        self.assertAlmostEqual(pesky.settings.util.converters.str_to_float('1.2'), 1.2)

    def test_convert_float_fails(self):
        "conversion of an invalid string to float should raise ConversionError"
        self.assertRaises(ConversionError, pesky.settings.util.converters.str_to_float, 'fails')

    def test_convert_timedelta(self):
        "a valid string should convert to timedelta"
        self.assertEqual(pesky.settings.util.converters.str_to_timedelta('42 microseconds'), datetime.timedelta(microseconds=42))
        self.assertEqual(pesky.settings.util.converters.str_to_timedelta('42 milliseconds'), datetime.timedelta(milliseconds=42))
        self.assertEqual(pesky.settings.util.converters.str_to_timedelta('42 seconds'), datetime.timedelta(seconds=42))
        self.assertEqual(pesky.settings.util.converters.str_to_timedelta('42 minutes'), datetime.timedelta(minutes=42))
        self.assertEqual(pesky.settings.util.converters.str_to_timedelta('42 hours'), datetime.timedelta(hours=42))
        self.assertEqual(pesky.settings.util.converters.str_to_timedelta('42 days'), datetime.timedelta(days=42))
        self.assertEqual(pesky.settings.util.converters.str_to_timedelta('42 weeks'), datetime.timedelta(weeks=42))

    def test_convert_timedelta_fails(self):
        "conversion of an invalid string to timedelta should raise ConversionError"
        self.assertRaises(ConversionError, pesky.settings.util.converters.str_to_timedelta, 'fails')

    def test_convert_size(self):
        "a valid string should convert to size in bytes"
        self.assertEqual(pesky.settings.util.converters.str_to_size('42kb'), 42 * 1024)
        self.assertEqual(pesky.settings.util.converters.str_to_size('42mb'), 42 * 1024 * 1024)
        self.assertEqual(pesky.settings.util.converters.str_to_size('42gb'), 42 * 1024 * 1024 * 1024)
        self.assertEqual(pesky.settings.util.converters.str_to_size('42tb'), 42 * 1024 * 1024 * 1024 * 1024)
        self.assertEqual(pesky.settings.util.converters.str_to_size('42pb'), 42 * 1024 * 1024 * 1024 * 1024 * 1024)

    def test_convert_size_fails(self):
        "conversion of an invalid string to size in bytes should raise ConversionError"
        self.assertRaises(ConversionError, pesky.settings.util.converters.str_to_size, 'fails')

    def test_convert_percentage(self):
        "a valid string should convert to a percentage represented as a float"
        self.assertAlmostEqual(pesky.settings.util.converters.str_to_percentage('.1%'), 0.001)
        self.assertAlmostEqual(pesky.settings.util.converters.str_to_percentage('0.1%'), 0.001)
        self.assertAlmostEqual(pesky.settings.util.converters.str_to_percentage('42%'), 0.42)
        self.assertAlmostEqual(pesky.settings.util.converters.str_to_percentage('742%'), 7.42)
        self.assertAlmostEqual(pesky.settings.util.converters.str_to_percentage('742.03%'), 7.4203)

    def test_convert_percentage_fails(self):
        "conversion of an invalid string to percentage should raise ConversionError"
        self.assertRaises(ConversionError, pesky.settings.util.converters.str_to_percentage, 'fails')

    def test_convert_args(self):
        "a valid string should convert to an argument list"

    def test_convert_args_fails(self):
        "conversion of an invalid string to an argument list should raise ConversionError"
