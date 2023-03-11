import ctypes
import ctypes.util
import getpass
import signal
import sys
import pexpect

from .check_ip import get_public_ip
from .configuration_handler import read_credentials

PR_SET_PDEATHSIG = 1


def _set_pdeathsig():
    libc = ctypes.CDLL(ctypes.util.find_library('c'), use_errno=True)
    if libc.prctl(PR_SET_PDEATHSIG, signal.SIGKILL) != 0:
        raise OSError(ctypes.get_errno(), 'SET_PDEATHSIG')


class ConnectorBackend:
    def __init__(self, debug=False):

        self.USER_PW: str = ""
        self.USER_NAME: str = ""
        self.SUDO_PW: str = ""
        self.OPENVPN_SCRIPT_PATH: str = ""
        self.VPN_PUB_IP = ""

        self.child_process: pexpect.spawn = None
        self.debug = debug

    def setup(self, on_read_credentials_failed, on_already_connected_by_other_process,
              on_connection_failed, on_connection_established, on_connection_stopped):

        self.on_read_credentials_failed = on_read_credentials_failed
        self.on_already_connected_by_other_process = on_already_connected_by_other_process
        self.on_connection_failed = on_connection_failed
        self.on_connection_established = on_connection_established
        self.on_connection_stopped = on_connection_stopped

    def stop_connection(self):
        if self.child_process is not None:
            self.child_process.kill(signal.SIGTERM)
            self.child_process.wait()
            self.child_process = None
        self.on_connection_stopped()

    def establish_connection(self, curr_ip):
        self.check_connection_status(curr_ip)

        self.child_process = pexpect.spawn(self.OPENVPN_SCRIPT_PATH, preexec_fn=_set_pdeathsig)
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
            self.on_connection_failed(e)

    def check_connection_status(self, curr_ip):
        if curr_ip == self.VPN_PUB_IP:
            self.on_already_connected_by_other_process(curr_ip)


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


    connector = ConnectorBackend(read_credentials_failed, on_already_connected, on_failure, on_success, debug=True)
    read_credentials(connector)
    connector.establish_connection()
    connector.child_process.wait()
