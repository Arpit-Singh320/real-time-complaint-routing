import heapq
from collections import defaultdict
from itertools import count
from typing import Dict, List, Optional

from .models import Agent, Complaint, Event


class ComplaintRoutingService:
    def __init__(self, category_map: Dict[str, str], agents: List[Agent]) -> None:
        self.category_map = {
            category.strip().lower(): department
            for category, department in category_map.items()
        }
        self.fallback_department = self.category_map.get("other", "General Support")
        self.complaints: Dict[str, Complaint] = {}
        self.department_heaps: Dict[str, list[tuple[int, int, str]]] = defaultdict(list)
        self.agents_by_department: Dict[str, List[Agent]] = defaultdict(list)
        self._complaint_sequence = count(1)
        self._heap_sequence = count()

        for agent in agents:
            self.agents_by_department[agent.department].append(agent)

    def submit_complaint(self, text: str, category: str, priority: int) -> tuple[Complaint, List[Event]]:
        normalized_category = category.strip().lower()
        department = self.resolve_department(normalized_category)
        complaint_id = f"C{next(self._complaint_sequence)}"

        complaint = Complaint(
            id=complaint_id,
            text=text.strip(),
            category=normalized_category,
            priority=priority,
            department=department,
        )
        self.complaints[complaint.id] = complaint

        events = [
            Event(
                title="Step 1 - Complaint Received",
                lines=[
                    f"Complaint ID : {complaint.id}",
                    f"Text         : {complaint.text}",
                    f"Category     : {complaint.category}",
                    f"Priority     : {complaint.priority}",
                ],
            ),
            Event(
                title="Step 2 - Category Routing",
                lines=[
                    f"Input category  : {complaint.category}",
                    f"Mapped department: {department}",
                ],
            ),
        ]

        if normalized_category not in self.category_map:
            events[-1].lines.append(
                f"Unknown category routed to fallback department: {self.fallback_department}"
            )

        heapq.heappush(
            self.department_heaps[department],
            (-complaint.priority, next(self._heap_sequence), complaint.id),
        )

        queue_view = self.get_department_queue_view(department)
        events.append(
            Event(
                title="Step 3 - Department Heap Updated",
                lines=[
                    f"Complaint inserted into {department} heap.",
                    f"Waiting complaints in {department}: {len(queue_view)}",
                    "Queue order (highest priority first):",
                    *[self._format_queue_line(item) for item in queue_view],
                ],
            )
        )

        events.extend(self._attempt_assignment(department))
        return complaint, events

    def resolve_department(self, category: str) -> str:
        return self.category_map.get(category, self.fallback_department)

    def resolve_agent(self, agent_id: str) -> List[Event]:
        agent = self.find_agent(agent_id)
        if agent is None:
            return [
                Event(
                    title="Resolve Request",
                    lines=[f"Agent {agent_id} was not found."],
                )
            ]

        if agent.current_complaint_id is None:
            return [
                Event(
                    title="Resolve Request",
                    lines=[
                        f"Agent {agent.id} is already free.",
                        f"Department: {agent.department}",
                    ],
                )
            ]

        complaint = self.complaints[agent.current_complaint_id]
        complaint.status = "resolved"
        agent.current_complaint_id = None
        agent.available = True

        events = [
            Event(
                title="Resolution Completed",
                lines=[
                    f"Agent {agent.id} resolved complaint {complaint.id}.",
                    f"Complaint status: {complaint.status}",
                    f"Department      : {agent.department}",
                    "Agent is available again.",
                ],
            )
        ]
        events.extend(self._attempt_assignment(agent.department))
        return events

    def find_agent(self, agent_id: str) -> Optional[Agent]:
        for agents in self.agents_by_department.values():
            for agent in agents:
                if agent.id.lower() == agent_id.lower():
                    return agent
        return None

    def get_department_queue_view(self, department: str) -> List[Complaint]:
        heap_items = sorted(self.department_heaps.get(department, []))
        return [self.complaints[complaint_id] for _, _, complaint_id in heap_items]

    def get_snapshot(self) -> dict:
        departments = {}
        all_departments = set(self.agents_by_department.keys()) | set(self.department_heaps.keys())

        for department in sorted(all_departments):
            departments[department] = [
                {
                    "id": complaint.id,
                    "priority": complaint.priority,
                    "status": complaint.status,
                    "text": complaint.text,
                }
                for complaint in self.get_department_queue_view(department)
            ]

        agents = {}
        for department in sorted(self.agents_by_department.keys()):
            agents[department] = [
                {
                    "id": agent.id,
                    "available": agent.available,
                    "current_complaint_id": agent.current_complaint_id,
                }
                for agent in self.agents_by_department[department]
            ]

        totals = {
            "complaints": len(self.complaints),
            "waiting": sum(len(queue) for queue in self.department_heaps.values()),
            "assigned": sum(
                1 for complaint in self.complaints.values() if complaint.status == "assigned"
            ),
            "resolved": sum(
                1 for complaint in self.complaints.values() if complaint.status == "resolved"
            ),
        }

        return {
            "flow": "Complaint -> Category Mapping -> Department Heap -> Available Agent -> Assignment",
            "departments": departments,
            "agents": agents,
            "totals": totals,
        }

    def _attempt_assignment(self, department: str) -> List[Event]:
        queue = self.department_heaps[department]
        available_agent = self._find_available_agent(department)

        check_lines = [
            f"Department checked: {department}",
            f"Waiting complaints: {len(queue)}",
        ]
        check_lines.append(
            f"Available agent found: {available_agent.id}" if available_agent else "Available agent found: None"
        )

        events = [Event(title="Step 4 - Agent Availability Check", lines=check_lines)]

        if not queue:
            events.append(
                Event(
                    title="Step 5 - No Assignment Needed",
                    lines=[f"No complaint is waiting in {department}."],
                )
            )
            return events

        if available_agent is None:
            top_complaint = self.complaints[sorted(queue)[0][2]]
            events.append(
                Event(
                    title="Step 5 - Complaint Waiting",
                    lines=[
                        f"Top complaint still waiting: {top_complaint.id}",
                        f"Reason: no free agent in {department}",
                    ],
                )
            )
            return events

        _, _, complaint_id = heapq.heappop(queue)
        complaint = self.complaints[complaint_id]
        complaint.status = "assigned"
        complaint.assigned_agent_id = available_agent.id
        available_agent.available = False
        available_agent.current_complaint_id = complaint.id

        events.append(
            Event(
                title="Step 5 - Complaint Assigned",
                lines=[
                    f"Assigned complaint: {complaint.id}",
                    f"Assigned agent    : {available_agent.id}",
                    f"Department        : {department}",
                    f"Remaining waiting : {len(queue)}",
                ],
            )
        )
        return events

    def _find_available_agent(self, department: str) -> Optional[Agent]:
        for agent in self.agents_by_department.get(department, []):
            if agent.available:
                return agent
        return None

    def _format_queue_line(self, complaint: Complaint) -> str:
        return f"- {complaint.id} | priority={complaint.priority} | status={complaint.status} | text={complaint.text}"
