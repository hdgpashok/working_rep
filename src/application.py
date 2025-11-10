from fastapi import FastAPI
from fastapi.responses import UJSONResponse

from starlette.middleware.cors import CORSMiddleware

from healthcheck import router as healthcheck_router
from one_to_one import router as one_to_one_router


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

    return app
