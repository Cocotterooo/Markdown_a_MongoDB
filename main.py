import os
import time
from colorama import Fore, Style

from connection import ConecctionMongoDB
from reeplace import reeplace_document, result_replace_document
from constants import *


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


def upload_document() -> None:
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
        print(f'{OK_TEXT}: ¡No se almacenó ningún archivo!\n {GETTING_BACK_TEXT}')
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
                    result_replace_document(files_md, file_id)
                elif replace_question.lower() == 'n':
                    print(f'{OK_TEXT}: ¡No se almacenó ningún archivo!\n {GETTING_BACK_TEXT}')
                time.sleep(2)
                return
        else:
            with open(os.path.join(directorio, filename), 'r') as file: # Lee el archivo
                content = file.read() 
            # Almacena el contenido del archivo en MongoDB
            document = {'name': filename, 'content': content}
            connection_markdown.upload_document(document)
            print(f'{OK_TEXT}: ¡Archivos almacenados con éxito en Base de Datos!')
        print(f' {GETTING_BACK_TEXT}')
        time.sleep(2)
        return 


def reeplace_document_menu() -> None:
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
    print(f'\n {Fore.BLACK}{Style.BRIGHT}0. {Style.NORMAL}si no quieres reemplazar ningún archivo.{Fore.RESET}')
    menu_file_id = take_option(number_files_md, 0, 'Selecciona el archivo a reemplazar: ') # Pregunta al usuario que archivo quiere reemplazar
    if menu_file_id == 0:
        print(f'{OK_TEXT}: ¡No se reemplazó ningún archivo!\n {GETTING_BACK_TEXT}')
        time.sleep(3)
        return
    else:
        result_replace_document(files_md, menu_file_id)
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
        error = True
        while error:
            try:
                option = int(input(f'{Style.BRIGHT}#{Style.NORMAL} Introduce una opción: '))
                if option > 4 or option < 1:
                    print('¡Debes ingresar un número válido!')
                else:
                    error = False
            except ValueError:
                print(f'{ERROR_TEXT} Debes ingresar un número.')
        if option == 1:
            upload_document()
        elif option == 2:
            reeplace_document_menu()
        elif option == 4:
            print(f'{OK_TEXT} ¡Hasta luego! 😯')
            break
            

main()