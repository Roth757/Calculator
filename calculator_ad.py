import math
import os
import sys
from datetime import datetime

# ── Colors ──────────────────────────────────────────────────
class Color:
    RESET   = "\033[0m"
    BOLD    = "\033[1m"
    DIM     = "\033[2m"
    CYAN    = "\033[36m"
    GREEN   = "\033[32m"
    YELLOW  = "\033[33m"
    RED     = "\033[31m"
    MAGENTA = "\033[35m"
    BLUE    = "\033[34m"
    WHITE   = "\033[97m"
    BG_DARK = "\033[48;5;235m"

def c(text, color):
    return f"{color}{text}{Color.RESET}"

# ── Operations ──────────────────────────────────────────────
BASIC_OPS = {
    "+": {"label": "Add",      "fn": lambda a, b: a + b},
    "-": {"label": "Subtract", "fn": lambda a, b: a - b},
    "*": {"label": "Multiply", "fn": lambda a, b: a * b},
    "/": {"label": "Divide",   "fn": lambda a, b: a / b if b != 0 else "Error: Cannot divide by 0"},
}

ADVANCED_OPS = {
    "^":   {"label": "Power (x^y)",   "fn": lambda a, b: a ** b},
    "%":   {"label": "Modulo (x%y)",  "fn": lambda a, b: a % b if b != 0 else "Error: Cannot mod by 0"},
    "sqrt": {"label": "Square Root",  "fn": lambda a: math.sqrt(a) if a >= 0 else "Error: Negative sqrt", "unary": True},
    "log":  {"label": "Log base 10",  "fn": lambda a: math.log10(a) if a > 0 else "Error: log ≤ 0",      "unary": True},
    "ln":   {"label": "Natural Log",  "fn": lambda a: math.log(a) if a > 0 else "Error: ln ≤ 0",         "unary": True},
    "!":    {"label": "Factorial",     "fn": lambda a: math.factorial(int(a)) if a >= 0 and a == int(a) and a <= 170 else "Error: Invalid factorial", "unary": True},
    "abs":  {"label": "Absolute",     "fn": lambda a: abs(a),                                              "unary": True},
    "sin":  {"label": "Sine (deg)",    "fn": lambda a: math.sin(math.radians(a)),                           "unary": True},
    "cos":  {"label": "Cosine (deg)",  "fn": lambda a: math.cos(math.radians(a)),                           "unary": True},
    "tan":  {"label": "Tangent (deg)", "fn": lambda a: math.tan(math.radians(a)),                           "unary": True},
}

ALL_OPS = {**BASIC_OPS, **ADVANCED_OPS}

# ── Formatting ──────────────────────────────────────────────
def format_result(val):
    if isinstance(val, str):
        return val
    if isinstance(val, float):
        if val == int(val) and abs(val) < 1e15:
            return f"{int(val):,}"
        return f"{val:,.10g}"
    return f"{val:,}"

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def draw_line(char="─", length=52):
    return c(char * length, Color.DIM)

def draw_box(lines, width=50):
    top    = c("╭" + "─" * width + "╮", Color.DIM)
    bottom = c("╰" + "─" * width + "╯", Color.DIM)
    rows = []
    rows.append(top)
    for line in lines:
        visible_len = len(line.replace("\033[0m", "").replace("\033[1m", "").replace("\033[2m", "")
                          .replace("\033[31m", "").replace("\033[32m", "").replace("\033[33m", "")
                          .replace("\033[34m", "").replace("\033[35m", "").replace("\033[36m", "")
                          .replace("\033[97m", "").replace("\033[48;5;235m", ""))
        padding = width - visible_len
        if padding < 0:
            padding = 0
        rows.append(f"{c('│', Color.DIM)} {line}{' ' * padding}{c('│', Color.DIM)}")
    rows.append(bottom)
    return "\n".join(rows)

