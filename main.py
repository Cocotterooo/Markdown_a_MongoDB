import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()
# Datos de conexión a MongoDB Atlas
usuario = os.getenv('MONGODB_USER')
contraseña = os.getenv('MONGODB_PASS')
nombre_base_datos = os.getenv('MONGODB_DB')
nombre_coleccion = os.getenv('MONGODB_COLLECTION')
cluster = os.getenv('MONGODB_CLUSTER')

# Conexión a MongoDB Atlas
uri_conexion = f'mongodb+srv://{usuario}:{contraseña}@{cluster}/{nombre_base_datos}?retryWrites=true&w=majority'
client = MongoClient(uri_conexion)
db = client[nombre_base_datos]
collection = db[nombre_coleccion]

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
with open(os.path.join(directorio, filename), 'r') as file:
    contenido = file.read()
    # Almacena el contenido del archivo en MongoDB
    documento = {'name': filename, 'content': contenido}
    collection.insert_one(documento)

print('¡Archivos almacenados con éxito en MongoDB Atlas!')
