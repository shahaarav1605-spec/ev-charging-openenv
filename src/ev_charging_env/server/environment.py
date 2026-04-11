import random
from openenv import Environment
from models import EVAction, EVObservation, ActionType, StationInfo


class EVChargingEnv(Environment):
    def __init__(self):
        self.start_pos = {"lat": 12.9716, "lng": 77.5946}
        self.battery = 100.0
        self.current_pos = self.start_pos.copy()
        self.token = None
        self.stations = {
            "ST_NORTH": {"lat": 12.985, "lng": 77.600, "wait": 10, "busy": False},
            "ST_WEST":  {"lat": 12.970, "lng": 77.570, "wait": 5,  "busy": False}
        }

    def reset(self) -> EVObservation:
        self.battery = 25.0
        self.token = None
        return self._get_obs("Mission Started: Find and book a station.")

    def step(self, action: EVAction) -> tuple[EVObservation, float, bool, bool, dict]:
        reward = -0.1
        done = False
        msg = "Moving..."

        if action.action == ActionType.BOOK:
            if action.target_id in self.stations and not self.stations[action.target_id]["busy"]:
                self.token = f"TOKEN-{action.target_id}-{random.randint(100,999)}"
                reward += 10.0
                msg = f"Booked! Token: {self.token}"
        
        elif action.action == ActionType.CHARGE:
            if self.token and action.target_id in self.token:
                self.battery = 100.0
                reward += 50.0
                done = True
                msg = "Charged successfully!"

        self.battery -= 0.5
        if self.battery <= 0:
            reward -= 100.0
            done = True
            msg = "Battery dead."

        return self._get_obs(msg), reward, done, False, {}

    def _get_obs(self, msg: str) -> EVObservation:
        nearby = [StationInfo(id=k, **v, is_available=not v['busy']) for k, v in self.stations.items()]
        return EVObservation(current_lat=self.current_pos["lat"], current_lng=self.current_pos["lng"], 
                             battery_level=round(self.battery, 2), nearby_stations=nearby, 
                             active_token=self.token, message=msg)