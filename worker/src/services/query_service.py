import time
from typing import Any

from src.services.graph_manager import GraphManager


class QueryService:
    def __init__(self, manager: GraphManager) -> None:
        self.manager = manager

    def execute(
        self,
        graph_id: str,
        cypher: str,
        parameters: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        graph = self.manager.graphs.get(graph_id)

        if graph is None:
            raise ValueError(f"Graph '{graph_id}' is not open")

        executor = graph["executor"]
        connection = graph["connection"]

        def run_query():
            cursor = connection.execute(cypher, parameters or {})

            return {
                "columns": cursor.keys(),
                "rows": [record.to_dict() for record in cursor.fetchall()],
            }

        future = executor.submit(run_query)

        try:
            return future.result()
        finally:
            graph["last_used"] = time.monotonic()
