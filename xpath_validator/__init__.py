'''
validate boolean expressions with XPath syntax

>>> validate('. >= 1 and . <= 100', 10)
True
>>> validate('. >= 1 and . <= 100', 101)
False
>>> validate('not(. >= 1 and . <= 100)', -10)
True
>>> validate('ceiling(.) = 5', 4.3)
True
>>> validate('floor(.) = 4', 4.7)
True
>>> validate('floor(.) = 4', 4.2)
True
>>> validate('int(.) = 4', 4.7)
True
>>> validate('number(.) = 3.2', 3.2)
True
>>> validate('choose(true(), 1, 2) = 1', None)
True
>>> validate('choose(false(), 1, 2) = 2', None)
True
>>> validate('contains("abc", .)', "b")
True
>>> validate('contains("abc", .)', "e")
False
>>> validate('number(string(.)) = 6', 6)
True
>>> validate('string_length(.) = 11', "40258997853")
True
>>> validate('string_length(.) = 7', "abacate")
True
>>> validate('5 < .', 10)
True
>>> validate('5 > .', 10)
False
>>> validate('5 != .', 5)
False
>>> validate('5 != .', 10)
True
>>> validate('5 + 5 = .', 10)
True
>>> validate('5 - 51 = .', -46)
True
>>> validate('true() or false()', None)
True
>>> validate('false() or false()', None)
False
>>> validate('(. div 5) = 2', 10)
True
>>> validate('(. * 5) = 50', 10)
True
>>> validate('(. div 5) < .', 10)
True
>>> validate('(. * 5) > .', 10)
True
>>> validate('(. mod 2) = 0', 10)
True
>>> validate('(. mod 2) = 1', 11)
True
>>> validate('(. mod 2) = 1', 10)
False
>>> validate('(. mod 2) = 0', 11)
False
>>> validate("int(format-date-time(., '%H')) = 19", '2019-05-14T19:13:35.450686Z')
True
>>> validate("int(format-date-time(., '%m')) = 5", '2019-05-14T19:13:35.450686Z')
True
>>> validate("int(format-date-time(., '%M')) = 13", '2019-05-14T19:13:35.450686Z')
True
>>> validate("int(format-date-time(., '%Y')) = 2019", '2019-05-14T19:13:35.450686Z')
True
>>> validate("int(format-date-time(., '%d')) = 14", '2019-05-14T19:13:35.450686Z')
True
>>> validate("format-date-time(., '%d/%m/%Y') = '14/05/2019'", '2019-05-14T19:13:35.450686Z')
True
>>> validate('. >= ${min} and . <= ${max}', 10, {"max": 100, "min": 10})
True
>>> validate('. >= ${min} and . <= ${max}', 10, {"max": 100, "min": 20})
False
>>> validate('${min} = "" and ${max} = ""', None, {"max": 100, "min": 20})
False
>>> validate('string-length(.) = 11', "01258997853")
True
>>> validate("number('') = 11", None)
False
>>> validate('normalize-space("   a ") = "a"', None)
True
>>> validate('starts-with("abacate", "a")', None)
True
>>> validate('starts-with("abacate", "b")', None)
False
>>> validate('substring-after("foo_bar", "_") = "bar"', None)
True
>>> validate('substring-before("foo_bar", "_") = "foo"', None)
True
>>> validate('boolean(substring-after("foo_bar", "j")) = false()', None)
True
>>> validate('boolean(substring-before("foo_bar", "j")) = false()', None)
True
>>> validate("int(format-date-time(., '%H')) = 19", '19:13:35')
True
>>> validate("int(format-date-time(., '%S')) = 35", '19:13:35')
True
>>> validate("int(format-date-time(., '%H')) = 19", '19:13')
True
>>> validate("int(format-date-time(., '%M')) = 13", '19:13')
True
'''

__author__ = 'Marcelo Fonseca Tambalo'
__version__ = '1.1.0'
__license__ = 'MIT'

import datetime

from math import floor, ceil

from xpath_validator.xp_tokenize import tokenize
from xpath_validator.xp_parse import parse


RETURNS_BOOL_AUTO = True


class Symbol(str):
    pass


class XPathStr(str):
    def __div__(self, other):
        return map(XPathStr, self.split(other))

    __truediv__ = __div__

    def __sub__(self, other):
        return XPathStr(self.replace(other, ''))

    def __add__(self, other):
        return XPathStr(super(XPathStr, self).__add__(other))

    def __mul__(self, other):
        return XPathStr(super(XPathStr, self).__mul__(other))


