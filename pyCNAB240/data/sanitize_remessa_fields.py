import json
import os
import re


from unidecode import unidecode

from raw_cnab_fields import HEADER_DE_ARQUIVO, HEADER_DE_LOTE, SEGMENTO_P,\
                            SEGMENTO_Q, SEGMENTO_R, TRAILER_DE_LOTE,\
                            TRAILER_DE_ARQUIVO

def clean_key(key):

    # Remove () from text
    key = key.replace('(', '').replace(')', '')

    key = key.replace('.', '').replace('/', ' ')

    # It does not remove other "spaces" like tabs, or other characters like \n
    # https://stackoverflow.com/a/1546244
    key = re.sub(' +', ' ', key)
    key = key.replace(' ', '_').replace(u'Nº', 'numero')
    key = key.lower()
    return unidecode(key)


def process_fields(fields):
    d = {}
    for field in fields.split('\n'):
        *key_splited, begin, end = field.split()
        key = ' '.join(key_splited)
        if key in d:
            raise ValueError(f'Duplicated key: {key}')
        d.update({key: [begin, end]})
    return d


def sanitize_keys(dictionary):
    d = {}
    for key in dictionary:
        cleaned_key = clean_key(key)
        d.update({cleaned_key: dictionary[key]})
    return d


def dump_dict_to_json(dictionary, file_name):
    with open(file_name, 'w', encoding='utf8') as json_file:
        json.dump(dictionary, json_file, sort_keys=True, indent=4)


def main(raw_fields, file_name, path='jsons'):
    full_file_name = os.path.join(path, file_name)

    processed_fields = process_fields(raw_fields)
    dictionary = sanitize_keys(processed_fields)
    dump_dict_to_json(dictionary, full_file_name)


main(HEADER_DE_ARQUIVO, 'HEADER_DE_ARQUIVO.json')
main(HEADER_DE_LOTE, 'HEADER_DE_LOTE.json')
main(SEGMENTO_P, 'SEGMENTO_P.json')
main(SEGMENTO_Q, 'SEGMENTO_Q.json')
main(SEGMENTO_R, 'SEGMENTO_R.json')
main(TRAILER_DE_LOTE, 'TRAILER_DE_LOTE.json')
main(TRAILER_DE_ARQUIVO, 'TRAILER_DE_ARQUIVO.json')

