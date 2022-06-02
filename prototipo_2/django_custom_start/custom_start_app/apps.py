from django.apps import AppConfig


class CustomStartAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'custom_start_app'
