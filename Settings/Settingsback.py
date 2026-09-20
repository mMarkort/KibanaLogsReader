import json
from pathlib import Path
import sys

def get_config_path():
    #base_dir = Path(__file__).resolve().parent

    if getattr(sys, "frozen", False):
    # Running as EXE
        BASE_DIR = Path(sys.executable).resolve().parent
    else:
    # Running as Python
        BASE_DIR = Path(__file__).resolve().parent.parent

    CONFIG_FILE = BASE_DIR / "Settings" / "config.json"

    print(CONFIG_FILE)
    return CONFIG_FILE


CONFIG_FILE = get_config_path()


def load_config():
    if not CONFIG_FILE.exists():
        return {
            "login": "",
            "password": "",
            "url": "",
            "isAuth": ""
        }

    #TO USE IN OTHER FILES
    # config = load_config()
    # login = config["login"]
    # password = config["password"]
    # url = config["url"]

    with open(CONFIG_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def save_config(login, password, url, isAuth):

    config = {
        "login": login,
        "password": password,
        "url": url,
        "isAuth": isAuth
    }

    with open(CONFIG_FILE, "w", encoding="utf-8") as file:
        json.dump(
            config,
            file,
            indent=4,
            ensure_ascii=False
        )