from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(title="Claim Processing API")

app.include_router(router)

@app.get("/")
def root():
    return {"message": "API is running"}