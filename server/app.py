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


# OpenEnv RESET

@app.post("/reset")
def reset():
    return {
        "observation": {},
        "reward": 0.0,
        "done": False,
        "info": {}
    }


# OpenEnv STEP

@app.post("/step")
def step():
    return {
        "observation": {"msg": "step"},
        "reward": 0.1,
        "done": False,
        "info": {}
    }

# 🔥 REQUIRED MAIN FUNCTION
def main():
    import uvicorn
    uvicorn.run("server.app:app", host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()