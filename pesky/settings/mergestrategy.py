
from pesky.settings.valuetree import ValueTree

class MergeStrategy(object):
    def merge(self, current, proposed):
        raise NotImplementedError()

class ReplaceStrategy(MergeStrategy):
    def merge(self, current, proposed):
        return proposed

class KeepStrategy(MergeStrategy):
    def merge(self, current, proposed):
        return current

class AppendStrategy(MergeStrategy):
    def merge(self, current, proposed):
        if isinstance(current, list) and isinstance(proposed, list):
            return current + proposed
        if not isinstance(current, list) and isinstance(proposed, list):
            return [current] + proposed
        if isinstance(current, list) and not isinstance(proposed, list):
            return current + [proposed]
        return [current, proposed]

class MergeAccumulator(object):
    """
    """
    def __init__(self, default_strategy):
        self.default_strategy = default_strategy
        self._rules = {}

    def add_field_rule(self, path, name, strategy):
        """
        :param path:
        :param name:
        :param strategy:
        :return:
        """
        self._rules[(path,name)] = strategy

    def add_container_rule(self, path, strategy):
        """
        :param path:
        :param strategy:
        :return:
        """
        self._rules[(path,None)] = strategy

    def merge(self, current_values, proposed_values):
        """
        :param current:
        :type current: pesky.settings.valuetree.ValueTree
        :param proposed:
        :type proposed: pesky.settings.valuetree.ValueTree
        :return:
        :rtype: pesky.settings.valuetree.ValueTree
        """
        for path,name,proposed in proposed_values.iter_fields():
            if (path,name) in self._rules:
                strategy = self._rules[(path,name)]
            elif (path,None) in self._rules:
                strategy = self._rules[(path,None)]
            else:
                strategy = self.default_strategy
            try:
                value = strategy.merge(current_values.get(path, name), proposed)
            except:
                value = proposed
            current_values.put_container(path)
            current_values.put_field(path, name, value)
        return current_values