# ── Calculator Class ────────────────────────────────────────
class AdvancedCalculator:
    def __init__(self):
        self.history = []
        self.memory = 0.0
        self.last_result = None

    def calculate(self, op_key, num1, num2=None):
        op = ALL_OPS[op_key]
        is_unary = op.get("unary", False)

        if is_unary:
            result = op["fn"](num1)
            expression = f"{op_key}({num1})"
        else:
            result = op["fn"](num1, num2)
            expression = f"{num1} {op_key} {num2}"

        if isinstance(result, str):  # error message
            return result, expression

        self.last_result = result
        self.history.append({
            "expression": expression,
            "result": result,
            "time": datetime.now().strftime("%H:%M:%S"),
        })
        # Keep last 50 entries
        if len(self.history) > 50:
            self.history = self.history[-50:]

        return result, expression

    def show_header(self):
        clear_screen()
        print()
        print(c("  ⚡ ADVANCED PYTHON CALCULATOR", Color.BOLD + Color.CYAN))
        print(c("  Scientific · Memory · History", Color.DIM))
        print(draw_line())

    def show_operations(self):
        print()
        print(c("  BASIC", Color.DIM))
        basic_line = "    "
        for key, op in BASIC_OPS.items():
            basic_line += f"{c(key, Color.CYAN)}  {c(op['label'], Color.DIM)}    "
        print(basic_line)

        print()
        print(c("  SCIENTIFIC", Color.DIM))
        sci_items = list(ADVANCED_OPS.items())
        line1 = "    "
        line2 = "    "
        for i, (key, op) in enumerate(sci_items):
            entry = f"{c(key, Color.MAGENTA)}  {c(op['label'], Color.DIM)}    "
            if i < 5:
                line1 += entry
            else:
                line2 += entry
        print(line1)
        print(line2)
        print()

    def show_status(self):
        mem_str = format_result(self.memory) if self.memory != 0 else "empty"
        last_str = format_result(self.last_result) if self.last_result is not None else "—"
        print(f"  {c('MEM:', Color.DIM)} {c(mem_str, Color.YELLOW)}    {c('LAST:', Color.DIM)} {c(last_str, Color.GREEN)}")
        print(draw_line())

    def show_history(self):
        clear_screen()
        print()
        print(c("  📋 CALCULATION HISTORY", Color.BOLD + Color.CYAN))
        print(draw_line())

        if not self.history:
            print(c("\n  No calculations yet.\n", Color.DIM))
        else:
            print()
            for i, entry in enumerate(reversed(self.history), 1):
                expr = c(entry["expression"], Color.WHITE)
                res = c(format_result(entry["result"]), Color.CYAN)
                time = c(entry["time"], Color.DIM)
                idx = c(f"  [{i:02d}]", Color.DIM)
                print(f"{idx}  {expr}  =  {res}    {time}")
            print()

        print(draw_line())
        input(c("  Press Enter to go back... ", Color.DIM))

    def show_memory_menu(self):
        clear_screen()
        print()
        print(c("  🧠 MEMORY OPERATIONS", Color.BOLD + Color.CYAN))
        print(draw_line())
        print()

        mem_val = format_result(self.memory) if self.memory != 0 else "0"
        print(f"  Current memory: {c(mem_val, Color.YELLOW)}")
        print()
        print(f"  {c('ms', Color.CYAN)}  Store last result to memory")
        print(f"  {c('mr', Color.CYAN)}  Recall memory value")
        print(f"  {c('m+', Color.CYAN)}  Add last result to memory")
        print(f"  {c('m-', Color.CYAN)}  Subtract last result from memory")
        print(f"  {c('mc', Color.CYAN)}  Clear memory")
        print(f"  {c('b', Color.DIM)}   Back")
        print()

        choice = input(c("  Choose: ", Color.GREEN)).strip().lower()

        if choice == "ms":
            if self.last_result is not None:
                self.memory = self.last_result
                print(c(f"\n  ✓ Stored {format_result(self.memory)} to memory", Color.GREEN))
            else:
                print(c("\n  ✗ No result to store", Color.RED))
        elif choice == "mr":
            print(c(f"\n  Memory value: {format_result(self.memory)}", Color.YELLOW))
            print(c("  (Use 'ans' or 'mem' as input to use this value)", Color.DIM))
        elif choice == "m+":
            if self.last_result is not None:
                self.memory += self.last_result
                print(c(f"\n  ✓ Memory is now {format_result(self.memory)}", Color.GREEN))
            else:
                print(c("\n  ✗ No result to add", Color.RED))
        elif choice == "m-":
            if self.last_result is not None:
                self.memory -= self.last_result
                print(c(f"\n  ✓ Memory is now {format_result(self.memory)}", Color.GREEN))
            else:
                print(c("\n  ✗ No result to subtract", Color.RED))
        elif choice == "mc":
            self.memory = 0.0
            print(c("\n  ✓ Memory cleared", Color.GREEN))
        elif choice == "b":
            return
        else:
            print(c("\n  ✗ Invalid choice", Color.RED))

        input(c("\n  Press Enter to continue... ", Color.DIM))

    def parse_number(self, prompt):
        """Parse input — supports 'ans' for last result, 'mem' for memory, 'pi', 'e'"""
        while True:
            raw = input(prompt).strip().lower()
            if raw in ("q", "quit", "exit"):
                return None, True
            if raw == "ans":
                if self.last_result is not None:
                    print(c(f"    → Using last result: {format_result(self.last_result)}", Color.DIM))
                    return self.last_result, False
                else:
                    print(c("    ✗ No previous result", Color.RED))
                    continue
            if raw == "mem":
                print(c(f"    → Using memory: {format_result(self.memory)}", Color.DIM))
                return self.memory, False
            if raw == "pi":
                print(c(f"    → Using π: {math.pi}", Color.DIM))
                return math.pi, False
            if raw == "e":
                print(c(f"    → Using e: {math.e}", Color.DIM))
                return math.e, False
            try:
                return float(raw), False
            except ValueError:
                print(c("    ✗ Invalid number. Try again (or type 'ans', 'mem', 'pi', 'e')", Color.RED))

    def run(self):
        while True:
            self.show_header()
            self.show_operations()
            self.show_status()
            print()
            print(f"  {c('Commands:', Color.DIM)} {c('history', Color.CYAN)} · {c('memory', Color.CYAN)} · {c('quit', Color.CYAN)}")
            print()

            # Get operation
            op_input = input(c("  Operation: ", Color.GREEN)).strip().lower()

            if op_input in ("q", "quit", "exit"):
                print(c("\n  Goodbye! 👋\n", Color.CYAN))
                break
            elif op_input in ("h", "history"):
                self.show_history()
                continue
            elif op_input in ("m", "memory", "mem"):
                self.show_memory_menu()
                continue
            elif op_input not in ALL_OPS:
                print(c("\n  ✗ Unknown operation. See the list above.", Color.RED))
                input(c("  Press Enter to continue... ", Color.DIM))
                continue

            op = ALL_OPS[op_input]
            is_unary = op.get("unary", False)

            print()
            print(f"  {c('Selected:', Color.DIM)} {c(op['label'], Color.CYAN)}")
            print(f"  {c('Tip:', Color.DIM)} type {c('ans', Color.YELLOW)} for last result, {c('mem', Color.YELLOW)} for memory, {c('pi', Color.YELLOW)}, {c('e', Color.YELLOW)}")
            print()

            # Get first number
            num1, should_quit = self.parse_number(c("  Number 1: ", Color.GREEN))
            if should_quit:
                print(c("\n  Goodbye! 👋\n", Color.CYAN))
                break

            # Get second number if needed
            num2 = None
            if not is_unary:
                num2, should_quit = self.parse_number(c("  Number 2: ", Color.GREEN))
                if should_quit:
                    print(c("\n  Goodbye! 👋\n", Color.CYAN))
                    break

            # Calculate
            result, expression = self.calculate(op_input, num1, num2)

            print()
            if isinstance(result, str) and result.startswith("Error"):
                print(f"  {c('✗', Color.RED)} {c(result, Color.RED)}")
            else:
                box_content = [
                    "",
                    f"  {c(expression, Color.WHITE)}",
                    "",
                    f"  = {c(format_result(result), Color.BOLD + Color.CYAN)}",
                    "",
                ]
                print(draw_box(box_content))

            print()
            input(c("  Press Enter for next calculation... ", Color.DIM))


# ── Entry Point ─────────────────────────────────────────────
if __name__ == "__main__":
    try:
        calc = AdvancedCalculator()
        calc.run()
    except KeyboardInterrupt:
        print(c("\n\n  Goodbye! 👋\n", Color.CYAN))
        sys.exit(0)