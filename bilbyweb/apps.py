from django.apps import AppConfig


class BilbywebConfig(AppConfig):
    name = 'bilbyweb'

    def ready(self):
        import bilbyweb.signals
