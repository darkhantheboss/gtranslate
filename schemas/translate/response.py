from typing import List, Optional

from schemas.base import CamelModel


class TranslateSchema(CamelModel):
    word: str
    info: dict


class TranslateListSchema(CamelModel):
    results: List[TranslateSchema]
    total_results: int
