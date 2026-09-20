import tkinter as tk
import threading

import Settings.SettingsForm
import Settings.Settingsback

import Home.HomeForm
import GetLogsForm.getLogs

import Auth.AuthForm
import Auth.AuthBack


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Better Logs")
        self.geometry("1000x700")

        self.auth = Auth.AuthBack.CreateSession()

        # Container for all forms
        container = tk.Frame(self)
        container.pack(fill="both", expand=True)

        # Create forms
        self.forms = {
            "home": Home.HomeForm._homeForm(container, self.show_form, self.auth),
            "settings": Settings.SettingsForm.SettingsForm(container, self.show_form, self.auth),
            "get_logs": GetLogsForm.getLogs.GetLogsOfSub(container, self.show_form, self.auth),
            "auth": Auth.AuthForm._authorisation(container, self.show_form, self.auth, self.show_status)
        }

        for form in self.forms.values():
            form.grid(
                row=0,
                column=0,
                sticky="nsew"
            )

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)


        self.config = Settings.Settingsback.load_config()

        if self.config["isAuth"] == "True":
            thread = threading.Thread(
                target=self.auto_login_thread,
                daemon=True
            )
            thread.start()
            self.block_buttons(False)
            self.show_form("home")
        else:
            self.show_form("auth") 

    def auto_login_thread(self):
        try:
            self.auth.login(
                self.config["url"],
                self.config["login"],
                self.config["password"]
            )
            self.after(0, lambda: self.show_status("Login Successful"))  
            self.after(0, lambda: self.block_buttons(True))  
        except Exception as e:
            self.after(0, lambda: self.show_status("Failed to Login"))
            self.after(0, lambda: self.show_form("auth"))

    def show_form(self, form_class):
        self.forms[form_class].tkraise()

    def show_status(self, status):
        self.forms["home"].statusLabel.configure(text=status)

    def block_buttons(self, status):
        if not status:
            self.forms["home"].logsButton.configure(state="disabled")
            #self.forms["home"].settingsButton.config(state="disable")
        else:
            self.forms["home"].logsButton.configure(state="normal")
            #self.forms["home"].settingsButton.config(state="normal")

def add_placeholder(entry, text):
    entry.insert(0, text)
    entry.configure(text_color="gray")

    def focus_in(event):
        if entry.get() == text:
            entry.delete(0, tk.END)
            entry.configure(text_color="black")

    def focus_out(event):
        if entry.get() == "":
            entry.insert(0, text)
            entry.configure(text_color="gray")

    entry.bind("<FocusIn>", focus_in)
    entry.bind("<FocusOut>", focus_out)

if __name__ == "__main__":
    app = App()
    app.mainloop()