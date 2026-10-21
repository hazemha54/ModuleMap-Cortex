# ModuleMap-Cortex — Enterprise Odoo Architecture Suite

ModuleMap-Cortex is an enterprise-grade desktop application designed for managing, auditing, visualizing, and analyzing Odoo ERP modules and database architectures.

## Architecture & Framework

- **GUI Framework**: Native Python **Tkinter** (`tkinter` / `ttk`) with a clean modular layered architecture.
- **Data Layer**: SQLite (`modulemap_cortex.db`) with foreign key enforcement (`PRAGMA foreign_keys = ON;`) and robust transaction management.
- **Integrations**: XML-RPC / JSON-RPC connector for Odoo instance synchronization.

## Project Structure

```text
ModuleMap-Cortex/
├── app/
│   ├── main.py                  # Entry point
│   ├── domain/                  # Domain dataclasses (Module, ModelRecord, ChangeRecord)
│   ├── repositories/            # SQLite DatabaseManager
│   ├── services/                # Odoo connector & ConfigManager
│   └── ui/                      # Tkinter Views & Dialogs
│       ├── main_window.py       # Master shell with sidebar navigation
│       ├── views/               # Dashboard, Modules, Dependencies, Models, Changes, Search, Settings, Help
│       └── dialogs/             # Add, Edit, and View details modal dialogs
├── tests/
│   └── unit/                    # Pytest unit tests
├── requirements.txt             # Project dependencies
└── README.md                    # Documentation
```

## Installation & Startup

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Application**:
   ```bash
   python3 app/main.py
   ```

3. **Run Tests**:
   ```bash
   PYTHONPATH=. pytest -v
   ```
