import bootstrap
import unittest
import pesky.settings.cifparser.parser

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
        root = pesky.settings.cifparser.parser.loads(self.multi_line_data)
        print(root)
        self.assertEquals(root['field1'], ' value1')
        self.assertEquals(root['field2'], ' value2')
        self.assertEquals(root['object1']['field3'], ' value3')
        self.assertEquals(root['object1']['field6'], ' value6')
        self.assertEquals(root['object1']['object2']['field4'], ' value4')
        self.assertEquals(root['object1']['object2']['object3']['field5'], ' value5')
        self.assertEquals(root['object1']['object4']['field7'], ' value7')
        self.assertEquals(root['field8'], ' value8')
        self.assertEquals(root['object5']['field9'], ' value9')

    def test_load_deep_path(self):
        "CIF should parse a multi-line document with deep paths"
        pesky.settings.cifparser.parser.debugs(self.deep_path_data)
        root = pesky.settings.cifparser.parser.loads(self.deep_path_data)
        print(root)
        self.assertEquals(root['toplevel']['this']['is']['deep']['field1'], ' value1')
        self.assertEquals(root['toplevel']['shallow']['field2'], ' value2')
        self.assertEquals(root['field3'], ' value3')

    def test_load_value_continuation_data(self):
        "CIF should parse a multi-line document with value continuations"
        pesky.settings.cifparser.parser.debugs(self.value_continuation_data)
        root = pesky.settings.cifparser.parser.loads(self.value_continuation_data)
        print(root)
        self.assertEquals(root['toplevel']['field1'], ' first line\n second line\n third line')
        self.assertEquals(root['toplevel']['field2'], ' value2')
        self.assertEquals(root['field3'], ' value3')
