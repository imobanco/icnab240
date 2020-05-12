from pyCNAB240.old_cnab import CNAB240


cnab_file_name = "Faturas2802.REM"
json_file_name = "Faturas1202.json"

cnab = CNAB240()

cnab.cnab_to_json(cnab_file_name, json_file_name)


# print(cnab.split_cnab(cnab.read_REM(cnab_file_name)))
