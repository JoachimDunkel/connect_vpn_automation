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
PATH_CREDENTIALS_FILE = PATH_ROOT_DIR / CREDENTIALS_FILE_NAME

PATH_HOME_DIR = Path(os.path.expanduser('~'))

PATH_BASH_ALIASES = PATH_HOME_DIR / '.bash_aliases'

PATH_CONNECT_VPN = PATH_ROOT_DIR / 'connect_vpn.bash'

PATH_DATA_DIR = PATH_ROOT_DIR / 'data'

PATH_IP2LOCATION_DB = PATH_DATA_DIR / 'IP2LOCATION-LITE-DB11.BIN'