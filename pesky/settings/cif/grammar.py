import collections
import pyparsing as pp

from pesky.settings.cif.path import Path

Comment = collections.namedtuple('Comment',['value'])
ObjectDef = collections.namedtuple('ObjectDef', ['path'])
FieldDef = collections.namedtuple('FieldDef', ['field_name','field_value'])
ValueContinuation = collections.namedtuple('ValueContinuation', ['value_continuation'])
ListContinuation = collections.namedtuple('ListContinuation', ['list_continuation'])

comment_parser = pp.Literal('#') + pp.restOfLine

pathsegment_parser = pp.Word(pp.alphanums) ^ pp.quotedString
path_parser = pp.ZeroOrMore(pathsegment_parser + pp.Literal('.')) + pathsegment_parser
objectdef_parser = path_parser + pp.Literal(':')

fieldkey_parser = pp.Word(pp.alphanums) ^ pp.quotedString
fielddef_parser = fieldkey_parser + pp.Literal('=') + pp.restOfLine

valuecontinuation_parser = pp.Literal('|') + pp.restOfLine
listcontinuation_parser = pp.Literal(',') + pp.restOfLine

def comment_parse_action(tokens):
    return Comment(tokens[1])
comment_parser.setParseAction(comment_parse_action)

def path_parse_action(tokens):
    return Path(list(filter(lambda x: x != '.', tokens)))
path_parser.setParseAction(path_parse_action)

def objectdef_parse_action(tokens):
    return ObjectDef(tokens[0])
objectdef_parser.setParseAction(objectdef_parse_action)

def fielddef_parse_action(tokens):
    return FieldDef(tokens[0], tokens[2])
fielddef_parser.setParseAction(fielddef_parse_action)

def valuecontinuation_parse_action(tokens):
    return ValueContinuation(tokens[1])
valuecontinuation_parser.setParseAction(valuecontinuation_parse_action)

def listcontinuation_parse_action(tokens):
    return ListContinuation(tokens[1])
listcontinuation_parser.setParseAction(listcontinuation_parse_action)

line_parser = comment_parser ^ objectdef_parser ^ fielddef_parser ^ valuecontinuation_parser ^ listcontinuation_parser

def line_parse_action(tokens):
    return None if len(tokens) == 0 else tokens[0]
line_parser.setParseAction(line_parse_action)

def calculate_indent(text):
    """
    :param text:
    :type text: str
    :return:
    """
    indent = 0
    for c in text:
        if c is '\t':
            raise ValueError()
        if c is not ' ':
            return indent,text[indent:]
        indent += 1
    return indent,''

def parse_line(text):
    """
    :param text:
    :type text: str
    :return:
    """
    indent,text = calculate_indent(text)
    results = line_parser.parseString(text, parseAll=True).asList()
    return indent,results[0]

def iter_lines(f):
    """
    :param f:
    :type f: file
    :return:
    """
    linenum = 1
    for text in f.readlines():
        # ignore lines that consist entirely of whitespace
        if text.isspace():
            continue
        indent,value = parse_line(text)
        yield linenum,indent,value
        linenum += 1
