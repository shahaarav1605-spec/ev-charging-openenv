"""
Baseline inference script for EVChargingEnvironment.
"""

import os
import copy
import random
from typing import Dict

from ev_charging_env.server.environment import EVChargingEnvironment
from ev_charging_env.tasks import TASKS
from ev_charging_env.models import StationAction


# 🌍 ENV VARIABLES
API_BASE_URL = os.getenv("API_BASE_URL", "http://host.docker.internal:8000")
MODEL_NAME = os.getenv("MODEL_NAME", "ev-agent")
HF_TOKEN = os.getenv("HF_TOKEN", None)


# ✅ ALL POSSIBLE ACTIONS
def get_all_actions():
    return [
        StationAction(price_level=0, power_mode=0),
        StationAction(price_level=0, power_mode=1),
        StationAction(price_level=1, power_mode=0),
        StationAction(price_level=1, power_mode=1),
        StationAction(price_level=2, power_mode=0),
        StationAction(price_level=2, power_mode=1),
    ]


# 🎯 SIMULATION FUNCTION
def simulate(env, action):
    sim_env = copy.deepcopy(env)
    _, rew = sim_env.step(action)
    return rew.value


# 🚀 MAIN RL LOGIC
def run_task(task_id: str) -> float:
    task_cfg: Dict = TASKS[task_id]
    env = EVChargingEnvironment(task_name=task_cfg["task_name"])

    # 🔹 START BLOCK
    print(f"[START] task={task_id}", flush=True)

    obs, rew = env.reset()

    rewards = []
    step_count = 0

    actions = get_all_actions()
    action_scores = [0.0] * len(actions)

    while not rew.done:
        step_count += 1

        best_action = None
        best_score = -1e9
        best_idx = 0

        # 🎲 Exploration
        if random.random() < 0.1:
            best_action = random.choice(actions)
            best_idx = actions.index(best_action)
        else:
            for i, action in enumerate(actions):
                score = simulate(env, action)

                # 📊 Features
                queue = obs.queue_length
                wait = obs.total_wait_steps
                charging = obs.num_charging
                chargers = obs.num_chargers
                overload = obs.overload_events

                utilization = charging / chargers if chargers > 0 else 0

                # 🔥 SCORING
                score += utilization * 8
                score += charging * 0.5
                score -= queue * 0.3
                score -= wait * 0.002

                target = 0.65
                score -= abs(utilization - target) * 5

                if overload > 0:
                    score -= 50

                score += action_scores[i] * 0.1

                if score > best_score:
                    best_score = score
                    best_action = action
                    best_idx = i

        # ✅ Apply action
        obs, rew = env.step(best_action)
        rewards.append(rew.value)

        # 📌 STEP BLOCK (IMPORTANT)
        print(f"[STEP] step={step_count} reward={rew.value}", flush=True)

        # 🧠 Learning update
        action_scores[best_idx] += rew.value

        for i in range(len(action_scores)):
            if i != best_idx:
                action_scores[i] *= 0.95

    # 📊 FINAL SCORE
    mean_reward = float(sum(rewards) / len(rewards)) if rewards else 0.0
    normalized = (mean_reward + 1.5) / 1.5

    # 🔚 END BLOCK
    print(
        f"[END] task={task_id} score={normalized:.4f} steps={step_count}",
        flush=True,
    )

    return normalized


# 🧠 MAIN ENTRY
def main():
    print(f"API_BASE_URL={API_BASE_URL}")
    print(f"MODEL_NAME={MODEL_NAME}")
    print(f"HF_TOKEN set={bool(HF_TOKEN)}")

    for task_id in TASKS.keys():
        run_task(task_id)


if __name__ == "__main__":
    main()