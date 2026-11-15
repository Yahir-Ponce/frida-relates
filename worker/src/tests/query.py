from services.graph_manager import manager
from services.query_service import QueryService

query_service = QueryService(manager)

manager.open_graph("test")

result = query_service.execute(
    graph_id="test",
    cypher="RETURN 1 AS number",
)

print(result)
