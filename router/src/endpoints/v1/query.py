from typing import Any

import requests
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from src.services.firebase import firestore_client

router = APIRouter(tags=["Query"])


class QueryResponse(BaseModel):
    project_id: str
    cypher: str
    params: dict[str, Any] | None = None


@router.post("/query")
def query(request: QueryResponse):
    project = firestore_client.collection("graphs").document(request.project_id).get()
    if not project.exists:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Graph not found"
        )

    worker_id = project.to_dict()["worker_id"]
    worker = firestore_client.collection("workers").document(worker_id).get()
    worker_url = (worker.to_dict() or {}).get("url")
    if not worker_url:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Assigned worker is unavailable",
        )

    graph_url = f"{worker_url.rstrip('/')}/v1/graphs/{request.project_id}"
    try:
        response = requests.post(f"{graph_url}/open", timeout=10)
        response.raise_for_status()

        response = requests.post(
            f"{graph_url}/query",
            json={"query": request.cypher, "params": request.params},
            timeout=10,
        )
        response.raise_for_status()

        return response.json()
    except requests.RequestException as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Worker request failed",
        ) from exc
    finally:
        requests.post(f"{graph_url}/close", timeout=10)
