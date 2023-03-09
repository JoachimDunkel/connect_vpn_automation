import src.resources as res
import os
import yaml

_CONFIGURATION_FORMAT = {
    'SUDO_PW': '',
    'USER_NAME': '',
    'USER_PW': '',
    'VPN_PUB_IP': '',
    'OPENVPN_SCRIPT_PATH': '~/bin/ovpn-KNAPP-AG_GRAZ'
}


def ensure_configuration_exists():
    created_anew = False
    if not os.path.exists(str(res.PATH_CREDENTIALS_FILE)):
        with open(res.PATH_CREDENTIALS_FILE, 'w') as file:
            yaml.dump(_CONFIGURATION_FORMAT, file)

        created_anew = True
    return created_anew


def _ensure_config_value_provided(source_param, failure_msg):

    if source_param == '':
        print("All parameters in {} need correct values in order for this login automation to work properly.\n{}"
              .format(res.PATH_CREDENTIALS_FILE, failure_msg))
        exit(-1)

    return source_param


def read_credentials(vpn_connector):
    created_anew = ensure_configuration_exists()
    if created_anew:
        print("Please fill out all the necessary credentials for your openvpn-login in:\n{}\n".format(
            res.PATH_CREDENTIALS_FILE))
        exit(-1)

    with open(str(res.PATH_CREDENTIALS_FILE), 'r') as stream:
        try:
            credentials = yaml.safe_load(stream)

            vpn_connector.VPN_PUB_IP = _ensure_config_value_provided(credentials['VPN_PUB_IP'], "Please provide the expected ipv4 address of your desired vpn to: VPN_PUB_IP")
            vpn_connector.OPENVPN_SCRIPT_PATH = _ensure_config_value_provided(credentials['OPENVPN_SCRIPT_PATH'], "Please provide a correct path to your openvpn-script to: OPENVPN_SCRIPT_PATH")
            vpn_connector.SUDO_PW = _ensure_config_value_provided(credentials['SUDO_PW'], "Please provide a correct sudo-pw to: SUDO_PW")
            vpn_connector.USER_NAME = _ensure_config_value_provided(credentials['USER_NAME'], "Please provide the correct username to your openvpn login to: USER_NAME")
            vpn_connector.USER_PW = _ensure_config_value_provided(credentials['USER_PW'], "Please provide the correct password to your openvpn login to: USER_PW")

        except yaml.YAMLError as e:
            vpn_connector.on_read_credentials_failed()
