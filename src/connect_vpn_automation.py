import tkinter
from tkinter import ttk, PhotoImage
import sv_ttk
from establish_connection import VPNConnector
from resources import *
from PIL import Image
from PIL import ImageTk


class VPNConnectorGUI(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, padding=15)

        self.connector = VPNConnector(self._read_credentials_failed, self._on_already_connected,
                                      self._on_connection_failure, self._on_connection_success, debug=True)

        self.description_text = tkinter.StringVar(self, value="Connect to vpn")
        self.description_label = ttk.Label(self, textvariable=self.description_text, font=("Helvetica", 20))
        self.description_label.grid(column=0, row=0, pady=20, sticky="nsew")
        img_path = str(PATH_POWER_BTN_IMG)
        img = Image.open(img_path)
        img = img.resize((50, 59), Image.LANCZOS)

        self.power_btn_img = ImageTk.PhotoImage(img)  # PhotoImage(file=img_path)

        # Add label above button

        # Add description below button

        self.connect_btn_style = ttk.Style()
        self.connect_btn_style.configure('my.TButton', font=("Helvetica", 20))
        self.vpn_connection_btn = ttk.Button(self, image=self.power_btn_img, style='my.TButton')

        self.vpn_connection_btn.grid(row=1, column=0, padx=5, pady=(0, 10), sticky="nsew")
        self.vpn_connection_btn.config(command=self.switch)

        self.description_of_situation_text = tkinter.StringVar(self, value="No connection established yet.")
        self.description_of_situation_label = ttk.Label(self, textvariable=self.description_of_situation_text, font=("Helvetica", 12))
        self.description_of_situation_label.grid(column=0, row=2, pady=20, sticky="nsew")

        self.vpn_is_active = tkinter.BooleanVar(self, value=False)

    def switch(self):
        # Determine is on or off
        if self.vpn_is_active.get():
            self.description_text.set("Connection established")
            self.description_of_situation_text.set("Connection established successfully")

            self.vpn_is_active.set(False)
        else:

            self.vpn_is_active.set(True)

    def _on_connection_success(self):
        pass

    def _on_connection_failure(self):
        pass

    def _on_already_connected(self, ip_address):
        print("Already connected.")
        print("IP - Addresss: {}".format(ip_address))

    def _read_credentials_failed(self):
        pass

    def start_vpn(self):
        pass
        # self.connector.read_credentials()
        # self.connector.establish_connection()


class App(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, padding=15)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        VPNConnectorGUI(self).grid(row=0, column=0, padx=(0, 10), sticky="nsew")


def main():
    root = tkinter.Tk()
    root.title("")
    sv_ttk.set_theme("light")
    App(root).pack(expand=True, fill="both")

    root.geometry("350x300")
    root.minsize(350, 300)
    root.maxsize(350, 300)
    root.mainloop()


if __name__ == "__main__":
    main()
