try:
    import re as regex
    from os import remove as rm
    import csv
    from random import random
    import codecs
except ModuleNotFoundError as identifier:
    print('Erro ao importar bibliotecas.')


def main():
    """
    Solicita o nome do arquivo a ser verificado e retorna o mesmo ou falso em caso em caso de erro.
    """
    while True:
        pergunta = input('Digite o nome do arquivo a ser verificado: \n\n\t>')
        try:
            arquivo = codecs.open(pergunta, 'r', encoding='iso-8859-1', errors='replace')
        except KeyboardInterrupt:
            print('\n\nProcesso cancelado pelo usuário.')
            exit(3)
        except FileNotFoundError as identifier:
            print('Erro ao abrir o arquivo inicial: ', str(identifier))
        else:
            while True:
                try:
                    oqfzr = int(input('O que deseja fazer?\n0-Sair\n1- Escolher outro arquivo'
                    + '\n2-Exportar CSV com um delimitador para CSV delimitado com vírgula'))
                    if oqfzr not in range(0, 3):
                        raise ValueError
                except ValueError:
                    print('\n\nDigite somente números entre as opções válidas.')
                except KeyboardInterrupt:
                    print('\n\nProcesso cancelado pelo usuário.')
                    exit(3)

                else:
                    if oqfzr == 0:
                        oqfzr = None
                        arquivo = None
                        pergunta = None
                        del oqfzr, arquivo, pergunta
                        exit(3)
                    elif oqfzr == 1:
                        oqfzr = None
                        arquivo = None
                        pergunta = None
                        del oqfzr, arquivo, pergunta
                        main()



class Modelo:
    def __init__(self, arquivoOrigem, opt=1):  # Modelo pai para outras classes com parâmetros sendo arquivo de origem e o que fazer
        self.__nomeArquivoTemp2 = 'temp2.tmp'
        self.__nomeTempFinal = 'temp_final.tmp'
        try:
            if (arquivoOrigem):                
                self.__novoarquivo_temp2 = codecs.open(self.__nomeArquivoTemp2, 'w', encoding='iso-8859-1', errors='ignore')
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
            except KeyboardInterrupt as identifier:
                print('Cancelado processo pelo usuário.')


class CSV(Modelo):
    def tratarEExportarParaCSVcomVirgula(self):
            try:
                arqCSV = codecs.open(self.__nomeArquivoTemp2, 'r',  encoding='iso-8859-1', errors='ignore')
                arqCSVNovoNome = arqCSV.name+'novo.csv'
                arqCSVNovo = codecs.open(arqCSVNovoNome, 'w',  encoding='iso-8859-1', errors='ignore')
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


class ajustaOrto8DAT(Modelo):

    def __finalizar(self):
        self.__nomeArquivoFinal = 'resultadoOrto'+str(random())+'.txt'
        try:
            self.__arquivoFinal = codecs.open(self.__nomeArquivoFinal, 'w', encoding='iso-8859-1', errors='ignore')
            self.__novoarquivo_temp = codecs.open(self.__nomeTempFinal, 'r', encoding='iso-8859-1', errors='ignore')
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
        self.__novoarquivo_temp2 = codecs.open(self.__nomeArquivoTemp2, 'r', encoding='iso-8859-1', errors='ignore')
        self.__novoarquivo_temp = codecs.open(self.__nomeTempFinal, 'w', encoding='iso-8859-1', errors='ignore')
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
        if not self.arquivo.name.lower().endswith('.csv'):
            self.__novo_arq_txt = regex.sub('\s{2,}[^\\n\w]', '\t', self.arquivo.read().replace('\n', '   '))
        else:
            self.__novo_arq_txt = self.arquivo.read()
        self.__novo_arq_txt = regex.sub('[,´`ºª]', '.', self.__novo_arq_txt)
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
            self.__novo_arq_txt = regex.sub('[^\w\s]', '', self.__novo_arq_txt)
        self.__novoarquivo_temp2.write(self.__novo_arq_txt)
        self.arquivo.close()
        self.__novoarquivo_temp2.close()
        self.__novo_arq_txt = None
        del self.__novo_arq_txt

x, y = main()
ajustaOrto8DAT(x, y)



# ainda sem funcionamento

