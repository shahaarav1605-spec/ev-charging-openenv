"""
Final inference script for EVChargingEnvironment (Hackathon Ready)
"""

import os
import copy
import random
from typing import Dict

from openai import OpenAI

from ev_charging_env.server.environment import EVChargingEnvironment
from ev_charging_env.tasks import TASKS
from ev_charging_env.models import StationAction


# 🌍 ENV VARIABLES
API_BASE_URL = os.getenv("API_BASE_URL")
API_KEY = os.getenv("API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME", "ev-agent")

# 🔥 SAFE CLIENT
client = None
if API_BASE_URL and API_KEY:
    client = OpenAI(
        base_url=API_BASE_URL,
        api_key=API_KEY,
    )


# 🎯 ACTION SPACE
def get_all_actions():
    return [
        StationAction(price_level=0, power_mode=0),
        StationAction(price_level=0, power_mode=1),
        StationAction(price_level=1, power_mode=0),
        StationAction(price_level=1, power_mode=1),
        StationAction(price_level=2, power_mode=0),
        StationAction(price_level=2, power_mode=1),
    ]


# 🧪 SIMULATION
def simulate(env, action):
    sim_env = copy.deepcopy(env)
    _, rew = sim_env.step(action)
    return rew.value


# 🤖 OPTIONAL LLM GUIDANCE (VERY IMPORTANT)
def get_llm_hint(obs):
    if not client:
        return None

    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": "You optimize EV charging stations."},
                {
                    "role": "user",
                    "content": f"""
Queue: {obs.queue_length}
Charging: {obs.num_charging}
Wait: {obs.total_wait_steps}

Suggest: increase price / decrease price / increase power / decrease power
"""
                },
            ],
            max_tokens=10,
        )

        return response.choices[0].message.content.strip().lower()

    except Exception as e:
        print(f"LLM error: {e}", flush=True)
        return None


# 🚀 MAIN TASK
def run_task(task_id: str) -> float:
    task_cfg: Dict = TASKS[task_id]
    env = EVChargingEnvironment(task_name=task_cfg["task_name"])

    print(f"[START] task={task_id}", flush=True)

    obs, rew = env.reset()

    rewards = []
    step_count = 0

    actions = get_all_actions()
    action_scores = [0.0] * len(actions)

    while not rew.done:
        step_count += 1

        # 🧠 GET LLM HINT
        hint = get_llm_hint(obs)

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

                # 🎯 HEURISTICS
                score += utilization * 8
                score += charging * 0.5
                score -= queue * 0.3
                score -= wait * 0.002

                target = 0.65
                score -= abs(utilization - target) * 5

                if overload > 0:
                    score -= 50

                score += action_scores[i] * 0.1

                # 🔥 APPLY LLM HINT
                if hint:
                    if "increase price" in hint and action.price_level > 0:
                        score += 2
                    if "decrease price" in hint and action.price_level < 2:
                        score += 2
                    if "increase power" in hint and action.power_mode == 1:
                        score += 2
                    if "decrease power" in hint and action.power_mode == 0:
                        score += 2

                if score > best_score:
                    best_score = score
                    best_action = action
                    best_idx = i

        # ✅ APPLY ACTION
        obs, rew = env.step(best_action)
        rewards.append(rew.value)

        print(f"[STEP] step={step_count} reward={rew.value}", flush=True)

        # 🧠 LEARNING
        action_scores[best_idx] += rew.value

        for i in range(len(action_scores)):
            if i != best_idx:
                action_scores[i] *= 0.95

    # 📊 FINAL SCORE
    mean_reward = float(sum(rewards) / len(rewards)) if rewards else 0.0
    normalized = (mean_reward + 1.5) / 1.5

    print(
        f"[END] task={task_id} score={normalized:.4f} steps={step_count}",
        flush=True,
    )

    return normalized


# 🧠 MAIN
def main():
    print(f"API_BASE_URL={API_BASE_URL}")
    print(f"MODEL_NAME={MODEL_NAME}")
    print(f"API_KEY set={bool(API_KEY)}")

    for task_id in TASKS.keys():
        run_task(task_id)


if __name__ == "__main__":
    main()