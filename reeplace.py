from constants import *
import time
import os

def reeplace_document(file_id) -> dict:
    filename = os.listdir(directorio)[file_id]
    try:
        with open(os.path.join(directorio, filename), 'r') as file: # Lee el archivo
            new_content = file.read()
        # Reemplaza el contenido del archivo en la Base de Datos
        connection_markdown.update_document('name', filename, 'content', new_content)
        return (True, None)
    except Exception as e:
        return (False, e)


def result_replace_document(files_md, menu_file_id) -> None:
    document = files_md[menu_file_id]
    replace_sucefully = reeplace_document(document[0])
    if replace_sucefully[0] == True:
        print(f'{OK_TEXT} ¡Archivo {document[1]} reemplazado con éxito en la Base de Datos!')
        print(f' {GETTING_BACK_TEXT}')
    else:
        print(f'{ERROR_TEXT} ¡No se pudo reemplazar el archivo! ({replace_sucefully[False]})')
        print(f' {GETTING_BACK_TEXT}')
    time.sleep(3)
    return