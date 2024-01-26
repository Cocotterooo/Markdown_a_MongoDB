import os
from dotenv import load_dotenv
from connection import ConecctionMongoDB

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
print('Archivos markdown encontrados:')
for file_id, filename in enumerate(os.listdir(directorio)):
    if filename.endswith('.md'):
        print(f'{file_id+1}. {filename}')

error = True
while error:
    try:
        file_id = int(input('¿Qué archivo desea almacenar en la Base de Datos? '))
        if file_id > len(os.listdir(directorio)) or file_id < 0:
            print('¡Debes ingresar un número válido!')
        else:
            error = False
    except ValueError:
        print('¡Debes ingresar un número!')

if file_id == 0:
    print('¡No se almacenó ningún archivo en la Base de Datos!')
    exit()

filename = os.listdir(directorio)[file_id-1]
if connection_markdown.count_documents('name', filename) > 0:
    print('ERROR: El archivo ya existe en la Base de Datos')
else:
    with open(os.path.join(directorio, filename), 'r') as file: # Lee el archivo
        content = file.read() 
    # Almacena el contenido del archivo en MongoDB
    document = {'name': filename, 'content': content}
    connection_markdown.upload_document(document)
    print('¡Archivos almacenados con éxito en MongoDB Atlas!')

exit()