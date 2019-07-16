xpath_validator 
===============

.. image:: https://travis-ci.org/znc-sistemas/xpath_validator.svg?branch=master
    :target: https://travis-ci.org/znc-sistemas/xpath_validator

.. image:: https://coveralls.io/repos/github/znc-sistemas/xpath_validator/badge.svg?branch=master
    :target: https://coveralls.io/github/znc-sistemas/xpath_validator?branch=master

.. image:: https://img.shields.io/badge/license-MIT-blue.svg?style=flat-square
    :target: https://raw.githubusercontent.com/znc-sistemas/xpath_validator/master/LICENSE.txt
    :alt: Package license

Validate boolean expressions with XPath syntax

validate('expression', 'value', 'context', 'returns_bool')

- expression: string with the expression text
- value: value that will be validated (it is replaced by the occurrences of '.' in the expression)
- context: dictionary that will make substitutions in $ {name}
- returns_bool: if true, automatically returns a boolean

Examples
--------

.. code-block:: python
    
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
    >>> validate("substring-after('aa&bb', ${sep}) = 'bb'", "&", {'sep': '&'})
    True
    >>> validate("substring-before('aa&bb', ${sep}) = 'aa'", "&", {'sep': '&'})
    True
    >>> validate("normalize-space('    abacate ') = 'abacate'", None)
    True
    >>> validate("starts-with('abacate', 'ab')", None)
    True
    >>> validate("starts-with('abacate', 'ac')", None)
    False
    >>> validate("uuid()", None, returns_bool=False)
    2327c8bc-ac46-4968-a73c-5f21f9e9b1ce
