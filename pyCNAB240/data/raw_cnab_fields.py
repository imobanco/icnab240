"""
Link para o LAYOUT FEBRABAN 240 POSIÇÕES COBRANÇA:

https://cms.santander.com.br/sites/WPS/documentos/arq-layout-de-arquivos-2/17-10-26_172236_149-382-cobranca+layout+cnab+240+febraban+puro+versao+setembro+2017.pdf

"""


# Pág. 6
HEADER_DE_ARQUIVO = """01.0 Código do Banco na Compensação 1 3
02.0 Lote de Serviço 4 7
03.0 Tipo de Registro 8 8
04.0 Uso Exclusivo FEBRABAN / CNABs_retorno 9 17
05.0 Tipo de Inscrição da Empresa 18 18
06.0 Número de Inscrição da Empresa 19 32
07.0 Código do Convênio no Banco 33 52
08.0 Agência Mantenedora da Conta 53 57
09.0 Dígito Verificador da Agência 58 58
10.0 Número da Conta Corrente 59 70
11.0 Dígito Verificador da Conta 71 71
12.0 Dígito Verificador da Ag/Conta 72 72
13.0 Nome da Empresa 73 102
14.0 Nome do Banco 103 132
15.0 Uso Exclusivo FEBRABAN / CNABs_retorno 133 142
16.0 Código Remessa / Retorno 143 143
17.0 Data de Geração do Arquivo 144 151
18.0 Hora de Geração do Arquivo 152 157
19.0 Número Seqüencial do Arquivo 158 163
20.0 Nº da Versão do Layout do Arquivo 164 166
21.0 Densidade de Gravação do Arquivo 167 171
22.0 Para Uso Reservado do Banco 172 191
23.0 Para Uso Reservado da Empresa 192 211
24.0 Uso Exclusivo FEBRABAN / CNABs_retorno 212 240"""


# Pág. 7
HEADER_DE_LOTE = """01.1 Código do Banco na Compensação 1 3
02.1 Lote de Serviço 4 7
03.1 Tipo de Registro 8 8
04.1 Uso Exclusivo FEBRABAN / CNABs_retorno 9 17
05.1 Tipo de Inscrição da Empresa 18 18
06.1 Número de Inscrição da Empresa 19 32
07.1 Código do Convênio no Banco 33 52
08.1 Agência Mantenedora da Conta 53 57
09.1 Dígito Verificador da Agência 58 58
10.1 Número da Conta Corrente 59 70
11.1 Dígito Verificador da Conta 71 71
12.1 Dígito Verificador da Ag/Conta 72 72
13.1 Nome da Empresa 73 102
14.1 Nome do Banco 103 132
15.1 Uso Exclusivo FEBRABAN / CNABs_retorno 133 142 
16.1 Código Remessa / Retorno 143 143
17.1 Data de Geração do Arquivo 144 151
18.1 Hora de Geração do Arquivo 152 157
19.1 Número Seqüencial do Arquivo 158 163
20.1 Nº da Versão do Layout do Arquivo 164 166 
21.1 Densidade de Gravação do Arquivo 167 171
22.1 Para Uso Reservado do Banco 172 191 
23.1 Para Uso Reservado da Empresa 192 211
24.1 Uso Exclusivo FEBRABAN / CNABs_retorno 212 240"""


# Pág. 8
SEGMENTO_P = """01.3P Código do Banco na Compensação 1 3
02.3P Lote de Serviço 4 7
03.3P Tipo de Registro 8 8
04.3P Nº Sequencial do Registro no Lote 9 13
05.3P Cód. Segmento do Registro Detalhe 14 14
06.3P 06 3P Uso Exclusivo FEBRABAN/CNABs_retorno 15 15
07.3P Código de Movimento Remessa 16 17
08.3P Agência Mantenedora da Conta 18 22
09.3P C/C Dígito Verificador da Agência 23 23
10.3P Número da Conta Corrente 24 35
11.3P Dígito Verificador da Conta 36 36
12.3P Dígito Verificador da Ag/Conta 37 37
13.3P Identificação do Título no Banco 38 57
14.3P Código da Carteira 58 58
15.3P Forma de Cadastr. do Título no Banco 59 59
16.3P Tipo de Documento 60 60
17.3P Identificação da Emissão do Bloqueto 61 61
18.3P Identificação da Distribuição 62 62
19.3P Número do Documento de Cobrança 63 77
20.3P Data de Vencimento do Título 78 85
21.3P Valor Nominal do Título 86 100
22.3P Agência Encarregada da Cobrança 101 105
23.3P Dígito Verificador da Agência 106 106
24.3P Espécie do Título 107 108
25.3P Identific. De Título 109 109
26.3P Data da Emissão do Título 110 117
27.3P Código do Juros de Mora 118 118
28.3P Data do Juros de Mora 119 126
29.3P Juros de Mora por Dia/Taxa 127 141
30.3P Código do Desconto 1 142 142
31.3P Data do Desconto 1 143 150
32.3P Valor/Percentual a ser Concedido 151 165
33.3P Valor do IOF a ser Recolhido 166 180
34.3P Valor do Abatimento 181 195
35.3P Identificação do Título na Empresa 196 220
36.3P Código para Protesto 221 221
37.3P Número de Dias para Protesto 222 223
38.3P Código para Baixa/Devolução 224 224
39.3P Número de Dias para Baixa/Devolução 225 227
40.3P Código da Moeda 228 229
41.3P Nº do Contrato da Operação de Créd. 230 239
42.3P Uso Exclusivo FEBRABAN/CNABs_retorno 240 240"""


