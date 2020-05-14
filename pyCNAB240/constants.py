import os

from .pipe_and_filter.build import build_list_from_csv, build_list_of_fields

path_to_diretory = os.path.dirname(__file__)
# csv_full_file_name = os.path.join(path_to_diretory, 'data', 'csvs',
#                                   'reformated_main_full.csv')
csv_full_file_name = os.path.join(
    path_to_diretory, "data", "csvs", "reformated_main_full_defaults.csv"
)
del path_to_diretory

LINES = build_list_from_csv(csv_full_file_name)
del csv_full_file_name

MAIN_FIELDS = build_list_of_fields(LINES)
del LINES
