import os
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import relate


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

        self.graphs[graph_id] = {"executor": executor, "connection": connection}

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


manager = GraphManager(os.environ["GRAPHS_DIR"])
