"""
Dashboard View with Modern Blue Theme
"""

import tkinter as tk
from tkinter import ttk
from app.repositories.database import DatabaseManager


class DashboardView(ttk.Frame):
    """Dashboard view showing overview stats and recent modules"""

    def __init__(self, parent, db_manager: DatabaseManager):
        super().__init__(parent, padding=25)
        self.db_manager = db_manager
        self.create_widgets()
        self.refresh()

    def create_widgets(self):
        # Header
        header_frame = ttk.Frame(self)
        header_frame.pack(fill=tk.X, pady=(0, 20))

        ttk.Label(header_frame, text="Dashboard Overview", style="Header.TLabel").pack(side=tk.LEFT)
        tk.Label(header_frame, text="Welcome to ModuleMap Cortex", fg="#64748b", bg="#f4f6f9", font=("Segoe UI", 10)).pack(side=tk.LEFT, padx=15, pady=5)

        # Stats Cards Frame
        cards_frame = ttk.Frame(self)
        cards_frame.pack(fill=tk.X, pady=(0, 25))

        cards_frame.columnconfigure((0, 1, 2, 3), weight=1, uniform="card")

        self.card_total = self.create_stat_card(cards_frame, "Total Modules", "0", 0, "#0284c7")
        self.card_custom = self.create_stat_card(cards_frame, "Custom Modules", "0", 1, "#0d9488")
        self.card_models = self.create_stat_card(cards_frame, "Odoo Models", "0", 2, "#6366f1")
        self.card_deps = self.create_stat_card(cards_frame, "Dependencies", "0", 3, "#4f46e5")

        # Recent Modules Section
        recent_frame = ttk.LabelFrame(self, text="  Recent Modules Inventory  ", padding=20)
        recent_frame.pack(fill=tk.BOTH, expand=True)

        columns = ("name", "display_name", "author", "version", "category", "type")
        self.tree = ttk.Treeview(recent_frame, columns=columns, show="headings", height=12)

        self.tree.heading("name", text="Technical Name")
        self.tree.heading("display_name", text="Display Name")
        self.tree.heading("author", text="Author")
        self.tree.heading("version", text="Version")
        self.tree.heading("category", text="Category")
        self.tree.heading("type", text="Type")

        self.tree.column("name", width=160, anchor=tk.W)
        self.tree.column("display_name", width=240, anchor=tk.W)
        self.tree.column("author", width=140, anchor=tk.W)
        self.tree.column("version", width=90, anchor=tk.CENTER)
        self.tree.column("category", width=130, anchor=tk.W)
        self.tree.column("type", width=100, anchor=tk.CENTER)

        scrollbar = ttk.Scrollbar(recent_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def create_stat_card(self, parent, title: str, initial_value: str, col: int, accent_color: str) -> ttk.Label:
        # Container frame with custom border effect
        outer = tk.Frame(parent, bg="#cbd5e1", padx=1, pady=1)
        outer.grid(row=0, column=col, sticky="nsew", padx=8)

        frame = tk.Frame(outer, bg="#ffffff", padx=18, pady=16)
        frame.pack(fill=tk.BOTH, expand=True)

        # Top accent bar
        bar = tk.Frame(frame, bg=accent_color, height=4)
        bar.pack(fill=tk.X, pady=(0, 10))

        tk.Label(frame, text=title.upper(), bg="#ffffff", fg="#64748b", font=("Segoe UI", 9, "bold")).pack(anchor=tk.W)
        val_lbl = tk.Label(frame, text=initial_value, bg="#ffffff", fg="#1e3d59", font=("Segoe UI", 26, "bold"))
        val_lbl.pack(anchor=tk.W, pady=(4, 0))

        return val_lbl

    def refresh(self):
        stats = self.db_manager.get_stats()
        self.card_total.config(text=str(stats["total_modules"]))
        self.card_custom.config(text=str(stats["custom_modules"]))
        self.card_models.config(text=str(stats["total_models"]))
        self.card_deps.config(text=str(stats["total_dependencies"]))

        for item in self.tree.get_children():
            self.tree.delete(item)

        modules = self.db_manager.get_all_modules()[:15]
        for mod in modules:
            mod_type = "Custom" if mod.is_custom else "Core"
            self.tree.insert("", tk.END, values=(
                mod.name, mod.display_name, mod.author, mod.version, mod.category, mod_type
            ))
