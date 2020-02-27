from django.apps import AppConfig


class OrganizationConfig(AppConfig):
    name = 'organization'

    # django recommended way of importing signals
    def ready(self):
        import organization.signals
