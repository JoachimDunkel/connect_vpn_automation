import subprocess
from threading import Thread

def start_script(arg):
    result = subprocess.run(["~/Desktop/test_bash_automation/user_input.sh",
                "joachim 1234"], shell=True)
    print(result.returncode)

script_thread = Thread(target = start_script, args = (10, ))

script_thread.start()

print("DONE")

# TODO it should create an independent process

# Create a gui and hook it up with the status bar above.

