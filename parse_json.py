import json as json_parser
import codecs
from var_dump import var_dump

line_args_global_list = []

def ler_arquivo():
    arq_in = input('\nNome do arquivo: \n\n\t>')
    arquivo = codecs.open(arq_in, 'r', encoding='utf-8', errors='ignore')
    return arquivo


def ler_arquivo_de_saida():
    arq_out = input('Digite o arquivo para inclusão do resultado:\n')
    arquivo = codecs.open(arq_out, 'a', encoding='utf-8')
    return arquivo


def incluir_no_arquivo(arquivo_saida: codecs.StreamReaderWriter, text = ''):
    arquivo_saida.write('\"' + text + '\"\n')


def monta_prontuario(arquivo_saida: codecs.StreamReaderWriter, parsed_json: dict = None):
    if parsed_json is None:
        incluir_no_arquivo(arquivo_saida)
    else:
        line_args_global_list.clear()
        scan_sub_json(parsed_json)
        tab = ''
        medical_record = ''
        for i, item_list in enumerate(line_args_global_list):
            for j, item in enumerate(item_list):
                if j == 0 and tab != item['tab']:
                    tab = item['tab']
                    medical_record += '<br><br>' + tab + ':<br>'
                if item['key'] == 'tab': continue
                if item['key'] == 'kind': continue
                if item['key'] == 'date_added': continue
                if item['key'] == 'ordering': continue
                if item['key'] == 'bmi_value': item['key'] = 'Resultado IMC'
                if item['key'] == 'height': item['key'] = 'Altura'
                if item['key'] == 'weight': item['key'] = 'Peso'
                if item['key'] in ['name', 'value']:
                    medical_record += (item['value'] + '<br>')
                else:
                    medical_record += (item['key'] + ': ' + item['value'] + '<br>')
        else:
            incluir_no_arquivo(arquivo_saida, medical_record)



def scan_sub_json(json: dict, tab = ''):
    line_args = ''
    for k, v in json.items():
        model = '{"tab": "[TAB]", "key": "[NAME]", "value": "[VALUE]"},'
        if isinstance(v, dict):
            scan_sub_json(v, tab)
        elif isinstance(v, list):
            for item in v:
                if isinstance(item, dict):
                    scan_sub_json(item, tab)
        else:
            try:
                tab = json['tab']
            except KeyError:
                pass
            temp_model = model.replace('[TAB]', tab )
            temp_model = temp_model.replace('[NAME]', str(k).replace('\"', '\\\"'))
            temp_model = temp_model.replace('[VALUE]', str(v).replace('\"', '\\\"'))
            line_args += temp_model
            temp_model = None
            del temp_model
    else:
        line_args_parseable = '[' + line_args[:-1] + ']'
        line_args = None
        del line_args
        line_args_global_list.append(json_parser.loads(line_args_parseable, strict=False))


def main():
    arquivo = ler_arquivo()
    arquivo_out = ler_arquivo_de_saida()
    for index, linha in enumerate(arquivo.readlines()):
        print(index)
        if index == 0 or linha.strip() == '':
            monta_prontuario(arquivo_out)
            continue
        parsed = json_parser.loads(linha, strict=False)
        monta_prontuario(arquivo_out, parsed)

main()