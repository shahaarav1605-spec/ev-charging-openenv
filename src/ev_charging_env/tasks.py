from __future__ import annotations
from typing import Dict, Callable

from .server.environment import EVChargingEnvironment
from .models import StationAction, StationReward


# Type aliases for clarity
GraderFn = Callable[[EVChargingEnvironment], float]


def _run_episode_fixed_policy(env: EVChargingEnvironment, price_level: int, power_mode: int) -> float:
    """Run one episode with a fixed discrete policy; return mean reward."""

    obs, rew = env.reset()
    rewards = []
    done = False

    while not done:
        action = StationAction(price_level=price_level, power_mode=power_mode)
        obs, rew = env.step(action)
        rewards.append(rew.value)
        done = rew.done

    if not rewards:
        return 0.0

    return float(sum(rewards) / len(rewards))


def grader_easy(env: EVChargingEnvironment) -> float:
    """
    Easy task:
    - Environment created with task_name='easy'
    - Baseline: medium price, normal power
    - Score is normalized mean reward, squashed to [0,1]
    """
    mean_reward = _run_episode_fixed_policy(env, price_level=1, power_mode=1)
    # assume good policy has mean_reward around 0.8, bad around -0.5
    score = (mean_reward + 0.5) / 1.3
    return float(max(0.0, min(1.0, score)))


def grader_medium(env: EVChargingEnvironment) -> float:
    """
    Medium task:
    - task_name='medium'
    - Slightly more demand + tighter grid.
    - We encourage more careful power choice: eco during peaks.
    """
    mean_reward = _run_episode_fixed_policy(env, price_level=1, power_mode=0)
    score = (mean_reward + 0.5) / 1.3
    return float(max(0.0, min(1.0, score)))


def grader_hard(env: EVChargingEnvironment) -> float:
    """
    Hard task:
    - task_name='hard'
    - Expect the agent (later) to adapt actions, but for baseline we just try eco with high price.
    """

    mean_reward = _run_episode_fixed_policy(env, price_level=2, power_mode=0)
    score = (mean_reward + 0.5) / 1.3
    return float(max(0.0, min(1.0, score)))


TASKS: Dict[str, Dict] = {
    "easy": {
        "description": "Single EV station, moderate demand, generous grid cap.",
        "grader": grader_easy,
        "task_name": "easy",
    },
    "medium": {
        "description": "Single station with strong peak demand and tighter grid cap.",
        "grader": grader_medium,
        "task_name": "medium",
    },
    "hard": {
        "description": "High demand and very tight grid cap; overload is costly.",
        "grader": grader_hard,
        "task_name": "hard",
    },
}