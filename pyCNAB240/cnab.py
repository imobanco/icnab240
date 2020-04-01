import io
import json
import os

from functools import partial

import xlsxwriter

from pycpfcnpj import cpfcnpj


class CNAB240:
    """

    """
    FIELDS = ('CPF_CNPJ', 'NOME_TITULAR', 'SOBRENOME_TITULAR', 'ENDERECO',
              'NUMERO', 'COMPLEMENTO', 'BAIRRO', 'CIDADE', 'UF', 'CEP',
              'VALOR', 'VENCIMENTO'
              )
    SHEET_FIELDS = {'NUM_TITULO': [],
                    'CPF_CNPJ': [],
                    'DEVEDOR': [],
                    'CEP': [],
                    'NUMERO': [],
                    'COMPLEMENTO': [],
                    'EMAIL': [],
                    'FONE': [],
                    'VALOR': [],
                    'VENCIMENTO': [],
                    'LIMITE': [],
                    'BASE': [],
                    'DE': [],
                    'MULTA': [],
                    'JUROS': [],
                    'DESCONTO': [],
                    'DESCONTO_DATA': [],
                    'INSTRUCOES': [],
                    }

    def __init__(self):

        self.CNAB_FIELDS = self.load_cnab_fiels()

    def load_cnab_fiels(self):
        base_dir = os.path.join('data', 'jsons')
        loader = partial(self.load_from_json_to_dict, data_dir=base_dir)

        d = {
            'HEADER_DE_ARQUIVO': loader('HEADER_DE_ARQUIVO.json'),
            'HEADER_DE_LOTE': loader('HEADER_DE_LOTE.json'),
            'SEGMENTO_P': loader('SEGMENTO_P.json'),
            'SEGMENTO_Q': loader('SEGMENTO_Q.json'),
            'SEGMENTO_R': loader('SEGMENTO_R.json'),
            'TRAILER_DE_LOTE': loader('TRAILER_DE_LOTE.json'),
            'TRAILER_DE_ARQUIVO': loader('TRAILER_DE_ARQUIVO.json'),
            }

        return d

    def read_REM(self, path):
        """"
        TODO: check what is the correct encode, this is from legacy ISO-8859-1
        """
        with open(path, mode='r', encoding='ISO-8859-1') as file:
            text = file.read()
        return text

    def load_from_json_to_dict(self, file_name, data_dir):
        full_path = os.path.join(data_dir, file_name)

        with open(full_path, 'r', encoding='utf8') as json_file:
            data = json.load(json_file)
        return data

    def cnab_line_to_dict(self, cnab_line, remessa_dict):
        d = {}
        for key in remessa_dict:
            begin = int(remessa_dict[key][0]) - 1
            end = int(remessa_dict[key][1])

            d.update({key: cnab_line[begin:end]})

        return d


    def split_cnab(self, cnab):

        # https://stackoverflow.com/a/25250485
        lines = [line for line in iter(partial(io.StringIO(cnab).read, 241), '')]

        # lines must be multiples of 3
        assert len(lines[2:-2]) % 3 == 0, 'The segments is not multiple of 3'

        d = {
            'HEADER_DE_ARQUIVO': lines[0],
            'HEADER_DE_LOTE':  lines[1],
            'SEGMENTOS': lines[2:-2],
            'TRAILER_DE_LOTE': lines[-2],
            'TRAILER_DE_ARQUIVO': lines[-1],
            }

        return d

    def process_remessa(self, cnab):

        cnab_splited = self.split_cnab(cnab)
        HEADER_DE_ARQUIVO = self.cnab_line_to_dict(cnab_splited['HEADER_DE_ARQUIVO'],
                                        self.CNAB_FIELDS['HEADER_DE_ARQUIVO']
                                                   )

        HEADER_DE_LOTE = self.cnab_line_to_dict(cnab_splited['HEADER_DE_LOTE'],
                                        self.CNAB_FIELDS['HEADER_DE_LOTE']
                                                )

        TRAILER_DE_LOTE = self.cnab_line_to_dict(cnab_splited['TRAILER_DE_LOTE'],
                                        self.CNAB_FIELDS['TRAILER_DE_LOTE']
                                                 )

        TRAILER_DE_ARQUIVO = self.cnab_line_to_dict(cnab_splited['TRAILER_DE_ARQUIVO'],
                                        self.CNAB_FIELDS['TRAILER_DE_ARQUIVO']
                                                    )

        lines = cnab_splited['SEGMENTOS']
        SEGMENTOS = []
        for p, q, r in zip(lines[0::3], lines[1::3], lines[2::3]):

            a = self.cnab_line_to_dict(p, self.CNAB_FIELDS['SEGMENTO_P'])
            b = self.cnab_line_to_dict(q, self.CNAB_FIELDS['SEGMENTO_Q'])
            c = self.cnab_line_to_dict(r, self.CNAB_FIELDS['SEGMENTO_R'])
            SEGMENTOS.append({'P': a, 'Q': b, 'R': c})

        d = {'HEADER_DE_ARQUIVO': HEADER_DE_ARQUIVO,
             'HEADER_DE_LOTE': HEADER_DE_LOTE,
             'SEGMENTOS': SEGMENTOS,
             'TRAILER_DE_LOTE': TRAILER_DE_LOTE,
             'TRAILER_DE_ARQUIVO': TRAILER_DE_ARQUIVO,
             }
        return d

    def _build_sheet_lines(self, d):

        for t in d['SEGMENTOS']:
            P, Q, R = t['P'], t['Q'], t['R']

            cpf_or_cnpj = self._format_cpf_or_cnpj(Q['093q_numero_de_inscricao'])
            devedor = Q['103q_nome']
            cep = Q['133q_cep'] + Q['143q_sufixo_do_cep']
            valor = self._format_valor(P['213p_valor_nominal_do_titulo'])
            data = self._format_data(P['203p_data_de_vencimento_do_titulo'])

            self.SHEET_FIELDS['NUM_TITULO'].append('')
            self.SHEET_FIELDS['CPF_CNPJ'].append(cpf_or_cnpj)
            self.SHEET_FIELDS['DEVEDOR'].append(devedor)
            self.SHEET_FIELDS['CEP'].append(cep)
            self.SHEET_FIELDS['NUMERO'].append('')
            self.SHEET_FIELDS['COMPLEMENTO'].append('')
            self.SHEET_FIELDS['EMAIL'].append('')
            self.SHEET_FIELDS['FONE'].append('')
            self.SHEET_FIELDS['VALOR'].append(valor)
            self.SHEET_FIELDS['VENCIMENTO'].append(data)
            self.SHEET_FIELDS['LIMITE'].append('')
            self.SHEET_FIELDS['BASE'].append('')
            self.SHEET_FIELDS['DE'].append('')
            self.SHEET_FIELDS['MULTA'].append('')
            self.SHEET_FIELDS['JUROS'].append('')
            self.SHEET_FIELDS['DESCONTO'].append('')
            self.SHEET_FIELDS['DESCONTO_DATA'].append('')
            self.SHEET_FIELDS['INSTRUCOES'].append('')

        # number_of_lines = len(d['SEGMENTOS'])
        # for key in self.SHEET_FIELDS:
        #     if not self.SHEET_FIELDS[key]:
        #         self.SHEET_FIELDS[key].extend(['']*number_of_lines)

    def _format_valor(self, valor_nominal_do_titulo):
        """Formats a string representing a currency value and returns it with
         a period separating the cents part

        Note:
        Olhar o G070 da pág 44. É previsto ter até 13 digitos no formato:
        ############# (13 vezes o #)
        Após fomatar:
        ###########.##

        :return: str formated in the form ###########.##

        Exemplo:
        >>> _format_valor('123456')
        >>> 1234.56
        """
        centavos = valor_nominal_do_titulo[-2:]
        reais = valor_nominal_do_titulo[:-2]

        value = str(int(reais)) + '.' + centavos

        return value

    def _format_data(self, data: str):
        """

        :param data:
        :return: a data string formated in the form dd/mm/yyyy

        Exemplo:
        >>> _format_data('25022020')
        >>> '25/02/2020'
        """

        formated_date = data[:2] + '/' + data[2:4] + '/' + data[4:]

        return formated_date

    def _format_cpf_or_cnpj(self, cpf_or_cnpj):
        """If the string is a valid cnpj return it, if not try cut 4 digits
        and validate as cpf, if neither is possible, raise ValueError.

        :param cpf_or_cnpj: str
        :return: str or raise ValueError

        Note:
        Valid cnpj: 00000908882432
        Valid  cpf: 03634374446
        I have no ideia why use 15 digits, adding a zero, to save a number
        that has a standard size of 14 digits.

        Discussão interessante:
        https://www.guj.com.br/t/identificacao-cpf-ou-cnpj-com-mesma-quantidade-de-caracteres/324740/7
        """

        cpf_or_cnpj = cpf_or_cnpj[1:]
        if cpfcnpj.validate(cpf_or_cnpj):
            return cpf_or_cnpj
        elif cpfcnpj.validate(cpf_or_cnpj[3:]):
            return cpf_or_cnpj[3:]
        else:
            raise ValueError(f'The value {cpf_or_cnpj} is neither cpf or cnpj valid.')


    def _write_workbook(self, workbook_file_name):

        workbook = xlsxwriter.Workbook(workbook_file_name)
        worksheet = workbook.add_worksheet()

        bold = workbook.add_format({'bold': True})

        for i, column in enumerate(self.SHEET_FIELDS):
            worksheet.write(0, i, column, bold)

        # It is ugly, but it is from official docs
        # https://xlsxwriter.readthedocs.io/working_with_data.html
        col_num = 0
        for key, value in self.SHEET_FIELDS.items():
            worksheet.write(0, col_num, key)
            worksheet.write_column(1, col_num, value)
            col_num += 1

        workbook.close()

    def cnab_to_json(self, cnab_file_name, json_file_name):
        pass

    def json_to_cnab(self, json_file_name, cnab_file_name):
        pass

    def cnab_to_sheet(self, cnab_file_name, sheet_file_name):

        cnab = self.read_REM(cnab_file_name)
        dictionary = self.process_remessa(cnab)
        self._build_sheet_lines(dictionary)
        self._write_workbook(sheet_file_name)

    def sheet_to_cnab(self, sheet_file_name, cnab_file_name):
        pass


cnab_file_name = 'Faturas1202.REM'
cnab_file_name = 'Faturas2802.REM'

sheet_file_name = 'test123.xlsx'

my_cnab = CNAB240()

my_cnab.cnab_to_sheet(cnab_file_name, sheet_file_name)

# cnab_data = my_cnab.read_REM(path)
# cnab_lines = my_cnab.process_remessa(cnab_data)




