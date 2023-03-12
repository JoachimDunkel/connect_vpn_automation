import threading


class BackgroundTask:

    def __init__(self, target, args, on_succeeded=None, on_failed=None):
        self.on_succeeded = on_succeeded
        self.on_failed = on_failed
        self.target = target
        self.args = args
        self.thread = threading.Thread(target=self.task)

    def start(self):
        self.thread.start()

    def task(self):
        try:
            self.target(self.args)
            self.on_succeeded()
        except Exception as e:
            self.on_failed(e)
