from fastapi import FastAPI
from routers.auth import router as auth_router
from routers.clients import router as clients_router
from routers.quotes import router as quotes_router
from routers.invoices import router as invoices_router
from routers.payments import router as payments_router
from routers.data_import import router as import_router

app = FastAPI(title="AEHub API")

app.include_router(auth_router)
app.include_router(clients_router)
app.include_router(quotes_router)
app.include_router(invoices_router)
app.include_router(payments_router)
app.include_router(import_router)


@app.get("/")
def root():
    return {"hello": "world"}