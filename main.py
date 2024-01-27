import os
import time
from colorama import Fore, Style

from functions import *
from constants import *

def take_option(max:int, min:int, text:str = 'Selecciona una opción: ') -> int:
    '''Pregunta al usuario que opción quiere y la devuelve'''
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


def upload_document_menu() -> None:
    '''
    Menú para Subir un archivo markdown a la Base de Datos.
    - Muestra los archivos markdown disponibles en el directorio local, si no hay ninguno, se sale.
    - Pregunta al usuario que archivo quiere almacenar.
    * Si el archivo ya existe en la Base de Datos, pregunta si quiere reemplazarlo.
    - Almacena el archivo en la Base de Datos llamando a la función upload_document().
    '''
    os.system('cls')
    print(f'{Style.BRIGHT}# SUBIDA DE ARCHIVOS #{Style.NORMAL}')
    print(f'{Style.BRIGHT}# Archivos markdown encontrados:{Style.NORMAL}\n | ID | Nombre de Archivo |')

    # Recorre todos los archivos en el directorio especificado y los pinta
    files_md: dict = {} # Guarda las ids reales de los archivos markdown sobre las ids del menu (1, 2, 3...)
    number_files_md: int = 0 # Para enumerarlos 1, 2, 3...
    for real_file_id, filename in enumerate(os.listdir(directorio)):
        if filename.endswith('.md'):
            number_files_md += 1
            files_md[number_files_md] = (real_file_id, filename)
            print(f'   {Fore.YELLOW}{Style.BRIGHT}{number_files_md}.{Fore.RESET}{Style.NORMAL}   {filename}')
    
    # Comprueba si hay archivos markdown disponibles en el directorio
    if number_files_md == 0: 
        print(f'    {Fore.BLACK}{Style.BRIGHT}-. {Style.NORMAL}Sin archivos{Fore.RESET}\n {GETTING_BACK_TEXT}')
        time.sleep(3)
        return
    else:
        print(f'\n {Fore.BLACK}{Style.BRIGHT}0. {Style.NORMAL}si no quieres almacenar ningún archivo.{Fore.RESET}')
        file_id = take_option(number_files_md, 0) # Pregunta al usuario que archivo quiere almacenar
    
    if file_id == 0:
        print(f'{OK_TEXT} ¡No se almacenó ningún archivo!\n {GETTING_BACK_TEXT}')
        time.sleep(2)
        return
    else:
        # Comprueba si el archivo ya existe en la Base de Datos
        filename = files_md[file_id][1]
        if connection_markdown.count_documents('name', filename) > 0:
            print(f'{ERROR_TEXT} Ese archivo ya existe en la Base de Datos')
            replace = True # Pregunta si quiere reemplazarlo por el existente
            while replace:
                replace_question = input(f'¿Quieres reemplazarlo? (s/n): ')
                if replace_question.lower() == 's':
                    print(replace_document(files_md, file_id))
                    input('Presiona enter para continuar...')
                elif replace_question.lower() == 'n':
                    print(f'{OK_TEXT} ¡No se almacenó ningún archivo!')
                    replace = False
                print(f' {GETTING_BACK_TEXT}')
                time.sleep(2)
                return
        else:
            with open(os.path.join(directorio, filename), 'r') as file: # Lee el archivo
                content = file.read() 
            # Almacena el contenido del archivo en MongoDB
            document = {'name': filename, 'content': content}
            connection_markdown.upload_document(document)
            print(f'{OK_TEXT} ¡Archivos almacenados con éxito en Base de Datos!')
        print(f' {GETTING_BACK_TEXT}')
        time.sleep(2)
        return 


