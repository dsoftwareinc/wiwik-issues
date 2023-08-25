import logging

from django.apps import AppConfig

logger = logging.getLogger(__package__)


class LandingpageConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'landingpage'
