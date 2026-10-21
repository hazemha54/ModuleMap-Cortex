"""
Modules Management View with Modern Blue Theme
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Optional
from app.repositories.database import DatabaseManager
from app.domain.models import Module
from app.ui.dialogs.module_dialogs import ViewModuleDialog, EditModuleDialog, AddModuleDialog


class ModulesView(ttk.Frame):
    """View for managing, searching, filtering, and editing modules"""

    def __init__(self, parent, db_manager: DatabaseManager):
        super().__init__(parent, padding=25)
        self.db_manager = db_manager
        self.create_widgets()
        self.refresh()

    def create_widgets(self):
        # Header / Controls Toolbar
        toolbar = ttk.Frame(self)
        toolbar.pack(fill=tk.X, pady=(0, 20))

        ttk.Label(toolbar, text="Module Inventory", style="Header.TLabel").pack(side=tk.LEFT)

        # Action Buttons on Right
        btn_frame = ttk.Frame(toolbar)
        btn_frame.pack(side=tk.RIGHT)

        ttk.Button(btn_frame, text="+ Add Custom Module", style="Primary.TButton", command=self.on_add).pack(side=tk.LEFT, padx=6)
        ttk.Button(btn_frame, text="🔄 Refresh", command=self.refresh).pack(side=tk.LEFT, padx=6)

        # Search & Filter Bar Container
        filter_card = tk.Frame(self, bg="#ffffff", padx=15, pady=12, highlightbackground="#cbd5e1", highlightthickness=1)
        filter_card.pack(fill=tk.X, pady=(0, 20))

        tk.Label(filter_card, text="Search:", bg="#ffffff", fg="#212529", font=("Segoe UI", 10, "bold")).pack(side=tk.LEFT, padx=(0, 8))
        self.search_var = tk.StringVar()
        self.search_var.trace("w", lambda *args: self.filter_modules())
        search_entry = ttk.Entry(filter_card, textvariable=self.search_var, width=35)
        search_entry.pack(side=tk.LEFT, padx=(0, 25))

        tk.Label(filter_card, text="Filter Category:", bg="#ffffff", fg="#212529", font=("Segoe UI", 10, "bold")).pack(side=tk.LEFT, padx=(0, 8))
        self.filter_var = tk.StringVar(value="All")
        filter_cb = ttk.Combobox(filter_card, textvariable=self.filter_var, values=["All", "Installed", "Custom", "Core"], state="readonly", width=18)
        filter_cb.pack(side=tk.LEFT)
        filter_cb.bind("<<ComboboxSelected>>", lambda e: self.filter_modules())

        # Data Table with Treeview
        table_frame = ttk.Frame(self)
        table_frame.pack(fill=tk.BOTH, expand=True)

        columns = ("id", "name", "display_name", "author", "version", "category", "type", "status")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=14)

        self.tree.heading("id", text="ID")
        self.tree.heading("name", text="Technical Name")
        self.tree.heading("display_name", text="Display Name")
        self.tree.heading("author", text="Author")
        self.tree.heading("version", text="Version")
        self.tree.heading("category", text="Category")
        self.tree.heading("type", text="Type")
        self.tree.heading("status", text="Status")

        self.tree.column("id", width=60, anchor=tk.CENTER)
        self.tree.column("name", width=170, anchor=tk.W)
        self.tree.column("display_name", width=230, anchor=tk.W)
        self.tree.column("author", width=130, anchor=tk.W)
        self.tree.column("version", width=90, anchor=tk.CENTER)
        self.tree.column("category", width=130, anchor=tk.W)
        self.tree.column("type", width=95, anchor=tk.CENTER)
        self.tree.column("status", width=95, anchor=tk.CENTER)

        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.tree.bind("<Double-1>", lambda e: self.on_view_details())

        # Bottom Actions Toolbar
        actions_bar = ttk.Frame(self)
        actions_bar.pack(fill=tk.X, pady=(20, 0))

        ttk.Button(actions_bar, text="👁 View Details", command=self.on_view_details).pack(side=tk.LEFT, padx=(0, 8))
        ttk.Button(actions_bar, text="✏ Edit Module", command=self.on_edit).pack(side=tk.LEFT, padx=(0, 8))
        ttk.Button(actions_bar, text="🗑 Delete Module", command=self.on_delete).pack(side=tk.LEFT, padx=(0, 8))

    def refresh(self):
        self.search_var.set("")
        self.filter_var.set("All")
        self.filter_modules()

    def filter_modules(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        filter_type = self.filter_var.get()
        search_query = self.search_var.get().strip()

        modules = self.db_manager.get_all_modules(filter_type=filter_type if filter_type != "All" else None, search_query=search_query if search_query else None)
        for mod in modules:
            mod_type = "Custom" if mod.is_custom else "Core"
            status = "Installed" if mod.is_installed else "Not Installed"
            self.tree.insert("", tk.END, values=(
                mod.id, mod.name, mod.display_name, mod.author, mod.version, mod.category, mod_type, status
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
        if module and messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete module '{module.name}'?", parent=self):
            if self.db_manager.delete_module(mod_id):
                messagebox.showinfo("Success", "Module deleted successfully.", parent=self)
                self.filter_modules()
            else:
                messagebox.showerror("Error", "Failed to delete module.", parent=self)
