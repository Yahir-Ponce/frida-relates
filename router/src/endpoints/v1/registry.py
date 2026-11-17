from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from src.services.firebase import firestore_client

router = APIRouter(tags=["Registry"])


class RegistryProjectRequest(BaseModel):
    projct_id: str
    worker_id: str
    name: str


@router.post("/registy/project")
def registy_project(request: RegistryProjectRequest):
    worker = firestore_client.collection("workers").document(request.worker_id).get()
    if not worker.exists:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Worker not found"
        )

    project_ref = firestore_client.collection("graphs").document(request.projct_id)
    project_ref.set(request.model_dump())
    project_snapshot = project_ref.get()

    return project_snapshot.to_dict()


class RegistryWorkerRequest(BaseModel):
    url: str
    worker_id: str


@router.post("/registry/worker")
def registy_worker(request: RegistryWorkerRequest):
    doc_ref = firestore_client.collection("workers").document(request.worker_id)
    doc_ref.set(request.model_dump())
    doc_snapshot = doc_ref.get()

    return doc_snapshot.to_dict()
