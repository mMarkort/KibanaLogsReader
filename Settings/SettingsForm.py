import requests
import urllib3
import customtkinter as ctk
import tkinter as tk
import Settings.Settingsback as Settingsback
import main2

class SettingsForm(tk.Frame):
    def __init__(self, parent, show_form, auth):
        super().__init__(parent)
        self.auth = auth
        self.show_form = show_form

        ctk.CTkLabel(self, text="SETTINGS", font=("Arial", 24), text_color="black").pack(pady=30)

        self.Url = ctk.CTkEntry(self, width=300, fg_color="white")
        self.Url.pack(pady=10)
        main2.add_placeholder(self.Url, "Change URL")
        
        self.entry2 = ctk.CTkEntry(self, width=300, fg_color="white")
        self.entry2.pack(pady=10)
        main2.add_placeholder(self.entry2, "")
        

        ctk.CTkButton(self, text="Apply", width=200, font=("Arial", 16), state="disabled").pack(pady=10)
        ctk.CTkButton(self, text="Back", width=200, font=("Arial", 16), command=lambda: show_form("home")).pack(pady=10)
        ctk.CTkButton(self, text="Log Out", width=200,  font=("Arial", 16), fg_color="red", text_color="black", command=self.on_click).pack(pady=10)

    def on_click(self):
        Settingsback.save_config("", "", "", "False")
        self.auth.logout()
        self.show_form("auth")