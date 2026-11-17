from typing import Any, Optional

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from src.services.graph_manager import manager
from src.services.query_service import QueryService

router = APIRouter(tags=["Query"])


class QueryRequest(BaseModel):
    query: str
    params: dict[str, Any] | None = None


@router.post("/{id}/query")
def query(id: str, request: QueryRequest):
    if id not in manager.graphs:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Graph {id} not found"
        )
    query_service = QueryService(manager)

    return query_service.execute(
        graph_id=id,
        cypher=request.query,
        parameters=request.params or {},
    )
