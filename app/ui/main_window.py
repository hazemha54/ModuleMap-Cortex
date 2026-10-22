"""
Main Window Shell — premium enterprise theme with a polished sidebar and
lazy-loaded views. All global styling lives in app.ui.theme.
"""

import tkinter as tk
from tkinter import ttk

from app.repositories.database import DatabaseManager
from app.services.config_manager import ConfigManager
from app.ui import theme
from app.ui.views.dashboard_view import DashboardView
from app.ui.views.modules_view import ModulesView
from app.ui.views.dependencies_view import DependenciesView
from app.ui.views.models_view import ModelsView
from app.ui.views.changes_view import ChangesView
from app.ui.views.search_view import SearchView
from app.ui.views.settings_view import SettingsView
from app.ui.views.help_view import HelpView


class MainWindow(tk.Tk):
    """Main Application Window for ModuleMap-Cortex."""

    def __init__(self, db_manager: DatabaseManager, config_manager: ConfigManager):
        super().__init__()
        self.db_manager = db_manager
        self.config_manager = config_manager

        app_cfg = self.config_manager.get_app_config()
        self.title("ModuleMap-Cortex — Enterprise Odoo Architecture Suite")
        self.geometry(f"{app_cfg.window_width}x{app_cfg.window_height}")
        self.minsize(1050, 720)

        self.p = theme.Palette
        self.f = theme.Font

        self.configure(bg=self.p.BG)
        theme.apply_theme(self)
        self.create_layout()

    def create_layout(self):
        p, f = self.p, self.f
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

        # ------------------------------------------------------------------
        # 1. Sidebar (deep navy)
        # ------------------------------------------------------------------
        sidebar = tk.Frame(self, bg=p.SIDEBAR, width=240)
        sidebar.grid(row=0, column=0, sticky="nsew")
        sidebar.grid_propagate(False)

        # Brand block
        brand = tk.Frame(sidebar, bg=p.SIDEBAR, pady=24)
        brand.pack(fill=tk.X, padx=20)

        # Logomark — a small rounded accent square with an inner "M"
        mark = tk.Frame(brand, bg=p.ACCENT, width=34, height=34,
                         highlightbackground=p.ACCENT_DARK, highlightthickness=0)
        mark.pack(anchor=tk.W, pady=(0, 10))
        mark.pack_propagate(False)
        tk.Label(mark, text="M", bg=p.ACCENT, fg="#ffffff", font=("Segoe UI", 15, "bold"))\
            .pack(expand=True)

        tk.Label(brand, text="ModuleMap", bg=p.SIDEBAR, fg="#ffffff",
                 font=f.BRAND).pack(anchor=tk.W)
        tk.Label(brand, text="Cortex · Enterprise Suite", bg=p.SIDEBAR,
                 fg=p.INFO, font=f.BRAND_SUB).pack(anchor=tk.W, pady=(2, 0))

        # Hairline divider
        tk.Frame(sidebar, bg=p.SIDEBAR_BORDER, height=1).pack(fill=tk.X, padx=20, pady=16)

        # Section caption
        tk.Label(sidebar, text="WORKSPACE", bg=p.SIDEBAR, fg=p.TEXT_FAINT,
                 font=(f.FAMILY, 8, "bold")).pack(anchor=tk.W, padx=22, pady=(0, 6))

        # Navigation
        nav_buttons = [
            ("📊", "Dashboard", "dashboard"),
            ("📦", "Modules", "modules"),
            ("🔗", "Dependencies", "dependencies"),
            ("🏗️", "Odoo Models", "models"),
            ("🔍", "Changes & Audit", "changes"),
            ("🔎", "Global Search", "search"),
            ("⚙️", "Settings", "settings"),
            ("📖", "Help & Docs", "help"),
        ]

        self.views = {}
        self.buttons = {}

        nav = tk.Frame(sidebar, bg=p.SIDEBAR)
        nav.pack(fill=tk.BOTH, expand=True, padx=12)

        for icon, label, key in nav_buttons:
            row = self._nav_button(nav, icon, label, key)
            self.buttons[key] = row

        # Footer
        footer = tk.Frame(sidebar, bg=p.SIDEBAR, pady=16)
        footer.pack(side=tk.BOTTOM, fill=tk.X, padx=20)
        tk.Frame(footer, bg=p.SIDEBAR_BORDER, height=1).pack(fill=tk.X, pady=(0, 12))
        tk.Label(footer, text="v0.1  ·  Hazem Hadj Ahmed", bg=p.SIDEBAR,
                 fg=p.TEXT_FAINT, font=f.CAPTION).pack(anchor=tk.W)

        # ------------------------------------------------------------------
        # 2. Content container
        # ------------------------------------------------------------------
        self.content_frame = ttk.Frame(self)
        self.content_frame.grid(row=0, column=1, sticky="nsew")
        self.content_frame.rowconfigure(0, weight=1)
        self.content_frame.columnconfigure(0, weight=1)

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

    def _nav_button(self, parent, icon: str, label: str, key: str) -> tk.Button:
        """A hoverable nav row that shows a persistent selected state.

        Uses a real tk.Button so the click is handled natively and reliably.
        We still control the three visual states ourselves (idle / hover /
        selected) via background colors and an accent indicator frame.
        """
        p = self.p
        f = self.f

        # Clickable button with the accent indicator packed inside its left.
        row = tk.Button(
            parent, text=f"{icon}   {label}",
            font=f.NAV, anchor="w", relief="flat", bd=0,
            bg=p.SIDEBAR, fg=p.TEXT_MUTED,
            activebackground=p.SIDEBAR, activeforeground=p.TEXT_MUTED,
            cursor="hand2", highlightthickness=0,
            command=lambda: self.switch_view(key),
        )
        row.pack(fill=tk.X, pady=2, ipady=6, padx=0)

        # Accent bar overlaid on the button's left edge.
        accent = tk.Frame(row, bg=p.SIDEBAR, width=3)
        accent.place(x=0, y=0, relheight=1.0)
        row._accent = accent
        row._key = key

        def hover(_):
            self._paint(row, selected=False, hover=True)

        def leave(_):
            self._paint(row, selected=(self._selected == key))

        row.bind("<Enter>", hover)
        row.bind("<Leave>", leave)

        # Initial paint.
        self._paint(row, selected=False)
        return row

    def _paint(self, row: tk.Button, selected: bool, hover: bool = False):
        """Paint a nav row in its idle, hover, or selected state."""
        p = self.p
        if selected:
            bg, fg, font = p.ACCENT, p.ACCENT_TEXT, self.f.NAV_BOLD
            accent_bg = "#ffffff"
        elif hover:
            bg, fg, font = p.SIDEBAR_HOVER, p.ACCENT_HOVER, self.f.NAV
            accent_bg = p.SIDEBAR_HOVER
        else:
            bg, fg, font = p.SIDEBAR, p.TEXT_MUTED, self.f.NAV
            accent_bg = p.SIDEBAR

        row.config(bg=bg, fg=fg, font=font,
                   activebackground=bg, activeforeground=fg)
        row._accent.config(bg=accent_bg)

    def switch_view(self, view_key: str):
        # Lazy-instantiate the view on first visit.
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

        # Repaint every nav row so exactly one shows the selected state.
        self._selected = view_key
        for key, row in self.buttons.items():
            self._paint(row, selected=(key == view_key))
