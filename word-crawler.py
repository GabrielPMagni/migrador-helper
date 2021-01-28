from logging import debug
from os import listdir as ls, path, stat
from gooey import Gooey, GooeyParser
from subprocess import Popen, PIPE
from pdfminer import high_level as pdf
import mimetypes

# Global var
items = []

@Gooey(
    program_name = 'Word Crawler',
    program_description = 'Busca palavra chave em arquivos listando subdiretórios.',
    requires_shell=False,
    show_success_modal=False,
    show_failure_modal=True,
    hide_progress_msg=True,
    default_size=(610, 580),
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
        metavar='Texto a ser procurado:',
        widget='Textarea'
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

    args = parser.parse_args()

    try:
        query = args.input_text
        debug = args.debug
    except UnicodeDecodeError:
        print('Entrada de texto inválida')
    else:
        if args.command == 'analyse_dir':
            list_sub_dir(args.dir, debug)
            found_on = search(items, query, debug)  # i = index, m = match
            if found_on != None:
                show_results(found_on)
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
        

def read_as_binary():  # a ser implementado
    return None


def read_as_pdf(file_name:str, query:str, debug=False):
    query = query.lower()
    try:
        # file_byte = open(file_name, 'rb')  # abre o arquivo binário como tal
        file_text = pdf.extract_text(file_name)  # lê o arquivo completo como PDF e decodifica para "ANSI"
        file_text = file_text.lower()
        metadata = enum_data(file_name, debug)
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
        result = file_text.find(query) # abre arquivo como texto no terminal e filtra pela busca
        if result >= 0:  # caso encontre algo executa príximos comandos
            found_array['index'] = file_text.find(query)  # adiciona à lista index onde foi encontrado
            found_array['match'] = query  # adiciona texto encontrado
            found_array['file_name'] = file_name  # adiciona texto encontrado
            found_array['file_size'] = stat(file_name).st_size  # adiciona tamanho do arquivo
            found_array['metadata'] = metadata  # adiciona metadados do arquivo
        if len(found_array) > 0:
            return found_array
        else:
            return None


def read_as_text(file_name:str, query:str, debug=False):
    query = query.lower()
    found_array = {}  # cria um dicionário vazio e limpa após cada loop
    try:
        file_text = open(file_name, 'r').read() # lê arquivo completo e armazena texto em variável (caso seja binário, pula para o próximo)
        file_text = file_text.lower()
        metadata = enum_data(file_name, debug)
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
        result = file_text.find(query)  # abre arquivo como texto no terminal e filtra pela busca
        if result >= 0:  # caso encontre algo executa príximos comandos
            found_array['index'] = file_text.find(query)  # adiciona à lista index onde foi encontrado
            found_array['match'] = query  # adiciona texto encontrado
            found_array['file_name'] = file_name  # adiciona texto encontrado
            found_array['file_size'] = stat(file_name).st_size  # adiciona tamanho do arquivo
            found_array['metadata'] = metadata  # adiciona metadados do arquivo
        if len(found_array) > 0:
            return found_array
        else:
            return None


def search(file_list:list, query:str, debug=False):
    num_file = len(file_list)
    found_on = []
    if debug:
        print('Procurando correspondências nos arquivos...')
    for i, file_name in enumerate(file_list):  # para cada arquivo encontrado
        print(str(i+1) + ' / ' + str(num_file))
        mimetype = mimetypes.MimeTypes().guess_type(file_name)[0]
        if mimetype == 'text/plain':
            if debug:
                print('Encontrado tipo texto')
            found_array = read_as_text(file_name, query, debug)
            if found_array == None:
                continue
            found_on.append(found_array)  # adiciona lista à lista maior contendo de todos os arquivos
        elif mimetype == 'application/pdf':
            print('Encontrado tipo pdf')
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

def show_results(found_on:list): # exibição de resultados
    found_on.sort(reverse=True, key=order_by_size)
    num_found = len(found_on)
    print('\n\n\n\n\n+------------------RESULTADOS------------------+')
    print('> Total de arquivos com correspondencia: '+str(num_found))
    for item in found_on:
        model = '|\n|\tArquivo: :file.!\n|\tIndex encontrado: :index.!\n|\tTamanho do Arquivo (Bytes): :file_size.!\n|\tTexto encontrado: :match.!\n|\tDetalhes: :metadata.!\n------------------------------------------------'
        model = model.replace(':index.!', str(item['index']))
        model = model.replace(':match.!', str(item['match']))
        model = model.replace(':file.!', str(item['file_name']))
        model = model.replace(':file_size.!', str(item['file_size']))
        model = model.replace(':metadata.!', (item['metadata']))
        print(model)
    print('+----------------------------------------------+')


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
    details = 'Número de metadados encontrados no arquivo: :num_itens.!\nMetadados: :metadata.!'
    details = details.replace(':num_itens.!', str(num_items))
    details = details.replace(':metadata.!', list_metadata(meta, debug))

    return details


if __name__ == '__main__':
    main()
    