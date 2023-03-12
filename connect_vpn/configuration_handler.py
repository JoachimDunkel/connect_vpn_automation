from .common import resources as res
import os
import yaml

CONFIGURATION_FORMAT = {
    'SUDO_PW': '',
    'USER_NAME': '',
    'USER_PW': '',
    'VPN_PUB_IP': '',
    'OPENVPN_SCRIPT_PATH': '~/bin/ovpn-KNAPP-AG_GRAZ'
}


def ensure_configuration_exists(config_path, config_format):
    created_anew = False
    if not os.path.exists(config_path):
        with open(config_path, 'w') as file:
            yaml.dump(config_format, file)

        created_anew = True
    return created_anew


def _ensure_config_value_provided(source_param, failure_msg):

    if source_param == '':
        print("All parameters in {} need correct values in order for this login automation to work properly.\n{}"
              .format(res.PATH_CREDENTIALS_FILE, failure_msg))
        exit(-1)

    return source_param


def read_credentials(connection_backend):
    created_anew = ensure_configuration_exists()
    if created_anew:
        print("Please fill out all the necessary credentials for your openvpn-login in:\n{}\n".format(
            res.PATH_CREDENTIALS_FILE))
        exit(-1)

    with open(str(res.PATH_CREDENTIALS_FILE), 'r') as stream:
        try:
            credentials = yaml.safe_load(stream)

            connection_backend.config.VPN_PUB_IP = _ensure_config_value_provided(credentials['VPN_PUB_IP'], "Please provide the expected ipv4 address of your desired vpn to: VPN_PUB_IP")
            connection_backend.config.OPENVPN_SCRIPT_PATH = _ensure_config_value_provided(credentials['OPENVPN_SCRIPT_PATH'], "Please provide a correct path to your openvpn-script to: OPENVPN_SCRIPT_PATH")
            connection_backend.config.SUDO_PW = _ensure_config_value_provided(credentials['SUDO_PW'], "Please provide a correct sudo-pw to: SUDO_PW")
            connection_backend.config.USER_NAME = _ensure_config_value_provided(credentials['USER_NAME'], "Please provide the correct username to your openvpn login to: USER_NAME")
            connection_backend.config.USER_PW = _ensure_config_value_provided(credentials['USER_PW'], "Please provide the correct password to your openvpn login to: USER_PW")

        except yaml.YAMLError as e:
            connection_backend.on_read_credentials_failed()
