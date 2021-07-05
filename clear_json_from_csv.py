import re as regex
import codecs

# (""description"": ""([^""])+)|(""name": ""([^""])+)|(""value""": ""([^""])+)|(""posology"": ""([^""])+)|(""tab"": ""([^""])+)|(""text"": ""([^""])+)
fields = []

def ler_arquivo():
    arq = input('\nNome do arquivo: \n\n\t>')
    arquivo = codecs.open(arq, 'r', encoding='utf-8', errors='ignore')
    main(arquivo)


def main(arquivo):
    regexes = []
    r0 = regex.compile(r'(("tab":) "([^"])+)')
    r1 = regex.compile(r'(("name":) "([^"])+)')
    r2 = regex.compile(r'(("value":) "([^"])+)')
    regexes.append(r0)
    regexes.append(r1)
    regexes.append(r2)
    clear = regex.compile(r'(\'\w\')|(\')|[\(\)]|\,|\[|\]|\t|\"')
    for index, linha in enumerate(arquivo.readlines()):
        model = '"'
        fields.clear()
        slice_json_fields(linha)
        for field in fields:
            tab = ''
            for index, reg in enumerate(regexes):
                text = get_field_values(reg, clear, field)
                if index == 0: 
                    tab = text
                else:
                    if tab != 'Exame físico':
                        model += text + '<br>'
            model += '<br>'
        model += '"\n'
        novoarquivo = codecs.open('novoarquivo.txt', 'a', encoding='utf-8', errors='ignore')
        novoarquivo.write(model)
    else:
        arquivo.close()
        novoarquivo.close()


def slice_json_fields(line: str, last_position = 0):
    starts_on = line.find('{', last_position)
    ends_on = line.find('}', starts_on)
    if starts_on == -1 or ends_on == -1:
        return None
    field = line[starts_on+1: ends_on]
    fields.append(field)
    slice_json_fields(line, ends_on+1)


def get_field_values(reg, clear, field):
    obj = regex.search(reg, field)
    if obj is not None:
        obj = regex.sub(clear, '', regex.sub(obj.group(2), '', obj.group(1))).strip()
    else:
        obj = ''
    return obj


ler_arquivo()