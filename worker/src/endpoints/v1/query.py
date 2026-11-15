from fastapi import APIRouter

from services.graph_manager import manager
from services.query_service import QueryService

router = APIRouter(tags=["Query"])


@router.post("/{id}/query")
def query(id: str, query: dict):



@router.get("/test")
def test():

    from services.graph_manager import manager
    from services.query_service import QueryService

    query_service = QueryService(manager)

    manager.open_graph("test")

    result = query_service.execute(
        graph_id="test",
        cypher="RETURN 1 AS number",
    )

    print(result)
