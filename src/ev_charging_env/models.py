from __future__ import annotations
from typing import List
from pydantic import BaseModel

from .simulation import StationState


class ChargerSummary(BaseModel):
    num_chargers: int
    num_charging: int
    queue_length: int


class StationObservation(BaseModel):
    """What the agent sees at each step."""

    step_idx: int
    time_of_day_fraction: float
    price_level: int             # 0,1,2
    power_mode: int              # 0,1,2
    num_chargers: int
    num_charging: int
    queue_length: int
    total_revenue: float
    total_wait_steps: int
    overload_events: int
    total_cars_served: int
    total_cars_lost: int


class StationAction(BaseModel):
    """Discrete actions chosen by the agent."""

    price_level: int  # 0 = low, 1 = medium, 2 = high
    power_mode: int   # 0 = eco, 1 = normal, 2 = max


class StationReward(BaseModel):
    """Reward plus useful breakdown for debugging."""

    value: float
    revenue: float
    wait_penalty: float
    overload_penalty: float
    done: bool


class EnvState(BaseModel):
    """Minimal environment metadata for OpenEnv state()."""

    episode_id: int
    step_idx: int


# Helper to convert internal StationState to Observation
def make_observation(
    st: StationState,
    time_of_day_fraction: float,
    price_level: int,
    power_mode: int,
) -> StationObservation:
    return StationObservation(
        step_idx=st.step_idx,
        time_of_day_fraction=time_of_day_fraction,
        price_level=price_level,
        power_mode=power_mode,
        num_chargers=4,
        num_charging=len(st.cars_charging),
        queue_length=len(st.queue),
        total_revenue=st.total_revenue,
        total_wait_steps=st.total_wait_steps,
        overload_events=st.overload_events,
        total_cars_served=st.total_cars_served,
        total_cars_lost=st.total_cars_lost,
    )