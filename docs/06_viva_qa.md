# 06. Viva Q&A

## Q1. What does this project do?

It takes a complaint, routes it to the correct department, stores it in that department's priority queue, and assigns it to that department's agent if the agent is free.

## Q2. Why is this a DSA project?

Because it uses data structures directly in the system flow:

- dictionary for routing
- heap for priority
- dictionary for complaint lookup
- dictionaries for agent access

## Q3. Where is the routing logic implemented?

In `complaint_routing/service.py`.

The mapping is stored in `self.category_map`.

## Q4. Where is the category map stored?

Inside `ComplaintRoutingService` as `self.category_map`.

## Q5. Why use a dictionary for routing?

Because category-to-department lookup should be fast.

## Q6. Where is the priority queue implemented?

In `complaint_routing/service.py` as `self.department_queues`.

Each department has its own heap.

## Q7. Why use a heap instead of a normal queue?

Because the most urgent complaint should be handled first, not just the oldest complaint.

## Q8. How is highest priority made to come first in Python's heap?

The code stores:

```python
(-complaint.priority, order, complaint.id)
```

Using negative priority makes larger priority numbers come out first.

## Q9. Why is there no global heap?

Because this design is intentionally simple.

Each department works independently, so each department only needs its own queue.

## Q10. What does department queue mean in this project?

It means the department heap itself.

## Q11. Where are complaints stored after creation?

In `self.complaints` inside `complaint_routing/service.py`.

## Q12. Why are complaints stored separately if they are already in the heap?

Because the heap stores ordering data, while the dictionary stores the full complaint objects for updates and lookups.

## Q13. What happens if no agent is free?

The complaint stays in the department queue and its status remains `waiting`.

## Q14. What happens when an agent resolves a complaint?

`resolve_agent()`:

- finds the agent through `self.agents_by_id`
- marks the current complaint as `resolved`
- marks the agent as available
- assigns the next waiting complaint from the same department if one exists

## Q15. What is the time complexity of routing a complaint?

Dictionary lookup for category mapping is O(1).

## Q16. What is the time complexity of pushing a complaint into the department heap?

Heap push is O(log n), where `n` is the number of waiting complaints in that department.

## Q17. What is the time complexity of assigning the next complaint?

Heap pop is O(log n).

Agent lookup is O(1) because the service stores `self.agents_by_department` and `self.agents_by_id`.

## Q18. Why did you keep the project terminal-based?

Because the goal is to show the logic clearly without web or database complexity.

## Q19. Which file should I open first in viva if asked to explain the logic?

Open `complaint_routing/service.py` first.

## Q20. What is the one-line summary of the project?

Complaint -> Category Mapping -> Department Queue -> Assign if Free -> Resolve Agent -> Assign Next
