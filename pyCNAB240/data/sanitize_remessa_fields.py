import itertools
import json
import os
import re

from pprint import pprint
from unidecode import unidecode

from raw_cnab_fields import (
    HEADER_DE_ARQUIVO,
    HEADER_DE_LOTE,
    SEGMENTO_P,
    SEGMENTO_Q,
    SEGMENTO_R,
    TRAILER_DE_LOTE,
    TRAILER_DE_ARQUIVO,
)


def clean_key(key):

    # Remove () from text
    key = key.replace("(", "").replace(")", "")

    key = key.replace(".", "").replace("/", " ")

    # It does not remove other "spaces" like tabs, or other characters like \n
    # https://stackoverflow.com/a/1546244
    key = re.sub(" +", " ", key)
    key = key.replace(" ", "_").replace("Nº", "numero")
    key = key.lower()
    return unidecode(key)


def process_fields(fields, field_extended_keys):
    d = {}
    for field in fields.split("\n"):
        *key_splited, start, end = field.split()
        key = " ".join(key_splited)
        if key in d:
            raise ValueError(f"Duplicated key: {key}")

        extended_keys = field_extended_keys.copy()
        extended_keys.update({"start": int(start), "end": int(end)})
        d.update({key: extended_keys})
    return d


def sanitize_keys(dictionary):
    d = {}
    for key in dictionary:
        cleaned_key = clean_key(key)
        d.update({cleaned_key: dictionary[key]})
    return d


def check_slices(dictionary):
    for key_1 in dictionary:
        for key_2 in dictionary:
            if key_1 != key_2:
                print(
                    f"{key_1}: {dictionary[key_1][1]} \n {key_2}: {dictionary[key_2][0]}"
                )
                input()
                # if int(dictionary[key_2][0]) - int(dictionary[key_1][1]) != 1:
                #     mensage = f'{key_1}: {dictionary[key_1][1]} \n {key_2}: {dictionary[key_2][0]}'
                #     raise ValueError(mensage)
            break


def dump_dict_to_json(dictionary, file_name):
    with open(file_name, "w", encoding="utf8") as json_file:
        json.dump(dictionary, json_file, sort_keys=True, indent=4)


def add_infos_to_dict(dictionaries, new_keys):
    for dictionary in dictionaries:
        dictionary.update(new_keys)

    return dictionaries


def process_raw_data(raw_fields, field_extended_keys):
    processed_fields = process_fields(raw_fields, field_extended_keys)
    dictionary = sanitize_keys(processed_fields)
    return dictionary


def main(raw_fields, file_name, path="jsons"):
    full_file_name = os.path.join(path, file_name)

    processed_fields = process_fields(raw_fields)
    dictionary = sanitize_keys(processed_fields)
    # check_slices(dictionary)
    dump_dict_to_json(dictionary, full_file_name)


# main(HEADER_DE_ARQUIVO, 'HEADER_DE_ARQUIVO.json')
# main(HEADER_DE_LOTE, 'HEADER_DE_LOTE.json')
# main(SEGMENTO_P, 'SEGMENTO_P.json')
# main(SEGMENTO_Q, 'SEGMENTO_Q.json')
# main(SEGMENTO_R, 'SEGMENTO_R.json')
# main(TRAILER_DE_LOTE, 'TRAILER_DE_LOTE.json')
# main(TRAILER_DE_ARQUIVO, 'TRAILER_DE_ARQUIVO.json')

field_extended_keys = {
    "type": "str",
    "length": 0,
    "default": "",
    "pad_content": 0,
    "pad_direction": "left",
    "required": True,
    "readed_from_cnab_value": None,
    "readed_from_cnab_value_cleaned": None,
    "cleaned_value": None,
    "raw_write_value": None,
    "raw_write_default_value": None,
}

d = process_raw_data(HEADER_DE_ARQUIVO, field_extended_keys)
