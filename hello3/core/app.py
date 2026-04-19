from fastapi import FastAPI
from core.config import settings
from core.logger import configure_logging

configure_logging(settings.LOG_LEVEL)

app = FastAPI(title="hello3", version="0.1.0")
