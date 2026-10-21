"""
Configuration Manager for Tkinter Application
"""

import json
import os
from dataclasses import dataclass, asdict


@dataclass
class OdooConfig:
    """Odoo connection configuration"""
    url: str = "http://localhost:8069"
    db: str = "odoo_db"
    username: str = "admin"
    password: str = "admin"
    timeout: int = 30


@dataclass
class AppConfig:
    """Application configuration"""
    db_path: str = "modulemap_cortex.db"
    debug: bool = False
    auto_import: bool = False
    theme: str = "light"  # light or dark
    window_width: int = 1400
    window_height: int = 900


class ConfigManager:
    """Manage application configuration persistence"""

    CONFIG_FILE = "config.json"

    def __init__(self):
        self.odoo_config = OdooConfig()
        self.app_config = AppConfig()
        self.load_config()

    def load_config(self):
        """Load configuration from file"""
        if os.path.exists(self.CONFIG_FILE):
            try:
                with open(self.CONFIG_FILE, 'r') as f:
                    data = json.load(f)

                if 'odoo' in data:
                    self.odoo_config = OdooConfig(**data['odoo'])

                if 'app' in data:
                    self.app_config = AppConfig(**data['app'])

            except Exception as e:
                print(f"Error loading config: {e}")

    def save_config(self):
        """Save configuration to file"""
        try:
            data = {
                'odoo': asdict(self.odoo_config),
                'app': asdict(self.app_config),
            }

            with open(self.CONFIG_FILE, 'w') as f:
                json.dump(data, f, indent=2)

            return True, "Configuration saved"

        except Exception as e:
            return False, f"Error saving config: {e}"

    def get_odoo_config(self) -> OdooConfig:
        return self.odoo_config

    def update_odoo_config(self, **kwargs) -> bool:
        for key, value in kwargs.items():
            if hasattr(self.odoo_config, key):
                setattr(self.odoo_config, key, value)
        return self.save_config()[0]

    def get_app_config(self) -> AppConfig:
        return self.app_config

    def update_app_config(self, **kwargs) -> bool:
        for key, value in kwargs.items():
            if hasattr(self.app_config, key):
                setattr(self.app_config, key, value)
        return self.save_config()[0]


def init_default_config():
    if not os.path.exists(ConfigManager.CONFIG_FILE):
        config = ConfigManager()
        config.save_config()
