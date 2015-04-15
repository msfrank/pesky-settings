from pesky.settings.cifparser.grammar import *
from pesky.settings.cifparser.parser import Parser
from pesky.settings.valuetree import ValueTree
from pesky.settings.errors import ConfigureError


class CifParser(object):
    """
    Contains configuration loaded from a CIF file object.
    """
    def __init__(self):
        pass

    def render(self, f):
        """

        :param f:
        :type f: file
        :returns:
        :rtype: pesky.settings.valuetree.ValueTree
        """
        values = ValueTree()
        parser = Parser(values)

        for linenum,indent,value in iter_lines(f):

            # skip comment lines
            if isinstance(value, Comment):
                continue

            # track the current indentation to determine if we descent, ascend,
            # or stay at the same indentation level
            current_indent = parser.current_indent()

            # add a new container
            if isinstance(value, ObjectDef):
                # object is a child of the root
                if current_indent is None:
                    parser.append_child_object(linenum, indent, value.path)
                # object is a child of the current object
                elif current_indent < indent:
                    parser.append_child_object(linenum, indent, value.path)
                # object is a sibling of the current object
                elif current_indent == indent:
                    parser.append_sibling_object(linenum, indent, value.path)
                # object is a parent of the current object
                else:
                    parser.append_parent_object(linenum, indent, value.path)

            # add a new field
            if isinstance(value, FieldDef):
                if current_indent is None:
                    parser.append_child_field(linenum, indent, value.field_name, value.field_value)
                elif current_indent < indent:
                    parser.append_child_field(linenum, indent, value.field_name, value.field_value)
                elif current_indent == indent:
                    parser.append_sibling_field(linenum, indent, value.field_name, value.field_value)
                else:
                    parser.append_parent_field(linenum, indent, value.field_name, value.field_value)

            # concatenate the continuation to value of the current field
            if isinstance(value, ValueContinuation):
                parser.append_value_continuation(linenum, indent, value.value_continuation)

            # append the continuation to the current field
            if isinstance(value, ListContinuation):
                parser.append_list_continuation(linenum, indent, value.list_continuation)

        return values

class CifFileParser(object):
    """

    """
    def render(self, cif_path, file_required):
        try:
            if cif_path is None:
                raise Exception("no configuration file was specified")
            with open(cif_path, 'r') as f:
                cifparser = CifParser()
                return cifparser.render(f)
        except EnvironmentError as e:
            if file_required:
                raise ConfigureError("failed to read configuration: %s" % e.strerror)
            return ValueTree()
