__author__ = 'Joe Linn'

import re
import dateutil.parser
import importlib

def get_param_name(name_or_object):
    """
    Attempts to determine the name of the parameter based on its class
    @param name_or_object: class instance or class name
    @type name_or_object: str or object
    @return: parameter name
    @rtype: str
    """
    if not isinstance(name_or_object, str) and isinstance(name_or_object, object):
        name_or_object = name_or_object.__class__.__name__
    name_or_object = re.sub(r'^(Facet|Query|Filter)|(Facet|Query|Filter)$', r'', name_or_object)
    return to_snake_case(name_or_object)

def to_snake_case(string):
    """
    Converts a CamelCase string to snake_case
    @param string:
    @type string: str
    @return:
    @rtype: str
    """
    string = re.sub(r'([A-Z])', r'_\1', string)
    return string[1:].lower()

def get_class(kls):
    parts = kls.split('.')
    module = ".".join(parts[:-1]) + '.' + parts[-1].lower()
    #m = __import__( module, level=0)
    m = importlib.import_module(module)
    # for comp in parts[1:]:
    #     m = getattr(m, comp)
    m = getattr(m, parts[-1])
    return m

def convert_date(date):
    return dateutil.parser.parse(date).strftime('%s')
