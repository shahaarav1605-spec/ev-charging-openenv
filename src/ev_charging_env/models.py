from pydantic import BaseModel
from typing import List, Optional
from enum import Enum

# Using Enums makes the agent's decision-making process strict and less error-prone
class ActionType(str, Enum):
    MOVE = "move"     # Navigate to a coordinate
    BOOK = "book"     # Reserve a slot at a station
    CHARGE = "charge" # Begin the charging process
    WAIT = "wait"     # Wait at the current location to reduce wait_time_mins

class StationInfo(BaseModel):
    """Metadata for charging stations visible to the agent"""
    id: str
    lat: float
    lng: float
    wait_time_mins: int  # Current congestion at the station
    is_available: bool

class EVAction(BaseModel):
    """The action schema the agent must follow"""
    action: ActionType
    target_id: Optional[str] = None 

class EVObservation(BaseModel):
    """What the agent 'sees' at every step"""
    current_lat: float
    current_lng: float
    battery_level: float
    nearby_stations: List[StationInfo]
    active_token: Optional[str] = None # Received after successful booking
    message: str