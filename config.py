import json
from pathlib import Path
from dataclasses import dataclass
from colorama import Fore, Style

@dataclass
class PosterConfig:
    """Dataclass for `config.json` file data"""
    dbuser: str
    dbpwrd: str
    dbhost: str
    dbname: str

def parse_poster_config():
    """Parses the `config.json` file into a `PosterConfig` dataclass."""
    cwd = Path.cwd()
    if not Path(cwd, "config.json").exists():
        raise FileNotFoundError("Missing config.json file")

    with open(Path(cwd, "config.json"), "r", encoding="utf-8") as config_file:
        config = json.loads(config_file.read())
        user = config["database"]["user"]
        pwrd = config["database"]["password"]
        host = config["database"]["host"]
        name = config["database"]["name"]

    if not (user and pwrd and host, name):
        raise ValueError
    return PosterConfig(user, pwrd, host, name)


# This shouldn't be here but I'll leave this for now. Looks very messy and has typos
ERROR_TEXT = f'{Fore.RED}{Style.BRIGHT}ERROR{Fore.RESET}{Style.NORMAL}:'
OK_TEXT = f'{Fore.GREEN}{Style.BRIGHT}OK{Fore.RESET}{Style.NORMAL}:'
GETTING_BACK_TEXT = f'{Fore.BLACK}Volviento...{Style.NORMAL}'
