# 04. Implementation Plan

## Why the project was split into files

The project was divided into small files so each file has one clear job.

That makes the code easier to understand and easier to explain in viva.

## File-by-file implementation idea

### `app.py`

This file was kept as the entry point.

Reason:

- it handles input and menu flow
- it should not contain all business logic
- it only calls the service and prints results

This keeps the terminal code separate from the core routing logic.

### `complaint_routing/models.py`

This file was created to hold the data objects.

Reason:

- `Complaint` should be defined once in one place
- `Agent` should be defined once in one place
- `Event` should be defined once in one place

This avoids mixing data definitions into the service file.

### `complaint_routing/sample_data.py`

This file was added to keep default input data outside the main logic.

Reason:

- category mapping can be changed easily
- demo complaints can be changed easily
- default agents can be changed easily

This makes testing easier.

### `complaint_routing/service.py`

This file was made as the main logic layer.

Reason:

- all routing logic belongs in one place
- all heap logic belongs in one place
- all assignment logic belongs in one place
- all resolution logic belongs in one place

This is the core file of the whole project.

### `complaint_routing/visuals.py`

This file was added to handle terminal printing.

Reason:

- box drawing code should not fill `app.py`
- screen formatting should stay separate from routing logic
- the project is easier to present when the output is clean

## Why the service class was used

The class `ComplaintRoutingService` was created to keep the whole system state in one object.

That object stores:

- category map
- complaints
- department heaps
- agents by department
- sequence counters

This is better than using many global variables.

## Why these exact data structures were chosen

### Routing

Used:

- dictionary

Why:

- fast category to department lookup

### Waiting complaints

Used:

- dictionary of heaps

Why:

- separate complaint queues for each department
- priority-based selection inside each department

### Agent storage

Used:

- dictionary of lists

Why:

- agents can be checked department by department

### Complaint storage

Used:

- dictionary by complaint ID

Why:

- easy status updates
- easy lookup during resolution

## Why the app shows step-by-step boxes

This was added because the project is meant to be understood visually.

Each complaint creates a list of `Event` objects in `service.py`.
Then `app.py` prints them using `show_events()`.

This design is useful because:

- the service prepares the meaning of the step
- the visuals file handles how it is displayed

## Why there is no global heap

This was a deliberate design choice.

Reason:

- this project is supposed to stay simple
- departments work independently in this version
- one heap per department is enough to show correct priority logic

So the project uses:

- category routing first
- department heap second
- assignment third

## How the implementation was built in simple order

1. define the data classes
2. add sample mapping and default agents
3. build the service class
4. add heap and assignment logic
5. add terminal display functions
6. add guided demo and menu
7. add docs

## Why this structure is good for understanding

If someone opens the project for the first time, the code can be studied in layers:

- start with the data objects
- then see the sample input
- then read the service logic
- then read the app flow
- finally read the display helpers

That is why the project was implemented this way.
