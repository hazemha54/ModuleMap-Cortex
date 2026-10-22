"""
Settings View — Odoo connection and app preferences, themed.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import threading

from app.services.config_manager import ConfigManager
from app.services.odoo_service import OdooConnector
from app.ui import theme


class SettingsView(ttk.Frame):
    """View for configuring Odoo credentials and app settings."""

    def __init__(self, parent, config_manager: ConfigManager):
        super().__init__(parent, padding=theme.SP_XL)
        self.config_manager = config_manager
        self.create_widgets()
        self.load_values()

    def create_widgets(self):
        p = theme.Palette
        f = theme.Font

        theme.toolbar(self, "Settings", "Odoo connection & application preferences")

        # Odoo Config card
        odoo_card = theme.surface_card(self)
        tk.Label(odoo_card, text="Odoo Server Configuration", bg=p.SURFACE,
                 fg=p.TEXT, font=f.H3, anchor="w").pack(anchor="w", pady=(0, 12))

        form = tk.Frame(odoo_card, bg=p.SURFACE)
        form.pack(fill=tk.X)

        fields = [
            ("Odoo URL", "url"),
            ("Database Name", "db"),
            ("Username", "user"),
            ("Password / API Key", "pass"),
        ]
        self.url_var = tk.StringVar()
        self.db_var = tk.StringVar()
        self.user_var = tk.StringVar()
        self.pass_var = tk.StringVar()
        vars = {"url": self.url_var, "db": self.db_var,
                "user": self.user_var, "pass": self.pass_var}

        for i, (label, key) in enumerate(fields):
            tk.Label(form, text=label, bg=p.SURFACE, fg=p.TEXT_MUTED,
                     font=f.MUTED, anchor="w").grid(row=i * 2, column=1, sticky="w",
                                                     pady=(8, 0))
            show = "*" if key == "pass" else ""
            entry = ttk.Entry(form, textvariable=vars[key], show=show)
            entry.grid(row=i * 2 + 1, column=1, sticky="ew", pady=(2, 8))
        form.columnconfigure(1, weight=1)

        btn_box = tk.Frame(odoo_card, bg=p.SURFACE)
        btn_box.pack(fill=tk.X, pady=(8, 0))
        ttk.Button(btn_box, text="Test Connection", style="Primary.TButton",
                   command=self.test_connection).pack(side=tk.LEFT)
        self.status_lbl = tk.Label(btn_box, text="Status: Not tested", bg=p.SURFACE,
                                   fg=p.TEXT_MUTED, font=f.MUTED)
        self.status_lbl.pack(side=tk.LEFT, padx=16)

        # General settings card
        gen_card = theme.surface_card(self)
        tk.Label(gen_card, text="General", bg=p.SURFACE, fg=p.TEXT,
                 font=f.H3, anchor="w").pack(anchor="w", pady=(0, 10))

        self.auto_import_var = tk.BooleanVar()
        ttk.Checkbutton(gen_card, text="Auto-import modules on startup",
                        variable=self.auto_import_var).pack(anchor="w", pady=4)
        self.debug_var = tk.BooleanVar()
        ttk.Checkbutton(gen_card, text="Enable debug logging",
                        variable=self.debug_var).pack(anchor="w", pady=4)

        # Save
        save_row = tk.Frame(self, bg=p.BG)
        save_row.pack(fill=tk.X, pady=(10, 0))
        ttk.Button(save_row, text="Save Settings", style="Primary.TButton",
                   command=self.save_settings).pack(side=tk.RIGHT)

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
            password=self.pass_var.get().strip(),
        )
        self.config_manager.update_app_config(
            auto_import=self.auto_import_var.get(),
            debug=self.debug_var.get(),
        )
        messagebox.showinfo("Success", "Settings saved successfully.", parent=self)

    def test_connection(self):
        self.status_lbl.config(text="Status: Testing connection…", foreground=theme.Palette.ACCENT)
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
        p = theme.Palette
        if success:
            self.status_lbl.config(text=f"Status: {msg}", foreground=p.SUCCESS)
            messagebox.showinfo("Connection Success", "Successfully connected to Odoo!", parent=self)
        else:
            self.status_lbl.config(text=f"Status: Failed ({msg})", foreground=p.DANGER)
            messagebox.showerror("Connection Failed", f"Could not connect to Odoo:\n{msg}", parent=self)
