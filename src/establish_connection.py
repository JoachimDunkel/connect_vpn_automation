import signal
import getpass
import pexpect
import sys
import os
from urllib.request import urlopen
import re as r
import yaml
from resources import *


def _get_public_ip():
    d = str(urlopen('http://checkip.dyndns.com/').read())
    return r.compile(r'Address: (\d+\.\d+\.\d+\.\d+)').search(d).group(1)


class VPNConnector:
    def __init__(self, on_read_credentials_failed, on_already_connected_by_other_process, on_connection_failed,
                 on_connection_established, debug=False):

        self.USER_PW: str = ""
        self.USER_NAME: str = ""
        self.SUDO_PW: str = ""
        self.OPENVPN_SCRIPT_PATH: str = ""
        self.VPN_PUB_IP = ""

        self.child_process: pexpect.spawn = None
        self.on_read_credentials_failed = on_read_credentials_failed
        self.on_already_connected_by_other_process = on_already_connected_by_other_process
        self.on_connection_failed = on_connection_failed
        self.on_connection_established = on_connection_established
        self.debug = debug

    def read_credentials(self):

        credentials_path = os.path.abspath(os.path.join(os.getcwd(), os.pardir)) + "/" + CREDENTIALS_FILE_NAME

        with open(credentials_path, 'r') as stream:
            try:
                credentials = yaml.safe_load(stream)

                self.VPN_PUB_IP = credentials['VPN_PUB_IP']
                self.OPENVPN_SCRIPT_PATH = credentials['OPENVPN_SCRIPT_PATH']
                self.SUDO_PW = credentials['SUDO_PW']
                self.USER_NAME = credentials['USER_NAME']
                self.USER_PW = credentials['USER_PW']

            except yaml.YAMLError as e:
                self.on_read_credentials_failed()

    def stop_connection(self):
        if self.child_process is not None:
            self.child_process.kill(signal.SIGTERM)
            self.child_process.wait()

    def establish_connection(self):
        ip_address = _get_public_ip()
        if ip_address == self.VPN_PUB_IP:
            self.on_already_connected_by_other_process(ip_address)
            return

        self.child_process = pexpect.spawn(self.OPENVPN_SCRIPT_PATH)
        if self.debug:
            self.child_process.logfile = sys.stdout.buffer

        print("Starting VPN")
        self.child_process.expect_exact('[sudo] password for {}: '.format(getpass.getuser()))
        self.child_process.sendline(self.SUDO_PW)
        self.child_process.expect_exact('Enter Auth Username: ')
        self.child_process.sendline(self.USER_NAME)
        self.child_process.expect_exact('Enter Auth Password: ')
        self.child_process.sendline(self.USER_PW)

        try:
            self.child_process.expect_exact('Initialization Sequence Completed')
            self.on_connection_established()
        except Exception as e:
            self.on_connection_failed()


if __name__ == "__main__":
    def on_success():
        print("SUCCESS - Connection established")


    def on_failure():
        print("FAILURE - Unable to establish connection.")


    def on_already_connected(ip_address):
        print("Your public ipv4 is: {} \nSeems like you already connected to the vpn.\nExiting ".format(ip_address))
        exit(-1)


    def read_credentials_failed():
        print("Can not read credentials. Make sure they are provided as expected in the "
              "configure_connection.yaml\nExiting")
        exit(-1)


    connector = VPNConnector(read_credentials_failed, on_already_connected, on_failure, on_success, debug=True)
    connector.read_credentials()
    connector.establish_connection()
    connector.child_process.wait()
