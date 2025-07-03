"""
App configuration for Inventory module.
"""
from django.apps import AppConfig


class InventoryConfig(AppConfig):
    """Configuration for the Inventory app."""
    
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.inventory'
    verbose_name = 'Inventory Management'
    
    def ready(self):
        """Import signals when the app is ready."""
        try:
            import apps.inventory.signals  # noqa F401
        except ImportError:
            pass
