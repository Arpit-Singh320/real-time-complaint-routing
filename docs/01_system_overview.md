# 01. System Overview

## Project idea

This project shows a simple terminal-based complaint routing system.

Each complaint is routed to one department, placed in that department's priority queue, and assigned to the department's single agent if the agent is free.

## Main flow

```text
Complaint -> Category Mapping -> Department Queue -> Agent Assignment
                                      |
                                      -> waits if agent is busy

Resolve Agent -> Agent becomes free -> Next waiting complaint auto-assigns
```

## Main files

### `app.py`

This is the entry point.

It handles:

- menu input
- complaint submission input
- agent resolution input
- status display
- printing event boxes

### `complaint_routing/service.py`

This is the main logic file.

It handles:

- category-to-department routing
- complaint creation
- priority queue insertion
- immediate assignment if the agent is free
- explicit agent resolution
- auto-assignment of the next waiting complaint
- system status generation

### `complaint_routing/models.py`

This file defines the core data objects:

- `Complaint`
- `Agent`
- `Event`

## Exact place where each data structure lives

| Data structure | Exact name | File |
| --- | --- | --- |
| Dictionary / HashMap | `self.category_map` | `complaint_routing/service.py` |
| Dictionary | `self.complaints` | `complaint_routing/service.py` |
| Dictionary of heaps | `self.department_queues` | `complaint_routing/service.py` |
| Heap items | `(-complaint.priority, order, complaint.id)` | `complaint_routing/service.py` |
| Dictionary | `self.agents_by_department` | `complaint_routing/service.py` |
| Dictionary | `self.agents_by_id` | `complaint_routing/service.py` |
| List | `Event.lines` | `complaint_routing/models.py` |

## Why this design is simple

This project does not use:

- a database
- a web framework
- background timers
- threads
- sockets
- a global queue

That keeps the project easy to read and explain.

## Important rule in this project

Priority is handled only once, inside each department queue.

So in this project:

- `department queue`
- `department heap`
- `priority queue`

all mean the same waiting structure for one department.

## What makes it a DSA project

This project uses:

- a dictionary for routing
- a heap for priority ordering
- a dictionary for complaint lookup
- dictionaries for fast agent access
