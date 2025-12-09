from fastapi import FastAPI


def create_app() -> FastAPI:
    app = FastAPI(
        title="{{ project_name }}",
        version="0.0.1",
    )

    return app
