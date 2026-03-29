from fastapi import FastAPI
from src.application.api.routes import accounts, transfers

app = FastAPI(title="Payments API")

app.include_router(accounts.router, prefix="/accounts", tags=["accounts"])
app.include_router(transfers.router, prefix="/transfers", tags=["transfers"])


@app.get("/")
def root():
    return {"message": "API running"}