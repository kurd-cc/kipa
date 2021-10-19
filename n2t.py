def convert(number):
    number = str(number)
    if len(number) == 1:
        return _convert_ones(number)
    elif len(number) == 2:
        return _convert_tens(number)
    elif len(number) == 3:
        return _convert_hundreds(number)
    elif len(number) == 4:
        return _convert_thousands(number)
    elif len(number) == 5:
        return _convert_tens_thousands(number)
    elif len(number) == 6:
        return _convert_hundreds_thousands(number)
    elif len(number) == 7:
        return _convert_millions(number)
    elif len(number) == 8:
        return _convert_tens_millions(number)
    elif len(number) == 9:
        return _convert_hundreds_millions(number)
    else:
        return _convert_large_numbers(number)


def _convert_ones(n):
    _dict = {
        '0': 'sifir',
        '1': 'yek',
        '2': 'du',
        '3': 'sê',
        '4': 'çar',
        '5': 'pênc',
        '6': 'şeş',
        '7': 'heft',
        '8': 'heşt',
        '9': 'neh'
    }

    return _dict[n]


def _convert_tens(n):
    if n[0] == '0':
        return _convert_ones(n)

    _dict = {
        '10': 'deh',
        '11': 'yanzdeh',
        '12': 'dwanzdeh',
        '13': 'sêzdeh',
        '14': 'çardeh',
        '15': 'panzdeh',
        '16': 'şanzdeh',
        '17': 'hivdeh',
        '18': 'hijdeh',
        '19': 'nozdeh',
        '20': 'bîst',
        '30': 'sî',
        '40': 'çil',
        '50': 'pêncî',
        '60': 'şêst',
        '70': 'heftê',
        '80': 'heştê',
        '90': 'nod'
    }

    if n in _dict:
        return _dict[n]
    first_n = str(int(str(n)[0:1]) * 10)
    second_n = str(int(str(n)[1:2]))
    return _dict[first_n] + _get_joint() + _convert_ones(second_n)


def _convert_hundreds(n):
    if n == '100':
        return 'sed'

    if n.endswith('00'):
        first_n = n[0:1]
        return _convert_ones(first_n) + 'sed'

    first_n = n[0:1]
    second_n = str(int(n[1:]))

    if len(second_n) == 1:
        return _convert_hundreds(str(int(first_n) * 100)) + _get_joint() + _convert_ones(second_n)
    elif len(second_n) == 2:
        return _convert_hundreds(str(int(first_n) * 100)) + _get_joint() + _convert_tens(second_n)


def _convert_thousands(n):
    if n == '1000':
        return 'hezar'

    if n.endswith('000'):
        current_n = n[0:1]
        if n[0] == '5':
            return 'pênj' + ' ' + 'hezar'
        else:
            return _convert_ones(current_n) + ' ' + 'hezar'

    rest_int = int(n[1:])
    rest = ''
    if len(str(rest_int)) == 1:
        rest = _convert_ones(str(rest_int))
    elif len(str(rest_int)) == 2:
        rest = _convert_tens(str(rest_int))
    elif len(str(rest_int)) == 3:
        rest = _convert_hundreds(str(rest_int))

    if n[0] == '5':
        return 'pênj' + ' ' + 'hezar' + _get_joint() + rest
    elif n[0] == '1':
        return 'hezar' + _get_joint() + rest
    else:
        current_n = int(n[0:1])
        return _convert_ones(str(current_n)) + ' ' + 'hezar' + _get_joint() + rest


def _convert_tens_thousands(n):
    if n.endswith('000'):
        current_n = n[0:2]
        return _convert_tens(current_n) + ' ' + 'hezar'

    rest_int = int(n[2:])
    rest = ''

    if len(str(rest_int)) == 1:
        rest = _convert_ones(str(rest_int))
    elif len(str(rest_int)) == 2:
        rest = _convert_tens(str(rest_int))
    else:
        rest = _convert_hundreds(str(rest_int))

    current_n = int(n[0:2])
    return _convert_tens(str(current_n)) + ' ' + 'hezar' + _get_joint() + rest


