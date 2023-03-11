from gi.repository import AppIndicator3


class IconStatusHandler:

    def __init__(self, app: AppIndicator3.Indicator):
        self.app = app
