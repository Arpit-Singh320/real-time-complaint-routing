from complaint_routing.sample_data import DEMO_COMPLAINTS, DEFAULT_CATEGORY_MAP, build_default_agents
from complaint_routing.service import ComplaintRoutingService
from complaint_routing.visuals import pause, print_box, print_header, print_menu, print_snapshot, print_tip


def build_service() -> ComplaintRoutingService:
    return ComplaintRoutingService(DEFAULT_CATEGORY_MAP, build_default_agents())


def show_events(service: ComplaintRoutingService, events, auto_pause: bool = True) -> None:
    for event in events:
        color = "cyan"
        if "Assigned" in event.title:
            color = "green"
        elif "Waiting" in event.title:
            color = "yellow"
        elif "Resolve" in event.title:
            color = "magenta"
        print_box(event.title, event.lines, color=color)
        pause(auto_pause)
    print_snapshot(service.get_snapshot())
    pause(auto_pause)


def run_guided_demo(service: ComplaintRoutingService) -> None:
    print_tip(
        [
            "This demo shows routing, heap insert, assignment, waiting, and next assignment after resolution.",
            "The third complaint waits because the Water Department has only one agent in this version.",
        ]
    )

    for item in DEMO_COMPLAINTS:
        _, events = service.submit_complaint(
            text=item["text"],
            category=item["category"],
            priority=item["priority"],
        )
        show_events(service, events)

    print_tip(
        [
            "First the Electricity agent resolves its complaint. No one is waiting there.",
            "Then the Water agent resolves C1, so the next Water complaint is assigned automatically.",
        ]
    )
    show_events(service, service.resolve_agent("A2"))
    show_events(service, service.resolve_agent("A1"))


def submit_custom_complaint(service: ComplaintRoutingService) -> None:
    print_tip(
        [
            "Available categories: water, electricity, road, other.",
            "Priority range: 1 to 5. Higher number means higher urgency.",
        ]
    )
    text = input("Complaint text: ").strip()
    category = input("Category: ").strip().lower()

    while True:
        priority_text = input("Priority (1-5): ").strip()
        if priority_text.isdigit() and 1 <= int(priority_text) <= 5:
            priority = int(priority_text)
            break
        print("Enter a valid number from 1 to 5.")

    _, events = service.submit_complaint(text=text, category=category, priority=priority)
    show_events(service, events, auto_pause=False)


def resolve_agent_complaint(service: ComplaintRoutingService) -> None:
    agent_id = input("Agent ID to resolve (example: A1): ").strip()
    events = service.resolve_agent(agent_id)
    show_events(service, events, auto_pause=False)


def view_state(service: ComplaintRoutingService) -> None:
    print_snapshot(service.get_snapshot())


def main() -> None:
    service = build_service()
    print_header()
    print_tip(
        [
            "This project uses a category map and one heap for each department.",
            "There is no global priority queue. Priority is handled inside each department.",
        ]
    )

    while True:
        print_menu()
        choice = input("Choose an option: ").strip()

        if choice == "1":
            run_guided_demo(service)
        elif choice == "2":
            submit_custom_complaint(service)
        elif choice == "3":
            resolve_agent_complaint(service)
        elif choice == "4":
            view_state(service)
        elif choice == "5":
            service = build_service()
            print_box("System Reset", ["A fresh system has been created."], color="blue")
        elif choice == "0":
            print_box("Exit", ["Goodbye. Check the docs folder for full details."], color="magenta")
            break
        else:
            print_box("Invalid Choice", ["Please select one of the menu options."], color="red")


if __name__ == "__main__":
    main()
