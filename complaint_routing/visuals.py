import sys
import textwrap
import time


RESET = "\033[0m"
STYLE_MAP = {
    "bold": "\033[1m",
    "cyan": "\033[96m",
    "green": "\033[92m",
    "yellow": "\033[93m",
    "blue": "\033[94m",
    "magenta": "\033[95m",
    "red": "\033[91m",
}


def _use_color() -> bool:
    return sys.stdout.isatty()


def style(text: str, *names: str) -> str:
    if not _use_color() or not names:
        return text
    prefix = "".join(STYLE_MAP[name] for name in names if name in STYLE_MAP)
    return f"{prefix}{text}{RESET}"


def pause(enabled: bool = True, seconds: float = 0.9) -> None:
    if enabled:
        time.sleep(seconds)


def print_header() -> None:
    line = "=" * 88
    print(style(line, "blue"))
    print(style("REAL-TIME COMPLAINT ROUTING SERVICE".center(88), "bold", "cyan"))
    print(style("Simple Terminal Demo".center(88), "magenta"))
    print(style("Complaint -> Category Mapping -> Department Heap -> Available Agent -> Assignment".center(88), "yellow"))
    print(style(line, "blue"))


def print_box(title: str, lines: list[str], color: str = "cyan", width: int = 88) -> None:
    inner_width = width - 4
    top = f"┌{'─' * (width - 2)}┐"
    bottom = f"└{'─' * (width - 2)}┘"
    print(style(top, color))
    print(style(f"│ {title[:inner_width].ljust(inner_width)} │", color))
    print(style(f"├{'─' * (width - 2)}┤", color))

    if not lines:
        lines = ["No data available."]

    for line in lines:
        wrapped = textwrap.wrap(line, width=inner_width) or [""]
        for piece in wrapped:
            print(f"│ {piece.ljust(inner_width)} │")

    print(style(bottom, color))


def print_snapshot(snapshot: dict) -> None:
    totals = snapshot["totals"]
    totals_lines = [
        f"Total complaints: {totals['complaints']}",
        f"Waiting         : {totals['waiting']}",
        f"Assigned        : {totals['assigned']}",
        f"Resolved        : {totals['resolved']}",
    ]
    print_box("System Totals", totals_lines, color="magenta")

    queue_lines: list[str] = []
    for department, complaints in snapshot["departments"].items():
        queue_lines.append(f"{department}:")
        if not complaints:
            queue_lines.append("  - empty")
            continue
        for complaint in complaints:
            queue_lines.append(
                f"  - {complaint['id']} | priority={complaint['priority']} | status={complaint['status']} | text={complaint['text']}"
            )
    print_box("Department Heaps", queue_lines, color="yellow")

    agent_lines: list[str] = []
    for department, agents in snapshot["agents"].items():
        agent_lines.append(f"{department}:")
        for agent in agents:
            state = "FREE" if agent["available"] else f"BUSY ({agent['current_complaint_id']})"
            agent_lines.append(f"  - {agent['id']} -> {state}")
    print_box("Agents", agent_lines, color="green")


def print_menu() -> None:
    menu_lines = [
        "1. Run guided demo",
        "2. Submit custom complaint",
        "3. Resolve agent complaint",
        "4. View current system state",
        "5. Reset system",
        "0. Exit",
    ]
    print_box("Menu", menu_lines, color="blue")


def print_tip(lines: list[str]) -> None:
    print_box("Note", lines, color="magenta")
