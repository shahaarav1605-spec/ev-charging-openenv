from fastapi import FastAPI
from inference import run_task

app = FastAPI()


@app.get("/")
def root():
    return {"message": "EV Charging Agent Running"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/run")
def run():
    results = {}
    for task_id in ["easy", "medium", "hard"]:
        results[task_id] = run_task(task_id)
    return results


@app.post("/reset")
def reset():
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


@app.post("/step")
def step():
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