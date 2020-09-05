import re as regex
from os import remove as rm
import csv
from random import random
import codecs
def arquivoInicial():
    """
    Solicita o nome do arquivo a ser verificado e retorna o mesmo ou falso em caso em caso de erro.
    """
    pergunta = input('Digite o nome do arquivo a ser verificado: \n\n\t>')
    try:
        arquivo = codecs.open(pergunta, 'r', encoding='cp1252', errors='replace')
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
                self.__novoarquivo_temp2 = codecs.open(self.__nomeArquivoTemp2, 'w', encoding='cp1252', errors='ignore')
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
                    # self.tratarEExportarParaCSVcomVirgula()
                    # self.__temp_final()
                    # print('70% concluído...')
                    self.__finalizar()
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
            arqCSV = codecs.open(self.__nomeArquivoTemp2, 'r',  encoding='cp1252', errors='ignore')
            arqCSVNovoNome = arqCSV.name+'novo.csv'
            arqCSVNovo = codecs.open(arqCSVNovoNome, 'w',  encoding='cp1252', errors='ignore')
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
                tmp = linha.replace(delimitador, ',')
                arqCSVNovo.write(tmp)
                tmp = None

# str(random())+

    def __finalizar(self):
        self.__nomeArquivoFinal = 'resultadoOrto'+'.txt'
        try:
            self.__arquivoFinal = codecs.open(self.__nomeArquivoFinal, 'w', encoding='cp1252', errors='ignore')
            self.__novoarquivo_temp = codecs.open(self.__nomeArquivoTemp2, 'r', encoding='cp1252', errors='ignore')
        except Exception as identifier:
            print('Erro ao finalizar: ', str(identifier))
        else:
            len_maior = 0
            maior_linha = ''
            for num_linha, linha in enumerate(self.__novoarquivo_temp):
                if len(linha) > len_maior:
                    maior_linha = linha
                    len_maior = len(linha)
            else:
                self.__arquivoFinal.write(maior_linha)

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
            # rm(self.__nomeArquivoTemp2)


    def formatarArquivo(self):
        if not self.arquivo.name.lower().endswith('.csv'):
            self.__novo_arq_txt = regex.sub('\s{2,}[^\\n\w]', '-', self.arquivo.read().replace('\n', '   '))
        else:
            self.__novo_arq_txt = self.arquivo.read()
        self.__novo_arq_txt = regex.sub('[´`ºª]', '.', self.__novo_arq_txt)
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
            self.__novo_arq_txt = regex.sub('([^\d/\w\s$])|([Þÿ½ÄåÖ])|(([a-z])([A-Z]))|(([A-Z])([A-Z]))', '', self.__novo_arq_txt)
        self.__novoarquivo_temp2.write(self.__novo_arq_txt)
        self.arquivo.close()
        self.__novoarquivo_temp2.close()
        self.__novo_arq_txt = None
        del self.__novo_arq_txt

x, y = arquivoInicial()
ajustaOrto8DAT(x, y)



# ainda sem funcionamento

