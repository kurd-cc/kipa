import re


def _clear_text(text, delimiter=""):
    kurdish_letters = "ABCÇDEÊFGHIÎJKLMNOPQRSŞTUÛVWXYZabcçdeêfghiîjklmnopqrsştuûvwxyz |0123456789\n"
    reg = "[^"+kurdish_letters+"]+"
    text = re.sub(reg, '*', text).rstrip()
    return delimiter.join(text.split('*'))


def _prepare_text(text):
    text = re.sub(' +', ' ', text.replace(',', '*').replace('.', '*').replace('!', '*').replace('?', '*').replace('\n', '*').replace(':', '*'))
    terms_list = list(filter(None, text.split('*')))
    terms_list = list(map(_strip_spaces, terms_list))
    terms_list = list(filter(None, terms_list))
    return terms_list


def _strip_spaces(term):
    return term.strip()


def process_text(text):
    result = ["|"]
    terms = _prepare_text(text)
    for term in terms:
        result.append(term + " |\n")
    return _clear_text(' '.join(result))


def extract_numbers(text):
    numbers = re.sub("[^0-9]", ' ', text)
    numbers = ' '.join(numbers.split())
    return numbers.split(' ')


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


kurdish_ipa = [
    "b",
    "dʒ",
    "tʃ",
    "d",
    "f",
    "ɡ",
    "ɣ",
    "h",
    "ħ",
    "ʒ",
    "k",
    "l",
    "ɫ",
    "m",
    "n",
    "ŋ",
    "p",
    "q",
    "ɾ",
    "r",
    "s",
    "ʃ",
    "t",
    "v",
    "w",
    "x",
    "j",
    "z",
    "ɑː",
    "eː",
    "ɛ",
    "iː",
    "ɪ",
    "oː",
    "ʊ",
    "uː"
]

kurdish_letters = [
    "b",
    "c",
    "ç",
    "d",
    "f",
    "g",
    "x",
    "h",
    "h",
    "j",
    "k",
    "l",
    "l",
    "m",
    "n",
    "ng",
    "p",
    "q",
    "r",
    "r",
    "s",
    "ş",
    "t",
    "v",
    "w",
    "x",
    "y",
    "z",
    "a",
    "ê",
    "e",
    "î",
    "i",
    "o",
    "u",
    "û"
]


def convert_ipa_word(word):
    # To lower case always
    word = word.lower()
    reasons = []

    # Replace numbers
    numbers = extract_numbers(word)
    for number in numbers:
        if number.isdigit():
            word = word.replace(str(number), convert(number))

    first_possibility = word
    second_possibility = word

    # Other alternatives for l and h
    if 'l' in word or 'h' in word or 'r' in word:
        reasons.append('Different accents or positions')

    # Replace ng
    if 'ng' in word:
        first_possibility = first_possibility.replace('ng', kurdish_ipa[kurdish_letters.index('ng')])
        second_possibility = second_possibility.replace('ng', kurdish_ipa[kurdish_letters.index('ng')])

    # Replace normal
    for letter in word:
        if letter == 'ŋ' or letter == ' ' or letter == '|':
            continue
        elif letter == 'h' or letter == 'l' or letter == 'r':
            indices = [i for i, x in enumerate(kurdish_letters) if x == letter]
            second_possibility = second_possibility.replace(letter, kurdish_ipa[indices[1]])
            first_possibility = first_possibility.replace(letter, kurdish_ipa[indices[0]])
        else:
            first_possibility = first_possibility.replace(letter, kurdish_ipa[kurdish_letters.index(letter)])
            second_possibility = second_possibility.replace(letter, kurdish_ipa[kurdish_letters.index(letter)])

    if second_possibility == first_possibility:
        second_possibility = ''

    return {'word': word, 'first_ipa': first_possibility, 'second_ipa': second_possibility, 'reasons': reasons}


def convert_ipa_text(text):
    terms_text = process_text(text)
    terms_list = terms_text.split("\n")
    all_list = []
    for term in terms_list:
        current_list = []
        for word in term.split(" "):
            current_res = convert_ipa_word(word)
            current_list.append(current_res)
        all_list.append(current_list)
    return all_list


def get_ipa(text):
    all_list = convert_ipa_text(text)
    result_list = []
    alternatives = []
    for current_list in all_list:
        term = []
        for current_term in current_list:
            term.append(current_term['first_ipa'])
            if len(current_term['second_ipa']) > 0:
                alternatives.append({'word': current_term['word'],
                                     'inserted_ipa': current_term['first_ipa'],
                                     'alternative_ipa': current_term['second_ipa'],
                                     'reasons': current_term['reasons']})
        result_list.append(term)

    parts = []
    for item in result_list:
        result_part = ' '.join(item)
        parts.append(result_part)

    resulted_text = '\n'.join(parts)
    return {'resulted_ipa': resulted_text, 'alternatives': alternatives}


def translate_text(text):
    return get_ipa(text)['resulted_ipa']

