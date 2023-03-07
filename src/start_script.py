import subprocess

import signal
import threading

# TODO should return the process id that can later be used to kill the process


def start_script():
    command = ["bash", "/home/jd/git/private/connect_vpn_automation/test_bash_automation/automation.sh"]

    # start the subprocess and continue executing the Python program
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    try:
        print("waiting for process")
        # stdout, stderr = process.communicate()
        process.wait(timeout=3)
        # print("Stdout: ", stdout.decode())
    except subprocess.TimeoutExpired:
        print("Dont want to wait anymore")
        # Signal the process to terminate
        process.send_signal(signal.SIGTERM)  #SIGINT) # which to use?
        # Wait for the process to terminate
        process.wait(timeout=10)


