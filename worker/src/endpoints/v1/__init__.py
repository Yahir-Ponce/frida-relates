from fastapi import APIRouter

from .graphs import router as graphs_router
from .query import router as query_router
from .stats import router as stats_router

router = APIRouter(prefix="/v1/graphs")

router.include_router(graphs_router)
router.include_router(query_router)
router.include_router(stats_router)
