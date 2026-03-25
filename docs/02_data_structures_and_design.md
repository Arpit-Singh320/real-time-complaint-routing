# 02. Data Structures and Design

## Why this file is important

This file connects the DSA theory to the exact code in the project.

It answers these questions:

- which data structure is used
- where it is created
- which method uses it
- why it is needed

## Full mapping of data structures in this project

| Data structure | Exact variable | File | Main methods using it | Purpose |
| --- | --- | --- | --- | --- |
| Dictionary / HashMap | `DEFAULT_CATEGORY_MAP` | `complaint_routing/sample_data.py` | used by `build_service()` through the service constructor | base routing data |
| Dictionary / HashMap | `self.category_map` | `complaint_routing/service.py` | `__init__()`, `resolve_department()`, `submit_complaint()` | category to department lookup |
| Dictionary | `self.complaints` | `complaint_routing/service.py` | `submit_complaint()`, `resolve_agent()`, `get_department_queue_view()`, `get_snapshot()` | stores full complaint objects by ID |
| Dictionary of heaps | `self.department_heaps` | `complaint_routing/service.py` | `submit_complaint()`, `get_department_queue_view()`, `_attempt_assignment()`, `get_snapshot()` | stores waiting complaints separately by department |
| Heap tuple | `(-complaint.priority, order, complaint.id)` | `complaint_routing/service.py` | `heapq.heappush()`, `heapq.heappop()` | keeps highest priority complaint on top |
| Dictionary of lists | `self.agents_by_department` | `complaint_routing/service.py` | `__init__()`, `find_agent()`, `_find_available_agent()`, `get_snapshot()` | groups agents department-wise |
| List | `DEMO_COMPLAINTS` | `complaint_routing/sample_data.py` | `run_guided_demo()` in `app.py` | demo input data |
| List | `Event.lines` | `complaint_routing/models.py` | created in service methods, printed by `show_events()` | stores output lines for each step |

## 1. Dictionary for category routing

### Where it is implemented

- `complaint_routing/sample_data.py` -> `DEFAULT_CATEGORY_MAP`
- `complaint_routing/service.py` -> `self.category_map`

### How it works

The project starts with a simple mapping like this:

```python
DEFAULT_CATEGORY_MAP = {
    "water": "Water Department",
    "electricity": "Electricity Department",
    "road": "Municipal Department",
    "other": "General Support",
}
```

When the service is created, this mapping is copied into `self.category_map` inside `ComplaintRoutingService.__init__()`.

The categories are normalized using:

```python
category.strip().lower()
```

This means input like `Water`, ` water `, or `WATER` can still be handled correctly after cleaning.

### Which method uses it

`resolve_department()`

That method does:

```python
return self.category_map.get(category, self.fallback_department)
```

So if the category exists, the department is returned.
If not, the complaint goes to the fallback department.

### Why dictionary is the right choice

Because lookup is fast and simple.
This is exactly what a HashMap is good for.

## 2. Dictionary for complaint storage

### Where it is implemented

`complaint_routing/service.py` -> `self.complaints`

### How it works

When a complaint is created in `submit_complaint()`, the full object is stored like this:

```python
self.complaints[complaint.id] = complaint
```

### Why this is needed

The heap does not store the full complaint object directly for ordering.
It stores only enough data to rank complaints.

So this dictionary is needed for:

- getting full complaint details later
- updating status to `assigned` or `resolved`
- generating queue views
- generating the system snapshot

## 3. Dictionary of heaps for department queues

### Where it is implemented

`complaint_routing/service.py` -> `self.department_heaps`

Defined as:

```python
self.department_heaps: Dict[str, list[tuple[int, int, str]]] = defaultdict(list)
```

### What this means

- key = department name
- value = a heap list for that department

Example idea:

```python
{
    "Water Department": [heap items...],
    "Electricity Department": [heap items...],
}
```

### Why `defaultdict(list)` is useful

If a department is used for the first time, Python creates an empty list automatically.
So the code can push directly into the department heap without first checking if the key exists.

### Which methods use it

- `submit_complaint()`
- `get_department_queue_view()`
- `_attempt_assignment()`
- `get_snapshot()`

## 4. Heap for priority handling

### Where it is implemented

`complaint_routing/service.py`

The heap is used through Python's `heapq` module.

### Push operation

Inside `submit_complaint()`:

```python
heapq.heappush(
    self.department_heaps[department],
    (-complaint.priority, next(self._heap_sequence), complaint.id),
)
```

### Pop operation

Inside `_attempt_assignment()`:

```python
_, _, complaint_id = heapq.heappop(queue)
```

### Why negative priority is used

Python's heap is a min-heap.
That means smaller values come out first.

But this project wants larger priority numbers first.

So:

- priority `5` becomes `-5`
- priority `2` becomes `-2`

Since `-5` is smaller than `-2`, the complaint with original priority `5` is popped first.

### Why `_heap_sequence` is added

This is the second value in the tuple.

It solves the equal-priority case.
If two complaints have the same priority, the one inserted earlier should come first.

So the heap item looks like:

```python
(-priority, insertion_order, complaint_id)
```

## 5. Dictionary of agent lists

### Where it is implemented

`complaint_routing/service.py` -> `self.agents_by_department`

Defined as:

```python
self.agents_by_department: Dict[str, List[Agent]] = defaultdict(list)
```

### How it is filled

Inside `__init__()`:

```python
for agent in agents:
    self.agents_by_department[agent.department].append(agent)
```

### Why this is useful

When a complaint goes to Electricity Department, the service only checks Electricity Department agents.

That keeps the logic simple.

### Which methods use it

- `find_agent()`
- `_find_available_agent()`
- `get_snapshot()`

## 6. Sequence counters

### Where they are implemented

`complaint_routing/service.py`

- `self._complaint_sequence = count(1)`
- `self._heap_sequence = count()`

### Why they exist

`self._complaint_sequence`

- gives unique complaint IDs like `C1`, `C2`, `C3`

`self._heap_sequence`

- keeps heap ordering stable when priorities match

These are not the main DSA structures, but they support the working of the system.

## 7. Event list used for terminal output

### Where it is implemented

- `complaint_routing/models.py` -> `Event`
- `app.py` -> `show_events()`
- `complaint_routing/service.py` -> event objects are created there

### How it works

Each major step creates an `Event` object.
That object stores:

- `title`
- `lines`

Then `show_events()` prints each event as a box in the terminal.

This is why the project can show each step clearly without mixing display code into the core logic too much.

## Final design rule

Priority is not handled twice.

This project uses:

- category routing once
- department priority handling once

There is no separate global heap before the department heap.

So in this project:

- department queue = department heap = priority queue
