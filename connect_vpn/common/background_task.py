import threading


class CallbackTask:

    def __init__(self, target, args, on_succeeded=None, on_failed=None, is_daemon=True):
        self.on_succeeded = on_succeeded
        self.on_failed = on_failed
        self.target = target
        self.args = args
        self.thread = threading.Thread(target=self.task)
        self.thread.setDaemon(is_daemon)

    def start(self):
        self.thread.start()

    def task(self):
        try:
            self.target(self.args)
            self.on_succeeded()
        except Exception as e:
            self.on_failed(e)


