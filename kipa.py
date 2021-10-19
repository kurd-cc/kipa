"""A library to convert Kurdish (Kurmanji) texts to phonetics"""
__version__ = 0.1

import n2t
import utext

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
    numbers = utext.extract_numbers(word)
    for number in numbers:
        if number.isdigit():
            word = word.replace(str(number), n2t.convert(number))

    first_possibility = word
    second_possibility = word

    # Other alternatives for l and h
    if 'l' in word or 'h' in word:
        reasons.append('Different accents or positions')

    # Replace ng
    if 'ng' in word:
        first_possibility = first_possibility.replace('ng', kurdish_ipa[kurdish_letters.index('ng')])
        second_possibility = second_possibility.replace('ng', kurdish_ipa[kurdish_letters.index('ng')])

    # Replace normal
    for letter in word:
        if letter == 'ŋ' or letter == ' ' or letter == '|':
            continue
        elif letter == 'h' or letter == 'l':
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
    terms_text = utext.process_text(text)
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

