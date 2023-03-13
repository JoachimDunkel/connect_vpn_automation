from pathlib import Path
import os
from enum import Enum


def _path_to_project_root(project_name):
    path = os.getcwd()
    while not str(path).endswith(project_name):
        path = Path(path).parent

    return path


PROJECT_ROOT_NAME = 'connect_vpn_automation'
PATH_ROOT_DIR = Path(_path_to_project_root(PROJECT_ROOT_NAME))
PATH_CONFIG_DIR = PATH_ROOT_DIR / 'config'
PATH_SRC = PATH_ROOT_DIR / 'connect_vpn'
PATH_CREDENTIALS_FILE = PATH_CONFIG_DIR / 'configure_connection.yaml'
PATH_USER_SETTINGS_FILE = PATH_CONFIG_DIR / 'user_settings.yaml'

PATH_UI_DIR = PATH_SRC / 'ui'
PATH_SETTINGS_UI_GLADE = PATH_UI_DIR / 'settings_ui.glade'

PATH_HOME_DIR = Path(os.path.expanduser('~'))
PATH_BASH_ALIASES = PATH_HOME_DIR / '.bash_aliases'
PATH_CONNECT_VPN = PATH_ROOT_DIR / 'connect_vpn'
PATH_DATA_DIR = PATH_CONNECT_VPN / 'data'
PATH_IP2LOCATION_DB = PATH_DATA_DIR / 'IP2LOCATION-LITE-DB11.BIN'

PATH_IMAGES = PATH_CONNECT_VPN / 'images'
PATH_VPN_ICON_DISCONNECTED = PATH_IMAGES / 'key_white.png'
PATH_VPN_ICON_CONNECTED = PATH_IMAGES / 'key_green.png'
PATH_VPN_ICON_ESTABLISH_CONNECTION_1 = PATH_IMAGES / "key_white.png"
PATH_VPN_ICON_ESTABLISH_CONNECTION_2 = PATH_IMAGES / 'grey_green.png'

LAUNCH_DESKTOP_FILENAME = 'connect_vpn.desktop'
PATH_LAUNCH_DESKTOP_FILE = PATH_ROOT_DIR / LAUNCH_DESKTOP_FILENAME
PATH_USR_LOCAL_SHARE = Path('/usr/local/share/applications') / LAUNCH_DESKTOP_FILENAME

PATH_BIN_DIR = PATH_ROOT_DIR / 'bin'
RUN_CONNECT_VPN_SCRIPT = './connect_vpn'
RUN_ONE_TIME_SETUP_SCRIPT = './one_time_setup'


class ApplicationStatus(Enum):
    DISCONNECTED = 0
    CONNECTED = 1
    CONNECTED_BY_OTHER_PROCESS = 2


ESTABLISH_CONNECTION = 'Connect to VPN'
STOP_CONNECTION = 'Disconnect from VPN'

ESTABLISHED_CONNECTION_FORMAT = 'Established connection to: {}'
STOPPED_CONNECTION = 'Stopped vpn connection.'

OTHER_PROCESS_HOLDS_CONNECTION_FORMAT = "Your ip: {} \n You are already connected.\nExiting"

READING_CREDENTIALS_FAILED = "Can not read credentials. Make sure they are provided as expected in the " \
                             "configure_connection.yaml\nExiting"

OTHER_CONNECTION_FAILURE_FORMAT = "FAILURE - Unable to establish connection.\nException:\n{}"
SETTINGS_BTN_LABEL = "Settings"
