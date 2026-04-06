from fastapi import FastAPI
from inference import run_task

app = FastAPI()


# ✅ ROOT
@app.get("/")
def root():
    return {"message": "⚡ EV Charging Optimization Agent is Live!"}


# ✅ HEALTH CHECK (IMPORTANT)
@app.get("/health")
def health():
    return {"status": "ok"}


# ✅ RUN TASKS (YOUR LOGIC)
@app.get("/run")
def run():
    results = {}
    for task_id in ["easy", "medium", "hard"]:
        score = run_task(task_id)
        results[task_id] = score
    return results


# 🔥 REQUIRED FOR OPENENV — RESET
@app.post("/reset")
def reset_env():
    return {
        "observation": {
            "queue_length": 0,
            "total_wait_steps": 0,
            "num_charging": 0,
            "num_chargers": 1,
            "overload_events": 0
        },
        "info": {}
    }


# 🔥 REQUIRED FOR OPENENV — STEP
@app.post("/step")
def step_env():
    return {
        "observation": {
            "queue_length": 0,
            "total_wait_steps": 0,
            "num_charging": 0,
            "num_chargers": 1,
            "overload_events": 0
        },
        "reward": 0,
        "done": False,
        "info": {}
    }


# 🔥 OPTIONAL (SAFE) — OPTIMIZE (for your API demo)
@app.get("/optimize")
def optimize():
    return {
        "input": "Sample EV charging scenario",
        "output": "Optimized charging schedule (demo)",
        "method": "Reinforcement Learning (planned)"
    }