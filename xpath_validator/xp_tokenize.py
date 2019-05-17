'''
    Based on http://www.tinypy.org/ code
'''


def u_error(ctx, s, i):
    y, x = i
    line = s.split('\n')[y - 1]
    p = ''
    if y < 10:
        p += ' '
    if y < 100:
        p += '  '
    r = p + str(y) + ": " + line + "\n"
    r += "     " + " " * x + "^" + '\n'
    raise Exception('error: ' + ctx + '\n' + r)


ISYMBOLS = list('-=,.*()+<>!')
SYMBOLS = [
    'div', 'and', 'or', 'mod',
    '-', '+', '*',
    '=', '!=', '<', '>',
    '<=', '>=', '(', ')', '.', ',',
]
B_BEGIN, B_END = ['('], [')']


class TData:
    def __init__(self):
        self.y, self.yi, self.nl = 1, 0, True
        self.res, self.indent, self.braces = [], [0], 0

    def add(self, t, v):
        self.res.append({'from': self.f, 'type': t, 'val': v})


def clean(s):
    s = s.replace('\r\n', '\n')
    s = s.replace('\r', '\n')
    return s


def tokenize(s):
    s = clean(s)
    try:
        return do_tokenize(s)
    except Exception:
        u_error('tokenize', s, T.f)


def do_tokenize(s):
    global T
    T, i, l = TData(), 0, len(s)  # noqa
    T.f = (T.y, i - T.yi + 1)
    while i < l:
        c = s[i]
        T.f = (T.y, i - T.yi + 1)
        if c in ISYMBOLS:
            i = do_symbol(s, i, l)
        elif c >= '0' and c <= '9':
            i = do_number(s, i, l)
        elif (c >= 'a' and c <= 'z') or \
                (c >= 'A' and c <= 'Z') or c == '_':
                i = do_name(s, i, l)
        elif c == '"' or c == "'":
            i = do_string(s, i, l)
        elif c == ' ' or c == '\t':
            i += 1
        else:
            u_error('tokenize', s, T.f)
    r = T.res
    T = None
    return r


def do_symbol(s, i, l):
    symbols = []
    v, f, i = s[i], i, i + 1
    if v in SYMBOLS:
        symbols.append(v)
    while i < l:
        c = s[i]
        if c not in ISYMBOLS:
            break
        v, i = v + c, i + 1
        if v in SYMBOLS:
            symbols.append(v)
    v = symbols.pop()
    n = len(v)
    i = f + n
    T.add('symbol', v)
    if v in B_BEGIN:
        T.braces += 1
    if v in B_END:
        T.braces -= 1
    return i


def do_number(s, i, l):
    v, i, c = s[i], i + 1, s[i]
    while i < l:
        c = s[i]
        if (c < '0' or c > '9') and (c < 'a' or c > 'f') and c != 'x':
            break
        v, i = v + c, i + 1
    if c == '.':
        v, i = v + c, i + 1
        while i < l:
            c = s[i]
            if c < '0' or c > '9':
                break
            v, i = v + c, i + 1
    T.add('number', v)
    return i


def do_name(s, i, l):
    v, i = s[i], i + 1
    while i < l:
        c = s[i]
        if (c < 'a' or c > 'z') and (c < 'A' or c > 'Z') and (c < '0' or c > '9') and c != '_':
            break
        v, i = v + c, i + 1
    if v in SYMBOLS:
        T.add('symbol', v)
    else:
        T.add('name', v)
    return i


def do_string(s, i, l):
    v, q, i = '', s[i], i + 1
    if (l - i) >= 5 and s[i] == q and s[i + 1] == q:
        i += 2
        while i < l - 2:
            c = s[i]
            if c == q and s[i + 1] == q and s[i + 2] == q:
                i += 3
                T.add('string', v)
                break
            else:
                v, i = v + c, i + 1
                if c == '\n':
                    T.y, T.yi = T.y + 1, i
    else:
        while i < l:
            c = s[i]
            if c == q:
                i += 1
                T.add('string', v)
                break
            else:
                v, i = v + c, i + 1
    return i
