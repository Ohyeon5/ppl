import logging
import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

LOGGER = logging.getLogger(__name__)

app = FastAPI(title="lwa-api", docs_url="/api/docs", openapi_url="/api")

origins = [
    "http://localhost:5173",
    "localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api")
async def welcome():
    return {"message": "Welcome to vlib api!"}


@app.get("/status")
async def index():
    testvar = os.getenv("AZURE_PSQL_SERVER_NAME")

    return {"message": testvar}
