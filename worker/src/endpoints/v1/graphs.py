from fastapi import APIRouter
from services.graph_manager import manager

router = APIRouter(tags=["Graphs"])


@router.post("/{id}/open")
def open(id: str):
    manager.open_graph(id)

    return {
        "message": "ok",
    }


@router.post("/{id}/close")
def close(id: str):
    response = manager.close_graph(id)
    if response is False:
        return {"message": "Error while clossing the graph"}

    return {"message": "Graph closed"}
