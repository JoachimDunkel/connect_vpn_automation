import signal

import pexpect
import sys
import time
import os

from urllib.request import urlopen
import re as r
from credentials import *


def _get_public_ip():
    d = str(urlopen('http://checkip.dyndns.com/').read())
    return r.compile(r'Address: (\d+\.\d+\.\d+\.\d+)').search(d).group(1)


class VPNConnector:
    def __init__(self, on_already_connected_by_other_process, on_connection_failed, on_connection_established, debug=False):
        self.child_process: pexpect.spawn = None
        self.on_already_connected_by_other_process = on_already_connected_by_other_process
        self.on_connection_failed = on_connection_failed
        self.on_connection_established = on_connection_established
        self.debug = debug

    def stop_connection(self):
        if self.child_process is not None:
            self.child_process.kill(signal.SIGTERM)
            self.child_process.wait()

    def establish_connection(self):
        ip_address = _get_public_ip()
        if ip_address == VPN_PUB_IP:
            self.on_already_connected_by_other_process(ip_address)

        self.child_process = pexpect.spawn(OPENVPN_SCRIPT_PATH)
        if self.debug:
            self.child_process.logfile = sys.stdout.buffer

        print("Starting VPN")
        self.child_process.expect_exact('[sudo] password for {}: '.format(UBUNTU_USER))
        self.child_process.sendline(SUDO_PW)
        self.child_process.expect_exact('Enter Auth Username: ')
        self.child_process.sendline(USER_NAME)
        self.child_process.expect_exact('Enter Auth Password: ')
        self.child_process.sendline(USER_PW)

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

    connector = VPNConnector(on_already_connected, on_failure, on_success, debug=True)

    connector.establish_connection()
    connector.child_process.wait()
