from typing import Dict

import uvicorn
from fastapi import FastAPI, HTTPException
from sqlalchemy.ext.asyncio import create_async_engine
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse

from apps.container import Container
from apps.controllers import (
    translate_controller,
)
from apps.routes import register_all_routes
from settings import settings, build_sqlalchemy_database_uri
from settings.enums import PingServices


def create_app() -> FastAPI:
    main_container = Container()
    main_container.config.from_value(settings)
    main_container.wire(
        modules=[
            translate_controller,
        ]
    )
    fast_app = FastAPI()

    @fast_app.get("/", include_in_schema=False)
    async def index() -> RedirectResponse:
        return RedirectResponse(url="/docs")

    fast_app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["*"],
    )
    fast_app.main_container = main_container
    register_all_routes(fast_app)
    return fast_app


app = create_app()


@app.get("/health")
async def health() -> Dict:
    failed_services = []

    try:
        # Check SQL connection
        engine = create_async_engine(build_sqlalchemy_database_uri(), echo=True)
        connection = await engine.connect()
        await connection.close()
    except Exception as e:
        failed_services.append({"service": PingServices.SQL.value, "reason": str(e)})

    if failed_services:
        raise HTTPException(status_code=500, detail=failed_services)

    return {"status": "ok"}


if __name__ == "__main__":
    import sys

    sys.dont_write_bytecode = True
    uvicorn.run(
        "app:app",
        port=settings.port,
        host=settings.host,
        log_level="debug",
        reload=True,
    )
