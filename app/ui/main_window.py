"""
Main Window Shell with Modern Blue Theme & Sidebar Navigation & Lazy-Loaded Views
"""

import tkinter as tk
from tkinter import ttk
from app.repositories.database import DatabaseManager
from app.services.config_manager import ConfigManager
from app.ui.views.dashboard_view import DashboardView
from app.ui.views.modules_view import ModulesView
from app.ui.views.dependencies_view import DependenciesView
from app.ui.views.models_view import ModelsView
from app.ui.views.changes_view import ChangesView
from app.ui.views.search_view import SearchView
from app.ui.views.settings_view import SettingsView
from app.ui.views.help_view import HelpView


class MainWindow(tk.Tk):
    """Main Application Window for ModuleMap-Cortex (Tkinter Modern Blue Theme)"""

    def __init__(self, db_manager: DatabaseManager, config_manager: ConfigManager):
        super().__init__()
        self.db_manager = db_manager
        self.config_manager = config_manager

        app_cfg = self.config_manager.get_app_config()
        self.title("ModuleMap-Cortex — Enterprise Odoo Architecture Suite")
        self.geometry(f"{app_cfg.window_width}x{app_cfg.window_height}")
        self.minsize(1050, 720)

        # Configure Modern Theme & Colors
        self.bg_dark = "#111e2e"       # Sidebar background (Dark Navy)
        self.bg_light = "#f4f6f9"      # Main background (Off-white / light gray)
        self.accent_blue = "#0056b3"   # Primary blue accent
        self.accent_hover = "#007bff"  # Hover blue
        self.text_light = "#ffffff"    # Sidebar text
        self.text_dark = "#212529"     # Content text

        self.configure(bg=self.bg_light)
        self.setup_styles()
        self.create_layout()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")

        # Configure global fonts and colors
        style.configure(".", background=self.bg_light, foreground=self.text_dark, font=("Segoe UI", 10))
        style.configure("TFrame", background=self.bg_light)
        style.configure("TLabel", background=self.bg_light, foreground=self.text_dark, font=("Segoe UI", 10))
        style.configure("Header.TLabel", font=("Segoe UI", 18, "bold"), foreground="#1e3d59")
        style.configure("SubHeader.TLabel", font=("Segoe UI", 13, "bold"), foreground="#1e3d59")

        # Modern Button Style
        style.configure("TButton",
                        font=("Segoe UI", 10, "bold"),
                        padding=8,
                        relief="flat",
                        background="#e2e8f0",
                        foreground="#1e293b")
        style.map("TButton",
                  background=[("active", self.accent_blue), ("pressed", "#004085")],
                  foreground=[("active", "#ffffff"), ("pressed", "#ffffff")])

        # Primary Action Button Style
        style.configure("Primary.TButton",
                        font=("Segoe UI", 10, "bold"),
                        padding=8,
                        background=self.accent_blue,
                        foreground="#ffffff")
        style.map("Primary.TButton",
                  background=[("active", self.accent_hover), ("pressed", "#004085")],
                  foreground=[("active", "#ffffff"), ("pressed", "#ffffff")])

        # Sidebar Button Style
        style.configure("Sidebar.TButton",
                        font=("Segoe UI", 11, "bold"),
                        anchor="w",
                        padding=12,
                        background=self.bg_dark,
                        foreground=self.text_light,
                        borderwidth=0)
        style.map("Sidebar.TButton",
                  background=[("active", self.accent_blue), ("pressed", "#004085")],
                  foreground=[("active", "#ffffff"), ("pressed", "#ffffff")])

        # Treeview Styling
        style.configure("Treeview",
                        background="#ffffff",
                        foreground="#212529",
                        fieldbackground="#ffffff",
                        rowheight=26,
                        font=("Segoe UI", 10))
        style.configure("Treeview.Heading",
                        background="#1e3d59",
                        foreground="#ffffff",
                        font=("Segoe UI", 10, "bold"),
                        relief="flat")
        style.map("Treeview.Heading", background=[("active", self.accent_blue)])

        # LabelFrame
        style.configure("TLabelframe", background=self.bg_light, bordercolor="#cbd5e1", relief="solid")
        style.configure("TLabelframe.Label", background=self.bg_light, foreground="#1e3d59", font=("Segoe UI", 11, "bold"))

    def create_layout(self):
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

        # 1. Sidebar Navigation Frame (Dark Navy)
        sidebar = tk.Frame(self, bg=self.bg_dark, width=240)
        sidebar.grid(row=0, column=0, sticky="nsew")
        sidebar.grid_propagate(False)

        # App Logo / Title
        logo_frame = tk.Frame(sidebar, bg=self.bg_dark, pady=25)
        logo_frame.pack(fill=tk.X, padx=15)

        title_lbl = tk.Label(logo_frame, text="MODULEMAP", bg=self.bg_dark, fg="#ffffff", font=("Segoe UI", 16, "bold"))
        title_lbl.pack(anchor=tk.W)
        subtitle_lbl = tk.Label(logo_frame, text="V 0.1 by Hazem Hadj Ahmed", bg=self.bg_dark, fg="#38bdf8", font=("Segoe UI", 9, "bold"))
        subtitle_lbl.pack(anchor=tk.W, pady=(2, 0))

        # Divider line
        ttk.Separator(sidebar, orient=tk.HORIZONTAL).pack(fill=tk.X, padx=15, pady=10)

        # Navigation Buttons
        nav_buttons = [
            ("📊  Dashboard", "dashboard"),
            ("📦  Modules", "modules"),
            ("🔗  Dependencies", "dependencies"),
            ("🏗️  Odoo Models", "models"),
            ("🔍  Changes & Audit", "changes"),
            ("🔎  Global Search", "search"),
            ("⚙️  Settings", "settings"),
            ("📖  Help & Docs", "help"),
        ]

        self.views = {}
        self.buttons = {}

        nav_container = tk.Frame(sidebar, bg=self.bg_dark)
        nav_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        for text, view_key in nav_buttons:
            btn = ttk.Button(nav_container, text=text, style="Sidebar.TButton", command=lambda vk=view_key: self.switch_view(vk))
            btn.pack(fill=tk.X, pady=3)
            self.buttons[view_key] = btn

        # Footer in sidebar
        footer_frame = tk.Frame(sidebar, bg=self.bg_dark, pady=15)
        footer_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=15)
        footer_lbl = tk.Label(footer_frame, text="V 0.1 — Hazem Hadj Ahmed", bg=self.bg_dark, fg="#94a3b8", font=("Segoe UI", 8), justify=tk.LEFT)
        footer_lbl.pack(anchor=tk.W)

        # 2. Content Container Frame
        self.content_frame = ttk.Frame(self)
        self.content_frame.grid(row=0, column=1, sticky="nsew")
        self.content_frame.rowconfigure(0, weight=1)
        self.content_frame.columnconfigure(0, weight=1)

        # Lazy-loaded views map (instantiated on first click)
        self.view_classes = {
            "dashboard": DashboardView,
            "modules": ModulesView,
            "dependencies": DependenciesView,
            "models": ModelsView,
            "changes": ChangesView,
            "search": SearchView,
            "settings": SettingsView,
            "help": HelpView,
        }

        self.switch_view("dashboard")

    def switch_view(self, view_key: str):
        # Lazy initialize view if not already created
        if view_key not in self.views:
            view_class = self.view_classes.get(view_key)
            if view_class:
                if view_key == "settings":
                    self.views[view_key] = view_class(self.content_frame, self.config_manager)
                elif view_key == "help":
                    self.views[view_key] = view_class(self.content_frame)
                else:
                    self.views[view_key] = view_class(self.content_frame, self.db_manager)
                self.views[view_key].grid(row=0, column=0, sticky="nsew")

        view = self.views.get(view_key)
        if view:
            view.tkraise()
            if hasattr(view, "refresh"):
                view.refresh()

            # Highlight active button
            for vk, btn in self.buttons.items():
                if vk == view_key:
                    btn.state(['pressed'])
                else:
                    btn.state(['!pressed'])
