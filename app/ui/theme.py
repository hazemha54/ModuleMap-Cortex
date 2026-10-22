"""
Centralized Premium Design System for ModuleMap-Cortex

Every view and dialog pulls colors, fonts, and spacing from this module so the
entire app reads as one cohesive, polished product instead of a patchwork of
per-file literals. Tune the palette here and the whole UI updates.
"""

from tkinter import ttk


# ---------------------------------------------------------------------------
# Palette — refined enterprise blue
# ---------------------------------------------------------------------------
class Palette:
    # Neutrals
    BG = "#f5f7fa"              # app background (cool off-white)
    SURFACE = "#ffffff"         # cards / panels
    BORDER = "#e2e8f0"         # hairline borders
    BORDER_SOFT = "#eef2f7"    # subtle inner borders

    TEXT = "#1e293b"           # primary text (slate-800)
    TEXT_MUTED = "#64748b"     # secondary (slate-500)
    TEXT_FAINT = "#94a3b8"     # tertiary (slate-400)

    # Sidebar
    SIDEBAR = "#0f1b2d"        # deep navy
    SIDEBAR_HOVER = "#16283f"
    SIDEBAR_BORDER = "#1c2f47"

    # Brand / accent
    ACCENT = "#2563eb"         # primary blue
    ACCENT_HOVER = "#3b82f6"
    ACCENT_DARK = "#1d4ed8"
    ACCENT_TEXT = "#ffffff"

    # Semantic
    SUCCESS = "#16a34a"
    WARNING = "#d97706"
    DANGER = "#dc2626"
    INFO = "#0ea5e9"

    # Table
    TABLE_HEAD_BG = "#0f1b2d"
    TABLE_HEAD_FG = "#cbd5e1"
    ROW_ALT = "#f8fafc"


# ---------------------------------------------------------------------------
# Fonts — a small, consistent set
# ---------------------------------------------------------------------------
class Font:
    FAMILY = "Segoe UI"
    BASE = ("Segoe UI", 10)
    SMALL = ("Segoe UI", 9)
    MUTED = ("Segoe UI", 9)
    CAPTION = ("Segoe UI", 8)

    H1 = ("Segoe UI", 22, "bold")
    H2 = ("Segoe UI", 15, "bold")
    H3 = ("Segoe UI", 12, "bold")

    NAV = ("Segoe UI", 11)
    NAV_BOLD = ("Segoe UI", 11, "bold")
    BRAND = ("Segoe UI", 17, "bold")
    BRAND_SUB = ("Segoe UI", 8)

    STAT = ("Segoe UI", 28, "bold")
    STAT_LABEL = ("Segoe UI", 9, "bold")


# ---------------------------------------------------------------------------
# Spacing
# ---------------------------------------------------------------------------
SP = 8
SP_MD = 12
SP_LG = 20
SP_XL = 28
CARD_PAD = (24, 20)


