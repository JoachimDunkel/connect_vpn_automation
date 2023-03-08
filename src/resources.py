from pathlib import Path
import os


def _path_to_project_root(project_name):
    path = os.getcwd()
    while not str(path).endswith(project_name):
        path = Path(path).parent

    return path


CREDENTIALS_FILE_NAME = 'configure_connection.yaml'
PROJECT_ROOT_NAME = 'connect_vpn_automation'

PATH_ROOT_DIR = Path(_path_to_project_root(PROJECT_ROOT_NAME))
PATH_SRC = PATH_ROOT_DIR / 'src'
PATH_IMAGES = PATH_ROOT_DIR / 'images'

PATH_POWER_BTN_IMG = PATH_IMAGES / 'power_button_icon.png'

