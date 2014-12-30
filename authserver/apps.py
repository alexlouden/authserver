from django.apps import AppConfig


class AuthServerConfig(AppConfig):
    name = 'authserver'

    def ready(self):
        pass
