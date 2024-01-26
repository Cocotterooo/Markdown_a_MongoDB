import os
import configparser
from colorama import Fore, Style

from connection import ConecctionMongoDB

config = configparser.ConfigParser()
config.read('config.ini')
# Datos de conexión a MongoDB Atlas
user = config['setup_connection']['mongodb_user']
password = config['setup_connection']['mongodb_pass']
cluster = config['setup_connection']['mongodb_cluster']
database = config['setup_connection']['mongodb_db']
collection = config['setup_connection']['mongodb_collection']

connection_markdown = ConecctionMongoDB(user, password, cluster, database, collection)

# Directorio donde se encuentran los archivos markdown
directorio = config['config_directory']['directory']


# Recorre todos los archivos en el directorio especificado
print(f'{Style.BRIGHT}# Archivos markdown encontrados:{Style.NORMAL}\n | ID | Nombre de Archivo |')
for file_id, filename in enumerate(os.listdir(directorio)):
    if filename.endswith('.md'):
        print(f'   {Fore.YELLOW}{Style.BRIGHT}{file_id+1}.{Fore.RESET}{Style.NORMAL}   {filename}')

print(f'\n {Fore.BLACK}{Style.BRIGHT}0. {Style.NORMAL}si no quieres almacenar ningún archivo.{Fore.RESET}')

error = True
while error:
    try:
        file_id = int(input(f'{Style.BRIGHT}#{Style.NORMAL} Introduce la ID del archivo que deseas almacenar: '))
        if file_id > len(os.listdir(directorio)) or file_id < 0:
            print('¡Debes ingresar un número válido!')
        else:
            error = False
    except ValueError:
        print(f'{Fore.RED}{Style.BRIGHT}ERROR{Fore.RESET}{Style.NORMAL}: Debes ingresar un correspondiente a un archivo.')

if file_id == 0:
    print(f'{Fore.GREEN}{Style.BRIGHT}OK{Fore.RESET}{Style.NORMAL}: ¡No se almacenó ningún archivo!')
    exit()

filename = os.listdir(directorio)[file_id-1]
if connection_markdown.count_documents('name', filename) > 0:
    print(f'{Fore.RED}{Style.BRIGHT}ERROR{Fore.RESET}{Style.NORMAL}: El archivo ya existe en la Base de Datos')
else:
    with open(os.path.join(directorio, filename), 'r') as file: # Lee el archivo
        content = file.read() 
    # Almacena el contenido del archivo en MongoDB
    document = {'name': filename, 'content': content}
    connection_markdown.upload_document(document)
    print(f'{Fore.GREEN}{Style.BRIGHT}OK{Fore.RESET}{Style.NORMAL}: ¡Archivos almacenados con éxito en MongoDB Atlas!')

exit()