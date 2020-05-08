import io
import json
import os

from functools import partial

import xlsxwriter

from pycpfcnpj import cpfcnpj


class CNAB240:
    """

    """

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

    CNAB_HEADERS_FOOTERS = ['HEADER_DE_ARQUIVO', 'HEADER_DE_LOTE',
                            'TRAILER_DE_LOTE', 'TRAILER_DE_ARQUIVO']

    CNAB_SEGMENTS = ['SEGMENTO_P', 'SEGMENTO_Q', 'SEGMENTO_R']

    CNAB_PARTS_FULL = CNAB_HEADERS_FOOTERS + CNAB_SEGMENTS

    CNAB_PARTS_SEGMENTS = CNAB_HEADERS_FOOTERS + ['SEGMENTOS']

    def __init__(self):

        self.CNAB_FIELDS = self.load_cnab_fiels()

    def load_cnab_fiels(self, jsons_diretory=('data', 'jsons')):
        """

        :param jsons_diretory:
        :return: a dict
        """
        base_diretory = os.path.join(os.path.dirname(__file__), *jsons_diretory)

        # uses partial to "freeze" one argument to short function call
        loader = partial(self.load_from_json_to_dict, base_diretory)

        d = {file_name.split('.')[0]: loader(file_name)
             for file_name in os.listdir(base_diretory)}

        return d

    def read_REM(self, path):
        """"
        TODO: check what is the correct encode, this is from legacy ISO-8859-1
        """
        with open(path, mode='r', encoding='ISO-8859-1') as file:
            text = file.read()
        return text

    def dump_dict_to_json(self, dictionary, file_name):
        with open(file_name, 'w', encoding='utf8') as json_file:
            json.dump(dictionary, json_file, sort_keys=True, indent=4)

    def load_from_json_to_dict(self, data_dir, file_name):
        """

        :param data_dir: diretory where the .json files are
        :param file_name: file name with extension
        :return: a dictionary from the json file

        Note: the order of arguments should not be changed because
        of the use of parcial from functools.
        https://stackoverflow.com/a/7811270
        """
        full_path_file_name = os.path.join(data_dir, file_name)

        with open(full_path_file_name, 'r', encoding='utf8') as json_file:
            data = json.load(json_file)
        return data

    def cnab_line_to_dict(self, cnab_line, remessa_dict):
        d = {}
        for key in remessa_dict:
            begin = int(remessa_dict[key][0]) - 1
            end = int(remessa_dict[key][1])

            d.update({key: cnab_line[begin:end]})

        return d


    def split_cnab(self, cnab: str):
        """Given a cnab in string format, split it in 241 length lines

        :param cnab: str
        :return: dict
        """

        # https://stackoverflow.com/a/25250485
        lines = [line for line in iter(partial(io.StringIO(cnab).read, 241), '')]

        # lines must be multiples of 3
        assert len(lines[2:-2]) % 3 == 0, 'The segments is not multiple of 3'

        # Note: this code relies in the ordering of self.CNAB_PARTS_SEGMENTS
        parts = [lines[0],  lines[1], lines[-2], lines[-1], lines[2:-2]]

        d = {key: parts for key, part in zip(self.CNAB_PARTS_SEGMENTS, parts)}

        return d

    def process_remessa(self, cnab: str):
        """
        TODO: change name remessa
        serialize the cnab string to dictionary

        :param cnab:
        :return:
        """
        cnab_splited = self.split_cnab(cnab)

        d = {}
        for key in self.CNAB_HEADERS_FOOTERS:
            value = self.cnab_line_to_dict(cnab_splited[key],
                                           self.CNAB_FIELDS[key])
            d.update({key: value})

        # TODO: find a better way to do this
        lines = cnab_splited['SEGMENTOS']
        SEGMENTOS = []
        for p, q, r in zip(lines[0::3], lines[1::3], lines[2::3]):

            a = self.cnab_line_to_dict(p, self.CNAB_FIELDS['SEGMENTO_P'])
            b = self.cnab_line_to_dict(q, self.CNAB_FIELDS['SEGMENTO_Q'])
            c = self.cnab_line_to_dict(r, self.CNAB_FIELDS['SEGMENTO_R'])
            SEGMENTOS.append({'P': a, 'Q': b, 'R': c})

        d.update({'SEGMENTOS': SEGMENTOS})

        return d

    def _build_sheet_lines(self, d):
        """Sets SHEET_FIELDS values from the "segmentos" P, Q and R that came
        from a CNABs_retorno and are in the dict d

        :param d: is a dict which has all "pieces" of a CNABs_retorno
        :return: None
        """

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

    def clean_sheet_lines(self):
        for key in self.SHEET_FIELDS:
            self.SHEET_FIELDS[key] = []

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
        cnab = self.read_REM(cnab_file_name)
        dictionary = self.process_remessa(cnab)
        self.dump_dict_to_json(dictionary, json_file_name)

    def json_to_cnab(self, json_file_name, cnab_file_name):
        pass

    def cnab_to_sheet(self, cnab_file_name, sheet_file_name):

        cnab = self.read_REM(cnab_file_name)
        dictionary = self.process_remessa(cnab)
        self._build_sheet_lines(dictionary)
        self._write_workbook(sheet_file_name)

        self.clean_sheet_lines()

    def sheet_to_cnab(self, sheet_file_name, cnab_file_name):
        pass