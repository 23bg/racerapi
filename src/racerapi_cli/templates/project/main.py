from fastapi import FastAPI
from app.core.app_factory import create_app

app = create_app()
