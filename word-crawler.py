from os import listdir as ls, path, stat
from gooey import Gooey, GooeyParser
from subprocess import Popen, PIPE
from pdfminer import high_level as pdf
import re
import magic
import mimetypes
from ast import literal_eval as to_dict

# Global var
items = []

@Gooey(
    program_name = 'Word Crawler',
    program_description = 'Busca palavra chave em arquivos listando subdiretórios.',
    requires_shell=False,
    show_success_modal=False,
    show_failure_modal=True,
    hide_progress_msg=True,
    default_size=(610, 770),
    navigation='TABBED',
    menu=[{'name': 'Sobre', 'items': [{'type': 'AboutDialog', 'name': 'Sobre o Word Crawler', 'menuTitle': 'Sobre', 'description': 'Busca palavra chave em arquivos listando subdiretórios e metadados', 'version': '1.0',  'developer': 'Gabriel Peres Magni','website': 'https://github.com/GabrielPMagni'}]}]
)

def main():
    parser = GooeyParser()
    subs = parser.add_subparsers(help="commands", dest="command")

    from_dir = subs.add_parser(
        'analyse_dir', prog='Validar de Diretório',
    ).add_argument_group('')
    
    #  de diretório
    from_dir.add_argument(
        'input_text',
        metavar='Expressão regular a ser procurada:',
        widget='Textarea'
    )

    from_dir.add_argument(
        '--find_email',
        dest='find_email',
        metavar='Procurar emails:',
        action='store_true'
    )

    from_dir.add_argument(
        '--find_phone',
        dest='find_phone',
        metavar='Procurar Telefones/Celulares:',
        action='store_true'
    )

    from_dir.add_argument(
        '--find_cpf',
        dest='find_cpf',
        metavar='Procurar CPF:',
        action='store_true'
    )

    from_dir.add_argument(
        '--find_cnpj',
        dest='find_cnpj',
        metavar='Procurar CNPJ:',
        action='store_true'
    )

    from_dir.add_argument(
        '--find_date',
        dest='find_date',
        metavar='Procurar Datas:',
        action='store_true'
    )

    from_dir.add_argument(
        '--find_cep',
        dest='find_cep',
        metavar='Procurar CEP:',
        action='store_true'
    )


    from_dir.add_argument(
        'dir',
        metavar='Pasta a ser verificada:',
        widget="DirChooser",
        gooey_options=dict(full_width=True)
    )

    from_dir.add_argument(
        '--debug',
        dest='debug',
        metavar='Verbosidade:',
        action='store_true'
    )

    from_dir.add_argument(
        '--scan_metadata',
        dest='scan_metadata',
        metavar='Escanear metadados:',
        action='store_true'
    )
    
    from_dir.add_argument(
        '--order_by',
        dest='order_by',
        metavar='Ordenar por:',
        choices=['Tamanho do Arquivo', 'Quantidade de Correspondências'],
        default='Tamanho do Arquivo'
    )
    

    args = parser.parse_args()

    try:
        search_for = {'email': args.find_email, 'phone': args.find_phone, 'cpf': args.find_cpf, 'cnpj': args.find_cnpj, 'date': args.find_date, 'cep': args.find_cep}
        scan_personal = any([args.find_email, args.find_phone, args.find_cpf, args.find_cnpj, args.find_date, args.find_cep])
        scan_metadata = args.scan_metadata
        query = args.input_text
        debug = args.debug
        if args.order_by == 'Tamanho do Arquivo':
            order_by = 1
        elif args.order_by == 'Quantidade de Correspondências':
            order_by = 2
        else:
            order_by = 1
    except UnicodeDecodeError:
        print('Entrada de texto inválida')
    else:
        if args.command == 'analyse_dir':
            list_sub_dir(args.dir, debug)
            found_on = search(items, query, debug)
            file_types = search_file_types(items, debug, scan_metadata)
            if len(file_types) > 0:
                show_file_types(file_types)
            if scan_personal:
                personal_data = search_personal(items, search_for, debug)
                if len(personal_data) > 0: 
                    show_personal_data(personal_data)
            if found_on != None:
                show_results(found_on, order_by)
            else:
                print('Nada encontrado')


