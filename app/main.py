from fastapi import FastAPI
from api import inventory

app = FastAPI()

app.include_router(inventory.router, prefix="/api", tags=["v1"])
