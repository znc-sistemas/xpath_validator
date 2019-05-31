'''
validate boolean expressions with XPath syntax

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
'''


from xpath_validator import *  # noqa


if __name__ == "__main__":
    import doctest
    doctest.testmod()