import threading
import gi

gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')
gi.require_version('Notify', '0.7')
from gi.repository import Gtk as gtk
from gi.repository import AppIndicator3 as appindicator
from gi.repository import GLib

from connect_vpn.common import resources
from check_ip import get_public_ip


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

        # Load two images to toggle between
        self.image1 = str(resources.PATH_VPN_ICON_ESTABLISH_CONNECTION_1)
        self.image2 = str(resources.PATH_VPN_ICON_ESTABLISH_CONNECTION_2)

        # Set the initial image
        self.current_image = self.image1

        self.toggle_icon = True
        self.ind.set_icon(self.current_image)
        self.menu = gtk.Menu()
        ip_addr_item = gtk.MenuItem(label=get_public_ip())
        ip_addr_item.connect("activate", self.stop_thread)
        self.menu.append(ip_addr_item)
        self.menu.show_all()
        self.ind.set_menu(self.menu)


    def update(self):
        print("Updating")
        self.ind.set_icon(self.current_image)
        return self.toggle_icon

    def start_thread(self):
        GLib.timeout_add_seconds(1, self.update)
        thread = threading.Thread(target=self.toggle_image)
        thread.start()

    def stop_thread(self, _):
        self.toggle_icon = False

    def toggle_image(self):
        import time

        while self.toggle_icon:
            self.current_image = self.image2 if self.current_image == self.image1 else self.image1
            print(self.current_image)
            time.sleep(1)




if __name__ == "__main__":
    indicator = AppIndicatorToggle()
    indicator.start_thread()
    gtk.main()