def apply_theme(root) -> ttk.Style:
    """Configure global ttk styling on the app root. Call once at startup."""
    style = ttk.Style(root)
    style.theme_use("clam")

    p, f = Palette, Font

    # Base look
    style.configure(".", background=p.BG, foreground=p.TEXT, font=f.BASE)
    style.configure("TFrame", background=p.BG)
    style.configure("TLabel", background=p.BG, foreground=p.TEXT, font=f.BASE)

    # Headings
    style.configure("Header.TLabel", font=f.H1, foreground=p.TEXT, background=p.BG)
    style.configure("SubHeader.TLabel", font=f.H2, foreground=p.TEXT, background=p.BG)
    style.configure("Caption.TLabel", font=f.CAPTION, foreground=p.TEXT_FAINT, background=p.BG)
    style.configure("Muted.TLabel", font=f.MUTED, foreground=p.TEXT_MUTED, background=p.BG)

    # Buttons — subtle by default, primary for the important action
    style.configure("TButton", font=f.BASE, padding=(12, 7), relief="flat",
                    background=p.SURFACE, foreground=p.TEXT, bordercolor=p.BORDER,
                    lightcolor=p.SURFACE, darkcolor=p.SURFACE)
    style.map("TButton",
              background=[("active", p.BORDER_SOFT), ("disabled", p.BG)],
              foreground=[("disabled", p.TEXT_FAINT)])

    style.configure("Primary.TButton", font=(f.FAMILY, 10, "bold"), padding=(16, 9),
                    background=p.ACCENT, foreground=p.ACCENT_TEXT, bordercolor=p.ACCENT_DARK,
                    lightcolor=p.ACCENT, darkcolor=p.ACCENT_DARK)
    style.map("Primary.TButton",
              background=[("active", p.ACCENT_HOVER), ("pressed", p.ACCENT_DARK),
                          ("disabled", p.BORDER)],
              foreground=[("active", p.ACCENT_TEXT), ("pressed", p.ACCENT_TEXT),
                         ("disabled", p.TEXT_FAINT)])

    # Inputs
    style.configure("TEntry", font=f.BASE, padding=6, fieldbackground=p.SURFACE,
                    bordercolor=p.BORDER, lightcolor=p.SURFACE, darkcolor=p.SURFACE)
    style.map("TEntry", fieldbackground=[("disabled", p.BG)])
    style.configure("TCombobox", font=f.BASE, padding=5, fieldbackground=p.SURFACE,
                    bordercolor=p.BORDER, lightcolor=p.SURFACE, darkcolor=p.SURFACE)
    style.map("TCombobox",
              fieldbackground=[("readonly", p.SURFACE), ("disabled", p.BG)],
              background=[("readonly", p.SURFACE), ("active", p.BORDER_SOFT)])

    style.configure("TCheckbutton", background=p.BG, foreground=p.TEXT, font=f.BASE)
    style.map("TCheckbutton", background=[("active", p.BORDER_SOFT)])

    # Tables
    style.configure("Treeview", font=f.BASE, background=p.SURFACE,
                    fieldbackground=p.SURFACE, rowheight=34,
                    bordercolor=p.BORDER, lightcolor=p.SURFACE, darkcolor=p.SURFACE)
    style.map("Treeview", background=[("selected", p.ACCENT)],
              foreground=[("selected", p.ACCENT_TEXT)])
    style.configure("Treeview.Heading", font=(f.FAMILY, 9, "bold"),
                    background=p.TABLE_HEAD_BG, foreground=p.TABLE_HEAD_FG,
                    padding=(10, 6), relief="flat", anchor="w",
                    bordercolor=p.TABLE_HEAD_BG)
    style.map("Treeview.Heading", background=[("active", p.ACCENT_DARK)],
              foreground=[("active", p.ACCENT_TEXT)])

    # Scrollbars — slim, modern
    style.configure("Vertical.TScrollbar", arrowcolor=p.TEXT_FAINT,
                    background=p.BORDER, troughcolor=p.BG, bordercolor=p.BG,
                    lightcolor=p.BORDER, darkcolor=p.BORDER)
    style.map("Vertical.TScrollbar", background=[("active", p.TEXT_FAINT)])
    style.configure("Horizontal.TScrollbar", arrowcolor=p.TEXT_FAINT,
                    background=p.BORDER, troughcolor=p.BG, bordercolor=p.BG,
                    lightcolor=p.BORDER, darkcolor=p.BORDER)

    # LabelFrame → rounded-looking card container
    style.configure("Card.TLabelframe", background=p.SURFACE, bordercolor=p.BORDER,
                    relief="solid", padding=CARD_PAD)
    style.configure("Card.TLabelframe.Label", background=p.SURFACE,
                    foreground=p.TEXT_MUTED, font=f.STAT_LABEL, padding=(0, 0, 0, 4))

    style.configure("TLabelframe", background=p.BG, bordercolor=p.BORDER, relief="solid")
    style.configure("TLabelframe.Label", background=p.BG, foreground=p.TEXT, font=f.H3)

    # Note: Sidebar navigation uses plain tk.Button so it can show a selected
    # (non-hover) state — handled in MainWindow, not here.
    return style


