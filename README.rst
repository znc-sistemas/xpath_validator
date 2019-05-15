xpath_validator
===============

Validate boolean expressions with XPath syntax

Examples
--------

.. code-block:: python
    
    >>> from xpath_validator import validate
    >>> validate('. >= 1 and . <= 100', "10")
    True
    >>> validate('. >= 1 and . <= 100', "101")
    False
    >>> validate('not(. >= 1 and . <= 100)', "-10")
    True
    >>> validate('ceiling(.) = 5', 4.3)
    True
    >>> validate('floor(.) = 4', "4.7")
    True
    >>> validate('floor(.) = 4', "4.2")
    True
    >>> validate('int(.) = 4', "4.7")
    True
    >>> validate('number(.) = 3.2', "3.2")
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
    >>> validate('5 < .', "10")
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