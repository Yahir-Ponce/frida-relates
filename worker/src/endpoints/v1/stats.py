from fastapi import APIRouter
from src.models import StatsResponse
from src.services.graph_manager import manager

router = APIRouter(tags=["Stats"])


@router.get("/stats", response_model=StatsResponse)
def get_stats():
    return manager.stats()


@router.get("/last_used")
def get_last_used():
    return manager.get_least_recently_used()
