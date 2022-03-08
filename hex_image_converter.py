import argparse
import re as regex
from os import remove as rm, listdir as ls, path
import codecs


class HexImageConverter:

    def __init__(self, input_file:str, output_folder:str, codification='utf8', delimiter=';') -> None:
        self.input_file = self.validate_input_file_config(input_file, codification)
        self.output_folder = self.validate_output_folder_config(output_folder)
        self.codification = codification
        self.delimiter = delimiter
        self.get_images_with_id()


    def get_images_with_id(self):
        for index, line in enumerate(self.input_file.readlines()):
            if index == 0: continue
            if index == 3: break
            identifier = regex.match(fr'^(.+?){self.delimiter}', line).group(1)
            file_extension = 'jpeg'
            hex_image = regex.search(r'0x(.+)$', line).group(1)
            image_data = bytes.fromhex(hex_image)
            with open(path.join(self.output_folder, identifier+'.'+file_extension), 'wb') as output_file:
                output_file.write(image_data)
        self.input_file.close()



    def confirm(self, question='') -> bool:
        answer = input(question+'\n\n\t> [S/n]').lower()
        return True if (answer or answer in ['yes', 'sim', 's', 'y']) else False
            

    def validate_output_folder_config(self, output_folder):
        try:
            if (path.isdir(output_folder)):
                return path.abspath(output_folder)
            else:
                raise FileNotFoundError
        except PermissionError:
            print('Sem permissão para utilizar o diretório de saída.')
            exit(1)
        except FileNotFoundError:
            print('Diretório de saída não encontrado.')
            exit(1)
        except Exception as e:
            print(f'Erro não tratado ao tentar abrir diretório de saída: {str(e)}')
            exit(1)


    def validate_input_file_config(self, input_file:str, codification:str):
        try:
            return codecs.open(input_file, 'r', encoding=codification, errors='strict')
        except PermissionError:
            print('Sem permissão para utilizar o arquivo de entrada.')
            exit(1)
        except FileNotFoundError:
            print('Arquivo de entrada não encontrado.')
            exit(1)
        except UnicodeError:
            if (self.confirm('Codificação selecionada inválida para arquivo de entrada. Deseja continuar e ignorar este erro?')):
                return codecs.open(input_file, 'r', encoding=codification, errors='ignore')
            else:
                print('Cancelado.')
                exit(1)
        except Exception as e:
            print(f'Erro não tratado ao tentar abrir arquivo de entrada: {str(e)}')
            exit(1)
        


def main():
    parser = argparse.ArgumentParser(prog='HexImage Converter')
    parser.add_argument(
            '-i',
            '--input_file',
            help='Arquivo a ser verificado:',
            type=str
    )

    parser.add_argument(
            '-o',
            '--output_folder',
            help='Pasta de saída:',
            type=str
    )

    parser.add_argument(
            '-c',
            '--codification',
            help='Codificação do Arquivo:',
            choices=['latin1', 'utf8', 'cp1252'],
            default='utf8',
            type=str
    )

    parser.add_argument(
            '-d',
            '--delimiter',
            help='Delimitador do Arquivo:',
            default=';',
            type=str
    )

    args = parser.parse_args()
    try:
        if (vars(args).get('input_file') and vars(args).get('output_folder')):
            HexImageConverter(args.input_file, args.output_folder, args.codification, args.delimiter)
        else:
            raise AttributeError
    except AttributeError as e:
        print('Argumentos inválidos para execução.')
        exit(1)

main()