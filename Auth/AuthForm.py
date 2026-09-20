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
        self.config = Settings.Settingsback.load_config
        self.auth = auth
        self.show_status = show_status

        tk.Label(self, text="Log in to Elastic", font=("Arial", 24)).pack(pady=30)

        def add_placeholder(entry, text):
            entry.insert(0, text)
            entry.config(fg="gray")

            def focus_in(event):
                if entry.get() == text:
                    entry.delete(0, tk.END)
                    entry.config(fg="black")

            def focus_out(event):
                if entry.get() == "":
                    entry.insert(0, text)
                    entry.config(fg="gray")

            entry.bind("<FocusIn>", focus_in)
            entry.bind("<FocusOut>", focus_out)

        self.Login = tk.Entry(self, width=40, font=("Arial", 16))
        self.Login.pack(pady=10)
        add_placeholder(self.Login, "Enter Login")

        self.Password = tk.Entry(self, width=40, font=("Arial", 16))
        self.Password.pack(pady=10)
        add_placeholder(self.Password, "Enter Password")

        self.Url = tk.Entry(self, width=40, font=("Arial", 16))
        self.Url.pack(pady=10)
        add_placeholder(self.Url, "Enter Url")

        tk.Button(self, text="Log in", font=("Arial", 16), command=self.Write).pack(pady=40)

        self.check_status = tk.Label(self, text="", font=("Arial", 16))
        self.check_status.pack(pady=30)

    def Write(self):
        url = self.Url.get()
        login = self.Login.get()
        password = self.Password.get()

        if self.auth.check_etnries(login, password, url):
            self.check_status.config(text="Please check that you entered credentials correctly")
        else:
            print("URL:", repr(url))
            print("LOGIN:", repr(login))
            print("PASSWORD:", repr(password))

            try:
                self.auth.login(url, login, password)
                Settings.Settingsback.save_config(login, password, url, "True")
                self.show_status("Login Successful")
                self.show_form("home")

                self.Login.delete(0, tk.END)
                self.Password.delete(0, tk.END)
                self.Url.delete(0, tk.END)

            except Exception as e:
                print("Login failed:", e)
