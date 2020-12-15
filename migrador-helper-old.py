import re as regex
from os import remove as rm
from random import random
import codecs
# utf-8
# cp1252 
# latin-1
encoding = 'cp1252'
delimitador2 = ','

def arquivoInicial():
    """
    Solicita o nome do arquivo a ser verificado e retorna o mesmo ou falso em caso em caso de erro.
    """
    pergunta = input('Digite o nome do arquivo a ser verificado: \n\n\t>')
    try:
        arquivo = codecs.open(pergunta, 'r', encoding=encoding, errors='ignore')
        oqfzr = int(input('O que deseja fazer?\n1-Exportar CSV com um delimitador para CSV delimitar com vírgula'))


    except Exception as identifier:
        print('Erro ao abrir o arquivo inicial: ', str(identifier))
        return False
    else:
        return arquivo, oqfzr



class ajustaOrto8DAT:
    def __init__(self, arquivoOrigem, oqfzr):
        """
        Gera um arquivo .txt formatado a partir de um arquivo .DAT do OrtoManager.\n
        arquivoOrigem: Arquivo de texto plano.
        """
        self.__nomeArquivoTemp2 = 'temp2.tmp'
        self.__nomeTempFinal = 'temp_final.tmp'
        try:
            if (arquivoOrigem):                
                self.__novoarquivo_temp2 = codecs.open(self.__nomeArquivoTemp2, 'w', encoding=encoding, errors='ignore')
                self.arquivo = arquivoOrigem
            else:
                return None
        except Exception as identifier:
            print('Erro ao abrir o arquivo: ', str(identifier))
        else:
            try:
                if oqfzr == 1:
                    print('Iniciado...')
                    self.formatarArquivo()
                    print('25% concluído...')
                    self.tratarEExportarParaCSVcomVirgula()
                    print('Concluído!')
                else:
                    print('Nope')
                    exit(2)
                # print('Iniciado...')
                # self.formatarArquivo()
                # print('25% concluído...')
                # self.__temp_final()
                # print('65% concluído...')
                # self.__finalizar()
                # print('Concluído!')
            except KeyboardInterrupt as identifier:
                print('Cancelado processo pelo usuário.')


    def tratarEExportarParaCSVcomVirgula(self):
        try:
            arqCSV = codecs.open(self.__nomeArquivoTemp2, 'r',  encoding=encoding, errors='ignore')
            arqCSVNovoNome = arqCSV.name+'novo.csv'
            arqCSVNovo = codecs.open(arqCSVNovoNome, 'w',  encoding=encoding, errors='ignore')
        except Exception as identifier:
            print('???', str(identifier))
        else:
            delimitador = input('Digite o delimitador do arquivo a ser exportado (padrão=;): \n\n\t>')
            if delimitador == '\\t':
                delimitador = '\t'
            elif delimitador == '\\n':
                delimitador = '\n'
            elif delimitador == '':
                delimitador = ';'
            for linha in arqCSV:
                tmp = linha.replace(delimitador, delimitador2)
                arqCSVNovo.write(tmp)
                tmp = None


    def __finalizar(self):
        self.__nomeArquivoFinal = 'resultadoOrto'+str(random())+'.txt'
        try:
            self.__arquivoFinal = codecs.open(self.__nomeArquivoFinal, 'w', encoding=encoding, errors='ignore')
            self.__novoarquivo_temp = codecs.open(self.__nomeTempFinal, 'r', encoding=encoding, errors='ignore')
        except Exception as identifier:
            print('Erro ao finalizar: ', str(identifier))
        else:
            self.__listaNomes = []
            for self.__index, self.__linha in enumerate(self.__novoarquivo_temp):
                if self.__linha not in self.__listaNomes:
                    self.__listaNomes.append(self.__linha)
                    self.__arquivoFinal.write(self.__linha + '\n')
                    if self.__index > 20:
                        break            
                

    def __temp_final(self):
        self.__novoarquivo_temp2 = codecs.open(self.__nomeArquivoTemp2, 'r', encoding=encoding, errors='ignore')
        self.__novoarquivo_temp = codecs.open(self.__nomeTempFinal, 'w', encoding=encoding, errors='ignore')
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
                        expRgl = regex.match('^(([a-z])([A-Z]))|^(([A-Z])([A-Z]))|^([\W])', self.__achado)
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
        #     self.__novo_arq_txt = regex.sub('\s{2,}[^\\n\w]', '\t', self.arquivo.read().replace('\n', '   '))
        # else:
        self.__novo_arq_txt = self.arquivo.read()
        self.__novo_arq_txt = regex.sub('(Ã³)|(├Á)|(├\│)|(Ã´)|[óòõôö]', 'o', self.__novo_arq_txt)
        self.__novo_arq_txt = regex.sub('(Ã£)|(Ã¢)|(Ã¡)|(├ú)|(├í)|[áàãâ]', 'a', self.__novo_arq_txt)
        self.__novo_arq_txt = regex.sub('(├º)|(Ã§)|[ç]', 'c', self.__novo_arq_txt)
        self.__novo_arq_txt = regex.sub('(Ã‡)|[Ç]', 'C', self.__novo_arq_txt)
        self.__novo_arq_txt = regex.sub('(ÃŠ)|[ÚÙÛÜ]', 'U', self.__novo_arq_txt)
        self.__novo_arq_txt = regex.sub('(Ãº)|(├║)|[úùûü]', 'u', self.__novo_arq_txt)
        self.__novo_arq_txt = regex.sub('(├¡)|(Ã-)|[íìî]', 'i', self.__novo_arq_txt)
        self.__novo_arq_txt = regex.sub('[ÍÌÎ]', 'I', self.__novo_arq_txt)
        self.__novo_arq_txt = regex.sub('(Ã©)|(├¬)|(├®)|[éèê]', 'e', self.__novo_arq_txt)
        self.__novo_arq_txt = regex.sub('(Ã‰)|[ÉÈÊ]', 'E', self.__novo_arq_txt)
        self.__novo_arq_txt = regex.sub('(Ã•)|(Ã“)|(Ã”)|[ÓÒÕÔÖ]', 'O', self.__novo_arq_txt)
        self.__novo_arq_txt = regex.sub('(Âº)|[´`ºª]', '.', self.__novo_arq_txt)
        self.__novo_arq_txt = regex.sub('(Ãƒ)|[ÁÃÂÀÅ]', 'A', self.__novo_arq_txt)
        self.__novo_arq_txt = regex.sub('(Ã)|[^0-9a-zA-Z\s\/\.\,\;\"\$\<\>\&\*\(\)\[\]\{\}\=\+\-\#\_\%\!\?\@]|[½⅓⅔¼¾⅕⅖⅗⅘⅙⅚⅐⅛⅜⅝⅞⅑⅒↉⅟ ]', '', self.__novo_arq_txt)


        # if not self.arquivo.name.lower().endswith('.csv'):
        #     self.__novo_arq_txt = regex.sub('[^\d\w\s]', '', self.__novo_arq_txt)
        self.__novoarquivo_temp2.write(self.__novo_arq_txt)
        self.arquivo.close()
        self.__novoarquivo_temp2.close()
        self.__novo_arq_txt = None
        del self.__novo_arq_txt

x, y = arquivoInicial()
ajustaOrto8DAT(x, y)



# ainda sem funcionamento

