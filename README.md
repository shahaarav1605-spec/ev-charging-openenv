# ⚡ EV Charging Optimization Agent

AI-powered EV Charging Optimization Agent using Reinforcement Learning.

## 📌 Overview

The EV Charging Optimization Agent is an intelligent system designed to optimize electric vehicle (EV) charging strategies in real time.

It simulates multiple charging scenarios and dynamically selects the most efficient actions using a reward-based decision mechanism inspired by reinforcement learning.

The goal is to improve charging efficiency, reduce waiting time, and ensure balanced energy utilization.

---

## 🎯 Problem Statement

With the increasing adoption of electric vehicles, current charging infrastructure faces several challenges:

- ⚠️ Long waiting queues at charging stations  
- ⚠️ Uneven distribution of charging load  
- ⚠️ Inefficient energy utilization  
- ⚠️ Lack of adaptive decision-making systems  

These issues lead to poor user experience and reduced system efficiency.

---

## 💡 Our Solution

We developed an intelligent EV charging agent that:

- Monitors charging conditions dynamically  
- Selects optimal actions based on system state  
- Uses a reward-based feedback mechanism  
- Ensures consistent and efficient performance across scenarios  

The system adapts its behavior based on different difficulty levels (easy, medium, hard), making it robust and scalable.

---

## 🚀 Key Features

- ⚡ Adaptive charging optimization  
- 🧠 Reward-driven decision system  
- 🔄 Multi-scenario simulation (easy, medium, hard)  
- 🚀 FastAPI-powered API interface  
- 🐳 Dockerized for seamless deployment  
- 📊 Stable and normalized performance output  

---

## 🧠 How It Works

1. The environment simulates EV charging conditions  
2. The agent observes the current system state  
3. Based on predefined logic, it selects an optimal action  
4. A reward is calculated based on efficiency and performance  
5. The process repeats, improving overall system behavior  

This creates a feedback loop similar to reinforcement learning, enabling adaptive optimization.

---

## 📊 Results

The agent produces stable and optimized outputs across different scenarios:

```json
{
  "easy": 0.60,
  "medium": 0.36,
  "hard": 0.25
}

## ⚙️ Tech Stack

- Python
- FastAPI
- Docker
- HuggingFace Integration (optional)
- Reinforcement-style logic (custom implementation)

---

## 🏗️ Project Structure

ev-charging-openenv/
│
├── server/
│ └── app.py # FastAPI server
│
├── src/
│ └── ev_charging_env/
│ ├── environment.py
│ ├── models.py
│ ├── simulation.py
│ ├── tasks.py
│
├── inference.py # Main logic runner
├── Dockerfile
├── requirements.txt
├── README.md


---

## 🚀 How to Run

### 1️⃣ Build Docker Image

```bash
docker build -t ev-agent .
```

---

### 2️⃣ Run the Container

```bash
docker run -p 8000:8000 -e HF_TOKEN=your_token ev-agent
```

> 🔑 Replace `your_token` with your HuggingFace token (optional)

---

### 3️⃣ Open API in Browser

Go to:

http://localhost:8000/docs

---

### 4️⃣ Run the Agent

- Click **GET /run**
- Click **Try it out**
- Click **Execute**

---

### ✅ Expected Output

```json
{
  "easy": 0.60,
  "medium": 0.36,
  "hard": 0.25
}
```

### 📸 Output Screenshot

![Output Screenshot](image-6.png)