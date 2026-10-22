"""
Changes & Customizations View — audit log of detected changes.
"""

import tkinter as tk
from tkinter import ttk

from app.repositories.database import DatabaseManager
from app.ui import theme


class ChangesView(ttk.Frame):
    """View showing detected module customizations and changes."""

    def __init__(self, parent, db_manager: DatabaseManager):
        super().__init__(parent, padding=theme.SP_XL)
        self.db_manager = db_manager
        self.create_widgets()
        self.refresh()

    def create_widgets(self):
        _, holder = theme.toolbar(self, "Changes & Customizations",
                                  "Detected customizations, newest first")
        ttk.Button(holder, text="🔄 Refresh", command=self.refresh).pack(side=tk.RIGHT)

        columns = {
            "id": ("ID", 60, tk.CENTER),
            "module_id": ("Module", 110, tk.CENTER),
            "change_type": ("Change Type", 130, tk.W),
            "change_description": ("Description", 360, tk.W),
            "severity": ("Severity", 100, tk.CENTER),
            "detected_at": ("Detected", 160, tk.CENTER),
        }
        self.tree, _ = theme.data_table(self, columns, height=15)

    def refresh(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        conn = self.db_manager.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM changes ORDER BY detected_at DESC")
            for row in cursor.fetchall():
                r = dict(row)
                self.tree.insert("", tk.END, values=(
                    r['id'], r['module_id'], r['change_type'],
                    r['change_description'], r['severity'], r['detected_at'],
                ))
        except Exception as e:
            print(f"Error loading changes: {e}")
        finally:
            conn.close()
