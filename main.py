# app/main.py

from fastapi import FastAPI
from app.routers import items, clock_in

app = FastAPI(
    title="Vodex App",
    description="API for managing Items and User Clock-In Records",
    version="1.0.0"
)

# Include Routers
app.include_router(items.router)
app.include_router(clock_in.router)

# Root Endpoint
@app.get("/")
async def root():
    return {"message": "Welcome to the Vodex Application!"}
