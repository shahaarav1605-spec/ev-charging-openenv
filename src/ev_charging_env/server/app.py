from fastapi import FastAPI
from inference import run_task

app = FastAPI()

@app.get("/")
def root():
    return {"message": "EV Charging Agent Running"}

@app.get("/run")
def run():
    results = {}
    for task_id in ["easy", "medium", "hard"]:
        score = run_task(task_id)
        results[task_id] = score
    return results

@app.post("/reset")
def reset_env():
    return {
        "message": "Environment reset successful"
    }

@app.post("/step")
def step_env():
    return {
        "message": "Step executed",
        "reward": 0,
        "done": False
    }