def list_sub_dir(directory:str, debug=False):  # lista subdiretórios e retorna lista com arquivos encontrados
    if debug:
        print('Listando diretórios...')
    try:
        for item in ls(directory):
            d = path.join(directory, item)
            if path.isdir(d):
                if debug:
                    print('Pasta encontrada')
                list_sub_dir(d, debug)
            else:
                if debug:
                    print('Arquivo Encontrado')
                items.append(str(d))
        else:
            if len(items) == 0:
                print('Não encontrados arquivos')
                exit(3)
                
    except PermissionError:
        if debug:
            print('Permissão Negada à Pasta')
        exit(1)
    except Exception as e:
        if debug:
            print('Erro não tratado list_sub_dir: '+str(e))
        exit(2)
        

def read_as_binary(file_name, debug=False, scan_metadata=False): 
    try:
        file = open(file_name, 'rb').read()
        file_text = magic.Magic().from_buffer(file)
        if scan_metadata:
            metadata = enum_data(file_name, debug)
        else:
            metadata = ''    
    except UnicodeDecodeError:
        if debug:
            print('Unicode Decode Error em read_as_binary')
        return None
    except PermissionError:
        if debug:
            print('Permissão Negada ao Arquivo read_as_binary')
        return None
    except Exception as e:
        if debug:
            print('Erro não tratado read_as_binary: '+str(e))
        return None
    else:
        found_array = {}  # cria um dicionário vazio e limpa após cada loop
        found_array['tot_found'] = 'Tipo do Aquivo'  # adiciona à lista index onde foi encontrado
        found_array['match'] = file_text  # adiciona texto encontrado (tipo do arquivo de acordo com libmagic)
        found_array['file_name'] = file_name  # adiciona texto encontrado
        found_array['file_size'] = stat(file_name).st_size  # adiciona tamanho do arquivo
        found_array['metadata'] = metadata  # adiciona metadados do arquivo
        if len(found_array) > 0:
            return found_array
        else:
            return None




def read_as_pdf(file_name:str, query:str, debug=False, scan_metadata=False):
    try:
        regex_query = re.compile(query, re.IGNORECASE)
        file_text = pdf.extract_text(file_name)  # lê o arquivo completo como PDF e decodifica para "ANSI"
        metadata = ''    
    except UnicodeDecodeError:
        if debug:
            print('Unicode Decode Error em read_as_pdf')
        return None
    except PermissionError:
        if debug:
            print('Permissão Negada ao Arquivo')
        return None
    except Exception as e:
        if debug:
            print('Erro não tratado read_as_pdf: '+str(e))
        return None
    else:

        found_array = {}  # cria um dicionário vazio e limpa após cada loop
        result =  re.findall(regex_query, file_text)  # abre arquivo como texto e busca como match de expressão regular
        if len(result) > 0:  # caso encontre algo executa próximos comandos
            found_array['tot_found'] = len(result)  # adiciona à lista index onde foi encontrado
            found_array['match'] = result  # adiciona texto encontrado
            found_array['file_name'] = file_name  # adiciona texto encontrado
            found_array['file_size'] = stat(file_name).st_size  # adiciona tamanho do arquivo
            found_array['metadata'] = metadata  # adiciona metadados do arquivo
        if len(found_array) > 0:
            return found_array
        else:
            return None

def remove_values_from_list(the_list:list):
    while ('' in the_list):
        the_list.remove('')
    else:
        return the_list