def _convert_hundreds_thousands(n):
    if n.endswith('000'):
        current_n = n[0:3]
        return _convert_hundreds(current_n) + ' ' + 'hezar'

    rest_int = int(n[3:])
    rest = ''

    if len(str(rest_int)) == 1:
        rest = _convert_ones(str(rest_int))
    elif len(str(rest_int)) == 2:
        rest = _convert_tens(str(rest_int))
    else:
        rest = _convert_hundreds(str(rest_int))

    current_n = int(n[0:3])
    return _convert_hundreds(str(current_n)) + ' ' + 'hezar' + _get_joint() + rest


def _convert_millions(n):
    if n == '1000000':
        return 'milyon'

    if n.endswith('000000'):
        current_n = n[0:1]
        if n[0] == '5':
            return 'pênj' + ' ' + 'milyon'
        else:
            return _convert_ones(current_n) + ' ' + 'milyon'

    rest_int = int(n[1:])
    rest = ''
    if len(str(rest_int)) == 1:
        rest = _convert_ones(str(rest_int))
    elif len(str(rest_int)) == 2:
        rest = _convert_tens(str(rest_int))
    elif len(str(rest_int)) == 3:
        rest = _convert_hundreds(str(rest_int))
    elif len(str(rest_int)) == 4:
        rest = _convert_thousands(str(rest_int))
    elif len(str(rest_int)) == 5:
        rest = _convert_tens_thousands(str(rest_int))
    elif len(str(rest_int)) == 6:
        rest = _convert_hundreds_thousands(str(rest_int))

    if n[0] == '5':
        return 'pênj' + ' ' + 'milyon' + _get_joint() + rest
    elif n[0] == '1':
        return 'milyon' + _get_joint() + rest
    else:
        current_n = int(n[0:1])
        return _convert_ones(str(current_n)) + ' ' + 'milyon' + _get_joint() + rest


def _convert_tens_millions(n):
    if n.endswith('000000'):
        current_n = n[0:2]
        return _convert_tens(current_n) + ' ' + 'milyon'

    rest_int = int(n[2:])
    rest = ''

    if len(str(rest_int)) == 1:
        rest = _convert_ones(str(rest_int))
    elif len(str(rest_int)) == 2:
        rest = _convert_tens(str(rest_int))
    elif len(str(rest_int)) == 3:
        rest = _convert_hundreds(str(rest_int))
    elif len(str(rest_int)) == 4:
        rest = _convert_thousands(str(rest_int))
    elif len(str(rest_int)) == 5:
        rest = _convert_tens_thousands(str(rest_int))
    elif len(str(rest_int)) == 6:
        rest = _convert_hundreds_thousands(str(rest_int))

    current_n = int(n[0:2])
    return _convert_tens(str(current_n)) + ' ' + 'milyon' + _get_joint() + rest


def _convert_hundreds_millions(n):
    if n.endswith('000000'):
        current_n = n[0:3]
        return _convert_hundreds(current_n) + ' ' + 'milyon'

    rest_int = int(n[3:])
    rest = ''

    if len(str(rest_int)) == 1:
        rest = _convert_ones(str(rest_int))
    elif len(str(rest_int)) == 2:
        rest = _convert_tens(str(rest_int))
    elif len(str(rest_int)) == 3:
        rest = _convert_hundreds(str(rest_int))
    elif len(str(rest_int)) == 4:
        rest = _convert_thousands(str(rest_int))
    elif len(str(rest_int)) == 5:
        rest = _convert_tens_thousands(str(rest_int))
    elif len(str(rest_int)) == 6:
        rest = _convert_hundreds_thousands(str(rest_int))

    current_n = int(n[0:3])
    return _convert_hundreds(str(current_n)) + ' ' + 'milyon' + _get_joint() + rest


def _convert_large_numbers(n):
    if n == '1000000000':
        return 'milyar'
    else:
        res = []
        n = str(n)
        for number in n:
            res.append(_convert_ones(number))
        return ' '.join(res)


def _get_joint():
    return ' û '

