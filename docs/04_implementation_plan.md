# 04. Implementation Plan

## Current file split

The project is intentionally small.

### `app.py`

This file is the terminal entry point.

It handles:

- menu input
- collecting complaint details
- collecting agent ID for resolution
- showing events and status

### `complaint_routing/models.py`

This file holds the shared data objects:

- `Complaint`
- `Agent`
- `Event`

### `complaint_routing/service.py`

This file contains the full routing logic.

It handles:

- category mapping
- complaint creation
- queue insertion
- immediate assignment
- explicit agent resolution
- next-complaint auto-assignment
- status generation

## Why the service class is used

`ComplaintRoutingService` keeps the whole system state in one object.

That object stores:

- the category map
- all complaints
- one queue per department
- one agent per department
- direct agent lookup by ID
- counters for complaint IDs and heap ordering

This is simpler than spreading the state across global variables.

## Why these data structures were chosen

### Routing

Used:

- dictionary

Why:

- fast category-to-department lookup

### Waiting complaints

Used:

- dictionary of heaps

Why:

- each department has its own waiting queue
- higher priority complaints can be selected first

### Agent storage

Used:

- dictionary by department
- dictionary by ID

Why:

- fast assignment by department
- fast explicit resolution by agent ID

### Complaint storage

Used:

- dictionary by complaint ID

Why:

- easy status updates
- easy lookup during assignment and resolution

## Implementation order

1. define the data models
2. build the service state and category map
3. implement complaint submission and queue insertion
4. implement assignment when the agent is free
5. implement explicit agent resolution
6. auto-assign the next complaint from the same department
7. add the simple terminal interface
8. update the docs

## Design goal

The design goal is to keep only the real flow:

```text
submit -> route -> queue -> assign if free
resolve agent -> free agent -> assign next waiting complaint
```

There is no guided demo, no timer, and no extra display layer.
