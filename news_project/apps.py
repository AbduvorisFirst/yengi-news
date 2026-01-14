from django.apps import AppConfig


class NewsProjectConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'news_project'

    def ready(self):
        from .signals import contact_signal, news_signal
