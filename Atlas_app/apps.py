from django.apps import AppConfig


class AtlasAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Atlas_app'

    def ready(self):
        import Atlas_app.signals