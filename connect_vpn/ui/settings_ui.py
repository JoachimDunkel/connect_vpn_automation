import gi

gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')
from gi.repository import Gtk
from connect_vpn.common.user_settings import UserSettings


class SettingsWindow:
    def __init__(self, app_indicator, on_window_closed, on_submit_changes):
        self.app_indicator = app_indicator
        self.user_settings = UserSettings()
        self.handlers = {
            "on_quit_btn_clicked": self.on_quit,
            "on_apply_btn_clicked": self.on_apply,
            "on_ok_btn_clicked": self.on_ok,
            "auto_connect_on_launch_toggled": self.on_auto_connect_toggled,
        }

    def on_quit(self, btn):
        print("Quit")

    def on_ok(self, btn):
        self.user_settings.saver_user_changes()
        print("Ok")

    def on_apply(self, btn):
        self.user_settings.saver_user_changes()
        print("Apply")

    def on_auto_connect_toggled(self, check_btn):
        self.user_settings.auto_connect_when_launched = check_btn.get_active()

    def show(self, caller):  # caller = appindicator
        builder = Gtk.Builder()
        builder.add_from_file("settings_ui.glade")
        builder.connect_signals(self.handlers)

        auto_connect_on_launch_check_box = builder.get_object('auto_connect_when_launched_check_box')
        auto_connect_on_launch_check_box.set_active(self.user_settings.auto_connect_when_launched)

        self.window = builder.get_object("settings_window")
        self.window.set_title("VPN - Connect")
        self.window.show()
        return self.window


if __name__ == "__main__":
    settings_window = SettingsWindow(None, None, None)
    settings_window.show(None)
    Gtk.main()
