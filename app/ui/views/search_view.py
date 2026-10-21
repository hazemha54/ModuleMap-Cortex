"""
Global Full-Text Search View with Modern Blue Theme
"""

import tkinter as tk
from tkinter import ttk
from app.repositories.database import DatabaseManager


class SearchView(ttk.Frame):
    """View for searching across modules, models, and dependencies"""

    def __init__(self, parent, db_manager: DatabaseManager):
        super().__init__(parent, padding=25)
        self.db_manager = db_manager
        self.create_widgets()

    def create_widgets(self):
        ttk.Label(self, text="Global Search", style="Header.TLabel").pack(anchor=tk.W, pady=(0, 20))

        search_card = tk.Frame(self, bg="#ffffff", padx=15, pady=12, highlightbackground="#cbd5e1", highlightthickness=1)
        search_card.pack(fill=tk.X, pady=(0, 20))

        tk.Label(search_card, text="Search Query:", bg="#ffffff", fg="#212529", font=("Segoe UI", 10, "bold")).pack(side=tk.LEFT, padx=(0, 8))
        self.search_var = tk.StringVar()
        self.search_var.trace("w", lambda *args: self.perform_search())
        entry = ttk.Entry(search_card, textvariable=self.search_var, width=50)
        entry.pack(side=tk.LEFT, padx=(0, 10))
        entry.focus()

        table_frame = ttk.Frame(self)
        table_frame.pack(fill=tk.BOTH, expand=True)

        columns = ("type", "name", "description")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=15)

        self.tree.heading("type", text="Category")
        self.tree.heading("name", text="Name / Title")
        self.tree.heading("description", text="Details")

        self.tree.column("type", width=140, anchor=tk.CENTER)
        self.tree.column("name", width=280, anchor=tk.W)
        self.tree.column("description", width=500, anchor=tk.W)

        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def perform_search(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        query = self.search_var.get().strip()
        if len(query) < 2:
            return

        modules = self.db_manager.get_all_modules(search_query=query)
        for mod in modules:
            self.tree.insert("", tk.END, values=("Module", mod.name, f"{mod.display_name} - {mod.author}"))
