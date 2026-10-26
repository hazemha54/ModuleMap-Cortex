"""
Workspace Discovery Service for Scanning Local Odoo Source Directories with Structured Logging
"""

import os
import ast
import logging
from pathlib import Path
from typing import List, Dict, Optional

logger = logging.getLogger(__name__)


class WorkspaceManager:
    """Scans local directories for Odoo modules, manifests, models, and files"""

    def __init__(self, workspace_path: Optional[str] = None):
        self.workspace_path = Path(workspace_path) if workspace_path else Path.cwd()

    def scan_modules(self) -> List[Dict]:
        """Scan workspace for Odoo modules containing __manifest__.py or __openerp__.py"""
        modules = []
        if not self.workspace_path.exists():
            return modules

        # Search for manifest files up to depth 3
        for manifest_path in self.workspace_path.glob("**/__manifest__.py"):
            mod_dir = manifest_path.parent
            mod_info = self._parse_manifest(manifest_path)

            # Find python files and XML files in module
            py_files = [str(p.relative_to(mod_dir)) for p in mod_dir.glob("**/*.py")]
            xml_files = [str(p.relative_to(mod_dir)) for p in mod_dir.glob("**/*.xml")]

            modules.append({
                "name": mod_dir.name,
                "path": str(mod_dir.resolve()),
                "display_name": mod_info.get("name", mod_dir.name.replace("_", " ").title()),
                "description": mod_info.get("summary", mod_info.get("description", "")),
                "author": mod_info.get("author", "Unknown"),
                "version": mod_info.get("version", "1.0.0"),
                "category": mod_info.get("category", "Uncategorized"),
                "is_custom": True,
                "is_installed": True,
                "dependencies": mod_info.get("depends", []),
                "py_files": py_files,
                "xml_files": xml_files
            })

        return modules

    @staticmethod
    def _parse_manifest(manifest_path: Path) -> Dict:
        """Safely parse Odoo __manifest__.py dictionary"""
        try:
            content = manifest_path.read_text(encoding="utf-8")
            node = ast.parse(content, filename=str(manifest_path))
            for expr in node.body:
                if isinstance(expr, ast.Expr) and isinstance(expr.value, ast.Dict):
                    # Evaluate dictionary literal safely
                    return ast.literal_eval(expr.value)
        except Exception as e:
            logger.error(f"Error parsing manifest {manifest_path}: {e}", exc_info=True)
        return {}

    def get_file_content(self, file_path: str) -> str:
        """Read and return relative or absolute file content"""
        try:
            p = Path(file_path)
            if not p.is_absolute():
                p = self.workspace_path / p
            if p.exists() and p.is_file():
                return p.read_text(encoding="utf-8", errors="ignore")
        except Exception as e:
            logger.error(f"Error reading file {file_path}: {e}", exc_info=True)
        return ""