# Pág. 9
SEGMENTO_Q = """01.3Q Código do Banco na Compensação 1 3
02.3Q Lote de Serviço 4 7
03.3Q Tipo de Registro 8 8
04.3Q Nº Sequencial do Registro no Lote 9 13
05.3Q Cód. Segmento do Registro Detalhe 14 14
06.3Q Uso Exclusivo FEBRABAN/CNABs_retorno 15 15
07.3Q Código de Movimento Remessa 16 17
08.3Q Tipo de Inscrição 18 18
09.3Q Número de Inscrição 19 33
10.3Q Nome 34 73
11.3Q Endereço 74 113
12.3Q Bairro 114 128
13.3Q CEP 129 133
14.3Q Sufixo do CEP 134 136
15.3Q Cidade 137 151
16.3Q Unidade da Federação 152 153
17.3Q Tipo de Inscrição 154 154
18.3Q Número de Inscrição 155 169
19.3Q Nome do Sacador/Avalista 170 209
20.3Q Cód. Bco. Corresp. na Compensação 210 212
21.3Q Nosso Nº no Banco Correspondente 213 232
22.3Q Uso Exclusivo FEBRABAN/CNABs_retorno 233 240"""


# Pág. 10
SEGMENTO_R = """01.3R Código do Banco na Compensação 1 3
02.3R Lote de Serviço 4 7
03.3R Tipo de Registro 8 8
04.3R Nº Sequencial do Registro no Lote 9 13
05.3R Cód. Segmento do Registro Detalhe 14 14
06.3R Uso Exclusivo FEBRABAN/CNABs_retorno 15 15
07.3R Código de Movimento Remessa 16 17
08.3R Código do Desconto 2 18 18
09.3R Data do Desconto 2 19 26
10.3R Valor/Percentual a ser Concedido 27 41 
11.3R Código do Desconto 3 42 42
12.3R Data do Desconto 3 43 50
13.3R Valor/Percentual a Ser Concedido 51 65
14.3R Código da Multa 66 66 
15.3R Data da Multa 67 74
16.3R Valor/Percentual a Ser Aplicado 75 89
17.3R Informação ao Pagador 90 99
18.3R Mensagem 3 100 139
19.3R Mensagem 4 140 179
20.3R Uso Exclusivo FEBRABAN/CNABs_retorno 180 199
21.3R Cód. Ocor. do Pagador 200 207
22.3R Cód. do Banco na Conta do Débito 208 210
23.3R Código da Agência do Débito 211 215
24.3R Dígito Verificador da Agência 216 216
25.3R Conta Corrente para Débito 217 228
26.3R Dígito Verificador da Conta 229 229
27.3R Dígito Verificador Ag/Conta 230 230
28.3R Aviso para Débito Automático 231 231
29.3R Uso Exclusivo FEBRABAN/CNABs_retorno 232 240"""


# Note: dosTítulos estava errado (junto) em três lugares
TRAILER_DE_LOTE = """01.5 Código do Banco na Compensação 1 3
02.5 Lote de Serviço 4 7
03.5 Tipo de Registro 8 8
04.5 Uso Exclusivo FEBRABAN/CNABs_retorno 9 17
05.5 Quantidade de Registros no Lote 18 23
06.5 Quantidade de Títulos em Cobrança 24 29
07.5 Valor Total dos Títulos em Carteiras 30 46
08.5 Quantidade de Títulos em Cobrança 47 52
09.5 Valor Total dos Títulos em Carteiras 53 69
10.5 Quantidade de Títulos em Cobrança 70 75
11.5 Quantidade de Títulos em Carteiras 76 92
12.5 Quantidade de Títulos em Cobrança 93 98
13.5 Valor Total dos Títulos em Carteiras 99 115
14.5 Número do Aviso de Lançamento 116 123
15.5 Uso Exclusivo FEBRABAN/CNABs_retorno 124 240"""


TRAILER_DE_ARQUIVO = """01.9 Código do Banco na Compensação 1 3
02.9 Lote de Serviço 4 7
03.9 Tipo de Registro 8 8
04.9 Uso Exclusivo FEBRABAN/CNABs_retorno 9 17
05.9 Quantidade de Lotes do Arquivo 18 23
06.9 Quantidade de Registros do Arquivo 24 29
07.9 Qtde de Contas p/ Conc. (Lotes) 30 35
08.9 Uso Exclusivo FEBRABAN/CNABs_retorno 36 240"""
