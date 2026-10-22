"""
Dependencies Mapping View — module dependency table with JSON export.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import json

from app.repositories.database import DatabaseManager
from app.ui import theme


class DependenciesView(ttk.Frame):
    """View showing module dependencies and allowing export."""

    def __init__(self, parent, db_manager: DatabaseManager):
        super().__init__(parent, padding=theme.SP_XL)
        self.db_manager = db_manager
        self.create_widgets()
        self.refresh()

    def create_widgets(self):
        _, holder = theme.toolbar(self, "Module Dependencies Map",
                                  "How your modules depend on one another")
        ttk.Button(holder, text="📥 Export JSON", style="Primary.TButton",
                   command=self.export_json).pack(side=tk.RIGHT)

        columns = {
            "module_name": ("Module Name", 220, tk.W),
            "display_name": ("Display Name", 280, tk.W),
            "dependency": ("Depends On", 280, tk.W),
        }
        self.tree, _ = theme.data_table(self, columns, height=15)

    def refresh(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        modules = self.db_manager.get_all_modules()
        for mod in modules:
            if mod.dependencies:
                for dep in mod.dependencies:
                    self.tree.insert("", tk.END, values=(mod.name, mod.display_name, dep))
            else:
                self.tree.insert("", tk.END, values=(mod.name, mod.display_name, "(None)"))

    def export_json(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON Files", "*.json"), ("All Files", "*.*")],
            title="Export Dependencies",
        )
        if not file_path:
            return

        try:
            data = []
            for mod in self.db_manager.get_all_modules():
                data.append({
                    "module": mod.name,
                    "display_name": mod.display_name,
                    "dependencies": mod.dependencies,
                })

            with open(file_path, "w") as f:
                json.dump(data, f, indent=2)

            messagebox.showinfo("Success", f"Dependencies exported successfully to {file_path}", parent=self)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export dependencies: {e}", parent=self)
