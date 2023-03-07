import tkinter
from tkinter import ttk
import sv_ttk

from start_script import start_script


class VPNConnectorGUI(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, padding=15)

        self.sub_process_id = 0

        self.start_vpn_btn = ttk.Button(self, text="Start vpn")
        self.start_vpn_btn.grid(row=3, column=0, padx=5, pady=(0, 10), sticky="nsew")
        self.start_vpn_btn.config(command=self.start_vpn)

    def start_vpn(self):
        # TODO it already starts the process independently.
        # When started the button should then read another result and also not start the vpn but kill it.
        self.sub_process_id = start_script()


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
