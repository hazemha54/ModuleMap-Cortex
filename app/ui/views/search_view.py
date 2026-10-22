"""
Global Full-Text Search View.
"""

import tkinter as tk
from tkinter import ttk

from app.repositories.database import DatabaseManager
from app.ui import theme


class SearchView(ttk.Frame):
    """View for searching across modules, models, and dependencies."""

    def __init__(self, parent, db_manager: DatabaseManager):
        super().__init__(parent, padding=theme.SP_XL)
        self.db_manager = db_manager
        self.create_widgets()

    def create_widgets(self):
        p = theme.Palette
        theme.toolbar(self, "Global Search",
                      "Search across modules, models, and components")

        # Hero search input in a surface card
        card = theme.surface_card(self)
        tk.Label(card, text="Search Query", bg=p.SURFACE, fg=p.TEXT_MUTED,
                 font=theme.Font.MUTED, anchor="w").pack(anchor="w")
        self.search_var = tk.StringVar()
        self.search_var.trace("w", lambda *a: self.perform_search())
        entry = ttk.Entry(card, textvariable=self.search_var)
        entry.pack(anchor="w", fill=tk.X, pady=(4, 0))
        entry.focus()

        # Results table
        columns = {
            "type": ("Category", 140, tk.CENTER),
            "name": ("Name / Title", 280, tk.W),
            "description": ("Details", 500, tk.W),
        }
        self.tree, _ = theme.data_table(self, columns, height=15)

    def perform_search(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        query = self.search_var.get().strip()
        if len(query) < 2:
            return

        for mod in self.db_manager.get_all_modules(search_query=query):
            self.tree.insert("", tk.END, values=(
                "Module", mod.name, f"{mod.display_name} - {mod.author}",
            ))
