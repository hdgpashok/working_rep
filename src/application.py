from fastapi import FastAPI
from fastapi.responses import UJSONResponse

from starlette.middleware.cors import CORSMiddleware

from src.healthcheck import router as healthcheck_router
from src.routes.users import router as one_to_one_router
from src.routes.authors import router as one_to_many_router
from src.routes.actors import router as many_to_many_router

from src.core.exceptions.handler import error_handler


def get_app() -> FastAPI:
    """
    Get FastAPI application.

    This is the main constructor of an application.

    :return: application.
    """
    app = FastAPI(
        docs_url='/docs',
        openapi_url='/openapi.json',
        default_response_class=UJSONResponse,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )

    app.include_router(healthcheck_router)
    app.include_router(one_to_one_router)
    app.include_router(one_to_many_router)
    app.include_router(many_to_many_router)

    error_handler(app)

    return app