# ---------------------------------------------------------------------------
# Reusable widget builders shared across views
# ---------------------------------------------------------------------------
def stat_card(parent, title: str, value: str, accent: str, index: int, total: int) -> "tk.Label":
    """A premium KPI card. Returns the value label so callers can refresh it.

    Uses a hairline border + top accent bar + soft shadow-free surface.
    """
    import tkinter as tk
    p = Palette
    outer = tk.Frame(parent, bg=p.SURFACE, highlightbackground=p.BORDER,
                      highlightthickness=1, padx=18, pady=16)
    outer.grid(row=0, column=index, sticky="nsew", padx=6)

    # top accent bar
    bar = tk.Frame(outer, bg=accent, height=3)
    bar.pack(fill=tk.X, pady=(0, 12))

    tk.Label(outer, text=title.upper(), bg=p.SURFACE, fg=p.TEXT_MUTED,
             font=Font.STAT_LABEL).pack(anchor="w")
    val = tk.Label(outer, text=value, bg=p.SURFACE, fg=p.TEXT, font=Font.STAT,
                   anchor="w")
    val.pack(anchor="w", pady=(6, 0))
    return val


def toolbar(parent, title: str, subtitle: str = ""):
    """Consistent view header. Returns (frame, buttons_holder) for actions."""
    import tkinter as tk
    p = Palette
    frame = tk.Frame(parent, bg=p.BG)
    frame.pack(fill=tk.X, pady=(0, 18))

    left = tk.Frame(frame, bg=p.BG)
    left.pack(side=tk.LEFT)
    tk.Label(left, text=title, bg=p.BG, fg=p.TEXT, font=Font.H1).pack(anchor="w")
    if subtitle:
        tk.Label(left, text=subtitle, bg=p.BG, fg=p.TEXT_MUTED, font=Font.MUTED).pack(anchor="w", pady=(2, 0))

    holder = tk.Frame(frame, bg=p.BG)
    holder.pack(side=tk.RIGHT)
    return frame, holder


def surface_card(parent, **kw):
    """A white card with a hairline border (for search/filter bars)."""
    import tkinter as tk
    card = tk.Frame(parent, bg=Palette.SURFACE,
                    highlightbackground=Palette.BORDER, highlightthickness=1,
                    padx=16, pady=12, **kw)
    card.pack(fill=tk.X, pady=(0, 18))
    return card


def surface_panel(parent, **kw):
    """A full-height white panel with a hairline border (for scrollable content)."""
    import tkinter as tk
    panel = tk.Frame(parent, bg=Palette.SURFACE,
                     highlightbackground=Palette.BORDER, highlightthickness=1, **kw)
    panel.pack(fill=tk.BOTH, expand=True)
    return panel


def data_table(parent, columns: dict, height: int = 14, pad: str = "16, 0, 16, 16"):
    """Build a styled Treeview inside a white surface card.

    `columns` maps colkey -> (heading, width, anchor).
    Returns (treeview, card). The vertical scrollbar is attached to `parent`
    so it stretches to the card's full height.
    """
    import tkinter as tk
    p = Palette
    card = tk.Frame(parent, bg=p.SURFACE,
                    highlightbackground=p.BORDER, highlightthickness=1)
    card.pack(fill=tk.BOTH, expand=True)
    body = tk.Frame(card, bg=p.SURFACE)
    body.pack(fill=tk.BOTH, expand=True)

    keys = list(columns.keys())
    tree = ttk.Treeview(body, columns=keys, show="headings", height=height)
    for key, (heading, width, anchor) in columns.items():
        tree.heading(key, text=heading)
        tree.column(key, width=width, anchor=anchor)

    tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    tree.pack_configure(padx=0)

    scrollbar = ttk.Scrollbar(body, orient=tk.VERTICAL, command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    return tree, card
