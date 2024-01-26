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


def delete_document(key:str, filename:str) -> str:
    try:
        connection_markdown.delete_document(key, filename)
        return f'{OK_TEXT} ¡Archivo {filename} eliminado de la Base de Datos con éxito!'
    except Exception as e:
        return f'{ERROR_TEXT} ¡No se pudo eliminar el archivo! ({e})'


def take_option(max:int, min:int, text:str = 'Selecciona una opción:') -> int:
    error = True
    while error:
        try:
            option = int(input(f'{Style.BRIGHT}#{Style.NORMAL} {text}'))
            if option > max or option < min:
                print(f'{ERROR_TEXT} Debes ingresar un número válido!')
            else:
                error = False
        except ValueError:
            print(f'{ERROR_TEXT} Debes ingresar un número.')
    return option