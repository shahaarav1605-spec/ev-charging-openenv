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