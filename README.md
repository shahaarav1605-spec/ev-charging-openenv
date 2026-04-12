---
title: EV Charging Optimization Agent
emoji: ⚡
colorFrom: blue
colorTo: purple
sdk: gradio
app_file: app.py
----------------


# ⚡ EV Charging Optimization Agent

🚀 An intelligent AI agent designed to optimize EV charging stations by balancing **throughput, congestion, and system stability** in real-time.

---

## 🎯 Objective

Maximize EV charging throughput while minimizing:

* 🚗 Waiting queues
* ⚡ Power overload
* ⏱️ Charging delays

---

## 🧠 Core Idea

Instead of using fixed rules, this system:

✔ Evaluates multiple actions at every step
✔ Adapts to real-time conditions
✔ Selects the best strategy dynamically

---

## ⚙️ Key Features

### 🔹 Multi-Action Decision Engine

* Simultaneously evaluates:

  * Pricing strategies
  * Power distribution
* Selects optimal action per timestep

### 🔹 Adaptive Load Handling

* Detects congestion (queue length)
* Adjusts pricing & power dynamically

### 🔹 Overload Control

* Penalizes unsafe power usage
* Stabilizes grid performance

### 🔹 Time-Aware Optimization

* Uses time-of-day factor (solar window)
* Encourages efficient energy usage

### 🔹 Explainable AI

* Provides reasoning behind decisions
* Improves transparency and trust

---

## 🏗️ Project Structure

```
ev-charging-openenv/
│
├── app.py              # Gradio UI (Hugging Face)
├── main.py             # FastAPI backend (OpenEnv)
├── inference.py        # Core AI logic
├── Dockerfile          # Container setup
├── requirements.txt    # Dependencies
├── README.md
│
└── src/
    └── ev_charging_env/
        ├── environment.py
        ├── tasks.py
        ├── models.py
```

---

## 🚀 Demo (Hugging Face)

👉 Run the simulation live:

* Click **“🚀 Run Simulation”**
* View:

  * 📊 Performance scores (easy / medium / hard)
  * 🧠 Decision explanation

---

## 📊 Sample Output

```json
{
  "easy": 1.48,
  "medium": 0.92,
  "hard": 0.73
}
```

---

## 🔬 How It Works

### Step-by-Step:

1. Environment provides system state:

   * Queue length
   * Charger utilization
   * Waiting time
   * Overload level

2. Agent evaluates multiple actions:

   * Price levels (0–2)
   * Power modes (0–1)

3. Each action is scored based on:

   * Utilization efficiency
   * Queue reduction
   * Overload control
   * Time-based optimization

4. Best action is selected and applied

---

## 📈 Why This Stands Out

✔ Not rule-based — fully adaptive
✔ Handles real-world dynamic scenarios
✔ Balances efficiency + stability
✔ Works across all difficulty levels

---

## 🧪 API Endpoints (OpenEnv)

| Method | Endpoint  | Description       |
| ------ | --------- | ----------------- |
| GET    | `/health` | Health check      |
| POST   | `/reset`  | Reset environment |
| POST   | `/step`   | Perform action    |
| GET    | `/run`    | Run evaluation    |

---

## 🐳 Run Locally (Docker)

```bash
docker build -t ev-agent .
docker run -p 7860:7860 ev-agent
```

Open:

```
http://localhost:7860/docs
```

---

## 🧩 Tech Stack

* ⚡ FastAPI — Backend API
* 🎛️ Gradio — Interactive UI
* 🐳 Docker — Deployment
* 🧠 Custom RL Logic — Decision engine

---

## 🏁 Judges Notes

* ✔ Multi-action evaluation (not fixed policy)
* ✔ Adaptive behavior under high demand
* ✔ Explainable decisions for transparency
* ✔ Stable scoring across difficulty levels

---

## 👨‍💻 Team

**AI AIchemists**
AI/ML Developer | Hackathon Enthusiast

---

## ⭐ Final Thought

> “Smart charging isn’t just about speed — it’s about balance.”

This agent ensures efficient, scalable, and intelligent EV charging for future smart cities 🚀


### 📸 Output Screenshot

![Output Screenshot](image.png)