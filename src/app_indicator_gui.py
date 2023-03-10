import os
import signal
import gi

gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')
gi.require_version('Notify', '0.7')

from gi.repository import Gtk as gtk
from gi.repository import AppIndicator3 as appindicator
from gi.repository import Notify as notify
from check_ip import get_public_ip
import resources
import IP2Location


class IPInformation:
    def __init__(self):
        self.city = ""
        self.region = ""
        self.ip_address = ""
        self.country_code = ""

        self._ip2_loc_db = IP2Location.IP2Location()
        self._ip2_loc_db.open(str(resources.PATH_IP2LOCATION_DB))
        self.update()

    def update(self):
        self.ip_address = get_public_ip()
        ip_record = self._ip2_loc_db.get_all(self.ip_address)
        self.country_code = ip_record.country_short
        self.region = ip_record.region
        self.city = ip_record.city

    def get_ip_details(self):
        return "{}, {}, {}".format(self.country_code, self.region, self.city)

    def get_ip_address(self):
        return "IP: {}".format(self.ip_address)


class VPNConnectorApp:
    def __init__(self):
        self.connect_btn_item = None
        self.connect_btn_label = None
        self.separator = None
        self.ip_details_item = None
        self.ip_addr_item = None
        self.menu = None
        self.ip_info = IPInformation()

        self.APPINDICATOR_ID = 'myappindicator'
        self.app = appindicator.Indicator.new(self.APPINDICATOR_ID, os.path.abspath('sample_icon.svg'),
                                              appindicator.IndicatorCategory.SYSTEM_SERVICES)
        self.app.set_status(appindicator.IndicatorStatus.ACTIVE)
        self.app.set_menu(self.build_app())
        notify.init(self.APPINDICATOR_ID)

    def build_app(self):
        self.menu = gtk.Menu()
        self.ip_addr_item = gtk.MenuItem(label=self.ip_info.get_ip_address(), sensitive=False)
        self.ip_details_item = gtk.MenuItem(label=self.ip_info.get_ip_details(), sensitive=False)

        self.separator = gtk.SeparatorMenuItem()

        self.connect_btn_label = "Connect"
        self.connect_btn_item = gtk.MenuItem(self.connect_btn_label)
        # TODO when the button is clicked then update the ip information and the connect btn label appropriatly.
        # While transitioning notify that a connection will be established.
        # https://stackoverflow.com/questions/52887891/how-to-periodically-update-gtk3-label-text -> periodically update a label (the ip address) # not necessary maybe.
        # We can also check the specified ip address to get the connection status.

        self.menu.append(self.ip_addr_item)
        self.menu.append(self.ip_details_item)
        self.menu.append(self.separator)
        self.menu.append(self.connect_btn_item)

        self.menu.show_all()
        return self.menu


# def main():
#     indicator =
#     indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
#     indicator.set_menu(build_menu())
#     notify.init(APPINDICATOR_ID)
#     gtk.main()
#
# def build_menu():
#     menu = gtk.Menu()
#     item_joke = gtk.MenuItem(label='Joke')
#     item_joke.connect('activate', joke)
#     menu.append(item_joke)
#     item_quit = gtk.MenuItem(label='Quit')
#     item_quit.connect('activate', quit)
#     menu.append(item_quit)
#     menu.show_all()
#     return menu
#
# count = 0
#
# def fetch_joke():
#
#     global count
#     count += 1
#     return "You called me {} times.".format(str(count))
#
# def joke(_):
#     notify.Notification.new("<b>Joke</b>", fetch_joke(), None).show()
#
# def quit(_):
#     notify.uninit()
#     gtk.main_quit()

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    connector = VPNConnectorApp()
    # main()
    gtk.main()
