"""
ModuleMap-Cortex - Tkinter Desktop Application Launcher
Main entry point for the application
"""

import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from app.services.config_manager import ConfigManager, init_default_config
from app.repositories.database import DatabaseManager
from app.ui.main_window import MainWindow
from app.domain.models import Module


def seed_sample_data_if_empty(db_manager: DatabaseManager):
    """Seed sample modules if database is empty"""
    modules = db_manager.get_all_modules()
    if not modules:
        sample = Module(
            id=0,
            name="modulemap_cortex_core",
            display_name="ModuleMap Cortex Core",
            description="Core Odoo module mapping and architecture analyzer engine.",
            author="Enterprise Software Factory",
            version="2.5.0",
            category="Analysis",
            is_custom=True,
            is_installed=True,
            dependencies=["base", "web"]
        )
        db_manager.add_module(sample)


def main():
    """Main application launcher"""
    # Initialize default config
    init_default_config()
    config_manager = ConfigManager()

    # Initialize Database
    app_cfg = config_manager.get_app_config()
    db_manager = DatabaseManager(db_path=app_cfg.db_path)

    # Seed sample data if needed
    seed_sample_data_if_empty(db_manager)

    # Create and run main Tkinter window
    app = MainWindow(db_manager, config_manager)

    try:
        print("Starting ModuleMap Cortex Tkinter Application...")
        app.mainloop()
    except KeyboardInterrupt:
        print("\nApplication closed by user")
        sys.exit(0)
    except Exception as e:
        print(f"Error running application: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
