from fastapi import FastAPI

app = FastAPI(title="AEHub API")


@app.get("/")
def root():
    return {"hello": "world"}