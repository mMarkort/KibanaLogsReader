import tkinter as tk

class _homeForm(tk.Frame):
    def __init__(self, parent, show_form, auth):
        super().__init__(parent)
        

        tk.Label(
            self,
            text="HOME",
            font=("Arial", 24)
        ).pack(pady=30)

        self.settingsButton = tk.Button(
            self,
            text="Find app version",
            width=20,
            command=lambda: show_form("find_version")
        )
        self.settingsButton.pack(pady=10)

        self.logsButton = tk.Button(
            self,
            text="Get Logs of Sub",
            width=20,
            command=lambda: show_form("get_logs")
        )
        self.logsButton.pack(pady=10)

        self.statusLabel = tk.Label(
            self,
            text="LOADING...",
            font=("Arial", 24)
        )

        self.statusLabel.pack(pady=30)
