import json
import logging
from typing import Dict, List

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from ppl.api.models import InferenceRequest, PubMedRequest
from ppl.path import DATA_PATH
from ppl.utils.pubmed import query_pubmed

from services.backend.src.ppl.utils.model_zoo import LLAMA_CPP

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


@app.get("/api/status")
async def status():
    # TODO Test query to the database
    # TODO Test connection to pubmed api
    return {"message": "OK"}


@app.post("/api/search/pubmed")
async def search_pubmed(request: PubMedRequest):
    articles: List[Dict] = query_pubmed(
        search_term=request.search_term,
        keywords=request.keywords,
        n_uids=request.n_uids,
        relative_date=request.relative_date,
    )
    return {"articles": articles, "total": len(articles)}


@app.post("/api/local_q_and_a")
async def local_q_and_a(request: InferenceRequest):
    # load json file
    json_file = DATA_PATH / "articles.json"
    with open(json_file, "r") as f:
        json_content = json.load(f)
    response = LLAMA_CPP.complete(
        f"Summary the benefit of {request.medicine} given following articles: "
        + " ".join([json_content[ii]["abstract"] for ii in request.indicies])
    )
    return {"response": response.text}
