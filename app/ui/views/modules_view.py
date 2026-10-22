"""
Modules Management View — inventory table with search, filter, and row actions.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Optional

from app.repositories.database import DatabaseManager
from app.domain.models import Module
from app.ui import theme
from app.ui.dialogs.module_dialogs import ViewModuleDialog, EditModuleDialog, AddModuleDialog


class ModulesView(ttk.Frame):
    """View for managing, searching, filtering, and editing modules."""

    def __init__(self, parent, db_manager: DatabaseManager):
        super().__init__(parent, padding=theme.SP_XL)
        self.db_manager = db_manager
        self.create_widgets()
        self.refresh()

    def create_widgets(self):
        p = theme.Palette

        # Toolbar
        _, holder = theme.toolbar(self, "Module Inventory",
                                  "Search, filter, and manage your modules")
        ttk.Button(holder, text="🔄 Refresh", command=self.refresh).pack(side=tk.LEFT, padx=6)
        ttk.Button(holder, text="+ Add Custom Module", style="Primary.TButton",
                   command=self.on_add).pack(side=tk.LEFT, padx=6)

        # Filter bar
        bar = theme.surface_card(self)
        tk.Label(bar, text="Search", bg=p.SURFACE, fg=p.TEXT_MUTED,
                 font=theme.Font.MUTED, anchor="w").pack(anchor="w")
        self.search_var = tk.StringVar()
        self.search_var.trace("w", lambda *a: self.filter_modules())
        ttk.Entry(bar, textvariable=self.search_var).pack(anchor="w", fill=tk.X, pady=(4, 10))

        tk.Label(bar, text="Filter by Type", bg=p.SURFACE, fg=p.TEXT_MUTED,
                 font=theme.Font.MUTED, anchor="w").pack(anchor="w")
        self.filter_var = tk.StringVar(value="All")
        combo = ttk.Combobox(bar, textvariable=self.filter_var,
                              values=["All", "Installed", "Custom", "Core"],
                              state="readonly", width=18)
        combo.pack(anchor="w", pady=(4, 0))
        combo.bind("<<ComboboxSelected>>", lambda e: self.filter_modules())

        # Table in a surface card
        table_card = tk.Frame(self, bg=p.SURFACE,
                              highlightbackground=p.BORDER, highlightthickness=1)
        table_card.pack(fill=tk.BOTH, expand=True)

        columns = ("id", "name", "display_name", "author", "version", "category", "type", "status")
        self.tree = ttk.Treeview(table_card, columns=columns, show="headings", height=14)

        headings = {
            "id": "ID", "name": "Technical Name", "display_name": "Display Name",
            "author": "Author", "version": "Version", "category": "Category",
            "type": "Type", "status": "Status",
        }
        for col, label in headings.items():
            self.tree.heading(col, text=label)

        self.tree.column("id", width=60, anchor=tk.CENTER)
        self.tree.column("name", width=170, anchor=tk.W)
        self.tree.column("display_name", width=230, anchor=tk.W)
        self.tree.column("author", width=130, anchor=tk.W)
        self.tree.column("version", width=90, anchor=tk.CENTER)
        self.tree.column("category", width=130, anchor=tk.W)
        self.tree.column("type", width=95, anchor=tk.CENTER)
        self.tree.column("status", width=95, anchor=tk.CENTER)

        scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.tree.bind("<Double-1>", lambda e: self.on_view_details())

        # Bottom actions
        actions = tk.Frame(self, bg=p.BG)
        actions.pack(fill=tk.X, pady=(16, 0))
        ttk.Button(actions, text="👁 View Details", command=self.on_view_details).pack(side=tk.LEFT, padx=(0, 8))
        ttk.Button(actions, text="✏ Edit Module", command=self.on_edit).pack(side=tk.LEFT, padx=(0, 8))
        ttk.Button(actions, text="🗑 Delete Module", command=self.on_delete).pack(side=tk.LEFT, padx=(0, 8))

    def refresh(self):
        self.search_var.set("")
        self.filter_var.set("All")
        self.filter_modules()

    def filter_modules(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        filter_type = self.filter_var.get()
        search_query = self.search_var.get().strip()

        modules = self.db_manager.get_all_modules(
            filter_type=filter_type if filter_type != "All" else None,
            search_query=search_query if search_query else None,
        )
        for mod in modules:
            mod_type = "Custom" if mod.is_custom else "Core"
            status = "Installed" if mod.is_installed else "Not Installed"
            self.tree.insert("", tk.END, values=(
                mod.id, mod.name, mod.display_name, mod.author, mod.version,
                mod.category, mod_type, status,
            ))

    def get_selected_module_id(self) -> Optional[int]:
        selected = self.tree.selection()
        if not selected:
            return None
        item = self.tree.item(selected[0])
        return int(item['values'][0])

    def on_view_details(self):
        mod_id = self.get_selected_module_id()
        if not mod_id:
            messagebox.showwarning("Selection", "Please select a module first.", parent=self)
            return
        module = self.db_manager.get_module(mod_id)
        if module:
            ViewModuleDialog(self, module)

    def on_edit(self):
        mod_id = self.get_selected_module_id()
        if not mod_id:
            messagebox.showwarning("Selection", "Please select a module first.", parent=self)
            return
        module = self.db_manager.get_module(mod_id)
        if module:
            EditModuleDialog(self, module, on_save=self.save_module_changes)

    def save_module_changes(self, module: Module):
        if self.db_manager.update_module(module):
            messagebox.showinfo("Success", f"Module {module.name} updated successfully.", parent=self)
            self.filter_modules()
        else:
            messagebox.showerror("Error", f"Failed to update module {module.name}.", parent=self)

    def on_add(self):
        AddModuleDialog(self, on_save=self.create_module)

    def create_module(self, module: Module):
        if self.db_manager.add_module(module):
            messagebox.showinfo("Success", f"Module {module.name} created successfully.", parent=self)
            self.filter_modules()
        else:
            messagebox.showerror("Error", f"Failed to create module {module.name} (name may already exist).", parent=self)

    def on_delete(self):
        mod_id = self.get_selected_module_id()
        if not mod_id:
            messagebox.showwarning("Selection", "Please select a module first.", parent=self)
            return
        module = self.db_manager.get_module(mod_id)
        if module and messagebox.askyesno(
            "Confirm Delete",
            f"Are you sure you want to delete module '{module.name}'?",
            parent=self,
        ):
            if self.db_manager.delete_module(mod_id):
                messagebox.showinfo("Success", "Module deleted successfully.", parent=self)
                self.filter_modules()
            else:
                messagebox.showerror("Error", "Failed to delete module.")
