from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Request
from fastapi_utils.cbv import cbv

from apps.container import Container
from apps.translate.service import TranslateService
from schemas.filters import OffsetParams
from schemas.translate import TranslateSchema, TranslateListSchema

router = APIRouter()


@cbv(router)
class TranslateController:
    base_route = "translate"
    tags = ["Translate Controller"]
    router = router

    @inject
    def __init__(self, translate_service: TranslateService = Depends(
        Provide[Container.translate_package.translate_service]),
                 ):
        self.translate_service = translate_service

    @router.get("/{word}", status_code=200, )
    async def search(self, word: str) -> TranslateSchema:
        return await self.translate_service.search(word)

    @router.get("/", status_code=200, )
    async def get(self, filters: OffsetParams = Depends()) -> TranslateListSchema:
        return await self.translate_service.get_all(filters)

    @router.delete("/{word}/", status_code=200, )
    async def delete(self, word: str) -> TranslateSchema:
        return await self.translate_service.remove_by_field("word", word)
