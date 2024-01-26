import os
from dotenv import load_dotenv
from connection import ConecctionMongoDB
from colorama import Fore, Style

load_dotenv()
# Datos de conexión a MongoDB Atlas
user = os.getenv('MONGODB_USER')
password = os.getenv('MONGODB_PASS')
database = os.getenv('MONGODB_DB')
collection = os.getenv('MONGODB_COLLECTION')
cluster = os.getenv('MONGODB_CLUSTER')

connection_markdown = ConecctionMongoDB(user, password, cluster, database, collection)

# Directorio donde se encuentran los archivos markdown
directorio = 'Directorio_markdowns'


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