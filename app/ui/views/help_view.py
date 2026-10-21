"""
Help & Documentation View with Modern Blue Theme
"""

import tkinter as tk
from tkinter import ttk


class HelpView(ttk.Frame):
    """View displaying help documentation and usage guide"""

    def __init__(self, parent):
        super().__init__(parent, padding=25)
        self.create_widgets()

    def create_widgets(self):
        ttk.Label(self, text="Help & Documentation", style="Header.TLabel").pack(anchor=tk.W, pady=(0, 20))

        text_frame = ttk.Frame(self)
        text_frame.pack(fill=tk.BOTH, expand=True)

        text = tk.Text(text_frame, wrap=tk.WORD, font=("Segoe UI", 11), padx=15, pady=15, bg="#ffffff", fg="#212529", highlightbackground="#cbd5e1", highlightthickness=1)
        text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(text_frame, orient=tk.VERTICAL, command=text.yview)
        text.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        help_content = """ModuleMap-Cortex: Professional Odoo Module Mapping & Analysis Suite

Overview:
ModuleMap-Cortex provides enterprise-grade tools for auditing, mapping, visualizing, and analyzing Odoo ERP modules and database architectures with a modern blue theme.

Features:
1. Dashboard: Overview metrics, KPI cards, and recent modules registry.
2. Modules: Comprehensive module inventory with search, filtering, custom module creation, editing, and deletion.
3. Dependencies: Dependency tree mapping and JSON export.
4. Models: Odoo model catalog browser.
5. Changes: Customization and change tracking log.
6. Search: Global full-text search across modules and components.
7. Settings: Odoo server connection configuration and live connection testing.

Navigation:
Use the left sidebar navigation buttons to switch between views instantly. All database actions operate against the local SQLite repository (modulemap_cortex.db).
"""

        text.insert("1.0", help_content)
        text.config(state=tk.DISABLED)
