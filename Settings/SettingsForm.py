import requests
import urllib3
import tkinter as tk
import Settings.Settingsback as Settingsback

class FindAppVersionModel(tk.Frame):
    def __init__(self, parent, show_form, auth):
        super().__init__(parent)

        tk.Label(
            self,
            text="Type method name and subID",
            font=("Arial", 24)
        ).pack(pady=30)

        self.entry1 = tk.Entry(self, width=40)
        self.entry1.pack(pady=10)

        self.entry2 = tk.Entry(self, width=40)
        self.entry2.pack(pady=10)
        

        tk.Button(
            self,
            text="Search",
            command=self.open_text_window
        ).pack(pady=10)

        tk.Button(
            self,
            text="Back",
            command=lambda: show_form("home")
        ).pack(pady=10)

    def open_text_window(self):
        METHOD = self.entry1.get()
        USERNAME = self.entry2.get()
        text = findAppVback.findAppVersion(main2.KIBANA_URL, main2.KIBANA_USERNAME, main2.KIBANA_PASSWORD, METHOD, USERNAME, main2.url)
        window = tk.Toplevel()
        window.title("Text")
        window.geometry("700x500")

        text_box = tk.Text(window, wrap="word")
        text_box.pack(fill="both", expand=True, padx=10, pady=10)

        text_box.insert("1.0", text)