from typing import Literal

from pydantic import BaseModel


class Memory(BaseModel):
    used_mb: float
    limit_mb: float
    percent: float


class Graph(BaseModel):
    id: str
    size_mb: float
    status: Literal["open", "close"]


class StatsResponse(BaseModel):
    worker_id: str
    memory: Memory
    graphs: list[Graph]
