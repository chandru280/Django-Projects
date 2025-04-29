from django.apps import AppConfig


class MyappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'myapp'


# students/apps.py

from django.apps import AppConfig

class StudentsConfig(AppConfig):
    name = 'students'

    def ready(self):
        import myapp.signals  # Import the signals so they are registered
