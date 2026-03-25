# 05. Complexity and Edge Cases

## Why this file matters

This file explains the cost of the main operations in the current code and shows how the project handles special cases.

## Time complexity by method

## `resolve_department()`

File:

`complaint_routing/service.py`

Operation:

- dictionary lookup in `self.category_map`

Complexity:

```text
O(1)
```

Reason:

- category is used as a key in a dictionary

## `submit_complaint()`

This method does multiple small operations.

### Create complaint ID

Uses `next(self._complaint_sequence)`

Complexity:

```text
O(1)
```

### Store complaint in `self.complaints`

Dictionary insert:

```text
O(1)
```

### Push into department heap

Uses `heapq.heappush()`

Complexity:

```text
O(log n)
```

Here `n` is the number of waiting complaints in that department.

### Build queue view for display

Uses `get_department_queue_view()` which sorts heap items for display.

Complexity:

```text
O(n log n)
```

Important point:

- this sorting is only for showing a clean queue view in the terminal
- it is not needed for the actual heap push itself

## `_attempt_assignment()`

This is the main assignment method.

### Find available agent

Calls `_find_available_agent(department)`

Complexity:

```text
O(a)
```

Here `a` is the number of agents in that department.

### Pop highest-priority complaint

Uses `heapq.heappop(queue)`

Complexity:

```text
O(log n)
```

### Update complaint and agent state

Simple field updates:

```text
O(1)
```

## `resolve_agent()`

This method does:

- `find_agent(agent_id)`
- complaint lookup
- state updates
- calls `_attempt_assignment()` again

### `find_agent()`

In this version, it scans the agent lists.

Complexity:

```text
O(total agents)
```

Because it loops through all department agent lists until it finds the correct ID.

### Complaint lookup after agent is found

Uses:

```python
self.complaints[agent.current_complaint_id]
```

Complexity:

```text
O(1)
```

## `get_snapshot()`

This method prepares data for the terminal display.

It loops through departments and agents and also calls `get_department_queue_view()`.

So the total cost depends on:

- number of departments
- number of agents
- number of waiting complaints

This method is for display, not core routing.

## Space complexity

## Complaints

Stored in `self.complaints`

If total complaints are `m`:

```text
O(m)
```

## Waiting complaints in heaps

Stored across all department heaps

If total waiting complaints are up to `m`:

```text
O(m)
```

## Agents

Stored in `self.agents_by_department`

If total agents are `a`:

```text
O(a)
```

## Edge cases and where they are handled

## 1. Unknown category

Handled in:

- `resolve_department()`
- extra display line added in `submit_complaint()`

Code idea:

```python
return self.category_map.get(category, self.fallback_department)
```

Meaning:

- if category is missing, route to `General Support`

## 2. No free agent in that department

Handled in:

- `_attempt_assignment()`

Branch:

```python
if available_agent is None:
```

Meaning:

- complaint stays in heap
- complaint status stays `waiting`
- system prints that it is still waiting

## 3. No complaint in queue

Handled in:

- `_attempt_assignment()`

Branch:

```python
if not queue:
```

Meaning:

- no assignment is needed

## 4. Agent ID not found

Handled in:

- `resolve_agent()`

Branch:

```python
if agent is None:
```

Meaning:

- system returns an event saying the agent was not found
- no state is changed

## 5. Agent already free

Handled in:

- `resolve_agent()`

Branch:

```python
if agent.current_complaint_id is None:
```

Meaning:

- system returns an event saying the agent is already free

## 6. Same priority complaints

Handled by:

- heap tuple second value `next(self._heap_sequence)`

Meaning:

- earlier complaint gets priority if both have same priority number

## 7. Mixed departments do not compete with each other

Handled by design through:

- `self.department_heaps`

Meaning:

- water complaints stay in water heap
- electricity complaints stay in electricity heap
- there is no global mixing of complaint priority

## Limitations of the current version

- no database persistence
- no automatic category detection from text meaning
- no web dashboard
- no parallel execution

## Why these limitations are acceptable here

Because the main goal of this project is to clearly show the DSA flow and the system state in a simple terminal program.
