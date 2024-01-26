import configparser
from colorama import Fore, Style

from connection import ConecctionMongoDB

config = configparser.ConfigParser()
config.read('config.ini')
# Datos de conexión a MongoDB Atlas
user:str = config['setup_connection']['mongodb_user']
password:str = config['setup_connection']['mongodb_pass']
cluster:str = config['setup_connection']['mongodb_cluster']
database:str = config['setup_connection']['mongodb_db']
collection:str = config['setup_connection']['mongodb_collection']

connection_markdown = ConecctionMongoDB(user, password, cluster, database, collection)

# Directorio donde se encuentran los archivos markdown
directorio:str = config['config_directory']['directory']

## Estilos
ERROR_TEXT = f'{Fore.RED}{Style.BRIGHT}ERROR{Fore.RESET}{Style.NORMAL}:'
OK_TEXT = f'{Fore.GREEN}{Style.BRIGHT}OK{Fore.RESET}{Style.NORMAL}:'
GETTING_BACK_TEXT = f'{Fore.BLACK}Volviento...{Style.NORMAL}'