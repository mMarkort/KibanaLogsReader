import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry

import requests
import urllib3
from datetime import datetime, time, timezone
import json

import main2
import Settings.Settingsback


urllib3.disable_warnings(
    urllib3.exceptions.InsecureRequestWarning
)


class GetLogsOfSub(tk.Frame):

    def __init__(self, parent, show_form, auth):
        super().__init__(parent)

        self.show_form = show_form

        # ============================================================
        # MAIN CONFIG
        # ============================================================

        self.config = Settings.Settingsback.load_config()
        self.auth = auth

        self.kibana_url = self.config["url"]
        self.kibana_login = self.config["login"]
        self.kibana_password = self.config["password"]
        self.index = "logger-backend-dev-*"

        # ============================================================
        # VARIABLES
        # ============================================================

        self.focus_column = 0

        # ============================================================
        # TITLE
        # ============================================================

        title_frame = ttk.Frame(self)
        title_frame.pack(
            fill="x",
            padx=10,
            pady=(10, 0)
        )

        ttk.Label(
            title_frame,
            text="Get Logs",
            font=("Arial", 20)
        ).pack(side="left")

        ttk.Button(
            title_frame,
            text="Back",
            command=lambda: self.show_form("home")
        ).pack(side="right")

        # ============================================================
        # SEARCH FRAME
        # ============================================================

        search_frame = ttk.Frame(self)
        search_frame.pack(
            fill="x",
            padx=10,
            pady=10
        )

        # ------------------------------------------------------------
        # METHOD
        # ------------------------------------------------------------

        ttk.Label(
            search_frame,
            text="METHOD:"
        ).pack(side="left")

        self.method_entry = ttk.Combobox(
            search_frame,
            width=27,
            values=[
                "Baridi",
                "Bankily",
                "Mercantil",
                "GazaPay",
                "MoovMoney",
                "Asiacell",
                "ATOMAPay",
                "Melbet",
                "BCIPay",
                "BIMBank",
                "CashPlus",
                "Click",
                "DabaPay",
                "Edahab",
                "EVC",
                "InstaPay",
                "Masrvi",
                "MonCash",
                "MTN",
                "NatCash",
                "Sahal",
                "Sedad",
                "Sinpe",
                "Ueno",
                "Waafi",
                "Yappy",
                "ZAAD"
            ]
        )

        self.method_entry.pack(
            side="left",
            padx=(5, 15)
        )

        # ------------------------------------------------------------
        # USERNAME
        # ------------------------------------------------------------

        ttk.Label(
            search_frame,
            text="USERNAME:"
        ).pack(side="left")

        self.username_entry = ttk.Entry(
            search_frame,
            width=20
        )

        self.username_entry.pack(
            side="left",
            padx=(5, 15)
        )

        # ------------------------------------------------------------
        # START DATE
        # ------------------------------------------------------------

        ttk.Label(
            search_frame,
            text="FROM:"
        ).pack(side="left")

        self.start_date = DateEntry(
            search_frame,
            width=12,
            date_pattern="dd.mm.yyyy"
        )

        self.start_date.pack(
            side="left",
            padx=(5, 15)
        )

        # ------------------------------------------------------------
        # END DATE
        # ------------------------------------------------------------

        ttk.Label(
            search_frame,
            text="TO:"
        ).pack(side="left")

        self.end_date = DateEntry(
            search_frame,
            width=12,
            date_pattern="dd.mm.yyyy"
        )

        self.end_date.pack(
            side="left",
            padx=(5, 15)
        )

        # ------------------------------------------------------------
        # SEARCH BUTTON
        # ------------------------------------------------------------

        ttk.Button(
            search_frame,
            text="Search",
            command=self.search_logs
        ).pack(
            side="left",
            padx=10
        )

        # ------------------------------------------------------------
        # STATUS
        # ------------------------------------------------------------

        self.status_label = ttk.Label(
            search_frame,
            text="Ready"
        )

        self.status_label.pack(
            side="left",
            padx=15
        )

        # ============================================================
        # CONTENT AREA
        # ============================================================

        self.content_frame = ttk.Frame(self)

        self.content_frame.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=(0, 10)
        )

        # ============================================================
        # TABLE FRAME
        # ============================================================

        self.table_frame = ttk.Frame(
            self.content_frame
        )

        self.table_frame.pack(
            fill="both",
            expand=True
        )

        self.create_table()

        # ============================================================
        # INFO FRAME
        # ============================================================

        self.info_frame = ttk.Frame(
            self.content_frame
        )

        # Don't show it yet.
        self.info_frame.pack_forget()

    # =================================================================
    # TABLE
    # =================================================================

    def create_table(self):

        columns = (
            "timestamp",
            "deviceModel",
            "appVersion",
            "username",
            "message",
            "info"
        )

        self.tree = ttk.Treeview(
            self.table_frame,
            columns=columns,
            show="headings"
        )

        # ============================================================
        # HEADERS
        # ============================================================

        self.tree.heading(
            "timestamp",
            text="Timestamp"
        )

        self.tree.heading(
            "deviceModel",
            text="Device Model"
        )

        self.tree.heading(
            "appVersion",
            text="App Version"
        )

        self.tree.heading(
            "username",
            text="Username"
        )

        self.tree.heading(
            "message",
            text="Message"
        )

        self.tree.heading(
            "info",
            text="Data Info"
        )

        # ============================================================
        # COLUMN WIDTHS
        # ============================================================

        self.tree.column(
            "timestamp",
            width=165,
            minwidth=165
        )

        self.tree.column(
            "deviceModel",
            width=150,
            minwidth=100
        )

        self.tree.column(
            "appVersion",
            width=110,
            minwidth=80
        )

        self.tree.column(
            "username",
            width=280,
            minwidth=150
        )

        self.tree.column(
            "message",
            width=450,
            minwidth=200
        )

        self.tree.column(
            "info",
            width=500,
            minwidth=200
        )

        # ============================================================
        # SCROLLBARS
        # ============================================================

        vertical_scroll = ttk.Scrollbar(
            self.table_frame,
            orient="vertical",
            command=self.tree.yview
        )

        horizontal_scroll = ttk.Scrollbar(
            self.table_frame,
            orient="horizontal",
            command=self.tree.xview
        )

        self.tree.configure(
            yscrollcommand=vertical_scroll.set,
            xscrollcommand=horizontal_scroll.set
        )

        vertical_scroll.pack(
            side="right",
            fill="y"
        )

        horizontal_scroll.pack(
            side="bottom",
            fill="x"
        )

        self.tree.pack(
            fill="both",
            expand=True
        )

        # ============================================================
        # EVENTS
        # ============================================================

        self.tree.bind(
            "<Double-1>",
            self.on_double_click
        )

        self.tree.bind(
            "<Button-3>",
            self.show_context_menu
        )

        self.tree.bind(
            "<Button-1>",
            self.track_column,
            add="+"
        )

        self.tree.bind(
            "<Control-c>",
            self.keyboard_copy
        )

    # =================================================================
    # TIMESTAMP
    # =================================================================

    @staticmethod
    def format_timestamp(timestamp):

        if not timestamp:
            return ""

        try:

            dt = datetime.fromisoformat(
                timestamp.replace("Z", "+00:00")
            )

            return dt.strftime(
                "%d.%m.%Y %H:%M:%S"
            )

        except Exception:

            return timestamp

    # =================================================================
    # DATE RANGE
    # =================================================================

    def get_start_timestamp(self):

        selected_date = self.start_date.get_date()

        dt = datetime.combine(
            selected_date,
            time.min
        ).replace(
            tzinfo=timezone.utc
        )

        return dt.isoformat().replace(
            "+00:00",
            "Z"
        )

    def get_end_timestamp(self):

        selected_date = self.end_date.get_date()

        dt = datetime.combine(
            selected_date,
            time.max
        ).replace(
            tzinfo=timezone.utc
        )

        return dt.isoformat().replace(
            "+00:00",
            "Z"
        )

    # =================================================================
    # FORMAT INFO
    # =================================================================

    @staticmethod
    def format_info(info):

        if info is None:
            return ""

        if isinstance(info, (dict, list)):

            return json.dumps(
                info,
                indent=4,
                ensure_ascii=False
            )

        return str(info)

    # =================================================================
    # SEARCH
    # =================================================================

    def search_logs(self):

        method = self.method_entry.get().strip()
        username = self.username_entry.get().strip()

        # ------------------------------------------------------------
        # VALIDATION
        # ------------------------------------------------------------

        if not method or not username:

            messagebox.showwarning(
                "Missing data",
                "Enter both METHOD and USERNAME."
            )

            return

        # ------------------------------------------------------------
        # DATE RANGE
        # ------------------------------------------------------------

        start_timestamp = self.get_start_timestamp()
        end_timestamp = self.get_end_timestamp()

        # ------------------------------------------------------------
        # CLEAR TABLE
        # ------------------------------------------------------------

        for item in self.tree.get_children():

            self.tree.delete(item)

        self.status_label.config(
            text="Searching..."
        )

        self.update_idletasks()

        # ============================================================
        # KIBANA
        # ============================================================

        url = (
            f"{self.kibana_url}"
            f"/s/default/api/console/proxy"
        )

        headers = {
            "kbn-xsrf": "true",
            "Content-Type": "application/json"
        }

        params = {
            "path": f"/{self.index}/_search",
            "method": "POST"
        }

        # ============================================================
        # ELASTICSEARCH QUERY
        # ============================================================

        body = {

            "size": 500,

            "_source": [

                "@timestamp",

                "local_log_data_json.context.deviceModel",

                "local_log_data_json.context.appVersion",

                "local_log_data_json.user.username",

                "local_log_data_json.message",

                "local_log_data_json.data.info"

            ],

            "query": {

                "bool": {

                    "must": [

                        # METHOD
                        {
                            "wildcard": {

                                "local_log_data_json.user.username.keyword": {

                                    "value": f"*{method}*",
                                    "case_insensitive": True

                                }

                            }

                        },

                        # USERNAME
                        {
                            "wildcard": {

                                "local_log_data_json.user.username.keyword": {

                                    "value": f"*{username}*"

                                }

                            }

                        }

                    ],

                    "filter": [

                        # DATE RANGE
                        {
                            "range": {

                                "@timestamp": {

                                    "gte": start_timestamp,
                                    "lte": end_timestamp

                                }

                            }

                        }

                    ]

                }

            },

            # Newest first
            "sort": [

                {
                    "@timestamp": {
                        "order": "desc"
                    }
                }

            ]

        }

        # ============================================================
        # REQUEST
        # ============================================================

        try:

            response = self.auth.post(

                url,

                params=params,

                headers=headers,

                json=body,

                verify=False,

                timeout=30

            )

        except requests.RequestException as e:

            self.status_label.config(
                text="Connection error"
            )

            messagebox.showerror(
                "Connection error",
                str(e)
            )

            return

        # ============================================================
        # CHECK RESPONSE
        # ============================================================

        if response.status_code != 200:

            self.status_label.config(
                text="Request failed"
            )

            messagebox.showerror(
                "Kibana error",
                f"Status: {response.status_code}\n\n"
                f"{response.text}"
            )

            return

        # ============================================================
        # PARSE JSON
        # ============================================================

        try:

            data = response.json()

        except ValueError:

            messagebox.showerror(
                "Error",
                "Kibana returned invalid JSON."
            )

            return

        hits = (
            data
            .get("hits", {})
            .get("hits", [])
        )

        # ============================================================
        # NO RESULTS
        # ============================================================

        if not hits:

            self.status_label.config(
                text="No logs found"
            )

            return

        # ============================================================
        # DISPLAY RESULTS
        # ============================================================

        for hit in hits:

            source = hit.get(
                "_source",
                {}
            )

            log_data = source.get(
                "local_log_data_json",
                {}
            )

            # --------------------------------------------------------
            # Timestamp
            # --------------------------------------------------------

            timestamp = self.format_timestamp(
                source.get(
                    "@timestamp",
                    ""
                )
            )

            # --------------------------------------------------------
            # Context
            # --------------------------------------------------------

            context = log_data.get(
                "context",
                {}
            )

            device_model = context.get(
                "deviceModel",
                ""
            )

            app_version = context.get(
                "appVersion",
                ""
            )

            # --------------------------------------------------------
            # User
            # --------------------------------------------------------

            user = log_data.get(
                "user",
                {}
            )

            log_username = user.get(
                "username",
                ""
            )

            # --------------------------------------------------------
            # Message
            # --------------------------------------------------------

            message = log_data.get(
                "message",
                ""
            )

            # --------------------------------------------------------
            # data.info
            # --------------------------------------------------------

            data_field = log_data.get(
                "data",
                {}
            )

            info = data_field.get(
                "info",
                ""
            )

            formatted_info = self.format_info(
                info
            )

            # --------------------------------------------------------
            # Insert row
            # --------------------------------------------------------

            self.tree.insert(

                "",

                "end",

                values=(

                    timestamp,

                    device_model,

                    app_version,

                    log_username,

                    message,

                    formatted_info

                ),

                # Store original info
                tags=(formatted_info,)

            )

        self.status_label.config(
            text=f"Found {len(hits)} logs"
        )

    # =================================================================
    # GET SELECTED CELL
    # =================================================================

    def get_selected_cell(self, event):

        row_id = self.tree.identify_row(
            event.y
        )

        column_id = self.tree.identify_column(
            event.x
        )

        if not row_id or not column_id:

            return None, None, None

        column_number = (
            int(
                column_id.replace("#", "")
            ) - 1
        )

        values = self.tree.item(
            row_id,
            "values"
        )

        if column_number >= len(values):

            return None, None, None

        value = values[column_number]

        return (
            row_id,
            column_number,
            value
        )

    # =================================================================
    # COPY CELL
    # =================================================================

    def copy_cell(self, event=None):

        if event:

            row_id, column_number, value = (
                self.get_selected_cell(event)
            )

        else:

            selection = self.tree.selection()

            if not selection:
                return

            row_id = selection[0]

            column_number = getattr(
                self.tree,
                "focus_column",
                0
            )

            values = self.tree.item(
                row_id,
                "values"
            )

            if column_number >= len(values):
                return

            value = values[column_number]

        if value is None:
            return

        self.clipboard_clear()

        self.clipboard_append(
            str(value)
        )

        self.update()

        self.status_label.config(
            text="Cell copied"
        )

    # =================================================================
    # DOUBLE CLICK
    # =================================================================

    def on_double_click(self, event):

        row_id, column_number, value = (
            self.get_selected_cell(event)
        )

        if not row_id:
            return

        # Column 5 = data.info
        if column_number == 5:

            tags = self.tree.item(
                row_id,
                "tags"
            )

            if tags:

                info = tags[0]

            else:

                info = value

            self.show_info(info)

            return

        # Other columns -> copy
        self.copy_cell(event)

    # =================================================================
    # RIGHT CLICK
    # =================================================================

    def show_context_menu(self, event):

        row_id, column_number, value = (
            self.get_selected_cell(event)
        )

        if not row_id:
            return

        # Select row
        self.tree.selection_set(
            row_id
        )

        self.tree.focus(
            row_id
        )

        # Remember column
        self.tree.focus_column = (
            column_number
        )

        # ------------------------------------------------------------
        # Menu
        # ------------------------------------------------------------

        context_menu = tk.Menu(
            self,
            tearoff=0
        )

        context_menu.add_command(
            label="Copy",
            command=lambda: self.copy_specific_cell(
                row_id,
                column_number
            )
        )

        # data.info
        if column_number == 5:

            context_menu.add_separator()

            context_menu.add_command(
                label="Open data.info",
                command=lambda: self.open_specific_info(
                    row_id
                )
            )

        context_menu.tk_popup(
            event.x_root,
            event.y_root
        )

    # =================================================================
    # COPY SPECIFIC CELL
    # =================================================================

    def copy_specific_cell(
        self,
        row_id,
        column_number
    ):

        values = self.tree.item(
            row_id,
            "values"
        )

        if column_number >= len(values):
            return

        value = values[column_number]

        self.clipboard_clear()

        self.clipboard_append(
            str(value)
        )

        self.update()

        self.status_label.config(
            text="Cell copied"
        )

    # =================================================================
    # OPEN SPECIFIC INFO
    # =================================================================

    def open_specific_info(self, row_id):

        tags = self.tree.item(
            row_id,
            "tags"
        )

        if not tags:
            return

        info = tags[0]

        self.show_info(info)

    # =================================================================
    # SHOW INFO IN SAME FRAME
    # =================================================================

    def show_info(self, info):

        # Hide table
        self.table_frame.pack_forget()

        # Remove old info widgets
        for widget in self.info_frame.winfo_children():

            widget.destroy()

        # Show info frame
        self.info_frame.pack(
            fill="both",
            expand=True
        )

        # ------------------------------------------------------------
        # Header
        # ------------------------------------------------------------

        header = ttk.Frame(
            self.info_frame
        )

        header.pack(
            fill="x",
            pady=(0, 5)
        )

        ttk.Label(
            header,
            text="local_log_data_json.data.info",
            font=("Arial", 14, "bold")
        ).pack(
            side="left"
        )

        ttk.Button(
            header,
            text="← Back to logs",
            command=self.hide_info
        ).pack(
            side="right"
        )

        # ------------------------------------------------------------
        # Text area
        # ------------------------------------------------------------

        text_frame = ttk.Frame(
            self.info_frame
        )

        text_frame.pack(
            fill="both",
            expand=True
        )

        text = tk.Text(
            text_frame,
            wrap="none",
            font=("Consolas", 10)
        )

        vertical_scroll = ttk.Scrollbar(
            text_frame,
            orient="vertical",
            command=text.yview
        )

        horizontal_scroll = ttk.Scrollbar(
            text_frame,
            orient="horizontal",
            command=text.xview
        )

        text.configure(
            yscrollcommand=vertical_scroll.set,
            xscrollcommand=horizontal_scroll.set
        )

        text.pack(
            side="left",
            fill="both",
            expand=True
        )

        vertical_scroll.pack(
            side="right",
            fill="y"
        )

        horizontal_scroll.pack(
            side="bottom",
            fill="x"
        )

        text.insert(
            "1.0",
            self.format_info(info)
        )

        text.configure(
            state="disabled"
        )

        # Allow Ctrl+C
        text.bind(
            "<Control-c>",
            lambda event: self.copy_text(text)
        )

    # =================================================================
    # HIDE INFO
    # =================================================================

    def hide_info(self):

        self.info_frame.pack_forget()

        self.table_frame.pack(
            fill="both",
            expand=True
        )

    # =================================================================
    # COPY TEXT
    # =================================================================

    def copy_text(self, text_widget):

        try:

            selected = text_widget.get(
                "sel.first",
                "sel.last"
            )

        except tk.TclError:

            return

        self.clipboard_clear()

        self.clipboard_append(
            selected
        )

        self.update()

        self.status_label.config(
            text="Text copied"
        )

    # =================================================================
    # KEYBOARD COPY
    # =================================================================

    def keyboard_copy(self, event):

        self.copy_cell()

        return "break"

    # =================================================================
    # TRACK COLUMN
    # =================================================================

    def track_column(self, event):

        column = self.tree.identify_column(
            event.x
        )

        if column:

            self.tree.focus_column = (
                int(
                    column.replace("#", "")
                ) - 1
            )