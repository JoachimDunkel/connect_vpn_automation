import gi

gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')
gi.require_version('Notify', '0.7')
from gi.repository import Gtk as gtk
from gi.repository import AppIndicator3 as appindicator

from connect_vpn.common import resources
from connect_vpn.ui.settings_ui import SettingsWindow


class AppIndicatorToggle:

    def __init__(self):
        self.ind = appindicator.Indicator.new("example-simple-client",
                                              "indicator-messages",
                                              appindicator.IndicatorCategory.SYSTEM_SERVICES)

        # self.app = AppIndicator3.Indicator.new(self.APPINDICATOR_ID, str(resources.PATH_VPN_ICON_DISCONNECTED),
        #                                        AppIndicator3.IndicatorCategory.SYSTEM_SERVICES)
        self.ind.set_status(appindicator.IndicatorStatus.ACTIVE)
        # self.app.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
        self.ind.set_attention_icon("indicator-messages-new")

        # Set the initial image
        self.current_image = str(resources.PATH_VPN_ICON_ESTABLISH_CONNECTION_1)

        self.ind.set_icon(self.current_image)
        self.menu = gtk.Menu()

        # Add settings window
        self.settings_window = SettingsWindow(self.ind)
        show_settings = gtk.MenuItem(label="Settings")
        show_settings.connect("activate", self.settings_window.show)
        self.menu.append(show_settings)

        self.menu.show_all()
        self.ind.set_menu(self.menu)


if __name__ == "__main__":
    indicator = AppIndicatorToggle()
    gtk.main()
