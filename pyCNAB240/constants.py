import os
import json

from .pipe_and_filter.build import build_list_of_fields


path_to_diretory = os.path.dirname(__file__)

file_path = os.path.join(path_to_diretory, "data", "reformated_main_full_defaults.json")

with open(file_path) as f:
    data = json.load(f)

MAIN_FIELDS = build_list_of_fields(data)
