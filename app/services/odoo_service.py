"""
Odoo Service Connector (Fixed XML-RPC / JSON-RPC Protocol & Timeouts)
"""

import xmlrpc.client
import socket
from typing import List, Dict, Tuple, Optional


class OdooConnector:
    """Connect to Odoo and fetch module/model data via standard XML-RPC endpoints"""

    def __init__(self, url: str, db: str, username: str, password: str, timeout: int = 30):
        self.url = url.rstrip('/')
        self.db = db
        self.username = username
        self.password = password
        self.timeout = timeout
        self.uid = None
        self.common = None
        self.models = None
        self.is_connected = False

    def connect(self) -> Tuple[bool, str]:
        """Establish connection to Odoo using standard XML-RPC endpoints with timeout"""
        try:
            # Set default socket timeout for xmlrpc calls
            socket.setdefaulttimeout(self.timeout)

            common_url = f'{self.url}/xmlrpc/2/common'
            models_url = f'{self.url}/xmlrpc/2/object'

            self.common = xmlrpc.client.ServerProxy(common_url, allow_none=True)
            self.models = xmlrpc.client.ServerProxy(models_url, allow_none=True)

            # Authenticate via standard xmlrpc/2/common authenticate
            uid = self.common.authenticate(self.db, self.username, self.password, {})

            if uid:
                self.uid = uid
                self.is_connected = True
                return True, "Connected successfully"
            else:
                return False, "Authentication failed (invalid credentials or database)"

        except Exception as e:
            return False, f"Connection error: {str(e)}"

    def get_installed_modules(self) -> List[Dict]:
        """Get list of installed modules from Odoo"""
        if not self.is_connected or not self.uid:
            return []

        try:
            modules = self.models.execute_kw(
                self.db, self.uid, self.password,
                'ir.module.module', 'search_read',
                [[('state', '=', 'installed')]],
                {'fields': ['name', 'shortdesc', 'description', 'author',
                           'version', 'category', 'license', 'depends_ids']}
            )

            result = []
            for mod in modules:
                result.append({
                    'name': mod.get('name', ''),
                    'display_name': mod.get('shortdesc', ''),
                    'description': mod.get('description', ''),
                    'author': mod.get('author', ''),
                    'version': mod.get('version', ''),
                    'category': mod.get('category', ''),
                    'license': mod.get('license', ''),
                    'is_custom': self.is_custom_module(mod.get('name', '')),
                    'dependencies': [str(d) for d in mod.get('depends_ids', [])],
                })

            return result

        except Exception as e:
            print(f"Error fetching modules: {e}")
            return []

    def get_models(self) -> List[Dict]:
        """Get all models from Odoo"""
        if not self.is_connected or not self.uid:
            return []

        try:
            models = self.models.execute_kw(
                self.db, self.uid, self.password,
                'ir.model', 'search_read',
                [[]],
                {'fields': ['model', 'name', 'module', 'transient', 'abstract']}
            )

            result = []
            for model in models:
                result.append({
                    'model_name': model.get('model', ''),
                    'display_name': model.get('name', ''),
                    'module': model.get('module', ''),
                    'model_type': 'transient' if model.get('transient') else
                                  'abstract' if model.get('abstract') else 'model',
                })

            return result

        except Exception as e:
            print(f"Error fetching models: {e}")
            return []

    @staticmethod
    def is_custom_module(module_name: str) -> bool:
        """Determine if module is custom (not core Odoo)"""
        core_modules = {
            'base', 'web', 'web_diagram', 'web_kanban', 'web_tour',
            'account', 'sale', 'purchase', 'stock', 'crm', 'hr', 'project',
            'mail', 'calendar', 'contacts', 'survey', 'website', 'iot',
            'im_live_support', 'im_support', 'digest', 'mrp', 'quality',
        }
        return module_name not in core_modules and not module_name.startswith('web_')
