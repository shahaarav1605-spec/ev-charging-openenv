from fastapi import FastAPI

app = FastAPI(title="EV Charging Optimization Agent")

@app.get("/")
def home():
    return {
        "message": "⚡ EV Charging Optimization Agent is Live!",
        "status": "running"
    }

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/optimize")
def optimize():
    return {
        "input": "Sample EV charging scenario",
        "output": "Optimized charging schedule (demo)",
        "method": "Reinforcement Learning (planned)"
    }