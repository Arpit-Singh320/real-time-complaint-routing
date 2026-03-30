# 07. File and Function Guide

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
```

## 1. `app.py`

`app.py` is the terminal entry point.

### Main functions

#### `print_box(title, content, width=60)`

Prints one output box in the terminal.

#### `show_events(events)`

Prints each `Event` returned by the service.

#### `show_status(status)`

Prints totals, department queues, and agent states.

#### `submit_complaint(service)`

Takes complaint input from the user and calls `service.submit_complaint()`.

#### `resolve_complaint(service)`

Takes an agent ID from the user and calls `service.resolve_agent()`.

#### `main()`

Runs the menu loop.

## 2. `complaint_routing/__init__.py`

Exports:

- `Agent`
- `Complaint`
- `ComplaintRoutingService`
- `Event`

## 3. `complaint_routing/models.py`

This file contains the core data objects.

### `Complaint`

Fields:

- `id`
- `text`
- `category`
- `priority`
- `department`
- `status`
- `assigned_agent_id`

### `Agent`

Fields:

- `id`
- `department`
- `available`
- `current_complaint_id`

### `Event`

Fields:

- `title`
- `lines`

## 4. `complaint_routing/service.py`

This is the core logic file.

### `ComplaintRoutingService.__init__()`

Creates:

- `self.category_map`
- `self.agents_by_department`
- `self.agents_by_id`
- `self.complaints`
- `self.department_queues`
- the complaint and queue counters

### `submit_complaint(text, category, priority)`

This method:

1. normalizes input
2. maps the category to a department
3. creates the complaint object
4. stores it in `self.complaints`
5. pushes it into that department queue
6. tries immediate assignment
7. returns the complaint and events

### `resolve_agent(agent_id)`

This method:

1. finds the agent directly from `self.agents_by_id`
2. checks whether the agent exists
3. checks whether the agent is already free
4. marks the current complaint as resolved
5. frees the agent
6. auto-assigns the next waiting complaint in the same department if available

### `_assign_next_complaint(department)`

This method is the assignment helper.

It only assigns when:

- the department agent is free
- the department queue is not empty

It pops the highest-priority complaint from the queue and updates both the complaint and agent state.

### `get_status()`

Returns a dictionary containing:

- complaint totals
- waiting complaints by department
- current agent states

## How the files connect together

### Startup flow

```text
app.py -> ComplaintRoutingService()
```

### Complaint submission flow

```text
app.py -> submit_complaint(service) -> service.submit_complaint()
```

### Resolution flow

```text
app.py -> resolve_complaint(service) -> service.resolve_agent()
```

### Display flow

```text
service returns Event objects -> app.py prints them
```

## Best reading order

1. `complaint_routing/models.py`
2. `complaint_routing/service.py`
3. `app.py`

If you understand `service.py`, you understand the core of the project.
