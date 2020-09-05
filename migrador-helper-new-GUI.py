from gooey import Gooey, GooeyParser
import re as regex
from os import remove as rm, listdir as ls
from random import random
import codecs

@Gooey(
    program_name = 'Migrador Helper',
    program_description = 'Multi funções para ajudar em migrações de banco de dados.',
    language = 'portuguese',
    default_size=(610, 580),
    navigation='TABBED',
    menu=[{'name': 'Sobre', 'items': [{'type': 'AboutDialog', 'name': 'Sobre o Migrador Helper', 'menuTitle': 'Sobre', 'description': 'Na tentativa de facilitar a vida das migrações de banco de dados', 'version': '0.5',  'developer': 'Gabriel Peres Magni','website': 'https://github.com/GabrielPMagni'}]}]
)
def main():
    parser = GooeyParser()
    subs = parser.add_subparsers(help="commands", dest="command")
    de_diretorio = subs.add_parser(
        'convert_dir', prog='Converter de Diretório',
    ).add_argument_group('')

    de_arquivo = subs.add_parser(
        'convert_arq', prog='Converter de Arquivo',
    ).add_argument_group('')

    # Aba de Arquivos

    de_arquivo.add_argument(
        'input_files',
        metavar='Arquivo a ser verificado:',
        widget="MultiFileChooser",
        nargs = '*',
        gooey_options=dict(wildcard="(*.dat, *.csv, *.txt)|*.dat; *.csv; *.txt", full_width=True)
    )



    de_arquivo.add_argument(
        'output_file',
        widget="FileSaver",
        metavar='Arquivo de saída:',
        gooey_options=dict(wildcard="(*.csv, *.txt)|*.csv; *.txt", default_file='sem_nome'+str(random())+'.csv', full_width=True)
    )

    de_arquivo.add_argument(
        '--csv',
        metavar='Exportar para CSV',
        action='store_true'
    )

    # Aba de Diretórios


    de_diretorio.add_argument(
        'dir',
        metavar='Pasta a ser verificada',
        widget="DirChooser",
        gooey_options=dict(full_width=True)
    )


    de_diretorio.add_argument(
        'output_file',
        widget="FileSaver",
        metavar='Arquivo de saída:',
        gooey_options=dict(wildcard="(*.csv, *.txt)|*.csv; *.txt", default_file='sem_nome'+str(random())+'.csv', full_width=True)
    )
    
    de_diretorio.add_argument(
        '--csv',
        metavar='Exportar para CSV',
        action='store_true'
    )


    args = parser.parse_args()

    # try:
    if args.command == 'convert_arq':
        for arq in args.input_files:
            arquivo = codecs.open(arq, 'r', encoding='cp1252', errors='ignore')
            mOrto = ajustaOrto8DAT
            mOrto(arquivo, args.output_file, args.csv)
    elif args.command == 'convert_dir':
        for arq in ls(args.dir):
            caminho = args.dir+'\\'+arq
            arquivo = codecs.open(caminho, 'r', encoding='cp1252', errors='ignore')
            mOrto = ajustaOrto8DAT
            mOrto(arquivo, args.output_file, args.csv)
    # except Exception as identifier:
    #     print('Erro ao abrir o arquivo inicial: ', str(identifier))