DATE_TIME_FORMATS = [
    '%Y-%m-%dT%H:%M:%S.%fZ',  # '1991/25/10T14:30:59.243860Z'
    '%Y-%m-%dT%H:%M:%S.%f',   # '1991/25/10T14:30:59.243860'
    '%d/%m/%Y %H:%M:%S',      # '25/10/1991 14:30:59'
    '%Y-%m-%d %H:%M:%S',      # '2006-10-25 14:30:59'
    '%Y-%m-%d %H:%M:%S.%f',   # '2006-10-25 14:30:59.000200'
    '%Y-%m-%d %H:%M',         # '2006-10-25 14:30'
    '%Y-%m-%d',               # '2006-10-25'
    '%m/%d/%Y %H:%M:%S',      # '10/25/2006 14:30:59'
    '%m/%d/%Y %H:%M:%S.%f',   # '10/25/2006 14:30:59.000200'
    '%m/%d/%Y %H:%M',         # '10/25/2006 14:30'
    '%m/%d/%Y',               # '10/25/2006'
    '%m/%d/%y %H:%M:%S',      # '10/25/06 14:30:59'
    '%m/%d/%y %H:%M:%S.%f',   # '10/25/06 14:30:59.000200'
    '%m/%d/%y %H:%M',         # '10/25/06 14:30'
    '%m/%d/%y',               # '10/25/06'
    '%H:%M',                  # '14:30:59'
    '%H:%M:%S',               # '14:30'
]


def _format_date_time(sdt, format):
    for f in DATE_TIME_FORMATS:
        try:
            return datetime.datetime.strptime(
                sdt, f
            ).strftime(format)
        except Exception:
            pass
    return None


def _int(v):
    try:
        return int(v)
    except Exception:
        return float('nan')


def _float(v):
    try:
        return float(v)
    except Exception:
        return float('nan')


def _substring_after(x, y):
    for i in range(len(x)):
        if x[i] == y:
            return x[i + 1:]
    return ''


def _substring_before(x, y):
    for i in range(len(x)):
        if x[i] == y:
            return x[0:i]
    return ''


FUNCTIONS = {
    'false': lambda: False,
    'true': lambda: True,
    'boolean': bool,
    'not': lambda x: not bool(x),
    'choose': lambda x, a, b: a if x else b,

    'ceiling': ceil,
    'floor': floor,
    'round': round,
    'int': _int,
    'number': _float,

    'contains': lambda x, y: y in x,
    'format_date_time': _format_date_time,
    'normalize_space': str.strip,
    'starts_with': str.startswith,
    'string': str,
    'string_length': len,
    'substring_after': _substring_after,
    'substring_before': _substring_before,
}


ENV = {
    '$': lambda f, *args: FUNCTIONS[f](*args),
    '*': lambda x, y: x * y,
    '+': lambda x, y: x + y,
    '-': lambda x, y: x - y,
    'mod': lambda x, y: x % y,
    'div': lambda x, y: x / y,
    'and': lambda x, y: x and y,
    'or': lambda x, y: x or y,
    '<': lambda x, y: x < y,
    '>': lambda x, y: x > y,
    '=': lambda x, y: x == y,
    '!=': lambda x, y: x != y,
    '<=': lambda x, y: x <= y,
    '>=': lambda x, y: x >= y,
}


def _lsp_atom(token):
    try:
        return float(token)
    except ValueError:
        if token in FUNCTIONS.keys():
            return token
        if token in ENV.keys():
            return Symbol(token)
        return XPathStr(token)


def _lsp_atomize(tokens):
    if len(tokens) == 0:
        raise SyntaxError('unexpected EOF')
    token = tokens.pop(0)
    if token == '(':
        r = []
        while tokens[0] != ')':
            r.append(_lsp_atomize(tokens))
        tokens.pop(0)
        return r
    elif token == ')':
        raise SyntaxError('unexpected )')
    else:
        return _lsp_atom(token)


def _lsp_parse(program, data_node=''):
    a = _lsp_atomize((program.replace(')', ' ) ').replace('(', ' ( ').split()))

    if isinstance(data_node, str):
        data_node = XPathStr(data_node)

    def replace_dot(atoms):
        for i, e in enumerate(atoms):
            if isinstance(e, list):
                atoms[i] = replace_dot(e)
            elif e == '.':
                atoms[i] = data_node
        return atoms

    return replace_dot(a)


def _lisp(t):
    if 'items' not in t:
        if t['val'] == '':
            return "''"
        return t['val']
    args = ''.join([" " + _lisp(tt) for tt in t['items']])
    return "(" + t['val'] + args + ")"


def _to_lsp(code):
    if not code.startswith('boolean') and RETURNS_BOOL_AUTO:
        code = "boolean(%s)" % code
    tokens = tokenize(code)
    tree = parse(code, tokens)
    return _lisp(tree)


def _xpath_boolean(x):
    if isinstance(x, Symbol):
        return ENV[x]
    elif not isinstance(x, list):
        return x
    else:
        return _xpath_boolean(
            x[0]
        )(*[
            _xpath_boolean(exp)
            for exp in x[1:]
        ])


def _prepare_ctx(ctx):
    new_ctx = {}
    for d, v in ctx.items():
        if isinstance(v, str):
            if "'" in v:
                v = '"%s"' % v
            else:
                v = "'%s'" % v
        new_ctx[d] = v
    return new_ctx


def _prepare_expression(exp, data):
    exp = exp.replace('${', '{')
    exp = exp.format(**data)
    for func_name in FUNCTIONS.keys():
        nf = func_name.replace('_', '-')
        exp = exp.replace(nf, func_name)
    return exp


def validate(expression, data_node, context={}):
    expression = _prepare_expression(
        expression,
        _prepare_ctx(context)
    )
    lsp_code = _to_lsp(expression)
    lsp_parsed = _lsp_parse(lsp_code, data_node=data_node)
    return _xpath_boolean(lsp_parsed)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
