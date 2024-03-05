import json
import logging
from typing import Dict, List

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from ppl.api.models import PubMedRequest  # ,  BrochureRequest, InferenceRequest
from ppl.path import DATA_PATH
from ppl.utils.pubmed import query_pubmed

## LLAMA_CPP is commented out because it requires downloading a 7B model
# from ppl.utils.model_zoo import LLAMA_CPP


LOGGER = logging.getLogger(__name__)

app = FastAPI(title="ppl-api", docs_url="/api/docs", openapi_url="/api")

origins = [
    "http://localhost:5173",
    "localhost:5173",
    "https://jolly-moss-0dba25e1e.5.azurestaticapps.net/",
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


# TODO: Remove following endpoints, demo purpose only
@app.get("/api/responses/{response_id}")
async def get_response(response_id: int):
    # load json file
    json_file = DATA_PATH / "responses.json"
    with open(json_file, "r") as f:
        json_content = json.load(f)
    return {
        "medicine": json_content[response_id]["medicine"],
        "response": json_content[response_id]["response"],
        "references": json_content[response_id]["references"],
    }


@app.get("/api/local_brochure/{response_id}")
async def get_brochure(response_id: int):
    # load json file
    json_file = DATA_PATH / "brochure.json"
    with open(json_file, "r") as f:
        json_content = json.load(f)
    return {
        "medicine": json_content[response_id]["medicine"],
        "response": json_content[response_id]["brochure"],
        "references": json_content[response_id]["references"],
    }


# @app.post("/api/local_q_and_a")
# async def local_q_and_a(request: InferenceRequest):
#     # load json file
#     json_file = DATA_PATH / "articles.json"
#     with open(json_file, "r") as f:
#         json_content = json.load(f)
#     response = LLAMA_CPP.complete(
#         f"Summary the benefit of {request.medicine} given following articles: "
#         + " ".join([json_content[ii]["abstract"] for ii in request.indicies])
#     )
#     return {
#         "response": response.text,
#         "references": [json_content[ii] for ii in request.indicies],
#     }


# @app.post("/api/brochure")
# async def brochure_text(request: BrochureRequest):
#     # load json file
#     json_file = DATA_PATH / "responses.json"
#     with open(json_file, "r") as f:
#         json_content = json.load(f)
#     response = LLAMA_CPP.complete(
#         f"Given the benefits from {request.medicine} "
#         + f"generate a marketing brochure for the medicine product {request.medicine} "
#         + "The audiences are medical doctors. Provide text and placeholders for the statistical graphs."
#         + "Here is the benefit : "
#         + f"{json_content[request.response_id]['response']}"
#     )
#     return {"response": response.text}