class ajustaOrto8DAT:
    def __init__(self, arquivoOrigem, arquivo_saida, opt=False):
        """
        Gera um arquivo .txt formatado a partir de um arquivo .DAT do OrtoManager.\n
        arquivoOrigem: Arquivo de texto plano.
        """
        self.__nomeArquivoTemp2 = 'temp2.tmp'
        self.__nomeTempFinal = 'temp_final.tmp'
        self.arquivo_saida = arquivo_saida
        try:
            if (arquivoOrigem):                
                self.__novoarquivo_temp2 = codecs.open(self.__nomeArquivoTemp2, 'w', encoding='cp1252', errors='ignore')
                self.arquivo = arquivoOrigem
            else:
                return None
        except Exception as identifier:
            print('Erro ao abrir o arquivo: ', str(identifier))
        else:
            try:
                self.formatarArquivo()
                self.__finalizar()                 
            except KeyboardInterrupt as identifier:
                print('Cancelado processo pelo usuário.')


    def tratarEExportarParaCSVcomVirgula(self):
        try:
            arqCSV = codecs.open(self.arquivo_saida, 'r',  encoding='cp1252', errors='ignore')
            arqCSVNovoNome = arqCSV.name+'novo.csv'
            arqCSVNovo = codecs.open(arqCSVNovoNome, 'a',  encoding='cp1252', errors='ignore')
        except Exception as identifier:
            print('???', str(identifier))
        else:
            # delimitador = input('Digite o delimitador do arquivo a ser exportado (padrão=;): \n\n\t>')
            if delimitador == '\\t':
                delimitador = '\t'
            elif delimitador == '\\n':
                delimitador = '\n'
            elif delimitador == '':
                delimitador = ';'
            for linha in arqCSV:
                tmp = linha.replace(delimitador, ',')
                arqCSVNovo.write(tmp)
                tmp = None


    def __finalizar(self):
        self.__nomeArquivoFinal = self.arquivo_saida
        try:
            self.__arquivoFinal = codecs.open(self.__nomeArquivoFinal, 'a', encoding='cp1252', errors='ignore')
            self.__novoarquivo_temp = codecs.open(self.__nomeArquivoTemp2, 'r', encoding='cp1252', errors='ignore')
        except Exception as identifier:
            print('Erro ao finalizar: ', str(identifier))
        else:
            temp = ''
            nome = self.arquivo.name
            nome = nome.split('\\')[-1]
            for num_linha, linha in enumerate(self.__novoarquivo_temp):
                if regex.match('^(TOTAL)|^(total)', linha.strip()) != None or regex.match('^(\d\d\/\d\d\/\d\d)', linha.strip()) != None:
                    if num_linha == 1 or num_linha % 2 == 0:
                        self.__arquivoFinal.write('\n'+nome+';'+linha.replace('\n', '<br><br>'))
                    else:
                        self.__arquivoFinal.write(linha.replace('\n', '<br><br>'))


              
              
              
              
                # if regex.match('[\(\)\^\/]', linha) != None:
                #     if regex.match('(\(\d\d\))', linha) != None or regex.match('(\d\d\/\d\d\/\d\d)', linha) != None:
                #         # self.__arquivoFinal.write(linha.replace('\n', '<br><br>'))
                #         self.__arquivoFinal.write(linha+'<br><br>')

                #     else:
                #         continue
                # else:
                #     # self.__arquivoFinal.write(linha.replace('\n', '<br><br>'))
                #     self.__arquivoFinal.write(linha+'<br><br>')



        
            # self.__listaNomes = []
            # for self.__index, self.__linha in enumerate(self.__novoarquivo_temp):
            #     if self.__linha not in self.__listaNomes:
            #         self.__listaNomes.append(self.__linha)
            #         self.__arquivoFinal.write(self.__linha + '\n')
                    # if self.__index > 20:
                    #     break            
                

    def __temp_final(self):
        self.__novoarquivo_temp2 = codecs.open(self.__nomeArquivoTemp2, 'r', encoding='cp1252', errors='ignore')
        self.__novoarquivo_temp = codecs.open(self.__nomeTempFinal, 'w', encoding='cp1252', errors='ignore')
        self.__conjuntoAnterior = ''
        for self.__linha_counter, self.__linha in enumerate(self.__novoarquivo_temp2):
            for self.__conjunto in self.__linha.split('\t'):
                if self.__conjuntoAnterior == '':
                    self.__conjuntoAnterior = self.__conjunto
                self.__palavra = self.__conjunto.split()
                self.__palavraAnterior = self.__conjuntoAnterior.split()
                self.__conjuntoAnterior = self.__conjunto
                if (self.__palavra and self.__palavraAnterior):
                    if self.__palavra[0] == self.__palavraAnterior[-1]:
                        if self.__palavraAnterior[0].isdigit():
                            self.__palavraAnterior.remove(self.__palavraAnterior[0])
                        self.__achado = ' '.join(self.__palavraAnterior)
                        regex.sub('^(_)|^(\s)|^(\d)', '', self.__achado)
                        expRgl = regex.match('(([a-z])([A-Z]))|(([A-Z])([A-Z]))|([\W])', self.__achado)
                        if expRgl != None:
                            x = expRgl.lastindex
                            self.__achado = self.__achado.replace(self.__achado[:x], '')
                        self.__local = self.__linha.find(self.__achado)
                        self.__paraLista = []
                        self.__paraLista[:0] = self.__linha
                        self.__paraLista.insert(self.__local, '\n')
                        self.__novalinha = ''.join(self.__paraLista)
                        self.__novoarquivo_temp.write(self.__novalinha)
        else:
            # limpar memória e salvar
            self.__achado = None
            self.__linha = None
            del self.__linha
            del self.__achado
            self.__novoarquivo_temp2.close()
            self.__novoarquivo_temp.close()
            rm(self.__nomeArquivoTemp2)


    def formatarArquivo(self):
        # if not self.arquivo.name.lower().endswith('.csv'):
        #     self.__novo_arq_txt = regex.sub('\s{2,}[^\\n\w]', '  ', self.arquivo.read())
        # else:
        self.__novo_arq_txt = self.arquivo.read()
        self.__novo_arq_txt = regex.sub('[,ºª]', '.', self.__novo_arq_txt)
        self.__novo_arq_txt = regex.sub('[ÚÙÛ]', 'U', self.__novo_arq_txt)
        self.__novo_arq_txt = regex.sub('[úùû]', 'u', self.__novo_arq_txt)
        self.__novo_arq_txt = regex.sub('[íìî¡]', 'i', self.__novo_arq_txt)
        self.__novo_arq_txt = regex.sub('[ÍÌÎ]', 'I', self.__novo_arq_txt)
        self.__novo_arq_txt = regex.sub('[éèê]', 'e', self.__novo_arq_txt)
        self.__novo_arq_txt = regex.sub('[ÉÈÊ]', 'E', self.__novo_arq_txt)
        self.__novo_arq_txt = regex.sub('[ÓÒÕÔ]', 'O', self.__novo_arq_txt)
        self.__novo_arq_txt = regex.sub('[óòõô]', 'o', self.__novo_arq_txt)
        self.__novo_arq_txt = regex.sub('[áàãâ]', 'a', self.__novo_arq_txt)
        self.__novo_arq_txt = regex.sub('[ÁÃÂÀÅ]', 'A', self.__novo_arq_txt)
        self.__novo_arq_txt = regex.sub('[ç]', 'c', self.__novo_arq_txt)
        self.__novo_arq_txt = regex.sub('[Ç]', 'C', self.__novo_arq_txt)
        if not self.arquivo.name.lower().endswith('.csv'):
            self.__novo_arq_txt = regex.sub('([^.\-(<br><br>)(R$)+\d/\w\s])|([Þÿ½ÄåÖëß´`Ü])|(Óÿ)', '', self.__novo_arq_txt)
        self.__novoarquivo_temp2.write(self.__novo_arq_txt)
        self.arquivo.close()
        self.__novoarquivo_temp2.close()
        self.__novo_arq_txt = None
        del self.__novo_arq_txt



if __name__ == '__main__':
    main()


# ainda sem funcionamento

