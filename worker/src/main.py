from fastapi import FastAPI

app = FastAPI()


@app.get("/health")
def healt():
    return {"status": "ok"}


from src.endpoints.v1 import router as v1_router

app.include_router(v1_router)
