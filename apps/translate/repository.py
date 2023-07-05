# import requests

from typing import Any

from googletrans import Translator
# from bs4 import BeautifulSoup
from pydantic import BaseModel

from apps.translate.entity import TranslateFactory
from helpers.repository import SQLRepository
from schemas.translate import TranslateSchema
from settings.base import Settings
from settings.constants import GOOGLE_TRANSLATE_URL


class TranslateRepository(SQLRepository):
    def __init__(
        self,
        model: Any,
        factory: TranslateFactory,
        schema: BaseModel,
        config: Settings,
    ) -> None:
        super().__init__(model, factory, schema)
        self.model = model
        self.factory = factory
        self.schema = schema
        self.config = config
        self.google_translate_url = GOOGLE_TRANSLATE_URL

    async def translate(self, word: str) -> TranslateSchema:
        # url = f"{GOOGLE_TRANSLATE_URL}&text={word}"
        # resp = requests.get(url=url, timeout=30)
        # soup = BeautifulSoup(resp.text, "html.parser")

        translator = Translator()
        res = translator.translate(word, dest='ru')

        info = {"definitions": [res.text], "synonyms": [res.text], "translations": [res.text]}
        return dict(word=word, info=info)

    async def search(self, word: str) -> TranslateSchema:
        obj = await self.upsert("word", word, await self.translate(word), (TranslateSchema, ))
        return TranslateSchema.from_orm(obj)
