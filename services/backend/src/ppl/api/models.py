from typing import List, Optional

from pydantic import BaseModel, Field


class InferenceRequest(BaseModel):
    medicine: str
    indicies: List[int]


class PubMedRequest(BaseModel):
    search_term: str
    keywords: list[str]
    n_uids: int = Field(description="Number of articles to return", default=15)
    relative_date: Optional[int] = Field(
        description="Number of days in the past", default=None
    )
