
class Path(object):
    def __init__(self, segments):
        self.segments = segments
    def __str__(self):
        return '.'.join(self.segments) if len(self.segments) > 0 else '.'
    def __repr__(self):
        return str(self)
    def __eq__(self, other):
        return self.segments == other.segments
    def __hash__(self):
        return hash(str(self))
    def __iter__(self):
        return iter(self.segments)
    def __add__(self, other):
        if isinstance(other, Path):
            return Path(self.segments + other.segments)
        elif isinstance(other, list):
            return Path(self.segments + other)
        elif isinstance(other, str):
            return Path(self.segments + [other])
        else:
            raise ValueError("can't concatenate Path with {0}".format(type(other)))
