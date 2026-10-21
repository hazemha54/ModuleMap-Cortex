"""
Comprehensive unit tests for DatabaseManager, ConfigManager, OdooConnector, WorkspaceManager, and DiffEngine
"""

import os
import pytest
from app.repositories.database import DatabaseManager
from app.services.config_manager import ConfigManager, OdooConfig, AppConfig
from app.services.odoo_service import OdooConnector
from app.services.workspace_service import WorkspaceManager
from app.services.diff_engine import DiffEngine
from app.domain.models import Module


@pytest.fixture
def test_db():
    storage_file = "modules_store.json"
    if os.path.exists(storage_file):
        os.remove(storage_file)
    db = DatabaseManager(db_path=storage_file)
    yield db
    if os.path.exists(storage_file):
        os.remove(storage_file)


def test_database_init_and_crud(test_db):
    mod = Module(
        id=0,
        name="test_module",
        display_name="Test Module",
        description="A test module",
        author="Tester",
        version="1.0.0",
        category="Testing",
        is_custom=True,
        is_installed=True,
        dependencies=["base"]
    )
    assert test_db.add_module(mod) is True
    modules = test_db.get_all_modules()
    assert len(modules) >= 1
    test_mod = next(m for m in modules if m.name == "test_module")
    assert test_mod.dependencies == ["base"]

    fetched = test_db.get_module(test_mod.id)
    assert fetched is not None
    assert fetched.display_name == "Test Module"

    fetched.display_name = "Updated Test Module"
    assert test_db.update_module(fetched) is True
    updated = test_db.get_module(fetched.id)
    assert updated.display_name == "Updated Test Module"

    assert test_db.delete_module(fetched.id) is True


def test_config_manager():
    config = ConfigManager()
    assert config.get_odoo_config().url == "http://localhost:8069"
    assert config.get_app_config().theme == "light"

    config.update_odoo_config(url="http://odoo.test:8069")
    assert config.get_odoo_config().url == "http://odoo.test:8069"

    if os.path.exists(ConfigManager.CONFIG_FILE):
        os.remove(ConfigManager.CONFIG_FILE)


def test_odoo_connector_custom_check():
    assert OdooConnector.is_custom_module("base") is False
    assert OdooConnector.is_custom_module("web") is False
    assert OdooConnector.is_custom_module("account") is False
    assert OdooConnector.is_custom_module("my_custom_module") is True


def test_workspace_manager(tmp_path):
    # Create sample module directory structure
    mod_dir = tmp_path / "custom_odoo_module"
    mod_dir.mkdir()
    manifest = mod_dir / "__manifest__.py"
    manifest.write_text("{\n    'name': 'Custom Module',\n    'depends': ['base'],\n}", encoding="utf-8")

    ws = WorkspaceManager(workspace_path=str(tmp_path))
    modules = ws.scan_modules()
    assert len(modules) == 1
    assert modules[0]["name"] == "custom_odoo_module"
    assert modules[0]["display_name"] == "Custom Module"


def test_diff_engine(tmp_path):
    f1 = tmp_path / "file1.py"
    f2 = tmp_path / "file2.py"
    f1.write_text("print('hello')\n", encoding="utf-8")
    f2.write_text("print('world')\n", encoding="utf-8")

    diff = DiffEngine.compare_files(str(f1), str(f2))
    assert len(diff) > 0
