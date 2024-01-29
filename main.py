import os
import sys
from pathlib import Path
from absl import app
from absl import flags
from colorama import Fore, Style

from config import parse_poster_config, OK_TEXT
from poster import DAIPoster
from posts import Post, Author

FLAGS = flags.FLAGS
flags.DEFINE_string("archivo", None, "El nombre del archivo del post.", required=False)
flags.DEFINE_string("nombre", None, "Tu nombre.", required=True)


def find_post_files(dirname: str, filename: str | None = None) -> list[Path] | None:
    cwd = Path.cwd()
    if filename and Path(cwd, dirname, filename).exists():
        return [Path(cwd, dirname, filename)]

    posts: list[Path] = []
    for fname in os.listdir(Path(cwd, dirname)):
        if not fname.endswith(".md"):
            continue
        posts.append(Path(cwd, dirname, fname))

    if len(posts) > 0:
        return posts

    return None

def get_file_content(paths: list[Path]) -> list[str]:
    contents = []
    for path in paths:
        with open(path, "r", encoding="utf-8") as file:
            contents.append(file.read())
    return contents


def main(argv):
    del argv  # Unused.

    print(
        f"{Fore.BLUE}{Style.BRIGHT}# MARCKDOWN x MONGODB #:{Fore.RESET}{Style.NORMAL}\n"
    )

    try :
        config_vals = parse_poster_config()
    except ValueError:
        print(
            "Algunos de los valores en el archivo config.ini están vacíos. "
            "Revisa que la configuración sea correcta."
        )


    post_files = find_post_files("posts", FLAGS.archivo)
    if not post_files:
        print(f"{Fore.BLACK}{Style.BRIGHT}-{Style.NORMAL}Sin archivos{Fore.RESET}\n")
        sys.exit(1)

    poster = DAIPoster(
        config_vals.dbuser,
        config_vals.dbhost,
        config_vals.dbname,
        config_vals.dbpwrd,
        False
    )
    author = Author(name=FLAGS.nombre)
    contents = get_file_content(post_files)
    posts = [
        Post(title="title", content=post, author=author) for post in contents
    ]

    result = poster.post(posts)
    if result is None:
        print("Reemplazar esto por un mensaje que diga que algo salió mal")
        sys.exit(1)

    print(f'{OK_TEXT} ¡Archivos almacenados con éxito en Base de Datos!')
    sys.exit(0)

if __name__ == "__main__":
    app.run(main)