def reeplace_document_menu() -> None:
    '''
    Menú para Reemplazar un archivo markdown en la Base de Datos.
    - Muestra los archivos markdown disponibles en el directorio que 
    además coinciden en nombre con alguno de la Base de Datos, si no hay ninguno, se sale.
    - Reemplaza el contenido del archivo en la Base de Datos llamando a la función replace_document().
    '''
    os.system('cls')
    print(f'{Style.BRIGHT}# REEMPLAZO DE ARCHIVOS #:{Style.NORMAL}')
    print(f'{Style.BRIGHT}# Archivos markdown coincidentes:{Style.NORMAL}\n | ID | Nombre de Archivo |')

    files_md: dict = {} # Guarda las ids reales de los archivos markdown sobre las ids del menu (1, 2, 3...)
    number_files_md: int = 0 # Para enumerarlos 1, 2, 3...
    for real_file_id, filename in enumerate(os.listdir(directorio)):
        if filename.endswith('.md'):
            if connection_markdown.count_documents('name', filename) > 0:
                number_files_md += 1
                files_md[number_files_md] = (real_file_id, filename)
                print(f'   {Fore.YELLOW}{Style.BRIGHT}{number_files_md}.{Fore.RESET}{Style.NORMAL}   {filename}')
    
    if number_files_md == 0: 
        print(f'    {Fore.BLACK}{Style.BRIGHT}-. {Style.NORMAL}Sin Archivos Coincidentes{Fore.RESET}\n {GETTING_BACK_TEXT}')
        time.sleep(3)
        return
    # Pregunta al usuario que archivo quiere reemplazar
    print(f'\n {Fore.BLACK}{Style.BRIGHT}0. {Style.NORMAL}si no quieres reemplazar ningún archivo.{Fore.RESET}')
    menu_file_id = take_option(number_files_md, 0, 'Selecciona el archivo a reemplazar: ') 
    if menu_file_id == 0:
        print(f'{OK_TEXT} ¡No se reemplazó ningún archivo!\n {GETTING_BACK_TEXT}')
        time.sleep(3)
        return
    else:
        print(replace_document(files_md, menu_file_id))
        input('Presiona enter para continuar...')
        print(f' {GETTING_BACK_TEXT}')
        time.sleep(2)
        return


def delete_document_menu() -> None:
    '''
    Menú para Eliminar un archivo markdown de la Base de Datos.
    - Muestra los todos archivos disponibles en la Base de Datos, si no hay ninguno, se sale.
    - Pregunta al usuario que archivo quiere eliminar y si está seguro.
    - Elimina el archivo de la Base de Datos llamando a la función delete_document().
    * No importa el tipo de archivo.
    '''
    os.system('cls')
    print(f'{Style.BRIGHT}# ELIMINACIÓN DE ARCHIVOS #:{Style.NORMAL}')
    print(f'{Style.BRIGHT}# Archivos en la Base de Datos:{Style.NORMAL}\n | ID | Nombre de Archivo |')
    # Imprime todos los archivos de la Collection de la Base de Datos
    file_id_names = {} # id: nombre
    for menu_id, doc in enumerate (connection_markdown.show_all_for_key('name')):
        menu_id += 1
        nombre = doc['name']
        file_id_names[menu_id] = nombre
        print(f'   {Fore.YELLOW}{Style.BRIGHT}{menu_id}.{Fore.RESET}{Style.NORMAL}   {nombre}')

    if len(file_id_names) == 0: 
        print(f'    {Fore.BLACK}{Style.BRIGHT}-. {Style.NORMAL}Sin Archivos Coincidentes{Fore.RESET}\n {GETTING_BACK_TEXT}')
        time.sleep(3)
        return
    print(f'\n {Fore.BLACK}{Style.BRIGHT}0. {Style.NORMAL}si no quieres almacenar ningún archivo.{Fore.RESET}')
    file_for_delete = take_option(len(file_id_names), 0, 'Introduce el ID del archivo a eliminar: ')
    if file_for_delete == 0:
        print(f'{OK_TEXT} ¡No se eliminó ningún archivo!')   
    else:
        file_name = file_id_names[int(file_for_delete)]
        print(f'Vas a eliminar el archivo {file_name}')
        sure = input('¿Estás seguro? (s/n): ')
        if sure.lower() == 's':
            print(delete_document('name', file_name))
            input('Presiona enter para continuar...')
        else:
            print(f'{OK_TEXT} ¡No se eliminó ningún archivo!')
    print(f' {GETTING_BACK_TEXT}')
    time.sleep(2)
    return



def main():
    while True:
        os.system('cls')
        print(
            f'\n{Fore.BLUE}{Style.BRIGHT}# MARCKDOWN x MONGODB #:{Fore.RESET}{Style.NORMAL} '
            f'\n{Fore.YELLOW}{Style.BRIGHT}1.{Fore.RESET}{Style.NORMAL} Subir un archivo'
            f'\n{Fore.YELLOW}{Style.BRIGHT}2.{Fore.RESET}{Style.NORMAL} Reemplazar un archivo'
            f'\n{Fore.YELLOW}{Style.BRIGHT}3.{Fore.RESET}{Style.NORMAL} Eliminar un archivo'
            f'\n{Fore.YELLOW}{Style.BRIGHT}4.{Fore.RESET}{Style.NORMAL} Salir'
        )
        option = take_option(4, 1)
        if option == 1:
            upload_document_menu()
        elif option == 2:
            reeplace_document_menu()
        elif option == 3:
            delete_document_menu()
        elif option == 4:
            print(f'{OK_TEXT} ¡Hasta luego! 😯')
            break
            

main()