"""Simple complaint routing terminal application."""

from complaint_routing.service import ComplaintRoutingService


# === UI FUNCTIONS ===

def print_box(title: str, content: list, width: int = 60):
    """Print a simple box around content."""
    border = "+" + "-" * (width - 2) + "+"
    print(border)
    print(f"| {title:^{width-4}} |")
    print(border)
    for line in content:
        print(f"| {line:<{width-4}} |")
    print(border)


def show_events(events: list):
    """Display events with user control."""
    for event in events:
        print_box(event.title, event.lines)
        input("Press Enter to continue...")


def show_status(status: dict):
    """Display system status."""
    print_box("SYSTEM STATUS", [
        f"Total: {status['complaints']['total']}",
        f"Waiting: {status['complaints']['waiting']}",
        f"Assigned: {status['complaints']['assigned']}",
        f"Resolved: {status['complaints']['resolved']}"
    ])

    print_box("DEPARTMENTS", [
        f"{dept}: {', '.join(complaints) if complaints else 'No waiting complaints'}"
        for dept, complaints in status['departments'].items()
    ])

    print_box("AGENTS", [
        f"{agent_id} ({info['department']}): {info['status']}"
        for agent_id, info in status['agents'].items()
    ])


# === USER INTERACTION FUNCTIONS ===

def submit_complaint(service: ComplaintRoutingService):
    """Handle user complaint submission."""
    print_box("SUBMIT COMPLAINT", [
        "Categories: water, electricity, road, other",
        "Priority: 1-5 (higher = more urgent)"
    ])

    text = input("Complaint text: ").strip()
    category = input("Category: ").strip()

    try:
        priority = int(input("Priority (1-5): ").strip())
        if not 1 <= priority <= 5:
            raise ValueError
    except ValueError:
        print("Invalid priority! Using 3.")
        priority = 3

    complaint, events = service.submit_complaint(text, category, priority)
    show_events(events)


def resolve_complaint(service: ComplaintRoutingService):
    """Handle complaint resolution."""
    print_box("RESOLVE COMPLAINT", [
        "Available agents: A1 (Water), A2 (Electricity),",
        "A3 (Municipal), A4 (General Support)"
    ])

    agent_id = input("Agent ID: ").strip()
    events = service.resolve_agent(agent_id)
    show_events(events)


# === MAIN APPLICATION ===

def main():
    """Main application loop."""
    service = ComplaintRoutingService()

    while True:
        print_box("MAIN MENU", [
            "1. Submit Complaint",
            "2. Resolve Complaint",
            "3. View Status",
            "0. Exit"
        ])

        choice = input("Choose option: ").strip()

        if choice == "1":
            submit_complaint(service)
        elif choice == "2":
            resolve_complaint(service)
        elif choice == "3":
            show_status(service.get_status())
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Invalid option!")


if __name__ == "__main__":
    main()
