import signal
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')
gi.require_version('Notify', '0.7')
from gi.repository import Gtk as gtk
from gi.repository import AppIndicator3
from gi.repository import Notify as notify
from gi.repository import GLib
from connect_vpn.ui.settings_ui import SettingsWindow
from connect_vpn.common import resources
from connect_vpn.common.resources import ApplicationStatus
from .establish_connection import ConnectorBackend
from .configuration_handler import read_credentials
from .ip_info import IPInformation
from .icon_status_handler import IconStatusHandler


class VPNConnectorApp:
    def __init__(self, on_disconnect_vpn, on_connect_vpn):
        self.on_disconnect_vpn = on_disconnect_vpn
        self.on_connect_vpn = on_connect_vpn
        self.application_status = ApplicationStatus.DISCONNECTED
        self.ip_info = IPInformation()

        self.APPINDICATOR_ID = 'connect_vpn_indicator'
        self.app = AppIndicator3.Indicator.new(self.APPINDICATOR_ID, str(resources.PATH_VPN_ICON_DISCONNECTED),
                                               AppIndicator3.IndicatorCategory.SYSTEM_SERVICES)
        self.app.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
        self.app.set_menu(self.build_app())
        self.settings_window = SettingsWindow(self.app, self.quit_application, self.unlock)
        self.icon_status_handler = IconStatusHandler(self.app)

        notify.init(self.APPINDICATOR_ID)

    def request_connection(self):
        self.notify_user("Connecting ... ")
        self.icon_status_handler.on_establishing_connection()
        self.on_connect_vpn(self.ip_info.ip_address)

    def on_connected(self):
        self.update_ip_information()
        self.notify_user(resources.ESTABLISHED_CONNECTION_FORMAT.format(self.ip_info.ip_address))
        self.perform_connection_change_btn_item.set_label(resources.STOP_CONNECTION)
        self.application_status = ApplicationStatus.CONNECTED
        self.change_connect_status_info()
        self.icon_status_handler.on_connected()

    def on_disconnected(self):
        self.update_ip_information()
        self.notify_user(resources.STOPPED_CONNECTION)
        self.perform_connection_change_btn_item.set_label(resources.ESTABLISH_CONNECTION)
        self.application_status = ApplicationStatus.DISCONNECTED
        self.change_connect_status_info()
        self.icon_status_handler.on_disconnected()

    def on_other_process_holds_connection(self, ip):
        msg = resources.OTHER_PROCESS_HOLDS_CONNECTION_FORMAT.format(ip)
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

    def open_settings(self, btn):
        self.lock()
        self.settings_window.show()

    def quit_application(self):
        self.request_disconnection()
        gtk.main_quit()

    def lock(self):
        self.perform_connection_change_btn_item.set_sensitive(False)
        self.open_settings_menu_item.set_sensitive(False)

    def unlock(self):
        self.perform_connection_change_btn_item.set_sensitive(True)
        self.open_settings_menu_item.set_sensitive(True)

    def build_app(self):
        self.menu = gtk.Menu()
        self.ip_addr_item = gtk.MenuItem(label=self.ip_info.get_ip_address(), sensitive=False)
        self.ip_details_item = gtk.MenuItem(label=self.ip_info.get_ip_details(), sensitive=False)

        self.connection_status_label = ApplicationStatus.DISCONNECTED.name
        self.connection_status_menu_item = gtk.MenuItem(label=self.connection_status_label, sensitive=False)
        self.perform_connection_change_btn_item = gtk.MenuItem(label=resources.ESTABLISH_CONNECTION)
        self.perform_connection_change_btn_item.connect("activate", self.toggle_vpn_connection)

        self.open_settings_menu_item = gtk.MenuItem(label=resources.SETTINGS_BTN_LABEL)
        self.open_settings_menu_item.connect('activate', self.open_settings)

        self.menu.append(self.ip_addr_item)
        self.menu.append(self.ip_details_item)
        self.menu.append(self.connection_status_menu_item)
        self.menu.append(gtk.SeparatorMenuItem())
        self.menu.append(self.perform_connection_change_btn_item)
        self.menu.append(gtk.SeparatorMenuItem())
        self.menu.append(self.open_settings_menu_item)
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
    app.notify_user("Started VPN - Connector")
    gtk.main()


if __name__ == "__main__":
    main()
