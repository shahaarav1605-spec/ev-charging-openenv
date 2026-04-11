from pydantic import BaseModel
from typing import List, Optional
from enum import Enum

class ActionType(str, Enum):
    MOVE = "move"
    BOOK = "book"
    CHARGE = "charge"
    WAIT = "wait"

class StationInfo(BaseModel):
    id: str
    lat: float
    lng: float
    wait_time_mins: int
    is_available: bool

class EVAction(BaseModel):
    action: ActionType
    target_id: Optional[str] = None 

class EVObservation(BaseModel):
    current_lat: float
    current_lng: float
    battery_level: float
    nearby_stations: List[StationInfo]
    active_token: Optional[str] = None
    message: str

    class Config:
        arbitrary_types_allowed = True