def search_personal(file_list, search_for, debug=False):
    num_file = len(file_list)
    email_found = []
    phone_found = []
    cpf_found = []
    cnpj_found = []
    date_found = []
    cep_found = []
    dict_model = {}
    if debug:
        print('Procurando correspondências nos arquivos...')
    for i, file_name in enumerate(file_list):  # para cada arquivo encontrado
        print('Dados Pessoais: ' + str(i+1) + ' / ' + str(num_file) + ' ('+ str(round(((i+1)/num_file), 2) * 100) + '%)')
        mimetype = mimetypes.MimeTypes().guess_type(file_name)[0]
        if mimetype == None:
            mimetype = 'text'
        if 'text' in mimetype or 'csv' in mimetype:
            if debug:
                print('Encontrado tipo texto em search_personal')
            if search_for.get('email'):
                if debug:
                    print('Enumerando emails...')
                query = '(?P<email>[a-zA-Z0-9.!#$%&\'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*)'
                found_array = read_as_text(file_name, query, debug)
                if found_array == None:
                    continue
                email_found.append(found_array)  # adiciona lista à lista maior contendo de todos os arquivos
            if search_for.get('phone'):
                if debug:
                    print('Enumerando telefone / celular...')
                query = '(?P<phone>\(?[1-9]{2}\)? ?(?:[2-8]|9[1-9])[0-9]{3}\-?[0-9]{4})'
                found_array = read_as_text(file_name, query, debug)
                if found_array == None:
                    continue
                phone_found.append(found_array)  # adiciona lista à lista maior contendo de todos os arquivos
            if search_for.get('cpf'):
                if debug:
                    print('Enumerando CPF...')
                query = '(?P<cpf>\d{3}\.\d{3}\.\d{3}\-\d{2})'
                found_array = read_as_text(file_name, query, debug)
                if found_array == None:
                    continue
                cpf_found.append(found_array)  # adiciona lista à lista maior contendo de todos os arquivos
            if search_for.get('cnpj'):
                if debug:
                    print('Enumerando CNPJ...')
                query = '(?P<cnpj>\d{2}\.\d{3}\.\d{3}\/\d{4}\-\d{2})'
                found_array = read_as_text(file_name, query, debug)
                if found_array == None:
                    continue
                cnpj_found.append(found_array)  # adiciona lista à lista maior contendo de todos os arquivos
            if search_for.get('date'):
                if debug:
                    print('Enumerando Data...')
                query = '(?P<date>(([1-3])(\d)).?(1([1-2])).?(\d){4}|(1([1-2])).?(([1-3])(\d)).?(\d){4}|(\d){4}.?(1([1-2])).?(([1-3])(\d)))'
                found_array = read_as_text(file_name, query, debug)
                if found_array == None:
                    continue
                date_found.append(found_array)  # adiciona lista à lista maior contendo de todos os arquivos
            if search_for.get('cep'):
                if debug:
                    print('Enumerando CEP...')
                query = '(?P<cep>(\d){5}.?(\d){3})'
                found_array = read_as_text(file_name, query, debug)
                if found_array == None:
                    continue
                cep_found.append(found_array)  # adiciona lista à lista maior contendo de todos os arquivos
        elif 'pdf' in mimetype:
            if debug:
                print('Encontrado tipo PDF em search_personal')
            if search_for.get('email'):
                if debug:
                    print('Enumerando emails...')
                query = '(?P<email>[a-zA-Z0-9.!#$%&\'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*)'
                found_array = read_as_pdf(file_name, query, debug)
                if found_array == None:
                    continue
                email_found.append(found_array)  # adiciona lista à lista maior contendo de todos os arquivos
            if search_for.get('phone'):
                if debug:
                    print('Enumerando telefone / celular...')
                query = '(?P<phone>\(?[1-9]{2}\)? ?(?:[2-8]|9[1-9])[0-9]{3}\-?[0-9]{4})'
                found_array = read_as_pdf(file_name, query, debug)
                if found_array == None:
                    continue
                phone_found.append(found_array)  # adiciona lista à lista maior contendo de todos os arquivos
            if search_for.get('cpf'):
                if debug:
                    print('Enumerando CPF...')
                query = '(?P<cpf>\d{3}\.\d{3}\.\d{3}\-\d{2})'
                found_array = read_as_pdf(file_name, query, debug)
                if found_array == None:
                    continue
                cpf_found.append(found_array)  # adiciona lista à lista maior contendo de todos os arquivos
            if search_for.get('cnpj'):
                if debug:
                    print('Enumerando CNPJ...')
                query = '(?P<cnpj>\d{2}\.\d{3}\.\d{3}\/\d{4}\-\d{2})'
                found_array = read_as_pdf(file_name, query, debug)
                if found_array == None:
                    continue
                cnpj_found.append(found_array)  # adiciona lista à lista maior contendo de todos os arquivos
            if search_for.get('date'):
                if debug:
                    print('Enumerando Data...')
                query = '(?P<date>(([1-3])(\d)).?(1([1-2])).?(\d){4}|(1([1-2])).?(([1-3])(\d)).?(\d){4}|(\d){4}.?(1([1-2])).?(([1-3])(\d)))'
                found_array = read_as_pdf(file_name, query, debug)
                if found_array == None:
                    continue
                date_found.append(found_array)  # adiciona lista à lista maior contendo de todos os arquivos
            if search_for.get('cep'):
                if debug:
                    print('Enumerando CEP...')
                query = '(?P<cep>(\d){5}.?(\d){3})'
                found_array = read_as_pdf(file_name, query, debug)
                if found_array == None:
                    continue
                cep_found.append(found_array)  # adiciona lista à lista maior contendo de todos os arquivos
    else:
        if len(email_found) > 0:
            dict_model['emails'] = str(email_found)
        if len(phone_found) > 0:
            dict_model['phones'] = str(phone_found)
        if len(cpf_found) > 0:
            dict_model['cpfs'] = str(cpf_found)
        if len(cnpj_found) > 0:
            dict_model['cnpjs'] = str(cnpj_found)
        if len(date_found) > 0:
            dict_model['dates'] = str(date_found)
        if len(cep_found) > 0:
            dict_model['ceps'] = str(cep_found)

        return dict_model



