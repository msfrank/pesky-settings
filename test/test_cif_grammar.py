import bootstrap
import unittest
import pesky.settings.cif.grammar

class TestCIFGrammar(unittest.TestCase):

    def test_parse_comment_line(self):
        "CIF should tokenise '#' + <RestOfLine> as a comment"
        indent,result = pesky.settings.cif.grammar.parse_line("# this is a comment")
        self.assertIsInstance(result, pesky.settings.cif.grammar.Comment)
        result_fields = vars(result)
        other_fields = vars(pesky.settings.cif.grammar.Comment(" this is a comment"))
        self.assertDictEqual(result_fields, other_fields)

    def test_parse_objectdef_line(self):
        "CIF should tokenise <PathSegment> + ':' as a simple object definition"
        indent,result = pesky.settings.cif.grammar.parse_line("object:")
        self.assertIsInstance(result, pesky.settings.cif.grammar.ObjectDef)
        result_fields = vars(result)
        other_fields = vars(pesky.settings.cif.grammar.ObjectDef(pesky.settings.cif.parser.Path(['object'])))
        self.assertDictEqual(result_fields, other_fields)

    def test_parse_deep_objectdef_line(self):
        "CIF should tokenise *(<PathSegment> + '.') + <PathSegment> + ':' as a deep object definition"
        indent,result = pesky.settings.cif.grammar.parse_line("deep.nested.object:")
        self.assertIsInstance(result, pesky.settings.cif.grammar.ObjectDef)
        result_fields = vars(result)
        other_fields = vars(pesky.settings.cif.grammar.ObjectDef(pesky.settings.cif.parser.Path(['deep','nested','object'])))
        self.assertDictEqual(result_fields, other_fields)

    def test_parse_fielddef_line(self):
        "CIF should tokenise <FieldDef> + '=' + <RestOfLine> as a field definition"
        indent,result = pesky.settings.cif.grammar.parse_line("foo = bar")
        self.assertIsInstance(result, pesky.settings.cif.grammar.FieldDef)
        result_fields = vars(result)
        other_fields = vars(pesky.settings.cif.grammar.FieldDef('foo', ' bar'))
        self.assertDictEqual(result_fields, other_fields)

    def test_parse_valuecontinuation_line(self):
        "CIF should tokenise '|' + <RestOfLine> as a value continuation"
        indent,result = pesky.settings.cif.grammar.parse_line("| this is a continuation")
        self.assertIsInstance(result, pesky.settings.cif.grammar.ValueContinuation)
        result_fields = vars(result)
        other_fields = vars(pesky.settings.cif.grammar.ValueContinuation(' this is a continuation'))
        self.assertDictEqual(result_fields, other_fields)

    def test_parse_listcontinuation_line(self):
        "CIF should tokenise ',' + <RestOfLine> as a list continuation"
        indent,result = pesky.settings.cif.grammar.parse_line(", this is a continuation")
        self.assertIsInstance(result, pesky.settings.cif.grammar.ListContinuation)
        result_fields = vars(result)
        other_fields = vars(pesky.settings.cif.grammar.ListContinuation(' this is a continuation'))
        self.assertDictEqual(result_fields, other_fields)
