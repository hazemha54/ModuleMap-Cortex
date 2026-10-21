"""
Settings View for Odoo Connection and Application Preferences (Modern Blue Theme)
"""

import tkinter as tk
from tkinter import ttk, messagebox
import threading
from app.services.config_manager import ConfigManager
from app.services.odoo_service import OdooConnector


class SettingsView(ttk.Frame):
    """View for configuring Odoo credentials and app settings"""

    def __init__(self, parent, config_manager: ConfigManager):
        super().__init__(parent, padding=25)
        self.config_manager = config_manager
        self.create_widgets()
        self.load_values()

    def create_widgets(self):
        ttk.Label(self, text="Application Settings & Odoo Connection", style="Header.TLabel").pack(anchor=tk.W, pady=(0, 20))

        # Odoo Config Frame
        odoo_frame = ttk.LabelFrame(self, text="  Odoo Server Configuration  ", padding=20)
        odoo_frame.pack(fill=tk.X, pady=(0, 20))

        form = ttk.Frame(odoo_frame)
        form.pack(fill=tk.X, expand=True)

        ttk.Label(form, text="Odoo URL:").grid(row=0, column=0, sticky=tk.W, pady=8)
        self.url_var = tk.StringVar()
        ttk.Entry(form, textvariable=self.url_var, width=50).grid(row=0, column=1, sticky=tk.W, pady=8)

        ttk.Label(form, text="Database Name:").grid(row=1, column=0, sticky=tk.W, pady=8)
        self.db_var = tk.StringVar()
        ttk.Entry(form, textvariable=self.db_var, width=50).grid(row=1, column=1, sticky=tk.W, pady=8)

        ttk.Label(form, text="Username:").grid(row=2, column=0, sticky=tk.W, pady=8)
        self.user_var = tk.StringVar()
        ttk.Entry(form, textvariable=self.user_var, width=50).grid(row=2, column=1, sticky=tk.W, pady=8)

        ttk.Label(form, text="Password / API Key:").grid(row=3, column=0, sticky=tk.W, pady=8)
        self.pass_var = tk.StringVar()
        ttk.Entry(form, textvariable=self.pass_var, show="*", width=50).grid(row=3, column=1, sticky=tk.W, pady=8)

        # Action Buttons for Odoo
        btn_box = ttk.Frame(odoo_frame)
        btn_box.pack(fill=tk.X, pady=(15, 0))

        ttk.Button(btn_box, text="Test Connection", style="Primary.TButton", command=self.test_connection).pack(side=tk.LEFT, padx=(0, 15))
        self.status_lbl = tk.Label(btn_box, text="Status: Not Tested", bg="#f4f6f9", fg="#212529", font=("Segoe UI", 10, "italic"))
        self.status_lbl.pack(side=tk.LEFT)

        # General App Settings Frame
        app_frame = ttk.LabelFrame(self, text="  General Settings  ", padding=20)
        app_frame.pack(fill=tk.X, pady=(0, 20))

        app_form = ttk.Frame(app_frame)
        app_form.pack(fill=tk.X, expand=True)

        self.auto_import_var = tk.BooleanVar()
        ttk.Checkbutton(app_form, text="Auto-import modules on startup", variable=self.auto_import_var).grid(row=0, column=0, sticky=tk.W, pady=6)

        self.debug_var = tk.BooleanVar()
        ttk.Checkbutton(app_form, text="Enable Debug Logging", variable=self.debug_var).grid(row=1, column=0, sticky=tk.W, pady=6)

        # Save Button
        save_frame = ttk.Frame(self)
        save_frame.pack(fill=tk.X, pady=(10, 0))
        ttk.Button(save_frame, text="Save Settings", style="Primary.TButton", command=self.save_settings).pack(side=tk.RIGHT)

    def load_values(self):
        odoo_cfg = self.config_manager.get_odoo_config()
        self.url_var.set(odoo_cfg.url)
        self.db_var.set(odoo_cfg.db)
        self.user_var.set(odoo_cfg.username)
        self.pass_var.set(odoo_cfg.password)

        app_cfg = self.config_manager.get_app_config()
        self.auto_import_var.set(app_cfg.auto_import)
        self.debug_var.set(app_cfg.debug)

    def save_settings(self):
        self.config_manager.update_odoo_config(
            url=self.url_var.get().strip(),
            db=self.db_var.get().strip(),
            username=self.user_var.get().strip(),
            password=self.pass_var.get().strip()
        )
        self.config_manager.update_app_config(
            auto_import=self.auto_import_var.get(),
            debug=self.debug_var.get()
        )
        messagebox.showinfo("Success", "Settings saved successfully.", parent=self)

    def test_connection(self):
        self.status_lbl.config(text="Status: Testing connection...", foreground="blue")
        url = self.url_var.get().strip()
        db = self.db_var.get().strip()
        user = self.user_var.get().strip()
        pwd = self.pass_var.get().strip()

        def run_test():
            connector = OdooConnector(url, db, user, pwd)
            success, msg = connector.connect()
            self.after(0, lambda: self.update_connection_result(success, msg))

        threading.Thread(target=run_test, daemon=True).start()

    def update_connection_result(self, success: bool, msg: str):
        if success:
            self.status_lbl.config(text=f"Status: {msg}", foreground="green")
            messagebox.showinfo("Connection Success", "Successfully connected to Odoo!", parent=self)
        else:
            self.status_lbl.config(text=f"Status: Failed ({msg})", foreground="red")
            messagebox.showerror("Connection Failed", f"Could not connect to Odoo:\n{msg}", parent=self)
