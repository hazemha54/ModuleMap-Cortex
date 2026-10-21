"""
Domain models for ModuleMap-Cortex
"""

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Module:
    """Module data class"""
    id: int
    name: str
    display_name: str
    description: str
    author: str
    version: str
    category: str
    is_custom: bool
    is_installed: bool
    dependencies: List[str] = field(default_factory=list)


@dataclass
class ModelRecord:
    """Odoo Model data class"""
    id: int
    module_id: int
    model_name: str
    display_name: str
    model_type: str
    parent_model: Optional[str]
    fields_data: str = "{}"


@dataclass
class ChangeRecord:
    """Module or Code Change data class"""
    id: int
    module_id: int
    change_type: str
    change_description: str
    severity: str
    detected_at: str
