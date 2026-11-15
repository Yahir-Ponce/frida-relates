from fastapi import APIRouter

from .graphs import router as graphs_router
from .query import router as query_router

router = APIRouter(prefix="/v1/graphs")

router.include_router(graphs_router)
router.include_router(query_router)
