import ctypes
import ctypes.util
import getpass
import signal
import sys
import pexpect
from .common.tasks import CallbackTask

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
        self.ensure_child_stopped()
        self.on_connection_stopped()

    def handle_connection_failed(self):
        self.ensure_child_stopped()
        self.on_connection_failed()

    def ensure_child_stopped(self):
        if self.child_process is not None:
            try:
                self.child_process.close()
            except Exception as _:
                self.child_process.kill(signal.SIGTERM)
            self.child_process.wait()
            self.child_process = None

    def _connect(self, args):
        self.child_process = pexpect.spawn(self.OPENVPN_SCRIPT_PATH, preexec_fn=_set_pdeathsig)
        if self.debug:
            self.child_process.logfile = sys.stdout.buffer

        self.child_process.expect_exact('[sudo] password for {}: '.format(getpass.getuser()))
        self.child_process.sendline(self.SUDO_PW)
        self.child_process.expect_exact('Enter Auth Username: ')
        self.child_process.sendline(self.USER_NAME)
        self.child_process.expect_exact('Enter Auth Password: ')
        self.child_process.sendline(self.USER_PW)
        self.child_process.expect_exact('Initialization Sequence Completed')

    def establish_connection(self, curr_ip):
        self.check_connection_status(curr_ip)
        self.connect_task = CallbackTask(self._connect, [], on_succeeded=self.on_connection_established,
                                         on_failed=self.handle_connection_failed)
        self.connect_task.start()

    def check_connection_status(self, curr_ip):
        if curr_ip == self.VPN_PUB_IP:
            self.on_already_connected_by_other_process(curr_ip)