def read_as_text(file_name:str, query:str, debug=False, scan_metadata=False):
    found_array = {}  # cria um dicionário vazio e limpa após cada loop
    try:
        regex_query = re.compile(query, re.IGNORECASE)
        file_text = open(file_name, 'r').read() # lê arquivo completo e armazena texto em variável (caso seja binário, pula para o próximo)
        metadata = ''
    except UnicodeDecodeError:
        if debug:
            print('Unicode Decode Error em read_as_text')
        # read_as_pdf(file_name, query, debug)  # abre o arquivo binário como PDF
        return None
    except PermissionError:
        if debug:
            print('Permissão Negada ao Arquivo')
        return None
    except Exception as e:
        if debug:
            print('Erro não tratado read_as_text: '+str(e))
        return None
    else:
        result =  re.findall(regex_query, file_text)  # abre arquivo como texto e busca como match de expressão regular
        if len(result) > 0:  # caso encontre algo executa próximos comandos
            found_array['tot_found'] = len(result)  # adiciona à lista index onde foi encontrado
            found_array['match'] = result  # adiciona texto encontrado
            found_array['file_name'] = file_name  # adiciona texto encontrado
            found_array['file_size'] = stat(file_name).st_size  # adiciona tamanho do arquivo
            found_array['metadata'] = metadata  # adiciona metadados do arquivo
        if len(found_array) > 0:
            return found_array
        else:
            return None
def search_file_types(file_list:list, debug=False, scan_metadata=False):
    num_file = len(file_list)
    found_on_types = []
    for i, file_name in enumerate(file_list):  # para cada arquivo encontrado
        print('Tipos de Dados: ' + str(i+1) + ' / ' + str(num_file) + ' ('+ str(round(((i+1)/num_file), 2) * 100) + '%)')
        found_types = read_as_binary(file_name, debug, scan_metadata)
        if found_types == None:
            continue
        found_on_types.append(found_types)
    else:
        return found_on_types

def search(file_list:list, query:str, debug=False):
    num_file = len(file_list)
    found_on = []
    if debug:
        print('Procurando correspondências nos arquivos...')
    for i, file_name in enumerate(file_list):  # para cada arquivo encontrado
        print(str(i+1) + ' / ' + str(num_file) + ' ('+ str(round(((i+1)/num_file), 2) * 100) + '%)')
        mimetype = mimetypes.MimeTypes().guess_type(file_name)[0]
        if mimetype == None:
            mimetype = 'text'
        if 'text' in mimetype or 'csv' in mimetype:
            if debug:
                print('Encontrado tipo texto')
            found_array = read_as_text(file_name, query, debug)
            if found_array == None:
                continue
            found_on.append(found_array)  # adiciona lista à lista maior contendo de todos os arquivos
        elif 'pdf' in mimetype:
            if debug:
                print('Encontrado tipo PDF')
            found_array = read_as_pdf(file_name, query, debug)
            if found_array == None:
                continue
            found_on.append(found_array)  # adiciona lista à lista maior contendo de todos os arquivos
        else:
            if debug:
                print('Encontrado tipo desconhecido')
            found_array = read_as_text(file_name, query, debug)
            if found_array == None:
                continue
            found_on.append(found_array)  # adiciona lista à lista maior contendo de todos os arquivos
    else:
        return found_on

