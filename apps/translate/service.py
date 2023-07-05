from apps.translate.repository import TranslateRepository
from helpers.base_service import BaseService
from schemas.translate import TranslateSchema


class TranslateService(BaseService):
    def __init__(self, repository: TranslateRepository) -> None:
        self.repository = repository

    async def search(self, word: str) -> TranslateSchema:
        result = await self.repository.get_by("word", word)
        if result is None:
            result = await self.repository.search(word)
        return result
