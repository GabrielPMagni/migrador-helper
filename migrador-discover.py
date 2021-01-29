from random import random
from os import listdir as ls, path
from gooey import Gooey, GooeyParser
from subprocess import Popen, PIPE

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
    from_archive = subs.add_parser(
        'analyse_arc', prog='Validar de Arquivo',
    ).add_argument_group('')

    from_dir = subs.add_parser(
        'analyse_dir', prog='Validar de Diretório',
    ).add_argument_group('')

    #  de arquivo
    from_archive.add_argument(
        'input_files',
        metavar='Arquivo a ser verificado:',
        widget="MultiFileChooser",
        nargs = '*',
        gooey_options=dict(wildcard="(*)|*", full_width=True)
    )

    from_archive.add_argument(
        'output_file',
        widget="FileSaver",
        metavar='Arquivo de saída:',
        gooey_options=dict(wildcard="(*.csv, *.txt)|*.csv; *.txt", default_file='migrador-dicover-'+str(random())+'.csv', full_width=True)
    )

    #  de diretório
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
        gooey_options=dict(wildcard="(*.csv, *.txt)|*.csv; *.txt", default_file='migrador-dicover-'+str(random())+'.csv', full_width=True)
    )

    args = parser.parse_args()

    if args.command == 'analyse_arc':
        for index, arc in enumerate(args.input_files):
            print('Arquivo #', index)
            nt, r, d = enum_data(arc)
            show_results(nt, r, d)
    elif args.command == 'analyse_dir':
        for index, arc in enumerate(list_sub_dir(args.dir)):
            print('Arquivo #', index)
            dir_path = args.dir+'\\'+arc
            nt, r, d = enum_data(dir_path)
            show_results(nt, r, d)

    # show_results()

def list_sub_dir(directory:str):
    items = []
    for item in ls(directory):
        d = path.join(directory, item)
        if path.isdir(d):
            list_sub_dir(d)
        else:
            items.append(d)
    return items

def show_results(num_testes:int, result:str, details:str): # exibição de resultados
    model = """
    +------------------RESULTADOS------------------+
    *                                   
    (  `                     (            
    )\))(  (  (  ( (      )  )\ )    (    
    ((_)()\ )\ )\))()(  ( /( (()/( (  )(   
    (_()((_|(_|(_))(()\ )(_)) ((_)))\(()\  
    |  \/  |(_)(()(_|(_|(_)_  _| |((_)((_) 
    | |\/| || / _` | '_/ _` / _` / _ \ '_| 
    |_| )|_||_\__, |_| \__,_\__,_\___/_|   
    ( /(     (___/                        
    )\())  ( )\         (  (              
    ((_)\  ))((_)`  )   ))\ )(             
    _((_)/((_)  /(/(  /((_|()\            
    | || (_))| |((_)_\(_))  ((_)           
    | __ / -_) || '_ \) -_)| '_|           
    |_||_\___|_|| .__/\___||_|             
                |_|             

    > Testes Executados: :num_testes.!

    > Resultado: :result.!

    > Detalhes: :details.!
    +----------------------------------------------+
    """
    model = model.replace(':num_testes.!', str(num_testes))
    model = model.replace(':result.!', str(result))
    model = model.replace(':details.!', str(details))
    print(model)

# --- lógica do software ---
def list_metadata(meta):
    output = '\r\n'
    for key in meta:
        output = output + str(key).replace('{', '').replace('}', '').replace('\'', '') + '\r\n'
    return str(output)

def enum_data(archive:str):
    # declaração de variáveis
    process = Popen(['assets/exiftool.exe', archive], stdout=PIPE, stderr=PIPE)
    stdout, stderr = process.communicate()
    num_testes = 0
    details = ''
    result = ''
    meta = []  # lista de itens dos metadados
    num_items = 0  # numero de itens

    # lista em meta cada metadado encontrado e o total de itens encontrados como chave-valor
    for index, item in enumerate(str(stdout).split('\\r\\n')):
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
    details = """
    Número de metadados encontrados no arquivo: :num_itens.!
    Metadados: :metadata.!
    """

    details = details.replace(':num_itens.!', str(num_items))
    details = details.replace(':metadata.!', list_metadata(meta))

    return num_testes, result, details


if __name__ == '__main__':
    main()
    
# --- fim lógica do software ---


