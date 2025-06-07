from contextlib import asynccontextmanager
from fastapi import FastAPI
from backend.app.core.db import create_db_tables
from backend.app.api.v1.predictions import router as pred_router
from backend.app.api.v1.actuals import router as actual_router
from backend.app.core.utils import *


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_tables()
    yield

app = FastAPI(
    title=API_TITLE,
    version=API_VERSION,
    lifespan=lifespan
)

app.include_router(pred_router, prefix=API_V1_PREFIX)
app.include_router(actual_router, prefix=API_V1_PREFIX)
