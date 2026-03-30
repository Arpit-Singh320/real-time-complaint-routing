# Real-Time Complaint Routing Service

This is a small terminal-based Python project for routing complaints to the correct department and assigning them to one department agent.

## Core flow

```text
Submit complaint
-> map category to department
-> push complaint into that department queue
-> assign immediately if the department agent is free
-> otherwise keep it waiting in the queue
-> explicitly resolve the agent when work is done
-> auto-assign the next waiting complaint in that same department
```

## What the project does

- receives a complaint with `text`, `category`, and `priority`
- maps the category to one department
- keeps a separate priority queue for each department
- assigns the complaint immediately if that department's agent is free
- keeps the complaint waiting if the agent is busy
- frees the agent only when you explicitly resolve that agent
- auto-assigns the next complaint from the same department queue after resolution

## Main data structures used

| Data structure | Exact variable | File | Purpose |
| --- | --- | --- | --- |
| Dictionary / HashMap | `self.category_map` | `complaint_routing/service.py` | category to department lookup |
| Dictionary | `self.complaints` | `complaint_routing/service.py` | stores complaints by ID |
| Dictionary of heaps | `self.department_queues` | `complaint_routing/service.py` | stores one priority queue per department |
| Heap tuple | `(-priority, order, complaint_id)` | `complaint_routing/service.py` | keeps higher-priority complaints first |
| Dictionary | `self.agents_by_department` | `complaint_routing/service.py` | stores one agent for each department |
| Dictionary | `self.agents_by_id` | `complaint_routing/service.py` | direct agent lookup by agent ID |
| List | `Event.lines` | `complaint_routing/models.py` | stores terminal output lines |

## Important design rule

This project uses one priority queue per department.

In this codebase:

- `department queue`
- `department heap`
- `priority queue`

all refer to the same per-department waiting structure.

There is no global queue and no timer-based processing.

## Project structure

```text
real-time-complaint-routing/
├── app.py
├── README.md
├── complaint_routing/
│   ├── __init__.py
│   ├── models.py
│   └── service.py
└── docs/
    ├── 01_system_overview.md
    ├── 02_data_structures_and_design.md
    ├── 03_step_by_step_flow.md
    ├── 04_implementation_plan.md
    ├── 05_complexity_and_edge_cases.md
    ├── 06_viva_qa.md
    ├── 07_file_and_function_guide.md
    ├── 08_clean_modular_design.md
    └── 09_final_summary.md
```

## How to run

```bash
python3 app.py
```

## Menu options in the terminal app

- submit complaint
- resolve agent complaint
- view current system state
- exit

## Best file to understand the core logic

Start with:

`complaint_routing/service.py`

That file contains the category mapping, queue handling, immediate assignment, explicit agent resolution, and auto-assignment logic.
