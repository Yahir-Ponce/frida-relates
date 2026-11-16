import os
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import psutil
import relate
from src.models import Graph, Memory, StatsResponse


class GraphManager:
    def __init__(self, graph_dir: str):
        self.graph_dir = Path(graph_dir)
        self.graphs = {}

    def open_graph(self, graph_id):
        if graph_id in self.graphs:
            return

        executor = ThreadPoolExecutor(max_workers=1)
        path = self.graph_dir / f"{graph_id}.rl"
        future = executor.submit(relate.connect, str(path))

        connection = future.result()

        self.graphs[graph_id] = {
            "executor": executor,
            "connection": connection,
            "last_used": time.monotonic(),
            "open_queries": 0,
        }

    def close_graph(self, graph_id: str):
        graph = self.graphs[graph_id]

        if graph is None:
            return False

        executor = graph["executor"]
        connection = graph["connection"]

        future = executor.submit(connection.close)
        future.result()

        executor.shutdown(wait=True)
        del self.graphs[graph_id]

        return True

    def _get_memory(self) -> Memory:
        process = psutil.Process(os.getpid())

        memory_bytes = process.memory_info().rss
        memory_mb = memory_bytes / (1024 * 1024)

        limit_mb = int(os.environ["MEMORY_LIMIT_MB"])

        return Memory(
            used_mb=round(memory_mb, 2),
            limit_mb=limit_mb,
            percent=round((memory_mb / limit_mb) * 100, 2),
        )

    def stats(self) -> StatsResponse:
        graphs = []
        for path in self.graph_dir.glob("*.rl"):
            graph_id = path.stem

            graphs.append(
                Graph(
                    id=graph_id,
                    status="open" if graph_id in self.graphs else "close",
                    size_mb=round(path.stat().st_size / (1024 * 1024), 2),
                )
            )

        memory = self._get_memory()

        return StatsResponse(
            worker_id=os.environ["WORKER_ID"], memory=memory, graphs=graphs
        )

    def get_least_recently_used(self) -> str | None:
        if len(self.graphs) == 0:
            return None

        non_used_graphs = {}
        for graph_id, graph_data in self.graphs.items():
            if graph_data["open_queries"] == 0:
                non_used_graphs[graph_id] = graph_data

        oldest_graph_id = min(
            self.graphs, key=lambda graph_id: non_used_graphs[graph_id]["last_used"]
        )

        return oldest_graph_id

    def evict_if_needed(self):
        memory = self._get_memory()
        if memory.percent < os.environ["MEMORY_THRESHOLD"]:
            return

        graph_id = self.get_least_recently_used()
        if graph_id is None:
            return

        self.close_graph(graph_id=graph_id)


manager = GraphManager(os.environ["GRAPHS_DIR"])
