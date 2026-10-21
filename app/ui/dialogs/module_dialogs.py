"""
Modal Dialogs for Module Management (Add, Edit, View Details)
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Callable
from app.domain.models import Module


class ViewModuleDialog(tk.Toplevel):
    """Dialog to view module details"""

    def __init__(self, parent, module: Module):
        super().__init__(parent)
        self.title(f"Module Details: {module.name}")
        self.geometry("600x500")
        self.minsize(500, 400)
        self.transient(parent)
        self.grab_set()

        self.module = module
        self.create_widgets()

    def create_widgets(self):
        main_frame = ttk.Frame(self, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(main_frame, text=f"Module: {self.module.name}", font=("Helvetica", 14, "bold")).pack(anchor=tk.W, pady=(0, 10))

        info_frame = ttk.LabelFrame(main_frame, text="Properties", padding=15)
        info_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        fields = [
            ("Display Name:", self.module.display_name),
            ("Author:", self.module.author),
            ("Version:", self.module.version),
            ("Category:", self.module.category),
            ("Type:", "Custom" if self.module.is_custom else "Core"),
            ("Status:", "Installed" if self.module.is_installed else "Not Installed"),
            ("Dependencies:", ", ".join(self.module.dependencies) if self.module.dependencies else "None")
        ]

        for i, (label, val) in enumerate(fields):
            tk.Label(info_frame, text=label, font=("Helvetica", 10, "bold")).grid(row=i, column=0, sticky=tk.W, pady=3, padx=5)
            ttk.Label(info_frame, text=val, wraplength=400).grid(row=i, column=1, sticky=tk.W, pady=3, padx=5)

        desc_frame = ttk.LabelFrame(main_frame, text="Description", padding=10)
        desc_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        text = tk.Text(desc_frame, wrap=tk.WORD, height=6, font=("Helvetica", 10))
        text.insert("1.0", self.module.description or "No description provided.")
        text.config(state=tk.DISABLED)
        text.pack(fill=tk.BOTH, expand=True)

        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X, pady=(10, 0))
        ttk.Button(btn_frame, text="Close", command=self.destroy).pack(side=tk.RIGHT)


class EditModuleDialog(tk.Toplevel):
    """Dialog to edit an existing module"""

    def __init__(self, parent, module: Module, on_save: Callable[[Module], None]):
        super().__init__(parent)
        self.title(f"Edit Module: {module.name}")
        self.geometry("550x550")
        self.transient(parent)
        self.grab_set()

        self.module = module
        self.on_save = on_save
        self.create_widgets()

    def create_widgets(self):
        main_frame = ttk.Frame(self, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(main_frame, text=f"Editing Module: {self.module.name}", font=("Helvetica", 12, "bold")).pack(anchor=tk.W, pady=(0, 10))

        form_frame = ttk.Frame(main_frame)
        form_frame.pack(fill=tk.BOTH, expand=True)

        # Fields
        ttk.Label(form_frame, text="Display Name:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.display_name_var = tk.StringVar(value=self.module.display_name)
        ttk.Entry(form_frame, textvariable=self.display_name_var, width=40).grid(row=0, column=1, sticky=tk.W, pady=5)

        ttk.Label(form_frame, text="Author:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.author_var = tk.StringVar(value=self.module.author)
        ttk.Entry(form_frame, textvariable=self.author_var, width=40).grid(row=1, column=1, sticky=tk.W, pady=5)

        ttk.Label(form_frame, text="Version:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.version_var = tk.StringVar(value=self.module.version)
        ttk.Entry(form_frame, textvariable=self.version_var, width=40).grid(row=2, column=1, sticky=tk.W, pady=5)

        ttk.Label(form_frame, text="Category:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.category_var = tk.StringVar(value=self.module.category)
        ttk.Entry(form_frame, textvariable=self.category_var, width=40).grid(row=3, column=1, sticky=tk.W, pady=5)

        self.is_custom_var = tk.BooleanVar(value=self.module.is_custom)
        ttk.Checkbutton(form_frame, text="Custom Module", variable=self.is_custom_var).grid(row=4, column=1, sticky=tk.W, pady=5)

        self.is_installed_var = tk.BooleanVar(value=self.module.is_installed)
        ttk.Checkbutton(form_frame, text="Installed", variable=self.is_installed_var).grid(row=5, column=1, sticky=tk.W, pady=5)

        ttk.Label(form_frame, text="Description:").grid(row=6, column=0, sticky=tk.NW, pady=5)
        self.desc_text = tk.Text(form_frame, width=40, height=5, wrap=tk.WORD)
        self.desc_text.insert("1.0", self.module.description)
        self.desc_text.grid(row=6, column=1, sticky=tk.W, pady=5)

        # Buttons
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X, pady=(15, 0))

        ttk.Button(btn_frame, text="Save", command=self.save).pack(side=tk.RIGHT, padx=5)
        ttk.Button(btn_frame, text="Cancel", command=self.destroy).pack(side=tk.RIGHT)

    def save(self):
        self.module.display_name = self.display_name_var.get().strip()
        self.module.author = self.author_var.get().strip()
        self.module.version = self.version_var.get().strip()
        self.module.category = self.category_var.get().strip()
        self.module.is_custom = self.is_custom_var.get()
        self.module.is_installed = self.is_installed_var.get()
        self.module.description = self.desc_text.get("1.0", tk.END).strip()

        self.on_save(self.module)
        self.destroy()


class AddModuleDialog(tk.Toplevel):
    """Dialog to add a new custom module"""

    def __init__(self, parent, on_save: Callable[[Module], None]):
        super().__init__(parent)
        self.title("Add New Custom Module")
        self.geometry("550x580")
        self.transient(parent)
        self.grab_set()

        self.on_save = on_save
        self.create_widgets()

    def create_widgets(self):
        main_frame = ttk.Frame(self, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(main_frame, text="Create New Custom Module", font=("Helvetica", 12, "bold")).pack(anchor=tk.W, pady=(0, 10))

        form_frame = ttk.Frame(main_frame)
        form_frame.pack(fill=tk.BOTH, expand=True)

        # Fields
        ttk.Label(form_frame, text="Technical Name (*):").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.name_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.name_var, width=40).grid(row=0, column=1, sticky=tk.W, pady=5)

        ttk.Label(form_frame, text="Display Name:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.display_name_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.display_name_var, width=40).grid(row=1, column=1, sticky=tk.W, pady=5)

        ttk.Label(form_frame, text="Author:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.author_var = tk.StringVar(value="Custom")
        ttk.Entry(form_frame, textvariable=self.author_var, width=40).grid(row=2, column=1, sticky=tk.W, pady=5)

        ttk.Label(form_frame, text="Version:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.version_var = tk.StringVar(value="1.0.0")
        ttk.Entry(form_frame, textvariable=self.version_var, width=40).grid(row=3, column=1, sticky=tk.W, pady=5)

        ttk.Label(form_frame, text="Category:").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.category_var = tk.StringVar(value="Uncategorized")
        ttk.Entry(form_frame, textvariable=self.category_var, width=40).grid(row=4, column=1, sticky=tk.W, pady=5)

        ttk.Label(form_frame, text="Dependencies (comma-sep):").grid(row=5, column=0, sticky=tk.W, pady=5)
        self.deps_var = tk.StringVar(value="base")
        ttk.Entry(form_frame, textvariable=self.deps_var, width=40).grid(row=5, column=1, sticky=tk.W, pady=5)

        ttk.Label(form_frame, text="Description:").grid(row=6, column=0, sticky=tk.NW, pady=5)
        self.desc_text = tk.Text(form_frame, width=40, height=5, wrap=tk.WORD)
        self.desc_text.grid(row=6, column=1, sticky=tk.W, pady=5)

        # Buttons
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X, pady=(15, 0))

        ttk.Button(btn_frame, text="Create", command=self.save).pack(side=tk.RIGHT, padx=5)
        ttk.Button(btn_frame, text="Cancel", command=self.destroy).pack(side=tk.RIGHT)

    def save(self):
        name = self.name_var.get().strip()
        if not name:
            messagebox.showerror("Validation Error", "Technical name is required.", parent=self)
            return

        deps = [d.strip() for d in self.deps_var.get().split(",") if d.strip()]

        new_module = Module(
            id=0,
            name=name,
            display_name=self.display_name_var.get().strip() or name,
            description=self.desc_text.get("1.0", tk.END).strip(),
            author=self.author_var.get().strip(),
            version=self.version_var.get().strip(),
            category=self.category_var.get().strip(),
            is_custom=True,
            is_installed=True,
            dependencies=deps
        )

        self.on_save(new_module)
        self.destroy()
