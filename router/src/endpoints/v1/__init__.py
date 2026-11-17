from fastapi import APIRouter


router = APIRouter(prefix="/v1/graphs")

from .query import router as query_router
from .registry import router as registry_router

router.include_router(query_router)
router.include_router(registry_router)
