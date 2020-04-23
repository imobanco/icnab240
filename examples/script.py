from pprint import pprint

from ruamel.yaml import YAML

# yaml = YAML(typ='safe')
yaml = YAML()
# yaml.default_flow_style = False


# d = {'bank_code': {
#     'type': 'int',
#     'length': 3,
#     'default': 341,
#     'pad_content': 0,
#     'pad_direction': 'left',
#     'required': True,
#     'start': 0,
#     'end': 3,
#     'value': None,
#     }}


field_template = {
    'type': 'int or float or str',
    'length': 'int',
    'default': 'None',
    'pad_content': 'depend if is Number 0, if str " "',
    'pad_direction': 'left or right',
    'required': 'boolean True or False',
    'start': 'int',
    'end': 'int',
    'readed_from_cnab_value': 'begin with None, when recive valor is the full value field',
    'readed_from_cnab_value_cleaned': 'begin with None, when readed_from_cnab_value is not None it is it cleaned',
    'cleaned_value': '',
    'raw_write_value': 'is the raw value to be wrote to the cnab field',
    'raw_write_default_value': 'if None needs to be provided',
    }

field = {
    'type': 'int float str',
    'length': 'int',
    'default': '',
    'pad_content': 'depend if is Number 0, if str " "',
    'pad_direction': 'left right',
    'required': True or False,
    'start': 'int',
    'end': 'int',
    'readed_from_cnab_value': None,
    'readed_from_cnab_value_cleaned': None,
    'cleaned_value': None,
    'raw_write_value': None,
    'raw_write_default_value': None,
    }

fields_line = [{f'key_{i}': field} for i in range(23)]

HEADER_DE_ARQUIVO = {'HEADER_DE_ARQUIVO': fields_line}

HEADER_DE_LOTE = {'HEADER_DE_LOTE': fields_line}

SEGMENTS = {'SEGMENTS': [{'P': fields_line},
                         {'Q': fields_line},
                         {'R': fields_line}]
            }

TRAILER_DE_ARQUIVO = {'TRAILER_DE_ARQUIVO': fields_line}

TRAILER_DE_LOTE = {'TRAILER_DE_LOTE': fields_line}


d = [HEADER_DE_ARQUIVO, HEADER_DE_LOTE, SEGMENTS, TRAILER_DE_ARQUIVO, TRAILER_DE_LOTE]

file_name = 'test.yaml'


def dump_dict_to_yaml(dictionary, file_name):
    with open(file_name, 'w', encoding='utf8') as yaml_file:
        # yaml.dump(dictionary, yaml_file)
        yaml.dump(dictionary, yaml_file)

def load_from_yaml_to_dict(yaml_file_name):
    with open(yaml_file_name, 'r', encoding='utf8') as yaml_file:
        data = yaml.safe_load(yaml_file)
    return data

q = {'a': [{'q': 'Pedro', 'w': None}, {'q': 'Pedro', 'w': None}]}
dump_dict_to_yaml(q, file_name)

# load_from_yaml_to_dict(file_name)
inp = """\
defaults: &defaults
  A: 1
  B: 2
mapping:
  << : *defaults
  A: 23
  C: 99
"""

# inp = """\
# a:
# - q: Pedro
#   w:
# - q: Pedro
#   w:
# """


print(yaml.load(inp))

