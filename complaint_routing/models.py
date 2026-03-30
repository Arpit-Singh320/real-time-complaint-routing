"""
Core data models for the complaint routing system.
Simple, clean dataclasses with minimal complexity.
"""

from dataclasses import dataclass
from typing import Optional, List


@dataclass
class Complaint:
    """Represents a citizen complaint."""
    id: str
    text: str
    category: str
    priority: int
    department: str
    status: str = "waiting"
    assigned_agent_id: Optional[str] = None


@dataclass
class Agent:
    """Represents a department agent."""
    id: str
    department: str
    available: bool = True
    current_complaint_id: Optional[str] = None


@dataclass
class Event:
    """Represents a system event for logging."""
    title: str
    lines: List[str] = None

    def __post_init__(self):
        if self.lines is None:
            self.lines = []
