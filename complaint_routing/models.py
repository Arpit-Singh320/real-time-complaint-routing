from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Complaint:
    id: str
    text: str
    category: str
    priority: int
    department: str
    status: str = "waiting"
    assigned_agent_id: Optional[str] = None


@dataclass
class Agent:
    id: str
    department: str
    available: bool = True
    current_complaint_id: Optional[str] = None


@dataclass
class Event:
    title: str
    lines: List[str] = field(default_factory=list)
