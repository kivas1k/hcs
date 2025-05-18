from django.apps import AppConfig
import logging

logger = logging.getLogger(__name__)

class NotificationsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'notifications'

    def ready(self):
        try:
            from . import signals  # noqa: F401
            logger.info("Notifications signals successfully loaded!")
        except ImportError:
            logger.error("Failed to load notifications signals!")
        super().ready()