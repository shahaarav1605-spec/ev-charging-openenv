from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Dict, Tuple

import requests


@dataclass
class OpenEnvClient:
    base_url: str

    def reset(self, task_id: str) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """Reset the environment for a given task_id."""
        resp = requests.post(f"{self.base_url}/reset", json={"task_id": task_id})
        resp.raise_for_status()
        data = resp.json()
        return data["observation"], data["reward"]

    def step(self, action: Dict[str, Any]) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """Send one action to the environment."""
        resp = requests.post(f"{self.base_url}/step", json={"action": action})
        resp.raise_for_status()
        data = resp.json()
        return data["observation"], data["reward"]

    def state(self) -> Dict[str, Any]:
        """Get current environment state."""
        resp = requests.get(f"{self.base_url}/state")
        resp.raise_for_status()
        return resp.json()