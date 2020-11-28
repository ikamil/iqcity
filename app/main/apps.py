from django.apps import AppConfig


class MainConfig(AppConfig):
    name = 'main'
    verbose_name = 'Справочники'


from suit.apps import DjangoSuitConfig


class SuitConfig(DjangoSuitConfig):
    # layout = 'horizontal'
    layout = 'vertical'
