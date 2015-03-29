import io

from pesky.settings.cif.path import Path
from pesky.settings.cif.grammar import *

class Frame(object):
    def __init__(self, linenum, indent):
        self.linenum = linenum
        self.indent = indent
    def __repr__(self):
        return str(self)

class ContainerFrame(Frame):
    def __init__(self, linenum, indent, path, container):
        super().__init__(linenum, indent)
        self.path = path
        self.container = container
    def __str__(self):
        return "ContainerFrame(linenum={0}, indent={1}, path={2})".format(self.linenum,self.indent,self.path)

class RootFrame(ContainerFrame):
    def __init__(self, root):
        super().__init__(None, None, Path([]), root)
    def __str__(self):
        return "RootFrame()"

class FieldFrame(Frame):
    def __init__(self, linenum, indent, path, container, field_name, field_value):
        super().__init__(linenum, indent)
        self.path = path
        self.container = container
        self.field_name = field_name
        self.field_value = field_value
    def __str__(self):
        return "FieldFrame(linenum={0}, indent={1}, path={2}, field_name={3})".format(
            self.linenum,self.indent,self.path,self.field_name)

class ValueContinuationFrame(Frame):
    def __init__(self, linenum, indent, path, container, field_name, field_value):
        super().__init__(linenum, indent)
        self.path = path
        self.container = container
        self.field_name = field_name
        self.field_value = field_value
    def __str__(self):
        return "ValueContinuationFrame(linenum={0}, indent={1}, path={2}, field_name={3})".format(
            self.linenum,self.indent,self.path,self.field_name)

class Parser(object):
    """
    """
    def __init__(self):
        self.root = {}
        self.root_frame = RootFrame(self.root)
        self.frames = [self.root_frame]

    def current_frame(self):
        return self.frames[0]

    def current_indent(self):
        return self.frames[0].indent

    def push_frame(self, frame):
        self.frames.insert(0, frame)

    def pop_frame(self):
        self.frames.pop(0)
        if len(self.frames) == 0:
            raise Exception("stack is exhausted")
        return self.frames[0]

    def append_child_object(self, linenum, indent, path):
        frame = self.current_frame()
        assert isinstance(frame,RootFrame) or isinstance(frame,ContainerFrame) and frame.indent < indent
        assert len(path.segments) > 0
        # create intermediate paths if necessary
        container = frame.container
        for segment in path.segments[0:-1]:
            if not segment in container:
                container[segment] = {}
                container = container[segment]
        container_name = path.segments[-1]
        if container_name in frame.container:
            raise KeyError("container exists at path {0}".format(path))
        container[container_name] = {}
        container = container[container_name]
        path = frame.path + path
        frame = ContainerFrame(linenum, indent, path, container)
        self.push_frame(frame)
        print("created container for path {0}".format(path))

    def append_sibling_object(self, linenum, indent, path):
        frame = self.current_frame()
        assert frame.indent is not None and frame.indent == indent
        self.pop_frame()
        self.append_child_object(linenum, indent, path)

    def append_parent_object(self, linenum, indent, path):
        frame = self.current_frame()
        assert frame.indent is not None and frame.indent > indent
        while frame.indent != indent:
            frame = self.pop_frame()
        self.append_sibling_object(linenum, indent, path)

    def append_child_field(self, linenum, indent, field_name, field_value):
        frame = self.current_frame()
        assert isinstance(frame,RootFrame) or isinstance(frame,ContainerFrame) and frame.indent < indent
        if field_name in frame.container:
            raise KeyError("field {0} exists in container at path {1}".format(field_name, frame.path))
        frame.container[field_name] = field_value
        frame = FieldFrame(linenum, indent, frame.path, frame.container, field_name, field_value)
        self.push_frame(frame)
        print("created field {0} in container at path {1}".format(field_name, frame.path))

    def append_sibling_field(self, linenum, indent, field_name, field_value):
        frame = self.current_frame()
        assert frame.indent is not None and frame.indent == indent
        self.pop_frame()
        self.append_child_field(linenum, indent, field_name, field_value)

    def append_parent_field(self, linenum, indent, field_name, field_value):
        frame = self.current_frame()
        assert frame.indent is not None and frame.indent > indent
        while frame.indent != indent:
            frame = self.pop_frame()
        self.append_sibling_field(linenum, indent, field_name, field_value)

    def append_value_continuation(self, linenum, indent, continuation):
        frame = self.current_frame()
        if isinstance(frame, FieldFrame):
            assert frame.indent < indent and frame.field_name in frame.container
        if isinstance(frame, ValueContinuationFrame):
            assert frame.indent == indent and frame.field_name in frame.container
            self.pop_frame()
        field_value = frame.field_value + '\n' + continuation
        frame.container[frame.field_name] = field_value
        frame = ValueContinuationFrame(linenum, indent, frame.path, frame.container, frame.field_name, field_value)
        self.push_frame(frame)

    def append_list_continuation(self, linenum, indent, continuation):
        pass

def load(f):
    """
    :param f:
    :type f: file
    :return:
    """
    parser = Parser()

    for linenum,indent,value in iter_lines(f):

        if isinstance(value, Comment):
            continue

        current_indent = parser.current_indent()

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

        if isinstance(value, FieldDef):
            if current_indent is None:
                parser.append_child_field(linenum, indent, value.field_name, value.field_value)
            elif current_indent < indent:
                parser.append_child_field(linenum, indent, value.field_name, value.field_value)
            elif current_indent == indent:
                parser.append_sibling_field(linenum, indent, value.field_name, value.field_value)
            else:
                parser.append_parent_field(linenum, indent, value.field_name, value.field_value)

        if isinstance(value, ValueContinuation):
            parser.append_value_continuation(linenum, indent, value.value_continuation)

        if isinstance(value, ListContinuation):
            parser.append_list_continuation(linenum, indent, value.list_continuation)

    return parser.root

def loads(s):
    """
    :param s:
    :type s: str
    :return:
    """
    return load(io.StringIO(s))

def debug(f):
    """
    :param f:
    :type f: file
    :return:
    """
    for linenum,indent,value in iter_lines(f):
        print("{0}{1}|{2}".format(str(linenum).rjust(3), ' ' * indent, value))

def debugs(s):
    """
    :param s:
    :type s: str
    :return:
    """
    debug(io.StringIO(s))


__all__ = [ 'load', 'loads', 'debug', 'debugs' ]
