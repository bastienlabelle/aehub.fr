from fastapi import FastAPI
from auth.router import router as auth_router

app = FastAPI(title="AEHub API")

app.include_router(auth_router)


@app.get("/")
def root():
    return {"hello": "world"}