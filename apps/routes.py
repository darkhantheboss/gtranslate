from fastapi import FastAPI

from apps.translate.controller import TranslateController
from helpers.base_router import register_routes


def register_all_routes(fast_app: FastAPI) -> None:
    register_routes(fast_app, TranslateController)
