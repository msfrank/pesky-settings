import bootstrap
import io
import unittest
import pesky.settings.cifparser
import pesky.settings.cifparser.parser
from pesky.settings.path import ROOT_PATH, make_path

class TestCIFParser(unittest.TestCase):

    multi_line_data = \
"""
field1 = value1
field2 = value2
object1:
    field3 = value3
    object2:
        field4 = value4
        object3:
            field5 = value5
    field6 = value6
    object4:
        field7 = value7
field8 = value8
object5:
        field9 = value9
"""

    deep_path_data = \
"""
toplevel:
    this.is.deep:
        field1 = value1
    shallow:
        field2 = value2
field3 = value3
"""

    value_continuation_data = \
"""
toplevel:
    field1 = first line
           | second line
           | third line
    field2 = value2
field3 = value3
"""

    def test_load_multi_line(self):
        "CIF should parse a multi-line document"
        pesky.settings.cifparser.parser.debugs(self.multi_line_data)
        parser = pesky.settings.cifparser.CifParser()
        values = parser.render(io.StringIO(self.multi_line_data))
        self.assertEquals(values.get_field(ROOT_PATH, 'field1'), ' value1')
        self.assertEquals(values.get_field(ROOT_PATH, 'field2'), ' value2')
        self.assertEquals(values.get_field(make_path('object1'), 'field3'), ' value3')
        self.assertEquals(values.get_field(make_path('object1'), 'field6'), ' value6')
        self.assertEquals(values.get_field(make_path('object1.object2'), 'field4'), ' value4')
        self.assertEquals(values.get_field(make_path('object1.object2.object3'), 'field5'), ' value5')
        self.assertEquals(values.get_field(make_path('object1.object4'), 'field7'), ' value7')
        self.assertEquals(values.get_field(ROOT_PATH, 'field8'), ' value8')
        self.assertEquals(values.get_field(make_path('object5'), 'field9'), ' value9')

    def test_load_deep_path(self):
        "CIF should parse a multi-line document with deep paths"
        pesky.settings.cifparser.parser.debugs(self.deep_path_data)
        parser = pesky.settings.cifparser.CifParser()
        values = parser.render(io.StringIO(self.deep_path_data))
        self.assertEquals(values.get_field(make_path('toplevel.this.is.deep'), 'field1'), ' value1')
        self.assertEquals(values.get_field(make_path('toplevel.shallow'), 'field2'), ' value2')
        self.assertEquals(values.get_field(ROOT_PATH, 'field3'), ' value3')

    def test_load_value_continuation_data(self):
        "CIF should parse a multi-line document with value continuations"
        pesky.settings.cifparser.parser.debugs(self.value_continuation_data)
        parser = pesky.settings.cifparser.CifParser()
        values = parser.render(io.StringIO(self.value_continuation_data))
        self.assertEquals(values.get_field(make_path('toplevel'), 'field1'), ' first line\n second line\n third line')
        self.assertEquals(values.get_field(make_path('toplevel'), 'field2'), ' value2')
        self.assertEquals(values.get_field(ROOT_PATH, 'field3'), ' value3')
