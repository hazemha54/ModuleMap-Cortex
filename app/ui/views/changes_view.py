"""
Changes & Customizations View with Modern Blue Theme
"""

import tkinter as tk
from tkinter import ttk
from app.repositories.database import DatabaseManager


class ChangesView(ttk.Frame):
    """View showing detected module customizations and changes"""

    def __init__(self, parent, db_manager: DatabaseManager):
        super().__init__(parent, padding=25)
        self.db_manager = db_manager
        self.create_widgets()
        self.refresh()

    def create_widgets(self):
        toolbar = ttk.Frame(self)
        toolbar.pack(fill=tk.X, pady=(0, 20))

        ttk.Label(toolbar, text="Module Changes & Customizations", style="Header.TLabel").pack(side=tk.LEFT)
        ttk.Button(toolbar, text="🔄 Refresh", command=self.refresh).pack(side=tk.RIGHT)

        table_frame = ttk.Frame(self)
        table_frame.pack(fill=tk.BOTH, expand=True)

        columns = ("id", "module_id", "change_type", "change_description", "severity", "detected_at")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=15)

        self.tree.heading("id", text="ID")
        self.tree.heading("module_id", text="Module ID")
        self.tree.heading("change_type", text="Change Type")
        self.tree.heading("change_description", text="Description")
        self.tree.heading("severity", text="Severity")
        self.tree.heading("detected_at", text="Detected At")

        self.tree.column("id", width=60, anchor=tk.CENTER)
        self.tree.column("module_id", width=90, anchor=tk.CENTER)
        self.tree.column("change_type", width=130, anchor=tk.W)
        self.tree.column("change_description", width=360, anchor=tk.W)
        self.tree.column("severity", width=100, anchor=tk.CENTER)
        self.tree.column("detected_at", width=160, anchor=tk.CENTER)

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
            cursor.execute("SELECT * FROM changes ORDER BY detected_at DESC")
            rows = cursor.fetchall()
            for row in rows:
                r = dict(row)
                self.tree.insert("", tk.END, values=(
                    r['id'], r['module_id'], r['change_type'], r['change_description'], r['severity'], r['detected_at']
                ))
        except Exception as e:
            print(f"Error loading changes: {e}")
        finally:
            conn.close()
