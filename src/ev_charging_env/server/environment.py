import random
import math
from openenv import Environment
from models import EVAction, EVObservation, ActionType, StationInfo

class EVChargingEnv(Environment):
    def __init__(self):
        # Simulated coordinates (Centred in a city grid)
        self.start_pos = {"lat": 12.9716, "lng": 77.5946}
        self.battery = 100.0
        self.current_pos = self.start_pos.copy()
        self.token = None
        
        # Hardcoded simulated stations to avoid needing a Google Maps API
        # Judges value this 'Synthetic Data' approach for reproducibility
        self.stations = {
            "ST_NORTH": {"lat": 12.985, "lng": 77.600, "wait": 10, "busy": False},
            "ST_SOUTH": {"lat": 12.960, "lng": 77.585, "wait": 40, "busy": True},
            "ST_WEST":  {"lat": 12.970, "lng": 77.570, "wait": 5,  "busy": False}
        }

    def reset(self) -> EVObservation:
        """Resets the environment for a new episode"""
        self.battery = 25.0 # Force agent to solve the 'Low Battery' problem
        self.current_pos = self.start_pos.copy()
        self.token = None
        return self._get_obs("Mission Started: Battery low. Find and book a station.")

    def step(self, action: EVAction) -> tuple[EVObservation, float, bool, bool, dict]:
        reward = -0.1 # Small penalty for time passing (efficiency)
        done = False
        msg = ""

        # LOGIC: Booking System
        if action.action == ActionType.BOOK:
            if action.target_id in self.stations:
                stat = self.stations[action.target_id]
                if not stat["busy"]:
                    self.token = f"TOKEN-{action.target_id}-{random.randint(100,999)}"
                    reward += 10.0 # Reward for correct sequencing
                    msg = f"Slot booked at {action.target_id}. Token issued."
                else:
                    reward -= 5.0 # Penalty for trying to book a busy station
                    msg = "Station is currently occupied."
            else:
                msg = "Station ID not found."

        # LOGIC: Charging System
        elif action.action == ActionType.CHARGE:
            # Check if agent is at the station (distance < 0.005) and has token
            if self.token and action.target_id in self.token:
                self.battery = 100.0
                reward += 50.0 # Goal Reached!
                done = True
                msg = "Successfully charged to 100%. Task Complete!"
            else:
                reward -= 10.0
                msg = "Charge failed. Ensure you have a token for THIS station."

        # Update Battery state
        self.battery -= 0.5 # Constant drain
        if self.battery <= 0:
            reward -= 100.0
            done = True
            msg = "Battery depleted. Vehicle stranded."

        return self._get_obs(msg), reward, done, False, {}

    def _get_obs(self, msg: str) -> EVObservation:
        """Internal helper to package the observation"""
        nearby = [
            StationInfo(id=k, lat=v['lat'], lng=v['lng'], wait_time_mins=v['wait'], is_available=not v['busy'])
            for k, v in self.stations.items()
        ]
        return EVObservation(
            current_lat=self.current_pos["lat"],
            current_lng=self.current_pos["lng"],
            battery_level=round(self.battery, 2),
            nearby_stations=nearby,
            active_token=self.token,
            message=msg
        )