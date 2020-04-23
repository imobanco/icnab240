from pyCNAB240.old_cnab import CNAB240


cnab_file_name = 'Faturas2802.REM'
sheet_file_name = 'Faturas2802.xlsx'

cnab = CNAB240()
cnab.cnab_to_sheet(cnab_file_name, sheet_file_name)


