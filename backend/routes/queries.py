import os

import requests
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(tags=["Queries"])


class QueryRelateDB(BaseModel):
    query: dict


@router.post("/query")
def query_realte(request: QueryRelateDB):
    response = requests.post(
        url=os.environ["RELATE_DB_URL"],
        auth=(os.environ["RELATE_DB_USER"], os.environ["RELATE_DB_PASSWORD"]),
        json=request.query,
    )

    response.raise_for_status()

    return response.json()
