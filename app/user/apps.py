from django.apps import AppConfig


class UserConfig(AppConfig):
    name = 'user'

    # django recommended way of importing signals
    def ready(self):
        import user.signals
