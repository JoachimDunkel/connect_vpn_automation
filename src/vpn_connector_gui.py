import tkinter
from tkinter import ttk
import sv_ttk
from establish_connection import VPNConnector


class VPNConnectorGUI(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, padding=15)

        self.connector = VPNConnector(self._read_credentials_failed, self._on_already_connected,
                                      self._on_connection_failure, self._on_connection_success, debug=True)

        self.start_vpn_btn = ttk.Button(self, text="Start vpn")
        self.start_vpn_btn.grid(row=3, column=0, padx=5, pady=(0, 10), sticky="nsew")
        self.start_vpn_btn.config(command=self.start_vpn)

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
        self.connector.read_credentials()
        self.connector.establish_connection()


class App(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, padding=15)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        VPNConnectorGUI(self).grid(row=0, column=0, padx=(0, 10), sticky="nsew")


def main():
    root = tkinter.Tk()
    root.title("")
    sv_ttk.set_theme("dark")
    App(root).pack(expand=True, fill="both")

    root.mainloop()


if __name__ == "__main__":
    main()
