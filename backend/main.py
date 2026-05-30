from fastapi import FastAPI
from routers.auth import router as auth_router
from routers.clients import router as clients_router
from routers.quotes import router as quotes_router

app = FastAPI(title="AEHub API")

app.include_router(auth_router)
app.include_router(clients_router)
app.include_router(quotes_router)


@app.get("/")
def root():
    return {"hello": "world"}