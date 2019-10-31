from django.apps import AppConfig
from django.db.models.signals import post_save

class ActivityConfig(AppConfig):
    name = 'activity'

    def ready(self):
        import activity.signals