"""
    Based on http://www.tinypy.org/ code
"""

from xpath_validator.xp_tokenize import clean, u_error


def mktok(t, typ, val, itms=None):
    '''
    >>> t = {'from': (1, 8), 'type': 'symbol', 'val': '(', 'bp': 80, 'lbp': 70, 'led': call_led, 'nud': paren_nud}
    >>> left = {'from': (1, 1), 'type': 'name', 'val': 'boolean', 'lbp': 0, 'nud': itself}
    >>> mktok(t, "call", "$", [left]) == {'from': (1, 8), 'type': 'call', 'val': '$', 'items': [{'from': (1, 1), 'type': 'name', 'val': 'boolean', 'lbp': 0, 'nud': itself}]}
    True
    '''
    r = {"from": t["from"], "type": typ, "val": val}
    if itms is not None:
        r["items"] = itms
    return r


def check(t, *vs):
    if vs[0] is None:
        return True
    if t["type"] in vs:
        return True
    if t["type"] == "symbol" and t["val"] in vs:
        return True
    return False


def tweak(k, v):
    P.stack.append((k, dmap[k]))
    if v:
        dmap[k] = omap[k]
    else:
        dmap[k] = {"lbp": 0, "nud": itself}


def restore():
    k, v = P.stack.pop()
    dmap[k] = v


class PData:
    def __init__(self, s, tokens):
        self.s = s
        self.tokens = tokens
        self.pos = 0
        self.token = None
        self.stack = []

    def init(self):
        global omap, dmap
        omap = base_dmap.copy()
        dmap = base_dmap.copy()
        self.advance()

    def advance(self, val=None):
        if not check(self.token, val):
            error("expected " + val, self.token)
        if self.pos < len(self.tokens):
            t = self.tokens[self.pos]
            self.pos += 1
        else:
            t = {"from": (0, 0), "type": "eof", "val": "eof"}
        self.token = do(t)
        return t


def error(ctx, t):
    u_error(ctx, P.s, t["from"])


def nud(t):
    if "nud" not in t:
        error("no nud", t)
    return t["nud"](t)


def led(t, left):
    if "led" not in t:
        error("no led", t)
    return t["led"](t, left)


def get_lbp(t):
    if "lbp" not in t:
        error("no lbp", t)
    return t["lbp"]


def expression(rbp):
    t = P.token
    advance()
    left = nud(t)
    while rbp < get_lbp(P.token):
        t = P.token
        advance()
        left = led(t, left)
    return left


def infix_led(t, left):
    t["items"] = [left, expression(t["bp"])]
    return t


def call_led(t, left):
    r = mktok(t, "call", "$", [left])
    while not check(P.token, ")"):
        tweak(",", 0)
        r["items"].append(expression(0))
        if P.token["val"] == ",":
            advance(",")
        restore()
    advance(")")
    return r


def itself(t):
    return t


def paren_nud(t):
    tweak(",", 1)
    r = expression(0)
    restore()
    advance(")")
    return r


def advance(t=None):
    return P.advance(t)


def vargs_nud(t):
    t["type"] = "var"
    t["val"] = "."
    return t


base_dmap = {
    "!=": {"bp": 40, "lbp": 40, "led": infix_led},
    "(": {"bp": 80, "lbp": 70, "led": call_led, "nud": paren_nud},
    ")": {"lbp": 0, "nud": itself},
    "+": {"bp": 50, "lbp": 50, "led": infix_led},
    ",": {"bp": 20, "lbp": 20},
    "-": {"bp": 50, "lbp": 50, "led": infix_led},
    ".": {"nud": vargs_nud},
    "<": {"bp": 40, "lbp": 40, "led": infix_led},
    "<=": {"bp": 40, "lbp": 40, "led": infix_led},
    "=": {"bp": 40, "lbp": 40, "led": infix_led},
    ">": {"bp": 40, "lbp": 40, "led": infix_led},
    ">=": {"bp": 40, "lbp": 40, "led": infix_led},
    "and": {"bp": 31, "lbp": 31, "led": infix_led},
    "or": {"bp": 30, "lbp": 30, "led": infix_led},
    "div": {"bp": 60, "lbp": 60, "led": infix_led},
    "*": {"bp": 60, "lbp": 60, "led": infix_led},
    "mod": {"bp": 60, "lbp": 60, "led": infix_led},
    "eof": {"lbp": 0, "type": "eof", "val": "eof"},
    "name": {"lbp": 0, "nud": itself},
    "nl": {"lbp": 0, "nud": itself, "val": "nl"},
    "number": {"lbp": 0, "nud": itself},
    "string": {"lbp": 0, "nud": itself},
}


def gmap(t, v):
    if v not in dmap:
        error('unknown "%s"' % v, t)
    return dmap[v]


def do(t):
    if t["type"] == "symbol":
        r = gmap(t, t["val"])
    else:
        r = gmap(t, t["type"])
    for k in r:
        t[k] = r[k]
    return t


def do_module():
    tok = P.token
    items = []
    while not check(P.token, "eof"):
        items.append(expression(0))
    if len(items) > 1:
        return mktok(tok, "statements", ";", items)
    return items.pop()


def parse(s, tokens, wrap=0):
    global P
    s = clean(s)
    P = PData(s, tokens)
    P.init()
    r = do_module()
    P = None
    return r
