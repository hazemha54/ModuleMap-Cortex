"""
JSON Local Storage Repository (Replacing SQLite)
"""

import json
import os
from typing import List, Dict, Optional
from dataclasses import asdict
from app.domain.models import Module


class DatabaseManager:
    """Manages local JSON file storage for modules, models, and changes"""

    def __init__(self, db_path: str = 'modules_store.json'):
        # db_path parameter kept for configuration compatibility
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
        if not os.path.exists(self.storage_file):
            return {"modules": [], "models": [], "changes": []}
        try:
            with open(self.storage_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading storage: {e}")
            return {"modules": [], "models": [], "changes": []}

    def _save_data(self, data: Dict):
        try:
            with open(self.storage_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Error saving storage: {e}")

    def get_all_modules(self, filter_type: Optional[str] = None, search_query: Optional[str] = None) -> List[Module]:
        data = self._load_data()
        modules = []
        for mod_dict in data.get("modules", []):
            is_installed = mod_dict.get("is_installed", True)
            is_custom = mod_dict.get("is_custom", False)

            if filter_type == "Installed" and not is_installed:
                continue
            if filter_type == "Custom" and not is_custom:
                continue
            if filter_type == "Core" and is_custom:
                continue

            if search_query:
                q = search_query.lower()
                matched = (
                    q in mod_dict.get("name", "").lower() or
                    q in mod_dict.get("display_name", "").lower() or
                    q in mod_dict.get("description", "").lower() or
                    q in mod_dict.get("author", "").lower()
                )
                if not matched:
                    continue

            modules.append(Module(
                id=mod_dict["id"],
                name=mod_dict["name"],
                display_name=mod_dict.get("display_name", ""),
                description=mod_dict.get("description", ""),
                author=mod_dict.get("author", ""),
                version=mod_dict.get("version", "1.0.0"),
                category=mod_dict.get("category", "General"),
                is_custom=is_custom,
                is_installed=is_installed,
                dependencies=mod_dict.get("dependencies", [])
            ))
        return modules

    def get_module(self, module_id: int) -> Optional[Module]:
        data = self._load_data()
        for mod_dict in data.get("modules", []):
            if mod_dict["id"] == module_id:
                return Module(
                    id=mod_dict["id"],
                    name=mod_dict["name"],
                    display_name=mod_dict.get("display_name", ""),
                    description=mod_dict.get("description", ""),
                    author=mod_dict.get("author", ""),
                    version=mod_dict.get("version", "1.0.0"),
                    category=mod_dict.get("category", "General"),
                    is_custom=mod_dict.get("is_custom", False),
                    is_installed=mod_dict.get("is_installed", True),
                    dependencies=mod_dict.get("dependencies", [])
                )
        return None

    def add_module(self, module: Module) -> bool:
        data = self._load_data()
        modules = data.get("modules", [])

        # Check unique name
        if any(m["name"] == module.name for m in modules):
            return False

        new_id = max([m["id"] for m in modules], default=0) + 1
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
            if m["id"] == module.id:
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
        modules = [m for m in modules if m["id"] != module_id]
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
        """Mock connection for views/models that query sqlite directly"""
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
