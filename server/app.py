from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from main import optimize_charging

app = FastAPI()

# -----------------------------
# Request Model
# -----------------------------
class ChargingRequest(BaseModel):
    battery_level: float        # current battery %
    target_level: float         # target battery %
    hours_available: int        # time available
    price_per_hour: List[float] # electricity price per hour
    solar_available: List[float]  # solar energy contribution (0-1)

# -----------------------------
# Root Endpoint
# -----------------------------
@app.get("/")
def root():
    return {"message": "EV Charging Optimization Agent Running 🚀"}

# -----------------------------
# Optimization Endpoint
# -----------------------------
@app.post("/optimize")
def optimize(request: ChargingRequest):
    result = optimize_charging(
        battery_level=request.battery_level,
        target_level=request.target_level,
        hours=request.hours_available,
        prices=request.price_per_hour,
        solar=request.solar_available
    )
    return result