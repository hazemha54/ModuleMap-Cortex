"""
Modal dialogs for module management (Add, Edit, View Details), themed.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Callable

from app.domain.models import Module
from app.ui import theme


class ViewModuleDialog(tk.Toplevel):
    """Dialog to view module details."""

    def __init__(self, parent, module: Module):
        super().__init__(parent)
        self.module = module
        p, f = theme.Palette, theme.Font
        self.title(f"Module Details: {module.name}")
        self.geometry("600x500")
        self.minsize(500, 400)
        self.configure(bg=p.BG)
        self.transient(parent)
        self.grab_set()
        self.create_widgets()

    def create_widgets(self):
        p, f = theme.Palette, theme.Font
        main = tk.Frame(self, bg=p.BG, padx=24, pady=20)
        main.pack(fill=tk.BOTH, expand=True)

        tk.Label(main, text=f"Module: {self.module.name}", bg=p.BG, fg=p.TEXT,
                 font=f.H2).pack(anchor="w", pady=(0, 14))

        info = theme.surface_panel(main)
        tk.Label(info, text="PROPERTIES", bg=p.SURFACE, fg=p.TEXT_MUTED,
                 font=f.STAT_LABEL, anchor="w").pack(anchor="w", pady=(0, 8))

        body = tk.Frame(info, bg=p.SURFACE)
        body.pack(fill=tk.BOTH, expand=True)

        fields = [
            ("Display Name", self.module.display_name),
            ("Author", self.module.author),
            ("Version", self.module.version),
            ("Category", self.module.category),
            ("Type", "Custom" if self.module.is_custom else "Core"),
            ("Status", "Installed" if self.module.is_installed else "Not Installed"),
            ("Dependencies", ", ".join(self.module.dependencies) or "None"),
        ]
        for i, (label, val) in enumerate(fields):
            tk.Label(body, text=label, bg=p.SURFACE, fg=p.TEXT_MUTED,
                     font=f.MUTED, anchor="w").grid(row=i, column=0, sticky="w",
                                                     pady=4, padx=(0, 16))
            tk.Label(body, text=str(val), bg=p.SURFACE, fg=p.TEXT,
                     font=f.BASE, anchor="w", wraplength=380,
                     justify="left").grid(row=i, column=1, sticky="w", pady=4)

        tk.Label(main, text="DESCRIPTION", bg=p.BG, fg=p.TEXT_MUTED,
                 font=f.STAT_LABEL, anchor="w").pack(anchor="w", pady=(18, 6))
        desc_card = theme.surface_panel(main)
        desc_card.pack(fill=tk.BOTH, expand=True)
        text = tk.Text(desc_card, wrap="word", height=6, font=f.BASE,
                       bg=p.SURFACE, fg=p.TEXT, highlightthickness=0, relief="flat")
        text.pack(fill=tk.BOTH, expand=True, padx=12, pady=12)
        text.insert("1.0", self.module.description or "No description provided.")
        text.config(state=tk.DISABLED)

        btn = tk.Frame(main, bg=p.BG)
        btn.pack(fill=tk.X, pady=(14, 0))
        ttk.Button(btn, text="Close", command=self.destroy).pack(side=tk.RIGHT)


class EditModuleDialog(tk.Toplevel):
    """Dialog to edit an existing module."""

    def __init__(self, parent, module: Module, on_save: Callable[[Module], None]):
        super().__init__(parent)
        self.module = module
        self.on_save = on_save
        p, f = theme.Palette, theme.Font
        self.title(f"Edit Module: {module.name}")
        self.geometry("560x560")
        self.configure(bg=p.BG)
        self.transient(parent)
        self.grab_set()
        self.create_widgets()

    def create_widgets(self):
        p, f = theme.Palette, theme.Font
        main = tk.Frame(self, bg=p.BG, padx=24, pady=20)
        main.pack(fill=tk.BOTH, expand=True)

        tk.Label(main, text=f"Editing: {self.module.name}", bg=p.BG, fg=p.TEXT,
                 font=f.H2).pack(anchor="w", pady=(0, 14))

        card = theme.surface_panel(main)
        card.pack(fill=tk.BOTH, expand=True)
        form = tk.Frame(card, bg=p.SURFACE)
        form.pack(fill=tk.BOTH, expand=True, padx=18, pady=18)
        form.columnconfigure(1, weight=1)

        def field(row, label, var):
            tk.Label(form, text=label, bg=p.SURFACE, fg=p.TEXT_MUTED,
                     font=f.MUTED, anchor="w").grid(row=row * 2, column=1, sticky="w",
                                                     pady=(8, 0))
            ttk.Entry(form, textvariable=var).grid(row=row * 2 + 1, column=1, sticky="ew",
                                                    pady=(2, 4))

        self.display_name_var = tk.StringVar(value=self.module.display_name)
        field(0, "Display Name", self.display_name_var)
        self.author_var = tk.StringVar(value=self.module.author)
        field(1, "Author", self.author_var)
        self.version_var = tk.StringVar(value=self.module.version)
        field(2, "Version", self.version_var)
        self.category_var = tk.StringVar(value=self.module.category)
        field(3, "Category", self.category_var)

        self.is_custom_var = tk.BooleanVar(value=self.module.is_custom)
        ttk.Checkbutton(form, text="Custom Module", variable=self.is_custom_var)\
            .grid(row=8, column=1, sticky="w", pady=6)
        self.is_installed_var = tk.BooleanVar(value=self.module.is_installed)
        ttk.Checkbutton(form, text="Installed", variable=self.is_installed_var)\
            .grid(row=9, column=1, sticky="w", pady=6)

        tk.Label(form, text="Description", bg=p.SURFACE, fg=p.TEXT_MUTED,
                 font=f.MUTED, anchor="w").grid(row=10, column=1, sticky="w", pady=(8, 0))
        self.desc_text = tk.Text(form, width=40, height=5, wrap="word",
                                 highlightthickness=0, relief="flat")
        self.desc_text.insert("1.0", self.module.description or "")
        self.desc_text.grid(row=11, column=1, sticky="ew", pady=(2, 4))

        btn = tk.Frame(main, bg=p.BG)
        btn.pack(fill=tk.X, pady=(14, 0))
        ttk.Button(btn, text="Cancel", command=self.destroy).pack(side=tk.RIGHT, padx=(0, 8))
        ttk.Button(btn, text="Save", style="Primary.TButton", command=self.save).pack(side=tk.RIGHT)

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
    """Dialog to add a new custom module."""

    def __init__(self, parent, on_save: Callable[[Module], None]):
        super().__init__(parent)
        self.on_save = on_save
        p, f = theme.Palette, theme.Font
        self.title("Add New Custom Module")
        self.geometry("560x580")
        self.configure(bg=p.BG)
        self.transient(parent)
        self.grab_set()
        self.create_widgets()

    def create_widgets(self):
        p, f = theme.Palette, theme.Font
        main = tk.Frame(self, bg=p.BG, padx=24, pady=20)
        main.pack(fill=tk.BOTH, expand=True)

        tk.Label(main, text="Create New Custom Module", bg=p.BG, fg=p.TEXT,
                 font=f.H2).pack(anchor="w", pady=(0, 14))

        card = theme.surface_panel(main)
        card.pack(fill=tk.BOTH, expand=True)
        form = tk.Frame(card, bg=p.SURFACE)
        form.pack(fill=tk.BOTH, expand=True, padx=18, pady=18)
        form.columnconfigure(1, weight=1)

        def field(row, label, var):
            tk.Label(form, text=label, bg=p.SURFACE, fg=p.TEXT_MUTED,
                     font=f.MUTED, anchor="w").grid(row=row * 2, column=1, sticky="w",
                                                     pady=(8, 0))
            ttk.Entry(form, textvariable=var).grid(row=row * 2 + 1, column=1, sticky="ew",
                                                    pady=(2, 4))

        self.name_var = tk.StringVar()
        field(0, "Technical Name (* required)", self.name_var)
        self.display_name_var = tk.StringVar()
        field(1, "Display Name", self.display_name_var)
        self.author_var = tk.StringVar(value="Custom")
        field(2, "Author", self.author_var)
        self.version_var = tk.StringVar(value="1.0.0")
        field(3, "Version", self.version_var)
        self.category_var = tk.StringVar(value="Uncategorized")
        field(4, "Category", self.category_var)
        self.deps_var = tk.StringVar(value="base")
        field(5, "Dependencies (comma-separated)", self.deps_var)

        tk.Label(form, text="Description", bg=p.SURFACE, fg=p.TEXT_MUTED,
                 font=f.MUTED, anchor="w").grid(row=10, column=1, sticky="w", pady=(8, 0))
        self.desc_text = tk.Text(form, width=40, height=5, wrap="word",
                                 highlightthickness=0, relief="flat")
        self.desc_text.grid(row=11, column=1, sticky="ew", pady=(2, 4))

        btn = tk.Frame(main, bg=p.BG)
        btn.pack(fill=tk.X, pady=(14, 0))
        ttk.Button(btn, text="Cancel", command=self.destroy).pack(side=tk.RIGHT, padx=(0, 8))
        ttk.Button(btn, text="Create", style="Primary.TButton", command=self.save).pack(side=tk.RIGHT)

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
            dependencies=deps,
        )
        self.on_save(new_module)
        self.destroy()
