from random import random
from os import listdir as ls, path, popen, stat
from gooey import Gooey, GooeyParser
from sys import platform

# global var
items = []
found_on = []
debug = False
if platform.startswith('win32') or platform.startswith('cygwin'):
    grep = ' | find '
    cat = ' type '
else:
    grep = ' | grep '
    cat = ' cat '

@Gooey(
    program_name = 'Word Crawler',
    program_description = 'Busca palavra chave em arquivos listando subdiretórios.',
    requires_shell=False,
    show_success_modal=False,
    show_failure_modal=True,
    hide_progress_msg=True,
    default_size=(610, 580),
    navigation='TABBED',
    menu=[{'name': 'Sobre', 'items': [{'type': 'AboutDialog', 'name': 'Sobre o Word Crawler', 'menuTitle': 'Sobre', 'description': 'Busca palavra chave em arquivos listando subdiretórios', 'version': '1.0',  'developer': 'Gabriel Peres Magni','website': 'https://github.com/GabrielPMagni'}]}]
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
        text = args.input_text
        debug = args.debug
    except UnicodeDecodeError:
        print('Entrada de texto inválida')
    else:
        if args.command == 'analyse_dir':
            list_sub_dir(args.dir, debug)
            search(items, text, debug)  # i = index, m = match
            if len(found_on) > 0:
                show_results()
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
                list_sub_dir(d)
            else:
                if debug:
                    print('Arquivo Encontrado')
                items.append(str(d))
    except PermissionError:
        if debug:
            print('Permissão Negada à Pasta')
        exit(2)
    except Exception as e:
        if debug:
            print('Erro não tratado list_sub_dir: '+str(e))
        exit(1)


def search(file_list, search, debug=False):
    num_file = len(file_list)
    if debug:
        print('Procurando correspondências nos arquivos...')
    for i, file_name in enumerate(file_list):  # para cada arquivo encontrado
        print(str(i+1) + ' / ' + str(num_file))
        try:
            file_text = open(file_name, 'r').read() # lê arquivo completo e armazena texto em variável (caso seja binário, pula para o próximo)
        except UnicodeDecodeError:
            if debug:
                print('Unicode Decode Error (arquivo binário ou não texto)')
            continue
        except PermissionError:
            if debug:
                print('Permissão Negada ao Arquivo')
            continue
        except Exception as e:
            if debug:
                print('Erro não tratado search: '+str(e))
            continue
        else:
            found_array = {}  # cria um dicionário vazio e limpa após cada loop
            result = popen(cat + '\"'+file_name+'\"' + grep + '\"'+search+'\"').read()  # abre arquivo como texto no terminal e filtra pela busca
            if result != '':  # caso encontre algo executa príximos comandos
                found_array['index'] = file_text.find(search)  # adiciona à lista index onde foi encontrado
                found_array['match'] = search  # adiciona texto encontrado
                found_array['file_name'] = file_name  # adiciona texto encontrado
                found_array['file_size'] = stat(file_name).st_size  # adiciona tamanho do arquivo
                found_on.append(found_array)  # adiciona lista à lista maior contendo de todos os arquivos

def order_by_size(e):
    return e['file_size']

def show_results(): # exibição de resultados
    found_on.sort(reverse=True, key=order_by_size)
    num_found = len(found_on)
    print('\n\n\n\n\n+------------------RESULTADOS------------------+')
    print('> Total de arquivos com correspondencia: '+str(num_found))
    for item in found_on:
        model = '|\n|\tArquivo: :file.!\n|\tIndex encontrado: :index.!\n|\tTamanho do Arquivo (Bytes): :file_size.!\n|\tTexto encontrado: :match.!\n|\n------------------------------------------------'
        model = model.replace(':index.!', str(item['index']))
        model = model.replace(':match.!', str(item['match']))
        model = model.replace(':file.!', str(item['file_name']))
        model = model.replace(':file_size.!', str(item['file_size']))
        print(model)
    print('+----------------------------------------------+')

if __name__ == '__main__':
    main()
    