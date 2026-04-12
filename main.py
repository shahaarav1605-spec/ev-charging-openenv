from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"msg": "ok"}

@app.post("/reset")
def reset():
    return {"observation": {}, "reward": 0, "terminated": False, "truncated": False, "info": {}}

@app.post("/step")
def step():
    return {"observation": {}, "reward": 0.1, "terminated": False, "truncated": False, "info": {}}

@app.get("/run")
def run():
    return {"easy": 1, "medium": 0.7, "hard": 0.5}