from .models import Agent


DEFAULT_CATEGORY_MAP = {
    "water": "Water Department",
    "electricity": "Electricity Department",
    "road": "Municipal Department",
    "other": "General Support",
}


DEMO_COMPLAINTS = [
    {
        "text": "Water leakage near my house",
        "category": "water",
        "priority": 3,
    },
    {
        "text": "Power cut in my area",
        "category": "electricity",
        "priority": 5,
    },
    {
        "text": "Low water pressure in lane 4",
        "category": "water",
        "priority": 1,
    },
]


def build_default_agents() -> list[Agent]:
    return [
        Agent(id="A1", department="Water Department"),
        Agent(id="A2", department="Electricity Department"),
        Agent(id="A3", department="Municipal Department"),
        Agent(id="A4", department="General Support"),
    ]
