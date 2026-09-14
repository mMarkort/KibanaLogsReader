import json
from pathlib import Path
import sys

def get_config_path():
    if getattr(sys, "frozen", False):
        # Running from EXE
        base_dir = Path(sys.executable).resolve().parent
    else:
        # Running from .py
        base_dir = Path(__file__).resolve().parent.parent

    return base_dir / "Settings" / "config.json"


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