"""
JSON Local Storage Repository with Schema Validation and Structured Logging
"""

import json
import os
import logging
from typing import List, Dict, Optional
from dataclasses import asdict
from app.domain.models import Module

logger = logging.getLogger(__name__)


class DatabaseManager:
    """Manages local JSON file storage for modules, models, and changes with validation"""

    def __init__(self, db_path: str = 'modules_store.json'):
        self.storage_file = "modules_store.json"
        self.init_storage()

    def init_storage(self):
        """Initialize storage file with sample data if not exists"""
        if not os.path.exists(self.storage_file):
            initial_data = {
                "modules": [
                    {
                        "id": 1,
                        "name": "modulemap_cortex_core",
                        "display_name": "ModuleMap Cortex Core",
                        "description": "Core Odoo module mapping and architecture analyzer engine.",
                        "author": "Enterprise Software Factory",
                        "version": "2.5.0",
                        "category": "Analysis",
                        "is_custom": True,
                        "is_installed": True,
                        "dependencies": ["base", "web"]
                    }
                ],
                "models": [
                    {
                        "id": 1,
                        "module_id": 1,
                        "model_name": "modulemap.analysis",
                        "display_name": "Module Analysis",
                        "model_type": "model",
                        "parent_model": ""
                    }
                ],
                "changes": [
                    {
                        "id": 1,
                        "module_id": 1,
                        "change_type": "Initialization",
                        "change_description": "Initial system setup via local JSON storage",
                        "severity": "Info",
                        "detected_at": "2026-10-21 00:00:00"
                    }
                ]
            }
            self._save_data(initial_data)

    def _load_data(self) -> Dict:
        default_data = {"modules": [], "models": [], "changes": []}
        if not os.path.exists(self.storage_file):
            return default_data
        try:
            with open(self.storage_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            if not isinstance(data, dict):
                logger.error("Storage root is not a dictionary. Resetting to default structure.")
                return default_data

            # Validate and normalize keys
            validated = {
                "modules": [],
                "models": [],
                "changes": []
            }

            modules = data.get("modules")
            if isinstance(modules, list):
                for m in modules:
                    if isinstance(m, dict) and "id" in m and "name" in m:
                        validated["modules"].append(m)
                    else:
                        logger.warning(f"Skipping malformed module entry: {m}")

            models = data.get("models")
            if isinstance(models, list):
                for model in models:
                    if isinstance(model, dict):
                        validated["models"].append(model)

            changes = data.get("changes")
            if isinstance(changes, list):
                for change in changes:
                    if isinstance(change, dict):
                        validated["changes"].append(change)

            return validated
        except Exception as e:
            logger.error(f"Error loading and validating storage: {e}", exc_info=True)
            return default_data

    def _save_data(self, data: Dict):
        try:
            with open(self.storage_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving storage: {e}", exc_info=True)

    def get_all_modules(self, filter_type: Optional[str] = None, search_query: Optional[str] = None) -> List[Module]:
        data = self._load_data()
        modules = []
        for mod_dict in data.get("modules", []):
            try:
                mod_id = int(mod_dict.get("id", 0))
                mod_name = str(mod_dict.get("name", ""))
                is_installed = bool(mod_dict.get("is_installed", True))
                is_custom = bool(mod_dict.get("is_custom", False))

                if filter_type == "Installed" and not is_installed:
                    continue
                if filter_type == "Custom" and not is_custom:
                    continue
                if filter_type == "Core" and is_custom:
                    continue

                if search_query:
                    q = search_query.lower()
                    matched = (
                        q in mod_name.lower() or
                        q in str(mod_dict.get("display_name", "")).lower() or
                        q in str(mod_dict.get("description", "")).lower() or
                        q in str(mod_dict.get("author", "")).lower()
                    )
                    if not matched:
                        continue

                modules.append(Module(
                    id=mod_id,
                    name=mod_name,
                    display_name=str(mod_dict.get("display_name", "")),
                    description=str(mod_dict.get("description", "")),
                    author=str(mod_dict.get("author", "")),
                    version=str(mod_dict.get("version", "1.0.0")),
                    category=str(mod_dict.get("category", "General")),
                    is_custom=is_custom,
                    is_installed=is_installed,
                    dependencies=list(mod_dict.get("dependencies", []))
                ))
            except Exception as e:
                logger.error(f"Error parsing module entry {mod_dict}: {e}")
        return modules

    def get_module(self, module_id: int) -> Optional[Module]:
        data = self._load_data()
        for mod_dict in data.get("modules", []):
            try:
                if int(mod_dict.get("id", -1)) == module_id:
                    return Module(
                        id=int(mod_dict["id"]),
                        name=str(mod_dict.get("name", "")),
                        display_name=str(mod_dict.get("display_name", "")),
                        description=str(mod_dict.get("description", "")),
                        author=str(mod_dict.get("author", "")),
                        version=str(mod_dict.get("version", "1.0.0")),
                        category=str(mod_dict.get("category", "General")),
                        is_custom=bool(mod_dict.get("is_custom", False)),
                        is_installed=bool(mod_dict.get("is_installed", True)),
                        dependencies=list(mod_dict.get("dependencies", []))
                    )
            except Exception as e:
                logger.error(f"Error parsing module for ID {module_id}: {e}")
        return None

    def add_module(self, module: Module) -> bool:
        data = self._load_data()
        modules = data.get("modules", [])

        if any(m.get("name") == module.name for m in modules):
            return False

        new_id = max([int(m.get("id", 0)) for m in modules], default=0) + 1
        module.id = new_id

        modules.append({
            "id": module.id,
            "name": module.name,
            "display_name": module.display_name,
            "description": module.description,
            "author": module.author,
            "version": module.version,
            "category": module.category,
            "is_custom": module.is_custom,
            "is_installed": module.is_installed,
            "dependencies": module.dependencies
        })
        data["modules"] = modules
        self._save_data(data)
        return True

    def update_module(self, module: Module) -> bool:
        data = self._load_data()
        modules = data.get("modules", [])
        found = False
        for m in modules:
            if int(m.get("id", -1)) == module.id:
                m["display_name"] = module.display_name
                m["description"] = module.description
                m["author"] = module.author
                m["version"] = module.version
                m["category"] = module.category
                m["is_custom"] = module.is_custom
                m["is_installed"] = module.is_installed
                m["dependencies"] = module.dependencies
                found = True
                break
        if found:
            data["modules"] = modules
            self._save_data(data)
            return True
        return False

    def delete_module(self, module_id: int) -> bool:
        data = self._load_data()
        modules = data.get("modules", [])
        initial_len = len(modules)
        modules = [m for m in modules if int(m.get("id", -1)) != module_id]
        if len(modules) < initial_len:
            data["modules"] = modules
            self._save_data(data)
            return True
        return False

    def get_stats(self) -> Dict:
        data = self._load_data()
        modules = data.get("modules", [])
        models = data.get("models", [])
        custom_count = sum(1 for m in modules if m.get("is_custom"))
        total_deps = sum(len(m.get("dependencies", [])) for m in modules)

        return {
            "total_modules": len(modules),
            "custom_modules": custom_count,
            "core_modules": len(modules) - custom_count,
            "total_models": len(models),
            "total_dependencies": total_deps,
        }

    def get_connection(self):
        class MockConnection:
            def __init__(self, storage_data):
                self.data = storage_data
            def cursor(self):
                return MockCursor(self.data)
            def close(self):
                pass

        class MockCursor:
            def __init__(self, data):
                self.data = data
                self.rows = []
            def execute(self, query, params=()):
                q = query.strip().lower()
                if "models" in q:
                    self.rows = self.data.get("models", [])
                elif "changes" in q:
                    self.rows = self.data.get("changes", [])
                else:
                    self.rows = []
            def fetchall(self):
                return [MockRow(r) for r in self.rows]

        class MockRow(dict):
            def __getitem__(self, key):
                return super().__getitem__(key)

        return MockConnection(self._load_data())