def order_by_size(e):
    return e['file_size']

def order_by_matches(e):
    return e['tot_found']


def show_results(found_on:list, sort_mode=1): # exibição de resultados
    if sort_mode == 1:
        found_on.sort(reverse=True, key=order_by_size)
    elif sort_mode == 2:
        found_on.sort(reverse=True, key=order_by_matches)
    num_found = len(found_on)
    print('\n\n\n\n\n+------------------RESULTADOS------------------+')
    print('> Total de arquivos com correspondencia: '+str(num_found))
    for item in found_on:
        model = '|\n|\tArquivo: :file.!\n|\tCorrespondências no aquivo: :tot_found.!\n|\tTamanho do Arquivo (Bytes): :file_size.!\n|\tTexto encontrado: :match.!\n|\tDetalhes: :metadata.!\n------------------------------------------------'
        model = model.replace(':tot_found.!', str(item['tot_found']))
        model = model.replace(':match.!', str(item['match']))
        model = model.replace(':file.!', str(item['file_name']))
        model = model.replace(':file_size.!', str(item['file_size']))
        model = model.replace(':metadata.!', str(item['metadata']))
        print(model)
    print('+----------------------------------------------+')


def show_personal_data(found_on:dict):
    print('\n\n\n\n\n+-----------------RESULTADOS DADOS PESSOAIS-----------------+')
    if 'emails' in found_on:
        model = '|\n|\tArquivo: :file.!\n|\n|\tTamanho do Arquivo (Bytes): :file_size.!\n|\n|\tTexto encontrado: :match.!\n------------------------------------------------'
        print('> Total de correspondências (EMAIL): '+str(to_dict(found_on.get('emails'))[0].get('tot_found')))
        model = model.replace(':match.!', str(to_dict(found_on.get('emails'))[0].get('match')))
        model = model.replace(':file.!', str(to_dict(found_on.get('emails'))[0].get('file_name')))
        model = model.replace(':file_size.!', str(to_dict(found_on.get('emails'))[0].get('file_size')))
        print(model)
    if 'phones' in found_on:
        model = '|\n|\tArquivo: :file.!\n|\n|\tTamanho do Arquivo (Bytes): :file_size.!\n|\n|\tTexto encontrado: :match.!\n------------------------------------------------'
        print('> Total de correspondências (TELEFONE / CELULAR): '+str(to_dict(found_on.get('phones'))[0].get('tot_found')))
        model = model.replace(':match.!', str(to_dict(found_on.get('phones'))[0].get('match')))
        model = model.replace(':file.!', str(to_dict(found_on.get('phones'))[0].get('file_name')))
        model = model.replace(':file_size.!', str(to_dict(found_on.get('phones'))[0].get('file_size')))
        print(model)
    if 'cpfs' in found_on:
        model = '|\n|\tArquivo: :file.!\n|\n|\tTamanho do Arquivo (Bytes): :file_size.!\n|\n|\tTexto encontrado: :match.!\n------------------------------------------------'
        print('> Total de correspondências (CPF): '+str(to_dict(found_on.get('cpfs'))[0].get('tot_found')))
        model = model.replace(':match.!', str(to_dict(found_on.get('cpfs'))[0].get('match')))
        model = model.replace(':file.!', str(to_dict(found_on.get('cpfs'))[0].get('file_name')))
        model = model.replace(':file_size.!', str(to_dict(found_on.get('cpfs'))[0].get('file_size')))
        print(model)
    if 'cnpjs' in found_on:
        model = '|\n|\tArquivo: :file.!\n|\n|\tTamanho do Arquivo (Bytes): :file_size.!\n|\n|\tTexto encontrado: :match.!\n------------------------------------------------'
        print('> Total de correspondências (CNPJ): '+str(to_dict(found_on.get('cnpjs'))[0].get('tot_found')))
        model = model.replace(':match.!', str(to_dict(found_on.get('cnpjs'))[0].get('match')))
        model = model.replace(':file.!', str(to_dict(found_on.get('cnpjs'))[0].get('file_name')))
        model = model.replace(':file_size.!', str(to_dict(found_on.get('cnpjs'))[0].get('file_size')))
        print(model)
    if 'dates' in found_on:
        model = '|\n|\tArquivo: :file.!\n|\n|\tTamanho do Arquivo (Bytes): :file_size.!\n|\n|\tTexto encontrado: :match.!\n------------------------------------------------'
        print('> Total de correspondências (DATA): '+str(to_dict(found_on.get('dates'))[0].get('tot_found')))
        model = model.replace(':match.!', str(to_dict(found_on.get('dates'))[0].get('match')))
        model = model.replace(':file.!', str(to_dict(found_on.get('dates'))[0].get('file_name')))
        model = model.replace(':file_size.!', str(to_dict(found_on.get('dates'))[0].get('file_size')))
        print(model)
    if 'ceps' in found_on:
        model = '|\n|\tArquivo: :file.!\n|\tTamanho do Arquivo (Bytes): :file_size.!\n|\n|\tTexto encontrado: :match.!\n------------------------------------------------'
        print('> Total de correspondências (DATA): '+str(to_dict(found_on.get('ceps'))[0].get('tot_found')))
        model = model.replace(':match.!', str(to_dict(found_on.get('ceps'))[0].get('match')))
        model = model.replace(':file.!', str(to_dict(found_on.get('ceps'))[0].get('file_name')))
        model = model.replace(':file_size.!', str(to_dict(found_on.get('ceps'))[0].get('file_size')))
        print(model)
    print('+'+('-'*59)+'+')


