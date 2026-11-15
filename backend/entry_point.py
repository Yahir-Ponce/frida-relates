from fastapi import FastAPI

app = FastAPI(title="RelateDB", summary="something")


@app.get("/health")
def _health():
    return {"message": "OK"}


from backend.routes.queries import router as queries_router
from backend.routes.registry import router as registry_router

app.include_router(registry_router)
app.include_router(queries_router)
