# 06. Viva Q&A

## Q1. What does this project do?

It takes a complaint, routes it to the correct department, stores it in that department's heap, and assigns it to a free agent if one is available.

## Q2. Why is this a DSA project?

Because the project uses data structures for real system behavior:

- dictionary for routing
- heap for priority
- dictionary for complaint storage
- dictionary of lists for agent grouping

## Q3. Where is the routing logic implemented?

In `complaint_routing/service.py`.

The method is `resolve_department()`.

## Q4. Where is the category map stored?

The default mapping is in `complaint_routing/sample_data.py` as `DEFAULT_CATEGORY_MAP`.

Inside the service, it is stored as `self.category_map`.

## Q5. Why use a dictionary for routing?

Because category-to-department lookup should be fast.
A dictionary gives near O(1) lookup time.

## Q6. Where is the priority queue implemented?

In `complaint_routing/service.py`.

The variable is `self.department_heaps`.
Each department has its own heap.

## Q7. Why use a heap instead of a normal queue?

A normal queue is FIFO.
This project needs priority-based handling.
So the most urgent complaint should come first.

## Q8. How is highest priority made to come first in Python's heap?

Python's `heapq` is a min-heap.
So the code stores negative priority:

```python
(-complaint.priority, order, complaint.id)
```

## Q9. Why is there no global heap?

Because this is the minimal version.
Departments work independently here, so priority is handled only inside each department.

## Q10. What does department queue mean in this project?

It means the department heap itself.
There is no separate normal queue before or after the heap.

## Q11. Where are complaints stored after creation?

In `self.complaints` inside `complaint_routing/service.py`.

That dictionary stores the full complaint object by complaint ID.

## Q12. Why are complaints stored separately if they are already in the heap?

Because the heap stores ordering data, not full working state.
The dictionary is needed for:

- status updates
- agent assignment info
- lookup during resolution
- display in snapshots

## Q13. What happens if no agent is free?

That case is handled in `_attempt_assignment()`.

The complaint stays in the department heap and its status stays `waiting`.

## Q14. What happens when an agent resolves a complaint?

The method `resolve_agent()`:

- finds the agent
- marks the current complaint as `resolved`
- marks the agent as available
- calls `_attempt_assignment()` again for that department

## Q15. What is the time complexity of routing a complaint?

Dictionary lookup is O(1).

## Q16. What is the time complexity of pushing a complaint into the department heap?

Heap push is O(log n), where `n` is the number of waiting complaints in that department.

## Q17. What is the time complexity of assigning the next complaint?

Heap pop is O(log n), and finding an available department agent is O(a), where `a` is the number of agents in that department.

## Q18. Why did you keep the project terminal-based?

Because the main goal was to clearly show the flow and data structures without adding web or database complexity.

## Q19. Which file should I open first in viva if asked to explain the logic?

Open `complaint_routing/service.py` first.
That file contains the main logic of the project.

## Q20. What is the one-line summary of the project?

Complaint -> Category Mapping -> Department Heap -> Available Agent -> Assignment
