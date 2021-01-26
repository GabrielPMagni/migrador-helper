from random import random
from os import listdir as ls, path, system
from gooey import Gooey, GooeyParser
from subprocess import Popen, PIPE
from sys import platform, stderr, stdin, stdout

# global var
items = []
found_on = []
if platform.startswith('win32') or platform.startswith('cygwin'):
    slash = '\\'
    grep = ' | findstr '
    cat = ' type '
else:
    slash = '/'
    grep = ' | grep '
    cat = ' cat '

@Gooey(
    program_name = 'Migrador Discover',
    program_description = 'Multi funções para ajudar em migrações de banco de dados.',
    default_size=(610, 580),
    navigation='TABBED',
    menu=[{'name': 'Sobre', 'items': [{'type': 'AboutDialog', 'name': 'Sobre o Migrador Helper', 'menuTitle': 'Sobre', 'description': 'Na tentativa de facilitar a vida das migrações de banco de dados', 'version': '1.0',  'developer': 'Gabriel Peres Magni','website': 'https://github.com/GabrielPMagni'}]}]
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
    )

    from_dir.add_argument(
        'dir',
        metavar='Pasta a ser verificada',
        widget="DirChooser",
        gooey_options=dict(full_width=True)
    )

    from_dir.add_argument(
        'output_file',
        widget="FileSaver",
        metavar='Arquivo de saída:',
        gooey_options=dict(wildcard="(*.txt)|*.txt", default_file='word-crawler.txt', full_width=True)
    )

    args = parser.parse_args()

    if args.command == 'analyse_dir':
        list_sub_dir(args.dir)
        search(items, args.input_text)  # i = index, m = match
        if len(found_on) > 0:
            show_results()
        else:
            print('Nada encontrado')


def list_sub_dir(directory:str):  # lista subdiretórios e retorna lista com arquivos encontrados
    for item in ls(directory):
        d = path.join(directory, item)
        if path.isdir(d):
            list_sub_dir(d)
        else:
            items.append(str(d))
    return items


def search(file_list, search):
    for file_name in file_list:  # para cada arquivo encontrado
        try:
            file_text = open(file_name, 'r').read() # lê arquivo completo e armazena texto em variável (caso seja binário, pula para o próximo)
        except UnicodeDecodeError:
            continue
        else:
            found_array = []  # cria uma lista vazia e limpa após cada loop
            result = system(cat + '\"'+file_name+'\"' + grep + search)  # abre arquivo como texto no terminal e filtra pela busca
            if result != '':  # caso encontre algo executa príximos comandos
                found_array.append(file_text.find(search))  # adiciona à lista index onde foi encontrado
                found_array.append(search)   # adiciona texto encontrado
                found_on.append(found_array)  # adiciona lista à lista maior contendo de todos os arquivos


def show_results(): # exibição de resultados
    for item in found_on:
        model = """
        +------------------RESULTADOS------------------+
        |Index encontrado: :index.!
        |
        |Texto encontrado: :match.!
        +----------------------------------------------+
        """
        model = model.replace(':index.!', str(item[0]+1))
        model = model.replace(':match.!', str(item[1]))
        print(model)

if __name__ == '__main__':
    main()
    
# --- fim lógica do software ---


