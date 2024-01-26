from constants import *
import os

def replace_document(files_md:dict, menu_file_id) -> str:
    document = files_md[menu_file_id] # id, filename
    filename = document[1]
    try:
        with open(os.path.join(directorio, filename), 'r') as file: # Lee el archivo
            new_content = file.read()
        # Reemplaza el contenido del archivo en la Base de Datos
        connection_markdown.update_document('name', filename, 'content', new_content)
        return f'{OK_TEXT} ¡Archivo {filename} reemplazado con éxito en la Base de Datos!'
    except Exception as e:
        return f'{ERROR_TEXT} ¡No se pudo reemplazar el archivo! ({e})'
