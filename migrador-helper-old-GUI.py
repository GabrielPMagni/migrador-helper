import argparse
import re as regex
from os import remove as rm, listdir as ls
from random import random
import codecs

def main():
    parser = argparse.ArgumentParser(prog='Migrador Helper', description='Funções para ajudar em migrações de banco de dados.')
    subs = parser.add_subparsers(help="commands", dest="command")
    de_arquivo = subs.add_parser(
        'from_file', prog='Converter de Arquivo',
    ).add_argument_group('')

    # Aba de Arquivos

    de_arquivo.add_argument(
        '-i',
        '--input_files',
        help='Arquivo a ser verificado:',
        nargs = '*',
    )



    de_arquivo.add_argument(
        '-o',
        '--output_file',
        help='Arquivo de saída:',
    )

    de_arquivo.add_argument(
        '--erros',
        help='Ignorar Erros',
        action='store_true'
    )

    de_arquivo.add_argument(
        '-cd',
        '--codificacao',
        help='Codificação do arquivo de origem:',
        choices=['cp1252', 'utf_8', 'latin-1'],
        default='utf_8'
    )

    de_arquivo.add_argument(
        '-de',
        '--delimitador',
        help='Delimitador do arquivo CSV | Padrão: ;',
    )
    
    de_arquivo.add_argument(
        '-df',
        '--delimitador_final',
        help='Novo delimitador do arquivo CSV | Padrão: ;',
    )

    args = parser.parse_args()

    try:
        if args.command == 'from_file':
            print('Iniciado processo...')
            cod = args.codificacao
            if args.delimitador != None:
                d = args.delimitador
            else:
                d = ';'
            if args.delimitador_final != None:
                df = args.delimitador_final
            else:
                df = ';'
            if not args.erros:
                erros = 'strict'
            else:
                erros = 'ignore'
            for index, arq in enumerate(args.input_files):
                print('Arquivo #', index)
                arquivo = codecs.open(arq, 'r', encoding=cod, errors=erros)
                ajustes = Ajustes(arquivo, args.output_file, args.erros, cod, d, df)
            else:
                print('Concluído')
    except Exception as identifier:
        print('Erro ao abrir o arquivo inicial: ', str(identifier))


class Ajustes:
    def __init__(self, arquivo_origem, arquivo_saida, opt=False, cod='utf_8', delimitador=';', delimitador2=';'):
        if not opt:
            self.erros = 'strict'
        else:
            self.erros = 'ignore'
        self.cod = cod
        self.delimitador = delimitador
        self.delimitador2 = delimitador2
        self.arquivo_saida = arquivo_saida
        self.arquivo_origem = arquivo_origem
        self.__nomeArquivoTemp2 = 'temp2.tmp'
        try:
            if (arquivo_origem):                
                self.__novoarquivo_temp2 = codecs.open(self.__nomeArquivoTemp2, 'w', encoding=self.cod, errors=self.erros)
                self.arquivo = arquivo_origem
            else:
                return None
        except Exception as identifier:
            print('Erro ao abrir o arquivo: ', str(identifier))
        else:
            try:
                self.formatarArquivo()
                self.tratarEExportarParaCSVcomVirgula()
                self.finalizar()
            except KeyboardInterrupt as identifier:
                print('Cancelado processo pelo usuário.')


    def tratarEExportarParaCSVcomVirgula(self):
        try:
            arqCSV = codecs.open(self.__nomeArquivoTemp2, 'r',  encoding=self.cod, errors=self.erros)
            arqCSVNovoNome = self.arquivo_saida
            arqCSVNovo = codecs.open(arqCSVNovoNome, 'w',  encoding=self.cod, errors=self.erros)
        except Exception as identifier:
            print('???', str(identifier))
        else:
            for linha in arqCSV:
                tmp = linha.replace(self.delimitador, self.delimitador2)
                arqCSVNovo.write(tmp)
                tmp = None


    def finalizar(self):
        rm('temp2.tmp')


    def formatarArquivo(self):
        self.__novo_arq_txt = self.arquivo.read()
        self.__novo_arq_txt = regex.sub(r'(Ã³)|(├Á)|(├\│)|(Ã´)|[óòõôö]', 'o', self.__novo_arq_txt)
        self.__novo_arq_txt = regex.sub(r'(Ã£)|(Ã¢)|(Ã¡)|(├ú)|(├í)|[áàãâ]', 'a', self.__novo_arq_txt)
        self.__novo_arq_txt = regex.sub(r'(├º)|(Ã§)|[ç]', 'c', self.__novo_arq_txt)
        self.__novo_arq_txt = regex.sub(r'(Ã‡)|[Ç]', 'C', self.__novo_arq_txt)
        self.__novo_arq_txt = regex.sub(r'(ÃŠ)|[ÚÙÛÜ]', 'U', self.__novo_arq_txt)
        self.__novo_arq_txt = regex.sub(r'(Ãº)|(├║)|[úùûü]', 'u', self.__novo_arq_txt)
        self.__novo_arq_txt = regex.sub(r'(├¡)|(Ã-)|[íìî]', 'i', self.__novo_arq_txt)
        self.__novo_arq_txt = regex.sub(r'[ÍÌÎ]', 'I', self.__novo_arq_txt)
        self.__novo_arq_txt = regex.sub(r'(Ã©)|(├¬)|(├®)|[éèê]', 'e', self.__novo_arq_txt)
        self.__novo_arq_txt = regex.sub(r'(Ã‰)|[ÉÈÊ]', 'E', self.__novo_arq_txt)
        self.__novo_arq_txt = regex.sub(r'(Ã•)|(Ã“)|(Ã”)|[ÓÒÕÔÖ]', 'O', self.__novo_arq_txt)
        self.__novo_arq_txt = regex.sub(r'(Âº)|[´`ºª]', '.', self.__novo_arq_txt)
        self.__novo_arq_txt = regex.sub(r'(Ãƒ)|[ÁÃÂÀÅ]', 'A', self.__novo_arq_txt)
        self.__novo_arq_txt = regex.sub(r'(&)([AEIOUCaeiouc])(.+;)', r'\2', self.__novo_arq_txt)
        self.__novo_arq_txt = regex.sub(r'(Ã)|[^0-9a-zA-Z\s\/\.\,\;\"\$\<\>\&\*\(\)\[\]\{\}\=\+\-\#\_\%\!\?\@]|[½⅓⅔¼¾⅕⅖⅗⅘⅙⅚⅐⅛⅜⅝⅞⅑⅒↉⅟ ]', '', self.__novo_arq_txt)
        self.__novoarquivo_temp2.write(self.__novo_arq_txt)
        self.arquivo.close()
        self.__novoarquivo_temp2.close()
        self.__novo_arq_txt = None
        del self.__novo_arq_txt

if __name__ == '__main__':
    main()



