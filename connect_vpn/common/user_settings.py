import os
import yaml
from .resources import PATH_USER_SETTINGS_FILE
from connect_vpn.configuration_handler import ensure_configuration_exists


class UserSettings:
    def __init__(self):
        self.user_settings_path = str(PATH_USER_SETTINGS_FILE)
        self.auto_connect_when_launched = False
        self._settings = {
            'auto_connect_when_launched': False,
        }
        self.restore_last_user_settings()

    def restore_last_user_settings(self):
        ensure_configuration_exists(self.user_settings_path, self._settings)

        with open(self.user_settings_path, 'r') as stream:
            self._settings = yaml.safe_load(stream)

        self.auto_connect_when_launched = self._settings['auto_connect_when_launched']

    def saver_user_changes(self):
        self._settings['auto_connect_when_launched'] = self.auto_connect_when_launched

        with open(self.user_settings_path, 'w') as file:
            yaml.dump(self._settings, file)
