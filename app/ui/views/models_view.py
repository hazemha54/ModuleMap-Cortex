"""
Odoo Models View with Modern Blue Theme
"""

import tkinter as tk
from tkinter import ttk, messagebox
from app.repositories.database import DatabaseManager


class ModelsView(ttk.Frame):
    """View showing Odoo models catalog"""

    def __init__(self, parent, db_manager: DatabaseManager):
        super().__init__(parent, padding=25)
        self.db_manager = db_manager
        self.create_widgets()
        self.refresh()

    def create_widgets(self):
        toolbar = ttk.Frame(self)
        toolbar.pack(fill=tk.X, pady=(0, 20))

        ttk.Label(toolbar, text="Odoo Models Catalog", style="Header.TLabel").pack(side=tk.LEFT)
        ttk.Button(toolbar, text="🔄 Refresh Models", command=self.refresh).pack(side=tk.RIGHT)

        table_frame = ttk.Frame(self)
        table_frame.pack(fill=tk.BOTH, expand=True)

        columns = ("id", "model_name", "display_name", "model_type", "parent_model")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=15)

        self.tree.heading("id", text="ID")
        self.tree.heading("model_name", text="Model Technical Name")
        self.tree.heading("display_name", text="Display Name")
        self.tree.heading("model_type", text="Type")
        self.tree.heading("parent_model", text="Parent Model")

        self.tree.column("id", width=60, anchor=tk.CENTER)
        self.tree.column("model_name", width=230, anchor=tk.W)
        self.tree.column("display_name", width=260, anchor=tk.W)
        self.tree.column("model_type", width=110, anchor=tk.CENTER)
        self.tree.column("parent_model", width=180, anchor=tk.W)

        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def refresh(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        conn = self.db_manager.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM models ORDER BY model_name")
            rows = cursor.fetchall()
            for row in rows:
                r = dict(row)
                self.tree.insert("", tk.END, values=(
                    r['id'], r['model_name'], r['display_name'] or "", r['model_type'] or "model", r['parent_model'] or ""
                ))
        except Exception as e:
            print(f"Error loading models: {e}")
        finally:
            conn.close()