def show_file_types(found_on:list):
    num_found = len(found_on)
    print('\n\n\n\n\n+------------------RESULTADOS TIPOS DE ARQUIVOS------------------+')
    print('> Total de arquivos com correspondencia: '+str(num_found))
    for item in found_on:
        model = '|\n|\tArquivo: :file.!\n|\tCorrespondências no aquivo: :tot_found.!\n|\tTamanho do Arquivo (Bytes): :file_size.!\n|\tTexto encontrado: :match.!\n|\tDetalhes: :metadata.!\n------------------------------------------------'
        model = model.replace(':tot_found.!', str(item['tot_found']))
        model = model.replace(':match.!', str(item['match']))
        model = model.replace(':file.!', str(item['file_name']))
        model = model.replace(':file_size.!', str(item['file_size']))
        model = model.replace(':metadata.!', str(item['metadata']))
        print(model)
    print('+'+('-'*64)+'+')



def list_metadata(meta:list, debug=False):
    if debug:
        print('Indexando metadados...')
    output = '\r\n'
    for key in meta:
        output = output + str(key).replace('{', '').replace('}', '').replace('\'', '') + '\r\n'
    return str(output)

def enum_data(archive:str, debug=False):
    if debug:
        print('Enumerando metadados...')
    # declaração de variáveis
    process = Popen(['assets/exiftool.exe', archive], stdout=PIPE, stderr=PIPE)
    out, err = process.communicate()
    details = ''
    meta = []  # lista de itens dos metadados
    num_items = 0  # numero de itens

    # lista em meta cada metadado encontrado e o total de itens encontrados como chave-valor
    for index, item in enumerate(str(out).split('\\r\\n')):
        if index == 0:
            continue
        else:
            subitems = item.split(' : ')
            if len(subitems) == 2:
                sub1, sub2 = subitems
                sub1 = sub1.strip()
                sub2 = sub2.strip()
                key_value = {sub1: sub2}
                meta.append(key_value)
    else:
        num_items = index - 1  # "-1" pois o index se dá pelo número de linhas, e a primeira é pulada por ser referente ao exiftool
    details = '\n\nNúmero de metadados encontrados no arquivo: :num_itens.!\nMetadados: :metadata.!'
    details = details.replace(':num_itens.!', str(num_items))
    details = details.replace(':metadata.!', list_metadata(meta, debug))

    return details


if __name__ == '__main__':
    main()
    