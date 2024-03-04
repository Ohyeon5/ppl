import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

LOGGER = logging.getLogger(__name__)

app = FastAPI(title="ppl-api", docs_url="/api/docs", openapi_url="/api")

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
    return {"message": "Welcome to ppl api!"}


@app.get("/api/health")
async def health():
    return {"message": "OK"}


@app.post("/api/search/pubmed")
async def search_pubmed():
    return {"message": "search_pubmed"}
