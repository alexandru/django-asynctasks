#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

def import_module(name):
    try:
        module = sys.modules[name]
    except KeyError:
        module = __import__(name)
        if module and module.__name__ != name:
            components = name[len(module.__name__)+1:].split('.')
            for c in components:
                module = getattr(module, c)
    return module


def import_object(module_name, item_name):
    module = import_module(module_name)
    if not hasattr(module, item_name): raise ImportError("Could not import '%s' from module '%s'" 
                                                         % (item_name, module_name))

    return getattr(module, item_name)


def import_namespace(namespace):
    comps = namespace.split('.')
    head, tail = '.'.join(comps[:-1]), comps[-1]
    return import_object(head, tail)