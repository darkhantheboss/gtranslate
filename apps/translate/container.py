from dependency_injector import containers, providers

from apps.translate import entity, repository, service
from models import Translate
from schemas.translate import TranslateSchema


class TranslateContainer(containers.DeclarativeContainer):
    config = providers.Configuration()

    translate_factory = providers.Factory(entity.TranslateFactory)

    translate_repository = providers.Singleton(
        repository.TranslateRepository,
        model=Translate,
        factory=translate_factory,
        schema=TranslateSchema,
        config=config,
    )

    translate_service = providers.Singleton(
        service.TranslateService,
        repository=translate_repository,
    )
