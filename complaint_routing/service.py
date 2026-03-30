"""Core complaint routing service."""

import heapq
from itertools import count
from typing import Dict, List, Tuple

from .models import Agent, Complaint, Event


class ComplaintRoutingService:
    """Route complaints by department and assign one agent per department."""

    def __init__(self):
        self.departments = [
            "Water Department",
            "Electricity Department",
            "Municipal Department",
            "General Support",
        ]
        self.category_map = {
            "water": "Water Department",
            "electricity": "Electricity Department",
            "road": "Municipal Department",
            "other": "General Support",
        }
        self.agents_by_department: Dict[str, Agent] = {
            "Water Department": Agent(id="A1", department="Water Department"),
            "Electricity Department": Agent(id="A2", department="Electricity Department"),
            "Municipal Department": Agent(id="A3", department="Municipal Department"),
            "General Support": Agent(id="A4", department="General Support"),
        }
        self.agents_by_id: Dict[str, Agent] = {
            agent.id: agent for agent in self.agents_by_department.values()
        }
        self.complaints: Dict[str, Complaint] = {}
        self.department_queues: Dict[str, List[Tuple[int, int, str]]] = {
            department: [] for department in self.departments
        }
        self.complaint_counter = count(1)
        self.queue_counter = count()

    def submit_complaint(self, text: str, category: str, priority: int) -> Tuple[Complaint, List[Event]]:
        normalized_category = category.strip().lower() if category.strip() else "other"
        department = self.category_map.get(normalized_category, "General Support")
        normalized_priority = max(1, min(5, priority))
        complaint = Complaint(
            id=f"C{next(self.complaint_counter)}",
            text=text.strip(),
            category=normalized_category,
            priority=normalized_priority,
            department=department,
        )
        self.complaints[complaint.id] = complaint
        heapq.heappush(
            self.department_queues[department],
            (-complaint.priority, next(self.queue_counter), complaint.id),
        )

        events = [
            Event(
                title="Complaint Received",
                lines=[
                    f"ID: {complaint.id}",
                    f"Text: {complaint.text}",
                    f"Category: {complaint.category}",
                    f"Department: {department}",
                    f"Priority: {complaint.priority}",
                ],
            )
        ]
        assignment_event = self._assign_next_complaint(department)
        if assignment_event is not None:
            events.append(assignment_event)
        else:
            events.append(
                Event(
                    title="Complaint Waiting",
                    lines=[f"No free agent in {department}. Complaint is waiting in the queue."],
                )
            )
        return complaint, events

    def resolve_agent(self, agent_id: str) -> List[Event]:
        normalized_agent_id = agent_id.strip().upper()
        agent = self.agents_by_id.get(normalized_agent_id)
        if agent is None:
            return [Event(title="Error", lines=[f"Agent {normalized_agent_id} does not exist."])]
        if agent.current_complaint_id is None:
            return [Event(title="Error", lines=[f"Agent {normalized_agent_id} is already free."])]

        complaint = self.complaints[agent.current_complaint_id]
        complaint.status = "resolved"
        agent.current_complaint_id = None
        agent.available = True

        events = [
            Event(
                title="Complaint Resolved",
                lines=[
                    f"Resolved complaint: {complaint.id}",
                    f"Agent: {agent.id}",
                    f"Department: {agent.department}",
                ],
            )
        ]
        assignment_event = self._assign_next_complaint(agent.department)
        if assignment_event is not None:
            events.append(assignment_event)
        else:
            events.append(
                Event(
                    title="No Waiting Complaint",
                    lines=[f"No complaint is waiting in {agent.department}."],
                )
            )
        return events

    def _assign_next_complaint(self, department: str):
        agent = self.agents_by_department[department]
        if not agent.available:
            return None
        queue = self.department_queues[department]
        if not queue:
            return None

        _, _, complaint_id = heapq.heappop(queue)
        complaint = self.complaints[complaint_id]
        complaint.status = "assigned"
        complaint.assigned_agent_id = agent.id
        agent.available = False
        agent.current_complaint_id = complaint.id

        return Event(
            title="Complaint Assigned",
            lines=[
                f"Assigned complaint: {complaint.id}",
                f"Assigned agent: {agent.id}",
                f"Department: {department}",
            ],
        )

    def get_status(self) -> dict:
        return {
            "complaints": {
                "total": len(self.complaints),
                "waiting": sum(1 for complaint in self.complaints.values() if complaint.status == "waiting"),
                "assigned": sum(1 for complaint in self.complaints.values() if complaint.status == "assigned"),
                "resolved": sum(1 for complaint in self.complaints.values() if complaint.status == "resolved"),
            },
            "departments": {
                department: [
                    f"{self.complaints[complaint_id].id} (priority={self.complaints[complaint_id].priority})"
                    for _, _, complaint_id in sorted(self.department_queues[department])
                ]
                for department in self.departments
            },
            "agents": {
                agent.id: {
                    "department": agent.department,
                    "status": "FREE" if agent.available else f"BUSY ({agent.current_complaint_id})",
                }
                for agent in self.agents_by_department.values()
            },
        }
