from fastapi import APIRouter
from pydantic import BaseModel

from backend.firebase import firestore_client

router = APIRouter(tags=["registry"], prefix="/registry")


class CreateProjectDB(BaseModel):
    project_name: str
    project_id: str


@router.post("/registry")
def registry_project(request: CreateProjectDB):
    try:
        doc_ref = firestore_client.collection("projects").document(request.project_id)
        doc_ref.set({"name": request.project_name})
    except Exception as e:
        raise Exception(f"Something went wrong {e}")
