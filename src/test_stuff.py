import random
from gi.repository import Gtk, GLib
from gi.repository import AppIndicator3 as appindicator

APPINDICATOR_ID = 'myappindicator'



def quit(source):
    Gtk.main_quit()

ind_app = appindicator.Indicator.new(APPINDICATOR_ID, Gtk.STOCK_INFO, appindicator.IndicatorCategory.SYSTEM_SERVICES)
ind_app.set_status(appindicator.IndicatorStatus.ACTIVE)

# create a menu
menu = Gtk.Menu()
menu_items = Gtk.MenuItem("Exit")

def change_label(self):
    global menu_items
    text = 'Hello world, what a beautiful day'.split()
    t = random.choice(text)
    print(t)
    # ind_app.set_label(t , '')
    menu_items.set_label(t)
    return True

menu.append(menu_items)
menu_items.connect("activate", change_label)
menu_items.show_all()
ind_app.set_menu(menu)
# GLib.timeout_add(1000, change_label, menu_items)
Gtk.main()