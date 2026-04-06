from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import math
import random


@dataclass
class Car:
    id: int
    required_kwh: float          # how much energy it needs
    remaining_kwh: float         # how much still to charge
    max_wait_steps: int          # patience in time steps
    waited_steps: int = 0        # how long it has waited so far


@dataclass
class StationConfig:
    num_chargers: int = 4
    step_minutes: int = 5        # simulation step size
    base_demand_rate: float = 0.4  # avg arrivals per step
    peak_multiplier: float = 2.0   # demand bump during peak
    power_per_charger_kw: float = 30.0
    grid_cap_kw: float = 100.0
    episode_steps: int = 288     # 24h * 60 / 5


@dataclass
class StationState:
    step_idx: int = 0
    cars_charging: List[Car] = field(default_factory=list)
    queue: List[Car] = field(default_factory=list)
    next_car_id: int = 0
    total_revenue: float = 0.0
    total_wait_steps: int = 0
    overload_events: int = 0
    total_cars_served: int = 0
    total_cars_lost: int = 0


class EVChargingSim:
    """
    Pure Python EV charging station simulator.
    - Discrete time steps
    - Simple queue + chargers
    - Stochastic arrivals
    """

    def __init__(self, config: StationConfig):
        self.config = config
        self.state = StationState()

    # --------- helpers ---------

    def _time_of_day_fraction(self) -> float:
        """Return value in [0,1) for time-of-day."""
        return (self.state.step_idx % self.config.episode_steps) / self.config.episode_steps

    def _arrival_rate_for_step(self) -> float:
        """Poisson rate depending on time of day."""
        t = self._time_of_day_fraction()
        # Morning + evening peaks, low at night
        peak = math.exp(-((t - 0.25) ** 2) / 0.01) + math.exp(-((t - 0.75) ** 2) / 0.01)
        return self.config.base_demand_rate * (1.0 + self.config.peak_multiplier * peak)

    def _sample_arrivals(self) -> List[Car]:
        lam = self._arrival_rate_for_step()
        # Poisson with small lambda: approximate with binomial
        count = 0
        p = min(lam, 0.9)
        for _ in range(5):
            if random.random() < p:
                count += 1
        arrivals = []
        for _ in range(count):
            required = random.uniform(10.0, 60.0)  # kWh
            max_wait = random.randint(6, 24)       # 6*5min = 30min to 2h
            car = Car(
                id=self.state.next_car_id,
                required_kwh=required,
                remaining_kwh=required,
                max_wait_steps=max_wait,
            )
            self.state.next_car_id += 1
            arrivals.append(car)
        return arrivals

    def _assign_cars_to_chargers(self):
        """Move cars from queue to free charger slots."""
        free_slots = self.config.num_chargers - len(self.state.cars_charging)
        if free_slots <= 0:
            return
        to_add = min(free_slots, len(self.state.queue))
        for _ in range(to_add):
            car = self.state.queue.pop(0)
            self.state.cars_charging.append(car)

    # --------- public API ---------

    def reset(self, seed: int | None = None) -> StationState:
        if seed is not None:
            random.seed(seed)
        self.state = StationState()
        return self.state

    def step(self, price_per_kwh: float, power_scale: float) -> tuple[StationState, float, bool]:
        """
        One simulation step.
        :param price_per_kwh: chosen price
        :param power_scale: between 0 and 1, scales charger power to respect grid cap
        :return: (state, reward, done)
        """
        cfg = self.config
        st = self.state

        # 1) Sample new arrivals and add to queue
        arrivals = self._sample_arrivals()
        st.queue.extend(arrivals)

        # 2) Update waiting times, drop impatient cars
        kept_queue: List[Car] = []
        for car in st.queue:
            car.waited_steps += 1
            if car.waited_steps > car.max_wait_steps:
                st.total_cars_lost += 1
            else:
                kept_queue.append(car)
                st.total_wait_steps += 1
        st.queue = kept_queue

        # 3) Assign cars to chargers
        self._assign_cars_to_chargers()

        # 4) Charge cars
        # power per charger
        charger_power = cfg.power_per_charger_kw * power_scale
        total_power = charger_power * len(st.cars_charging)

        overload = 0
        if total_power > cfg.grid_cap_kw:
            overload = 1
            st.overload_events += 1

        # energy delivered in this step
        hours = cfg.step_minutes / 60.0
        energy_this_step = charger_power * hours

        finished: List[Car] = []
        revenue = 0.0

        for car in st.cars_charging:
            delivered = min(energy_this_step, car.remaining_kwh)
            car.remaining_kwh -= delivered
            revenue += delivered * price_per_kwh
            if car.remaining_kwh <= 1e-3:
                finished.append(car)

        # remove finished cars
        st.cars_charging = [c for c in st.cars_charging if c not in finished]
        st.total_cars_served += len(finished)
        st.total_revenue += revenue

        # 5) Step index + done
        st.step_idx += 1
        done = st.step_idx >= cfg.episode_steps

        # 6) Define reward: revenue - penalties
        # normalize revenue and penalties
        revenue_term = revenue / 1000.0
        wait_penalty = (len(st.queue) * 0.02)
        overload_penalty = overload * 0.5

        reward = revenue_term - wait_penalty - overload_penalty

        return st, reward, done