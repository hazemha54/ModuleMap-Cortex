"""
Dashboard View — KPI cards + recent modules, using the shared theme.
"""

import tkinter as tk
from tkinter import ttk

from app.repositories.database import DatabaseManager
from app.ui import theme


class DashboardView(ttk.Frame):
    """Dashboard view showing overview stats and recent modules."""

    def __init__(self, parent, db_manager: DatabaseManager):
        super().__init__(parent, padding=theme.SP_XL)
        self.db_manager = db_manager
        self.create_widgets()
        self.refresh()

    def create_widgets(self):
        p = theme.Palette

        # Header
        header, _ = theme.toolbar(self, "Dashboard Overview",
                                  "Welcome to ModuleMap Cortex")

        # Stats card row
        cards = ttk.Frame(self)
        cards.pack(fill=tk.X, pady=(0, 24))
        for i in range(4):
            cards.columnconfigure(i, weight=1, uniform="card")

        self.card_total = theme.stat_card(cards, "Total Modules", "0", "#2563eb", 0, 4)
        self.card_custom = theme.stat_card(cards, "Custom Modules", "0", "#0d9488", 1, 4)
        self.card_models = theme.stat_card(cards, "Odoo Models", "0", "#7c3aed", 2, 4)
        self.card_deps = theme.stat_card(cards, "Dependencies", "0", "#4f46e5", 3, 4)

        # Recent modules card
        recent = ttk.Frame(self)
        recent.pack(fill=tk.BOTH, expand=True)

        title_row = tk.Frame(recent, bg=p.BG)
        title_row.pack(fill=tk.X, pady=(0, 12))
        tk.Label(title_row, text="Recent Modules Inventory", bg=p.BG,
                 fg=p.TEXT, font=theme.Font.H2).pack(side=tk.LEFT)

        # Table inside a white surface card
        table_card = tk.Frame(recent, bg=p.SURFACE,
                              highlightbackground=p.BORDER, highlightthickness=1)
        table_card.pack(fill=tk.BOTH, expand=True)

        columns = ("name", "display_name", "author", "version", "category", "type")
        self.tree = ttk.Treeview(table_card, columns=columns, show="headings", height=12)

        headings = {
            "name": "Technical Name", "display_name": "Display Name",
            "author": "Author", "version": "Version",
            "category": "Category", "type": "Type",
        }
        for col, label in headings.items():
            self.tree.heading(col, text=label)

        self.tree.column("name", width=160, anchor=tk.W)
        self.tree.column("display_name", width=240, anchor=tk.W)
        self.tree.column("author", width=140, anchor=tk.W)
        self.tree.column("version", width=90, anchor=tk.CENTER)
        self.tree.column("category", width=130, anchor=tk.W)
        self.tree.column("type", width=100, anchor=tk.CENTER)

        scrollbar = ttk.Scrollbar(recent, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def refresh(self):
        stats = self.db_manager.get_stats()
        self.card_total.config(text=str(stats["total_modules"]))
        self.card_custom.config(text=str(stats["custom_modules"]))
        self.card_models.config(text=str(stats["total_models"]))
        self.card_deps.config(text=str(stats["total_dependencies"]))

        for item in self.tree.get_children():
            self.tree.delete(item)

        modules = self.db_manager.get_all_modules()[:15]
        for mod in modules:
            mod_type = "Custom" if mod.is_custom else "Core"
            self.tree.insert("", tk.END, values=(
                mod.name, mod.display_name, mod.author, mod.version, mod.category, mod_type
            ))
