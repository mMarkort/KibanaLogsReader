import tkinter as tk
import customtkinter as ctk

class _homeForm(tk.Frame):
    def __init__(self, parent, show_form, auth):
        super().__init__(parent)
        

        tk.Label(self, text="HOME PAGE", font=("Arial", 24)).pack(pady=30)

        self.logsButton = ctk.CTkButton(self, text="Get Logs of Sub", corner_radius=10, width=300, height=40, font=("Arial", 24), command=lambda: show_form("get_logs"))
        self.logsButton.pack(pady=10)

        self.settingsButton = ctk.CTkButton(self, text="Settings", corner_radius=10, width=300, height=40, font=("Arial", 24), command=lambda: show_form("settings"))
        self.settingsButton.pack(pady=10)

        self.statusLabel = ctk.CTkLabel(self, text="LOADING...", font=("Arial", 24), text_color="black")

        self.statusLabel.pack(pady=30)
