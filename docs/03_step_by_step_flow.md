# 03. Step-by-Step Flow

## Why this file matters

This file explains the actual path a complaint takes in the current code.

It connects the terminal screen to the exact methods that run behind it.

## Full flow in the current project

```text
main() -> submit_custom_complaint() -> service.submit_complaint()
                                     -> resolve_department()
                                     -> heap push into department
                                     -> _attempt_assignment()
                                     -> _find_available_agent()
```

When a complaint is resolved, the flow is:

```text
resolve_agent_complaint() -> service.resolve_agent()
                          -> _attempt_assignment()
```

## Example 1: one complaint enters the system

Take this example:

```text
Text: my fan is not working
Category: electricity
Priority: 2
```

## Step 1: input is taken in `app.py`

The function `submit_custom_complaint()` asks for:

- complaint text
- category
- priority

After that, it calls:

```python
service.submit_complaint(text=text, category=category, priority=priority)
```

## Step 2: `submit_complaint()` normalizes the input

Inside `complaint_routing/service.py`, the method starts with:

```python
normalized_category = category.strip().lower()
department = self.resolve_department(normalized_category)
```

This means:

- extra spaces are removed
- category is converted to lowercase
- department is found using the category map

## Step 3: complaint object is created

Still inside `submit_complaint()`, a `Complaint` object is created.

It gets:

- a new ID like `C1`
- text
- category
- priority
- department

Then the complaint is stored in:

```python
self.complaints[complaint.id] = complaint
```

At this point, the complaint exists in the system, but it is not assigned yet.

## Step 4: complaint goes into the correct department heap

This happens here:

```python
heapq.heappush(
    self.department_heaps[department],
    (-complaint.priority, next(self._heap_sequence), complaint.id),
)
```

For the complaint above, the stored heap item will look similar to:

```python
(-2, 0, "C1")
```

Important point:

- the heap stores ordering data
- the full complaint stays in `self.complaints`

## Step 5: queue view is prepared for display

After insertion, the code calls:

```python
queue_view = self.get_department_queue_view(department)
```

This method reads the heap and returns the full complaint objects in sorted order for display.

That is why the terminal can show:

```text
Queue order (highest priority first)
```

## Step 6: assignment is attempted

Then the code calls:

```python
events.extend(self._attempt_assignment(department))
```

This is the method that decides whether the complaint is assigned now or kept waiting.

## Step 7: `_attempt_assignment()` checks agent availability

Inside `_attempt_assignment()`:

```python
available_agent = self._find_available_agent(department)
```

Then the method checks three cases.

### Case A: queue is empty

No assignment is needed.

### Case B: queue has complaint but no free agent

The complaint remains in the heap.
Its status stays `waiting`.

### Case C: queue has complaint and a free agent exists

The method pops the top complaint:

```python
_, _, complaint_id = heapq.heappop(queue)
```

Then it updates both complaint and agent:

- complaint status becomes `assigned`
- complaint gets `assigned_agent_id`
- agent becomes unavailable
- agent gets `current_complaint_id`

## Example 2: two electricity complaints

This matches the behavior you saw in the terminal.

### First complaint

```text
C1: electricity, priority 2
```

What happens:

- complaint goes to `Electricity Department`
- `A2` is free
- `C1` is assigned to `A2`

### Second complaint

```text
C2: electricity, priority 4
```

What happens:

- complaint goes to `Electricity Department`
- it is pushed into the electricity heap
- `_attempt_assignment()` checks for a free electricity agent
- `A2` is already busy with `C1`
- so `available_agent` becomes `None`
- `C2` stays in the heap with status `waiting`

This is why the terminal showed:

```text
Available agent found: None
Top complaint still waiting: C2
```

## What happens when the agent resolves the complaint

In `app.py`, the function `resolve_agent_complaint()` takes the agent ID and calls:

```python
service.resolve_agent(agent_id)
```

Inside `resolve_agent()`:

- the agent is found using `find_agent()`
- the current complaint is marked `resolved`
- the agent becomes available again
- `_attempt_assignment(agent.department)` is called again

So if `A2` resolves `C1`, then `C2` can be assigned immediately.

## Why this feels like real-time routing

The program is still running step by step.
But after every important change, the system immediately checks whether the next complaint can move forward.

That is enough to show real complaint flow behavior in a simple terminal project.

## Final understanding

The complaint does not move through two separate priority stages.

It moves through:

- one routing stage
- one department heap stage
- one assignment stage

That is the clean design used in this project.
