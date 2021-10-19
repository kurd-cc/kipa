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


