from dependency_injector import containers, providers

from apps.translate.container import TranslateContainer


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    translate_package = providers.Container(
        TranslateContainer,
        config=config,
    )
