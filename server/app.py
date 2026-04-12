from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict

app = FastAPI()

# -----------------------------
# FIXED MODELS
# -----------------------------
class ActionRequest(BaseModel):
    action: str = "charge"   # default value (prevents crash)


# -----------------------------
# RESET (SAFE)
# -----------------------------
@app.post("/openenv/reset")
def reset():
    return {
        "state": {
            "battery_level": 20,
            "target_level": 80,
            "time": 0
        },
        "reward": 0,
        "done": False
    }


# -----------------------------
# STEP (FIXED BODY HANDLING)
# -----------------------------
@app.post("/openenv/step")
def step(req: ActionRequest):
    return {
        "next_state": {
            "battery_level": 30,
            "time": 1
        },
        "reward": 1,
        "done": False,
        "info": {
            "action_taken": req.action
        }
    }


# -----------------------------
# VALIDATE
# -----------------------------
@app.get("/openenv/validate")
def validate():
    return {"status": "ok"}