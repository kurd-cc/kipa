import itertools
import re
import math
from kwiki import kwiki

kurdish_vowels = [
    'a',
    'e',
    'ê',
    'i',
    'î',
    'o',
    'u',
    'û'
]

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


def _clear_text(text, delimiter=""):
    reg = "[^ABCÇDEÊFGHIÎJKLMNOPQRSŞTUÛVWXYZabcçdeêfghiîjklmnopqrsştuûvwxyz |0123456789\n]+"
    text = re.sub(reg, '*', text).rstrip()
    return delimiter.join(text.split('*'))


def _prepare_text(text):
    text = re.sub(' +', ' ',
                  text.replace(',', '*').replace('. ', '*').replace('!', '*').replace('?', '*').replace('\n', '*').replace(':', '*'))
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
    numbers = re.findall(r"[-+]?\d*\.?\d+(?:/\d*\.?\d+)?", text)
    return numbers


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


def get_ordinal(number):
    number_text = convert(number)
    number_text = number_text.strip()
    last_letter = number_text[len(number_text) - 1]
    if last_letter in kurdish_vowels:
        return number_text + 'yemîn'
    else:
        return number_text + 'emîn'


def get_weird_number(text):
    all_numbers = re.split('[./]', text)
    all_numbers = [i for i in all_numbers if i]
    text = text.replace('/', ' belavî ').replace('.', ' nûqte ')
    for number in all_numbers:
        if all_numbers.index(number) != 0 and all_numbers.index(number) != len(all_numbers) - 1:
            text = text.replace(' ' + number + ' ', ' ' + convert(number) + ' ')
        elif all_numbers.index(number) == 0:
            text = text.replace(number + ' ', convert(number) + ' ')
        elif all_numbers.index(number) == len(all_numbers) - 1:
            text = text.replace(' ' + number, ' ' + convert(number))
    return text.strip()


def get_fraction(number):
    if '/' not in number:
        raise TypeError('It should be in number/number format, e.g.: 3/4')

    if len(number.split('/')) > 2:
        return get_weird_number(number)

    sign = ''
    if number[0] == '-':
        sign = 'negatîf'
        number = number[1:]

    number_parts = number.split('/')
    second_part = number_parts[1].strip()
    first_part = number_parts[0].strip()
    if first_part[0] == '.':
        first_part = '0' + first_part
    if second_part[0] == '.':
        second_part = '0' + second_part

    is_denominator_decimal = False
    denominator = float(second_part)
    if '.' in second_part and int(second_part.split('.')[1]) != 0:
        denominator_text = get_decimal(second_part, False)
        is_denominator_decimal = True
    else:
        denominator_text = convert(int(denominator))

    if len(first_part) == 0:  # for example if there is 1/1/1 we will have /1
        return 'belavî' + ' ' + denominator_text

    numerator = float(first_part)
    if '.' in first_part and int(first_part.split('.')[1]) != 0:
        numerator_text = get_decimal(first_part, False)
    else:
        numerator_text = convert(int(numerator))

    if not is_denominator_decimal:
        denominator_text_with_an = denominator_text + 'an'
    else:
        denominator_text_with_an = denominator_text

    if denominator_text[len(denominator_text) - 1] in kurdish_vowels:
        denominator_text_with_an = denominator_text + 'yan'

    if '.' in number_parts[0].strip() and '.' in number_parts[0].strip():
        if len(sign.strip()) > 0:
            return sign + ' ' + numerator_text + ' ' + 'belavî' + ' ' + denominator_text_with_an
        else:
            return numerator_text + ' ' + 'belavî' + ' ' + denominator_text_with_an

    if numerator > denominator:
        if len(sign.strip()) > 0:
            return sign + ' ' + numerator_text + ' ' + 'belavî' + ' ' + denominator_text_with_an
        else:
            return numerator_text + ' ' + 'belavî' + ' ' + denominator_text_with_an

    elif numerator == 1 and denominator == 2:
        if len(sign.strip()) > 0:
            return sign + ' ' + 'nîv'
        else:
            return 'nîv'

    elif numerator == 1 and denominator == 4:
        if len(sign.strip()) > 0:
            return sign + ' ' + 'çarîk'
        else:
            return 'çarîk'

    else:
        if len(sign.strip()) > 0:
            return sign + ' ' + 'ji' + ' ' + denominator_text_with_an + ' ' + numerator_text
        else:
            return 'ji' + ' ' + denominator_text_with_an + ' ' + numerator_text


def get_higher_ten_power(number):
    if number == 1 or number == 0:
        return 10
    else:
        return round(10 ** math.ceil(math.log10(number)))


def get_decimal(number, in_complex_form):
    if '.' not in number:
        raise TypeError('It should be in number.number format, e.g.: 3.4 when the provided number was ' + number)

    if len(number.split('.')) > 2:
        return get_weird_number(number)

    sign = ''
    if number[0] == '-':
        sign = 'negatîf'
        number = number[1:]

    if number[0] == '.':
        number = '0' + number

    number_parts = number.split('.')
    whole_number = int(number_parts[0].strip())
    num_of_leading_zeros = sum(1 for _ in itertools.takewhile('0'.__eq__, number_parts[1].strip()))
    fractional_part = int(number_parts[1].strip())

    if not in_complex_form or len(number_parts[1].strip()) > 9:
        if len(sign.strip()) > 0:
            return sign + ' ' + convert(whole_number) + ' ' \
                   + 'nûqte' \
                   + ' ' + 'sifir ' * num_of_leading_zeros + convert(fractional_part)
        else:
            return convert(whole_number) + ' ' + 'nûqte' \
                   + ' ' + 'sifir ' * num_of_leading_zeros + convert(fractional_part)

    else:
        higher_power_of_ten = convert(get_higher_ten_power(fractional_part))
        if num_of_leading_zeros > 0:
            higher_power_of_ten = convert(get_higher_ten_power(fractional_part * int('1' + '0' * num_of_leading_zeros)))
        if higher_power_of_ten[len(higher_power_of_ten) - 1] in kurdish_vowels:
            higher_power_of_ten = higher_power_of_ten + 'yan'
        else:
            higher_power_of_ten = higher_power_of_ten + 'an'
        if len(sign.strip()) > 0:
            return sign + ' ' + convert(whole_number) + ' ' \
                   + 'û' \
                   + ' ' + 'ji' + ' ' + higher_power_of_ten + '' + ' ' + convert(fractional_part)
        else:
            return convert(whole_number) + ' ' \
                   + 'û' \
                   + ' ' + 'ji' + ' ' + higher_power_of_ten + '' + ' ' + convert(fractional_part)


def convert_ipa_word(word):
    # To lower case always
    word = word.lower()
    try:
        ipa = kwiki.get_sounds(word)['sounds'][0]['ipa'].replace('/', '').replace('[', '').replace(']', '').strip()
        return {word: word, 'first_ipa': ipa, 'second_ipa': '', 'reasons': ['The sound has been found in Wikiferheng']}
    except Exception as ex:
        pass
    reasons = []

    # Replace numbers
    numbers = extract_numbers(word)
    for number in numbers:
        if '/' in str(number):
            word = word.replace(str(number), get_fraction(number))
        elif '.' in str(number):
            word = word.replace(str(number), get_decimal(number, True))  # Use False if want simple format
        else:
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
        elif letter not in kurdish_letters:
            reasons.append('Not a Kurdish letter')
            return {'word': word, 'first_ipa': '', 'second_ipa': '', 'reasons': reasons}
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
