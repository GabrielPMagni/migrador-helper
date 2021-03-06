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

    de_arquivo.add_argument(
        '-cd',
        '--codificacao',
        metavar='Codificação do arquivo de origem:',
        choices=['cp1252', 'utf_8'],
        default='utf_8'
    )

    de_arquivo.add_argument(
        '-de',
        '--delimitador',
        metavar='Delimitador do arquivo CSV',
        help='Padrão: ;'
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

    de_diretorio.add_argument(
        '-cd',
        '--codificacao',
        metavar='Codificação do arquivo de origem:',
        choices=['cp1252', 'utf_8'],
        default='utf_8'
    )

    de_diretorio.add_argument(
        '-de',
        '--delimitador',
        metavar='Delimitador do arquivo CSV',
        help='Padrão: ;'
    )


    args = parser.parse_args()

    try:
        if args.command == 'convert_arq':
            print('Iniciado processo...')
            for index, arq in enumerate(args.input_files):
                print('Arquivo #', index)
                cod = args.codificacao
                if args.delimitador != None:
                    d = args.delimitador
                else:
                    d = ';'
                arquivo = codecs.open(arq, 'r', encoding=cod, errors='ignore')
                mOrto = ajustaOrto8DAT
                mOrto(arquivo, args.output_file, args.csv, cod, d)
            else:
                print('Concluído')
        elif args.command == 'convert_dir':
            print('Iniciado processo...')
            for index, arq in enumerate(ls(args.dir)):
                print('Arquivo #', index)
                cod = args.codificacao
                if args.delimitador != None:
                    d = args.delimitador
                else:
                    d = ';'                
                caminho = args.dir+'\\'+arq
                arquivo = codecs.open(caminho, 'r', encoding=cod, errors='ignore')
                mOrto = ajustaOrto8DAT
                mOrto(arquivo, args.output_file, args.csv, cod, d)
            else:
                print('Concluído')
    except Exception as identifier:
        print('Erro ao abrir o arquivo inicial: ', str(identifier))




class ajustaOrto8DAT:
    def __init__(self, arquivoOrigem, arquivo_saida, opt=False, cod='utf_8', delimitador=';'):
        """
        Gera um arquivo .txt formatado a partir de um arquivo .DAT do OrtoManager.\n
        arquivoOrigem: Arquivo de texto plano.
        """
        self.__nomeArquivoTemp2 = 'temp2.tmp'
        self.__nomeTempFinal = 'temp_final.tmp'
        self.arquivo_saida = arquivo_saida
        self.codificacao = cod
        self.d = delimitador
        try:
            if (arquivoOrigem):                
                self.__novoarquivo_temp2 = codecs.open(self.__nomeArquivoTemp2, 'w', encoding=self.codificacao, errors='ignore')
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



    def __finalizar(self):
        self.__nomeArquivoFinal = self.arquivo_saida
        try:
            self.__arquivoFinal = codecs.open(self.__nomeArquivoFinal, 'a', encoding=self.codificacao, errors='ignore')
            self.__novoarquivo_temp = codecs.open(self.__nomeArquivoTemp2, 'r', encoding=self.codificacao, errors='ignore')
        except Exception as identifier:
            print('Erro ao finalizar: ', str(identifier))
        else:
            temp = ''
            nome = self.arquivo.name
            nome = nome.split('\\')[-1]
            nome_id = nome.split('.')[-2]
            nome_id = regex.search('(\d+)', nome_id).group(0)

            for num_linha, linha in enumerate(self.__novoarquivo_temp):
                if regex.match('^(\d\d\/\d\d\/\d\d\d\d)', linha.strip()) != None:
                    data = regex.match('(\d\d)\/(\d\d)\/\d\d(\d\d)', linha.strip())
                    data1 = data.group(1)+'/'+data.group(2)+'/'+data.group(3)
                    self.__arquivoFinal.write('\n'+nome_id+self.d+data1+self.d+linha.replace('\n', '<br><br>')[0:30000])
                elif regex.match('^(\d\d\/\d\d\/\d\d)', linha.strip()) != None:
                    data = regex.match('^(\d\d\/\d\d\/\d\d)', linha.strip())
                    self.__arquivoFinal.write('\n'+nome_id+self.d+data.group(0)+self.d+linha.replace('\n', '<br><br>')[0:30000])



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
            self.__novo_arq_txt = regex.sub('([^.\-(<br><br>)(R$)+\d/\w\s])|([Þÿ½ÄåÖëß´`Ü±\"¤])|(Óÿ)', '', self.__novo_arq_txt)
        self.__novoarquivo_temp2.write(self.__novo_arq_txt)
        self.arquivo.close()
        self.__novoarquivo_temp2.close()
        self.__novo_arq_txt = None
        del self.__novo_arq_txt



if __name__ == '__main__':
    main()


# ainda sem funcionamento

