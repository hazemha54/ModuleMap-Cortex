"""
Odoo Models View — catalog table of registered models.
"""

import tkinter as tk
from tkinter import ttk

from app.repositories.database import DatabaseManager
from app.ui import theme


class ModelsView(ttk.Frame):
    """View showing Odoo models catalog."""

    def __init__(self, parent, db_manager: DatabaseManager):
        super().__init__(parent, padding=theme.SP_XL)
        self.db_manager = db_manager
        self.create_widgets()
        self.refresh()

    def create_widgets(self):
        _, holder = theme.toolbar(self, "Odoo Models Catalog",
                                  "Registered models and their hierarchy")
        ttk.Button(holder, text="🔄 Refresh", command=self.refresh).pack(side=tk.RIGHT)

        columns = {
            "id": ("ID", 60, tk.CENTER),
            "model_name": ("Model Technical Name", 230, tk.W),
            "display_name": ("Display Name", 260, tk.W),
            "model_type": ("Type", 110, tk.CENTER),
            "parent_model": ("Parent Model", 180, tk.W),
        }
        self.tree, _ = theme.data_table(self, columns, height=15)

    def refresh(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        conn = self.db_manager.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM models ORDER BY model_name")
            for row in cursor.fetchall():
                r = dict(row)
                self.tree.insert("", tk.END, values=(
                    r['id'], r['model_name'], r['display_name'] or "",
                    r['model_type'] or "model", r['parent_model'] or "",
                ))
        except Exception as e:
            print(f"Error loading models: {e}")
        finally:
            conn.close()
