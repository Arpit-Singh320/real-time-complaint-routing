# 02. Data Structures and Design

## Main data structures in the current project

| Data structure | Exact variable | File | Purpose |
| --- | --- | --- | --- |
| Dictionary / HashMap | `self.category_map` | `complaint_routing/service.py` | category to department lookup |
| Dictionary | `self.complaints` | `complaint_routing/service.py` | complaint lookup by ID |
| Dictionary of heaps | `self.department_queues` | `complaint_routing/service.py` | one waiting queue per department |
| Heap tuple | `(-priority, order, complaint_id)` | `complaint_routing/service.py` | highest priority first, stable order for ties |
| Dictionary | `self.agents_by_department` | `complaint_routing/service.py` | one agent per department |
| Dictionary | `self.agents_by_id` | `complaint_routing/service.py` | direct lookup by agent ID |
| List | `Event.lines` | `complaint_routing/models.py` | terminal output lines |

## 1. Category routing dictionary

The service stores a simple mapping in `self.category_map`.

It is used to convert the submitted category into a department.

Example:

```python
{
    "water": "Water Department",
    "electricity": "Electricity Department",
    "road": "Municipal Department",
    "other": "General Support",
}
```

This is the right choice because dictionary lookup is fast and simple.

## 2. Complaint storage dictionary

The service stores every complaint object in `self.complaints` using complaint ID as the key.

This is needed because the heap stores only ordering data. When the service resolves or assigns a complaint, it uses this dictionary to get the full complaint object.

## 3. Department priority queues

Each department has its own heap in `self.department_queues`.

The heap item format is:

```python
(-priority, order, complaint_id)
```

Why this format is used:

- negative priority makes larger priorities come first in Python's min-heap
- `order` keeps insertion order stable when two complaints have the same priority
- `complaint_id` links the queue entry back to the stored complaint object

## 4. Agent dictionaries

The project has one agent per department.

So the service stores agents in two ways:

- `self.agents_by_department` for assignment within a department
- `self.agents_by_id` for direct resolution using agent ID from the menu

This avoids unnecessary searching through lists.

## 5. Event output structure

The service returns `Event` objects.

Each event has:

- `title`
- `lines`

The app prints those events in boxes.

This keeps business logic in the service and printing logic in the app.

## Design rule

Priority is handled only inside the department queue.

So in this project:

- department queue
- department heap
- priority queue

all mean the same thing.
