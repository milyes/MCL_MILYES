import sys

class Colors:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    GREEN = "\033[92m"
    CYAN = "\033[96m"
    YELLOW = "\033[93m"
    MAGENTA = "\033[95m"
    RED = "\033[91m"

if not sys.stdout.isatty():
    for a in vars(Colors):
        if not a.startswith("_") and a != "RESET":
            setattr(Colors, a, "")
