import re as regex
import codecs

# (""description"": ""([^""])+)|(""name": ""([^""])+)|(""value""": ""([^""])+)|(""posology"": ""([^""])+)|(""tab"": ""([^""])+)|(""text"": ""([^""])+)

def ler_arquivo():
    arq = input('\nNome do arquivo: \n\n\t>')
    arquivo = codecs.open(arq, 'r', encoding='utf-8', errors='ignore')
    tratar_arquivo(arquivo)

def tratar_arquivo(arquivo):
    # rx1 = regex.compile(r'((""text"":) ""([^""])+)')
    # rx2 = regex.compile(r'((""posology"":) ""([^""])+)')
    # rx3 = regex.compile(r'((""name"":) ""([^""])+)')
    # rx4 = regex.compile(r'((""value"":) ""([^""])+)')
    rx1 = regex.compile(r'(("text":) "([^"])+)')
    rx2 = regex.compile(r'(("posology":) "([^"])+)')
    rx3 = regex.compile(r'(("name":) "([^"])+)')
    rx4 = regex.compile(r'(("value":) "([^"])+)')
    rx5 = regex.compile(r'(("bmi_value":) "([^"])+)')

    
    clear = regex.compile(r'(\'\w\')|(\')|[\(\)]|\,|\[|\]|\t|\"')
    for linha in arquivo.readlines():
        novo_arq_txt = ret_val(rx4, clear, linha)
        novoarquivo = codecs.open('novoarquivo.txt', 'a', encoding='utf-8', errors='ignore')
        novoarquivo.write(novo_arq_txt+'\n')
    else:
        arquivo.close()
        novoarquivo.close()

def ret_val(reg, clear, linha):
    novo_arq_txt = ''
    try:
        novo_arq_match = regex.finditer(reg, linha)
        novo_arq_match = novo_arq_match if novo_arq_match else None
        # novo_arq_txt += regex.sub(clear, '', (regex.sub(novo_arq_match.group(2), '', novo_arq_match.group(0)) + '<BR>' if novo_arq_match != None else ''))
        # print(get_elem(novo_arq_match, 0))
        for i in regex.finditer(reg, linha):
            x = regex.sub(clear, '', regex.sub(i.group(2), '', i.group(1)))
            novo_arq_txt += x + '<br>'
    except Exception as e:
        pass
    finally:
        return novo_arq_txt

def get_elem(arr, n):
    itens = ''
    for x in arr:
        itens += x[n]
    else:
        return itens

                
ler_arquivo()