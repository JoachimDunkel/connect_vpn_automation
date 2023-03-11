import os
import signal
import gi

gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')
gi.require_version('Notify', '0.7')
from gi.repository import Gtk as gtk
from gi.repository import AppIndicator3 as appindicator
from gi.repository import Notify as notify
from gi.repository import GLib
from .check_ip import get_public_ip
from . import resources
from .resources import ApplicationStatus
import IP2Location
from .establish_connection import ConnectorBackend
from .configuration_handler import read_credentials


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
    def __init__(self, on_disconnect_vpn, on_connect_vpn):
        self.on_disconnect_vpn = on_disconnect_vpn
        self.on_connect_vpn = on_connect_vpn
        self.application_status = ApplicationStatus.DISCONNECTED
        self.ip_info = IPInformation()

        self.APPINDICATOR_ID = 'myappindicator'
        self.app = appindicator.Indicator.new(self.APPINDICATOR_ID, os.path.abspath('sample_icon.svg'),
                                              appindicator.IndicatorCategory.SYSTEM_SERVICES)
        self.app.set_status(appindicator.IndicatorStatus.ACTIVE)
        self.app.set_menu(self.build_app())
        notify.init(self.APPINDICATOR_ID)

    def request_connection(self):
        self.on_connect_vpn(self.ip_info.ip_address)

    def on_connected(self):
        self.update_ip_information()
        self.notify_user(resources.ESTABLISHED_CONNECTION_FORMAT.format(self.ip_info.ip_address))
        self.perform_connection_change_btn_item.set_label(resources.STOP_CONNECTION)
        self.application_status = ApplicationStatus.CONNECTED
        self.change_connect_status_info()

    def on_disconnected(self):
        self.notify_user(resources.STOPPED_CONNECTION)
        self.perform_connection_change_btn_item.set_label(resources.ESTABLISH_CONNECTION)
        self.application_status = ApplicationStatus.DISCONNECTED
        self.change_connect_status_info()

    def on_other_process_holds_connection(self):
        msg = resources.OTHER_PROCESS_HOLDS_CONNECTION_FORMAT.format(self.ip_info.ip_address)
        self.notify_user(msg)
        exit(-1)

    @staticmethod
    def on_other_connection_failure(exception: Exception):
        print(resources.OTHER_CONNECTION_FAILURE_FORMAT.format(str(exception)))

    @staticmethod
    def on_read_credentials_failed():
        print(resources.READING_CREDENTIALS_FAILED)
        exit(-1)

    @staticmethod
    def notify_user(msg):
        notify.Notification.new(msg, None).show()

    def request_disconnection(self):
        self.on_disconnect_vpn()

    def change_connect_status_info(self):
        self.connection_status_label = self.application_status.name
        self.connection_status_menu_item.set_label(self.connection_status_label)

    def toggle_vpn_connection(self, btn):

        if self.application_status == ApplicationStatus.DISCONNECTED:
            self.request_connection()

        elif self.application_status == ApplicationStatus.CONNECTED:
            self.request_disconnection()

        else:
            print("Other process holds connection. Aborting program")
            exit(-1)

    def update_ip_information(self):
        self.ip_info.update()
        self.ip_addr_item.set_label(self.ip_info.get_ip_address())
        self.ip_details_item.set_label(self.ip_info.get_ip_details())

    def build_app(self):
        self.menu = gtk.Menu()
        self.ip_addr_item = gtk.MenuItem(label=self.ip_info.get_ip_address(), sensitive=False)
        self.ip_details_item = gtk.MenuItem(label=self.ip_info.get_ip_details(), sensitive=False)

        self.separator = gtk.SeparatorMenuItem()

        self.connection_status_label = ApplicationStatus.DISCONNECTED.name
        self.connection_status_menu_item = gtk.MenuItem(label=self.connection_status_label, sensitive=False)
        self.perform_connection_change_btn_item = gtk.MenuItem(label=resources.ESTABLISH_CONNECTION)
        self.perform_connection_change_btn_item.connect("activate", self.toggle_vpn_connection)

        # TODO when the button is clicked then update the ip information and the connect btn label appropriatly.
        # While transitioning notify that a connection will be established.
        # https://stackoverflow.com/questions/52887891/how-to-periodically-update-gtk3-label-text -> periodically update a label (the ip address) # not necessary maybe.
        # We can also check the specified ip address to get the connection status.

        self.menu.append(self.ip_addr_item)
        self.menu.append(self.ip_details_item)

        self.menu.append(self.connection_status_menu_item)
        self.menu.append(self.separator)
        self.menu.append(self.perform_connection_change_btn_item)

        self.menu.show_all()
        return self.menu


def main():
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    connection_backend = ConnectorBackend()
    read_credentials(connection_backend)
    app = VPNConnectorApp(on_disconnect_vpn=connection_backend.stop_connection,
                          on_connect_vpn=connection_backend.establish_connection)

    connection_backend.setup(app.on_read_credentials_failed, app.on_other_process_holds_connection,
                             app.on_other_connection_failure, app.on_connected, app.on_disconnected)
    connection_backend.check_connection_status(app.ip_info.ip_address)

    gtk.main()


if __name__ == "__main__":
    main()
