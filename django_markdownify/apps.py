from django.apps import AppConfig


class DjangoMarkdownifyConfig(AppConfig):
    name = 'django_markdownify'

    def ready(self):
        import django_markdownify.checks
