from dependency_injector import containers, providers

from users.services import CodeService, UserService


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    code_service = providers.Factory(CodeService)
    user_service = providers.Factory(UserService, code_service=code_service)


def configure_containers(settings):
    container = Container()
    container.config.from_dict(settings.__dict__)
    container.wire(modules=["users.views"])
