import sys, os
parent = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent)

import logging
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s %(name)s: %(message)s")

from pesky.settings.path import ROOT_PATH

def print_valuetree(values, f):
    """
    """
    def _print_container(containers, fields, indent, level):
        for name,value in fields.items():
            f.write("{0}{1} = {2}\n".format(' ' * indent * level, name, value))
        for name,container in containers.items():
            f.write("{0}{1}:\n".format(' ' * indent * level, name))
            _containers = container.get_container_containers(ROOT_PATH)
            _fields = container.get_container_fields(ROOT_PATH)
            _print_container(_containers, _fields, indent, level + 1)
    containers = values.get_container_containers(ROOT_PATH)
    fields = values.get_container_fields(ROOT_PATH)
    _print_container(containers, fields, 2, 0)
