from pathlib import Path
import os
from enum import Enum


def _path_to_project_root(project_name):
    path = os.getcwd()
    while not str(path).endswith(project_name):
        path = Path(path).parent

    return path


CREDENTIALS_FILE_NAME = 'configure_connection.yaml'
PROJECT_ROOT_NAME = 'connect_vpn_automation'
PATH_ROOT_DIR = Path(_path_to_project_root(PROJECT_ROOT_NAME))
PATH_SRC = PATH_ROOT_DIR / 'connect_vpn'
PATH_CREDENTIALS_FILE = PATH_ROOT_DIR / CREDENTIALS_FILE_NAME
PATH_HOME_DIR = Path(os.path.expanduser('~'))
PATH_BASH_ALIASES = PATH_HOME_DIR / '.bash_aliases'
PATH_CONNECT_VPN = PATH_ROOT_DIR / 'connect_vpn.bash'
PATH_DATA_DIR = PATH_ROOT_DIR / 'data'
PATH_IP2LOCATION_DB = PATH_DATA_DIR / 'IP2LOCATION-LITE-DB11.BIN'


class ApplicationStatus(Enum):
    DISCONNECTED = 0
    CONNECTED = 1
    CONNECTED_BY_OTHER_PROCESS = 2


ESTABLISH_CONNECTION = 'Connect to VPN'
STOP_CONNECTION = 'Disconnect from VPN'

ESTABLISHED_CONNECTION_FORMAT = 'Established connection to: {}'
STOPPED_CONNECTION = 'Stopped vpn connection.'

OTHER_PROCESS_HOLDS_CONNECTION_FORMAT = "Your public ipv4 is: {} \nSeems like you already connected to the " \
                                        "vpn.\nExiting"

READING_CREDENTIALS_FAILED = "Can not read credentials. Make sure they are provided as expected in the " \
                             "configure_connection.yaml\nExiting"

OTHER_CONNECTION_FAILURE_FORMAT = "FAILURE - Unable to establish connection.\nException:\n{}"
