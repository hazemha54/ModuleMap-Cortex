"""
Dependencies Mapping View with Modern Blue Theme
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import json
from app.repositories.database import DatabaseManager


class DependenciesView(ttk.Frame):
    """View showing module dependencies and allowing export"""

    def __init__(self, parent, db_manager: DatabaseManager):
        super().__init__(parent, padding=25)
        self.db_manager = db_manager
        self.create_widgets()
        self.refresh()

    def create_widgets(self):
        toolbar = ttk.Frame(self)
        toolbar.pack(fill=tk.X, pady=(0, 20))

        ttk.Label(toolbar, text="Module Dependencies Map", style="Header.TLabel").pack(side=tk.LEFT)
        ttk.Button(toolbar, text="📥 Export Dependencies JSON", style="Primary.TButton", command=self.export_json).pack(side=tk.RIGHT)

        table_frame = ttk.Frame(self)
        table_frame.pack(fill=tk.BOTH, expand=True)

        columns = ("module_name", "display_name", "dependency")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=15)

        self.tree.heading("module_name", text="Module Name")
        self.tree.heading("display_name", text="Display Name")
        self.tree.heading("dependency", text="Depends On")

        self.tree.column("module_name", width=220, anchor=tk.W)
        self.tree.column("display_name", width=280, anchor=tk.W)
        self.tree.column("dependency", width=280, anchor=tk.W)

        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

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
            title="Export Dependencies"
        )
        if not file_path:
            return

        try:
            data = []
            modules = self.db_manager.get_all_modules()
            for mod in modules:
                data.append({
                    "module": mod.name,
                    "display_name": mod.display_name,
                    "dependencies": mod.dependencies
                })

            with open(file_path, 'w') as f:
                json.dump(data, f, indent=2)

            messagebox.showinfo("Success", f"Dependencies exported successfully to {file_path}", parent=self)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export dependencies: {e}", parent=self)
