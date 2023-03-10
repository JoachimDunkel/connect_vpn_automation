import gi
gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')

from gi.repository import Gtk as gtk
from gi.repository import AppIndicator3 as appindicator
from gi.repository import Gio as gio

from check_ip import get_public_ip

def on_button_clicked(widget):
    print("Button on clicked")

def off_button_clicked(widget):
    print("Button off clicked")

def init_indicator():
    ind = appindicator.Indicator.new(
        "example-simple-client",
        "indicator-messages",
        appindicator.IndicatorCategory.APPLICATION_STATUS
    )
    ind.set_status(appindicator.IndicatorStatus.ACTIVE)
    ind.set_attention_icon("indicator-messages-new")
    ind.set_icon("indicator-messages")

    # create a menu
    menu_item = gtk.MenuItem(label="KNAPP VPN", sensitive=False)

    pub_ip = get_public_ip()
    ip_address_menu_item = gtk.MenuItem(label=pub_ip, sensitive=False)

    import IP2Location
    import resources

    IP2LocObj = IP2Location.IP2Location()
    IP2LocObj.open(str(resources.PATH_IP2LOCATION_DB))

    record = IP2LocObj.get_all(pub_ip)

    print("IP: {}".format(pub_ip))

    print("{}, {}, {}".format(record.country_short, record.region, record.city))

    menu = gtk.Menu()

    menu.append(menu_item)

    menu.append(ip_address_menu_item)

    # Add a separator
    separator = gtk.SeparatorMenuItem()
    menu.append(separator)

    # create on and off menu items
    on_item = gtk.MenuItem("On")
    on_item.connect("activate", on_button_clicked)
    menu.append(on_item)

    off_item = gtk.MenuItem("Off")
    off_item.connect("activate", off_button_clicked)
    menu.append(off_item)

    # show the menu
    menu.show_all()

    # set the menu to the AppIndicator
    ind.set_menu(menu)

    # display the AppIndicator
    gtk.main()

if __name__ == "__main__":
    init_indicator()
