"""
prontuario - Copia.csv
temp2.tmpnovo.csv
"""

import re as regex
import codecs

encoding = 'utf-8'
# reg = r'((\s){1,}(\d{1,},))'
reg = r'((.*\,\w{1,}(( )?(\w{1,})?){0,3}\n)(\d{1,}\,))'
def arquivoInicial():
    """
    Solicita o nome do arquivo a ser verificado e retorna o mesmo ou falso em caso em caso de erro.
    """
    pergunta = input('Digite o nome do arquivo a ser verificado: \n\n\t>')
    try:
        arquivo = codecs.open(pergunta, 'r', encoding=encoding)
    except Exception as identifier:
        print('Erro ao abrir o arquivo inicial: ', str(identifier))
        return False
    else:
        return arquivo

arquivo = arquivoInicial()
arquivo2 = codecs.open('tmp_retirar_quebras.csv', 'w',encoding=encoding)
tmp3 = ''
tmp4 = ''
tmp5 = ''

linha = arquivo.read()
if regex.search(reg, linha) != None:
    tmp1 = regex.sub(reg, r'\g<2>|\g<6>', linha)
    linha = None
    tmp5 = regex.sub(r'\n|\r', '', tmp1)
    tmp1 = None
arquivo2.write(tmp5)
tmp5 = None

arquivo.close()
arquivo2.close()
arquivo2 = codecs.open('tmp_retirar_quebras.csv', 'r',
                       encoding=encoding)
arquivo3 = codecs.open('res_retirar_quebras.csv', 'w',
                       encoding=encoding)
tmp = arquivo2.read()
posicao = 0
tmp2 = tmp.replace('|', '\n')
arquivo3.write(tmp2)
