import requests
import urllib3
import tkinter as tk
import main2
import Auth.AuthBack as AuthBack
import Settings.Settingsback

class _authorisation(tk.Frame):
    def __init__(self, parent, show_form, auth, show_status):
        super().__init__(parent)

        self.show_form = show_form
        self.show_status = show_status
        self.auth = auth
        self.config = Settings.Settingsback.load_config

        tk.Label(
            self,
            text="Log in to Elastic",
            font=("Arial", 24)
        ).pack(pady=30)

        self.Login = tk.Entry(self, width=40)
        self.Login.pack(pady=10)

        self.Password = tk.Entry(self, width=40)
        self.Password.pack(pady=10)

        self.Url = tk.Entry(self, width=40)
        self.Url.pack(pady=10)
        
        tk.Button(
            self,
            text="Log in",
            command=self.Write
        ).pack(pady=10)

        tk.Button(
            self,
            text="Back",
            command=lambda: show_form("home")
        ).pack(pady=10)

    def Write(self):
        url = self.Url.get()
        login = self.Login.get()
        password = self.Password.get()

        print("LOGIN BUTTON PRESSED")
        print("URL:", repr(url))
        print("LOGIN:", repr(login))
        print("PASSWORD:", repr(password))

        try:
            self.auth.login(url, login, password)
            Settings.Settingsback.save_config(login, password, url, "True")
            self.show_status("Login Successful")
            self.show_form("home")
        except Exception as e:
            print("Login failed:", e)
