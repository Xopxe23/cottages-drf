from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'
    verbose_name = "Пользователи"

    def ready(self):
        from django.conf import settings

        from core.containers import configure_containers
        configure_containers(settings)
