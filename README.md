# Real-Time Complaint Routing Service

This is a small terminal-based Python project that shows how a complaint moves through a system.

The project is built around one simple flow:

```text
Complaint -> Category Mapping -> Department Heap -> Available Agent -> Assignment
```

## What this project shows

- a complaint comes in
- the category is mapped to a department
- the complaint is stored in that department's priority queue
- the system checks if an agent is free
- the complaint is assigned if possible
- if no agent is free, the complaint waits in the heap

## Main data structures used

| Data structure | Exact variable | File | Where it is used |
| --- | --- | --- | --- |
| Dictionary / HashMap | `DEFAULT_CATEGORY_MAP` | `complaint_routing/sample_data.py` | Stores basic category to department mapping |
| Dictionary / HashMap | `self.category_map` | `complaint_routing/service.py` | Used in `resolve_department()` for fast routing |
| Dictionary | `self.complaints` | `complaint_routing/service.py` | Stores every complaint by ID |
| Dictionary of heaps | `self.department_heaps` | `complaint_routing/service.py` | Stores one heap for each department |
| Heap | each value inside `self.department_heaps` | `complaint_routing/service.py` | Used with `heapq.heappush()` and `heapq.heappop()` |
| Dictionary of lists | `self.agents_by_department` | `complaint_routing/service.py` | Groups agents by department |
| List | `DEMO_COMPLAINTS` | `complaint_routing/sample_data.py` | Guided demo input |
| List | `lines` in `Event` | `complaint_routing/models.py` | Stores text shown in the terminal boxes |

## Important design rule

This project does **not** use priority twice.

It uses:

- one category mapping step
- one heap per department

So in this project:

- `department queue`
- `department heap`
- `priority queue`

all mean the same thing.

There is no separate global priority queue.

## Project structure

```text
DSA_Project/
├── app.py
├── README.md
├── complaint_routing/
│   ├── __init__.py
│   ├── models.py
│   ├── sample_data.py
│   ├── service.py
│   └── visuals.py
└── docs/
    ├── 01_system_overview.md
    ├── 02_data_structures_and_design.md
    ├── 03_step_by_step_flow.md
    ├── 04_implementation_plan.md
    ├── 05_complexity_and_edge_cases.md
    ├── 06_viva_qa.md
    └── 07_file_and_function_guide.md
```

## How to run

```bash
python3 app.py
```

## Menu options in the terminal app

- run guided demo
- submit custom complaint
- resolve agent complaint
- view current system state
- reset system

## Best way to study this project

1. `docs/01_system_overview.md`
2. `docs/02_data_structures_and_design.md`
3. `docs/03_step_by_step_flow.md`
4. `docs/04_implementation_plan.md`
5. `docs/05_complexity_and_edge_cases.md`
6. `docs/06_viva_qa.md`
7. `docs/07_file_and_function_guide.md`

## Best file to understand the core logic

If you want to understand the main working first, read:

`complaint_routing/service.py`

That file contains the full routing, heap management, assignment, and resolution logic.
