from django.apps import AppConfig


class TupakwebConfig(AppConfig):
    name = 'tupakweb'

    def ready(self):
        import tupakweb.signals
