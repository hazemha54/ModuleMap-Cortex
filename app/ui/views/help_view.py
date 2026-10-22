"""
Help & Documentation View — themed.
"""

import tkinter as tk
from tkinter import ttk

from app.ui import theme


class HelpView(ttk.Frame):
    """View displaying help documentation and usage guide."""

    def __init__(self, parent):
        super().__init__(parent, padding=theme.SP_XL)
        self.create_widgets()

    def create_widgets(self):
        p = theme.Palette
        f = theme.Font

        theme.toolbar(self, "Help & Documentation",
                      "Guide to the ModuleMap-Cortex suite")

        card = theme.surface_panel(self)

        text = tk.Text(card, wrap=tk.WORD, font=f.BASE, padx=18, pady=18,
                       bg=p.SURFACE, fg=p.TEXT, highlightthickness=0,
                       relief="flat")
        text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(card, orient=tk.VERTICAL, command=text.yview)
        text.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        help_content = """ModuleMap-Cortex: Professional Odoo Module Mapping & Analysis Suite

Overview
ModuleMap-Cortex provides enterprise-grade tools for auditing, mapping, visualizing,
and analyzing Odoo ERP modules and database architectures.

Features
1. Dashboard — overview metrics, KPI cards, and the recent modules registry.
2. Modules — comprehensive module inventory with search, filtering, and full CRUD.
3. Dependencies — dependency map and JSON export.
4. Models — Odoo model catalog browser.
5. Changes — customization and change tracking log.
6. Search — global full-text search across modules and components.
7. Settings — Odoo server connection configuration and live connection testing.

Navigation
Use the left sidebar to switch between views instantly. All database actions
operate against the local SQLite repository (modulemap_cortex.db).
"""

        text.insert("1.0", help_content)
        text.config(state=tk.DISABLED)
