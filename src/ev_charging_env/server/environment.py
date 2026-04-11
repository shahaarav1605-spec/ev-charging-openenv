from __future__ import annotations
from typing import Tuple

from ..simulation import EVChargingSim, StationConfig
from ..models import (
    StationAction,
    StationObservation,
    StationReward,
    EnvState,
    make_observation,
)


class EVChargingEnvironment:
    """
    OpenEnv-compatible environment for a smart EV charging station.
    """

    def __init__(self, task_name: str = "easy"):
        self.task_name = task_name
        self.episode_id = 0

        if task_name == "easy":
            cfg = StationConfig(
                num_chargers=4,
                base_demand_rate=0.3,
                peak_multiplier=1.5,
                grid_cap_kw=120.0,
            )
        elif task_name == "medium":
            cfg = StationConfig(
                num_chargers=4,
                base_demand_rate=0.4,
                peak_multiplier=2.0,
                grid_cap_kw=100.0,
            )
        elif task_name == "hard":
            cfg = StationConfig(
                num_chargers=4,
                base_demand_rate=0.5,
                peak_multiplier=2.5,
                grid_cap_kw=90.0,
            )
        else:
            raise ValueError(f"Unknown task_name: {task_name}")

        self.config = cfg
        self.sim = EVChargingSim(cfg)

        # last action (for observation)
        self._price_level = 1
        self._power_mode = 1

    # -------- OpenEnv API --------

    def reset(self) -> Tuple[StationObservation, StationReward]:
        """Start a new episode."""
        self.episode_id += 1
        st = self.sim.reset()
        self._price_level = 1
        self._power_mode = 1

        obs = make_observation(
            st,
            time_of_day_fraction=self.sim._time_of_day_fraction(),
            price_level=self._price_level,
            power_mode=self._power_mode,
        )
        rew = StationReward(
            value=0.0,
            revenue=0.0,
            wait_penalty=0.0,
            overload_penalty=0.0,
            done=False,
        )
        return obs, rew

    def step(self, action: StationAction) -> Tuple[StationObservation, StationReward]:
        """Apply action and advance the simulation by one step."""

        # map discrete levels to real values
        price_map = {0: 6.0, 1: 9.0, 2: 14.0}  # rupees per kWh, for example
        power_scale_map = {0: 0.6, 1: 0.9, 2: 1.1}

        self._price_level = int(action.price_level)
        self._power_mode = int(action.power_mode)

        price = price_map.get(self._price_level, 9.0)
        power_scale = power_scale_map.get(self._power_mode, 0.9)

        st, reward_value, done = self.sim.step(price_per_kwh=price, power_scale=power_scale)

        # reconstruct reward breakdown to help graders
        revenue_term = reward_value  # here we just expose value; adjust if you want breakdown
        wait_penalty = 0.0  # not split out for now
        overload_penalty = 0.0

        obs = make_observation(
            st,
            time_of_day_fraction=self.sim._time_of_day_fraction(),
            price_level=self._price_level,
            power_mode=self._power_mode,
        )

        rew = StationReward(
            value=reward_value,
            revenue=revenue_term,
            wait_penalty=wait_penalty,
            overload_penalty=overload_penalty,
            done=done,
        )

        return obs, rew

    def state(self) -> EnvState:
        """Return basic metadata for OpenEnv."""
        return EnvState(
            episode_id=self.episode_id,
            step_idx=self.sim.state.step_idx,
        )