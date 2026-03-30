# 08. Clean Modular Design

## Overview

The current project keeps only the real routing flow:

- submit complaint
- map category to department
- put complaint in that department queue
- assign immediately if the agent is free
- otherwise keep it waiting
- explicitly resolve the agent
- auto-assign the next complaint in that department

## Official files

```text
app.py
complaint_routing/models.py
complaint_routing/service.py
```

## What makes the design clean

### Models are small

`models.py` only contains:

- `Complaint`
- `Agent`
- `Event`

### Service owns the state

`service.py` stores:

- category mapping
- agents by department
- agents by ID
- complaints by ID
- one heap queue per department

### App only handles interaction

`app.py` only handles:

- menu input
- printing event boxes
- calling service methods
- showing status

## Core methods

### `submit_complaint()`

Creates the complaint, pushes it into the right department queue, and tries immediate assignment.

### `resolve_agent()`

Frees the selected agent and then tries to assign the next complaint from that same department queue.

### `_assign_next_complaint()`

Assigns the highest-priority waiting complaint if the department agent is free.

### `get_status()`

Builds a simple snapshot for the terminal UI.

## Why this is better than the earlier version

- no duplicate implementations
- no guided demo
- no timer logic
- no unused helper files
- no unnecessary agent-search loops
- one clear path through the code

## Performance

- category lookup: O(1)
- agent lookup by ID: O(1)
- queue push: O(log n)
- queue pop: O(log n)

The design is minimal, readable, and directly matches the intended complaint flow.
