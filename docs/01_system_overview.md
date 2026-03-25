# 01. System Overview

## Project idea

This project shows how a complaint can move through a simple system in the terminal.

The system does five main things:

- receives a complaint
- finds the correct department
- stores the complaint in that department's priority queue
- checks for a free agent
- assigns the complaint if possible

## Main flow

```text
Complaint -> Category Mapping -> Department Heap -> Available Agent -> Assignment
```

## Where the main logic is written

### `app.py`

This is the entry point.

It handles:

- menu input
- guided demo
- custom complaint input
- calling the service methods
- showing output in the terminal

### `complaint_routing/service.py`

This is the main logic file.

It handles:

- category routing
- complaint creation
- heap insertion
- agent checking
- complaint assignment
- complaint resolution
- system snapshot creation

### `complaint_routing/models.py`

This file defines the basic objects used by the system:

- `Complaint`
- `Agent`
- `Event`

### `complaint_routing/sample_data.py`

This file stores:

- `DEFAULT_CATEGORY_MAP`
- `DEMO_COMPLAINTS`
- `build_default_agents()`

### `complaint_routing/visuals.py`

This file prints the boxes, header, menu, notes, and system state in the terminal.

## Exact place where each data structure lives

| Data structure | Exact name | File |
| --- | --- | --- |
| Dictionary / HashMap | `DEFAULT_CATEGORY_MAP` | `complaint_routing/sample_data.py` |
| Dictionary / HashMap | `self.category_map` | `complaint_routing/service.py` |
| Dictionary | `self.complaints` | `complaint_routing/service.py` |
| Dictionary of heaps | `self.department_heaps` | `complaint_routing/service.py` |
| Dictionary of lists | `self.agents_by_department` | `complaint_routing/service.py` |
| Heap items | `(-complaint.priority, sequence, complaint.id)` | `complaint_routing/service.py` |
| List | `DEMO_COMPLAINTS` | `complaint_routing/sample_data.py` |
| List | `Event.lines` | `complaint_routing/models.py` |

## Why this design is simple

This project does not use:

- database
- web framework
- threads
- sockets
- global priority queue

That keeps the project easy to understand.

## Important rule in this project

Priority is handled only once.

It happens inside the department heap.

So if someone says `department queue`, in this project that means the same thing as the department heap.

## What makes it a DSA project

This project is based on choosing the right data structure for the right job:

- dictionary for fast routing
- heap for priority order
- list for agent grouping and display
- dictionary for fast complaint lookup
