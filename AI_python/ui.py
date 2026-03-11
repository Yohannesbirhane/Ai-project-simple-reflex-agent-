import tkinter as tk
from tkinter import ttk


class DormitoryEnergyAgent:

    def perceive(self, motion, light_level, time_period):
        return {
            "motion": motion,
            "light_level": light_level,
            "time_period": time_period,
        }

    def evaluate(self, percept):
        motion = percept["motion"]
        light = percept["light_level"]
        time_period = percept["time_period"]

        if not motion and time_period == "class":
            return {
                "rule": "Rule 1",
                "action": "TURN OFF LIGHT",
                "reason": "Room appears empty during class hours.",
                "impact": "Prevents unnecessary daytime electricity waste.",
            }

        if not motion and time_period == "night":
            return {
                "rule": "Rule 2",
                "action": "TURN OFF LIGHT",
                "reason": "No movement detected at night.",
                "impact": "Reduces overnight energy consumption.",
            }

        if motion and light == "dark":
            return {
                "rule": "Rule 3",
                "action": "TURN ON LIGHT",
                "reason": "Student is present and environment is dark.",
                "impact": "Maintains safety and comfort while occupied.",
            }

        if light == "bright":
            return {
                "rule": "Rule 4",
                "action": "TURN OFF LIGHT",
                "reason": "Natural light is already sufficient.",
                "impact": "Avoids duplicate lighting and saves cost.",
            }

        if not motion:
            return {
                "rule": "Rule 5",
                "action": "TURN OFF LIGHT",
                "reason": "No occupancy detected.",
                "impact": "Supports base energy-saving behavior.",
            }

        return {
            "rule": "No rule matched",
            "action": "NO ACTION",
            "reason": "Current state does not require switching.",
            "impact": "System remains stable.",
        }


agent = DormitoryEnergyAgent()


SCENARIOS = {
    "Class Time (Room Empty)": {"motion": "No", "light": "bright", "time": "class"},
    "Student Returns (Dark Room)": {"motion": "Yes", "light": "dark", "time": "free"},
    "Night (No Activity)": {"motion": "No", "light": "dark", "time": "night"},
    "Daylight + Occupied": {"motion": "Yes", "light": "bright", "time": "free"},
}


def apply_scenario(*_):
    selected = scenario_var.get()
    if selected not in SCENARIOS:
        return

    scenario = SCENARIOS[selected]
    motion_var.set(scenario["motion"])
    light_var.set(scenario["light"])
    time_var.set(scenario["time"])
    status_text.set(f"Loaded scenario: {selected}")


def run_agent():
    motion = motion_var.get() == "Yes"
    light = light_var.get()
    time_period = time_var.get()

    percept = agent.perceive(motion, light, time_period)
    decision = agent.evaluate(percept)

    decision_action.set(decision["action"])
    decision_rule.set(decision["rule"])
    decision_reason.set(decision["reason"])
    decision_impact.set(decision["impact"])

    if decision["action"] == "TURN OFF LIGHT":
        status_text.set("Energy-saving action selected.")
    elif decision["action"] == "TURN ON LIGHT":
        status_text.set("Comfort/safety action selected.")
    else:
        status_text.set("No switching required.")


def hex_to_rgb(value):
    value = value.lstrip("#")
    return tuple(int(value[i:i + 2], 16) for i in (0, 2, 4))


def rgb_to_hex(rgb):
    return f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}"


def blend_colors(start_hex, end_hex, ratio):
    start = hex_to_rgb(start_hex)
    end = hex_to_rgb(end_hex)
    blended = tuple(int(start[i] + (end[i] - start[i]) * ratio) for i in range(3))
    return rgb_to_hex(blended)


def draw_background(event=None):
    width = background_canvas.winfo_width()
    height = background_canvas.winfo_height()

    if width <= 1 or height <= 1:
        return

    background_canvas.delete("bg")

    top_color = "#3B0764"
    mid_color = "#1D4ED8"
    bottom_color = "#0F172A"

    half = max(height // 2, 1)

    for y in range(height):
        if y <= half:
            ratio = y / half
            color = blend_colors(top_color, mid_color, ratio)
        else:
            ratio = (y - half) / max(height - half, 1)
            color = blend_colors(mid_color, bottom_color, ratio)
        background_canvas.create_line(0, y, width, y, fill=color, tags="bg")

    background_canvas.create_oval(-140, -120, 260, 260, fill="#7C3AED", outline="", tags="bg")
    background_canvas.create_oval(width - 300, -80, width + 120, 300, fill="#06B6D4", outline="", tags="bg")
    background_canvas.create_oval(width - 260, height - 220, width + 80, height + 120, fill="#EC4899", outline="", tags="bg")


window = tk.Tk()
window.title("Smart Dormitory Energy Agent - Real World Simulator")
window.geometry("860x560")
window.configure(bg="#0F172A")

background_canvas = tk.Canvas(window, highlightthickness=0, bd=0)
background_canvas.pack(fill="both", expand=True)

style = ttk.Style()
style.theme_use("clam")
style.configure("TFrame", background="#1E1B4B")
style.configure("Card.TFrame", background="#1E1B4B")
style.configure("TLabel", background="#1E1B4B", foreground="#E2E8F0", font=("Segoe UI", 10))
style.configure("Title.TLabel", background="#1E1B4B", foreground="#F8FAFC", font=("Segoe UI", 18, "bold"))
style.configure("Subtitle.TLabel", background="#1E1B4B", foreground="#C4B5FD", font=("Segoe UI", 10))
style.configure("CardTitle.TLabel", background="#1E1B4B", foreground="#FDE68A", font=("Segoe UI", 11, "bold"))
style.configure("CardText.TLabel", background="#1E1B4B", foreground="#DBEAFE", font=("Segoe UI", 10))
style.configure("TButton", font=("Segoe UI", 10, "bold"))
style.configure("Primary.TButton", background="#7C3AED", foreground="#FFFFFF", borderwidth=0)
style.map("Primary.TButton", background=[("active", "#8B5CF6")])
style.configure("Secondary.TButton", background="#0891B2", foreground="#FFFFFF", borderwidth=0)
style.map("Secondary.TButton", background=[("active", "#06B6D4")])
style.configure("TCombobox", font=("Segoe UI", 10))

container = ttk.Frame(background_canvas, padding=16)
container.columnconfigure(0, weight=1)
container.columnconfigure(1, weight=1)
container.rowconfigure(1, weight=1)

container_window = background_canvas.create_window(18, 18, window=container, anchor="nw")


def on_resize(event):
    draw_background()
    width = max(event.width - 36, 780)
    height = max(event.height - 36, 500)
    background_canvas.itemconfigure(container_window, width=width, height=height)


background_canvas.bind("<Configure>", on_resize)

header = ttk.Frame(container)
header.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 12))

ttk.Label(header, text="Smart Dormitory Electricity Control", style="Title.TLabel").pack(anchor="w")
ttk.Label(
    header,
    text="Real-world problem: lights are often left on when rooms are empty, increasing cost and waste.",
    style="Subtitle.TLabel",
).pack(anchor="w", pady=(2, 0))

left_card = ttk.Frame(container, style="Card.TFrame", padding=14)
left_card.grid(row=1, column=0, sticky="nsew", padx=(0, 8))
left_card.columnconfigure(0, weight=1)

ttk.Label(left_card, text="Simulation Inputs", style="CardTitle.TLabel").grid(row=0, column=0, sticky="w", pady=(0, 10))

scenario_var = tk.StringVar(value="Class Time (Room Empty)")
ttk.Label(left_card, text="Scenario Preset", style="CardText.TLabel").grid(row=1, column=0, sticky="w")
scenario_box = ttk.Combobox(
    left_card,
    state="readonly",
    textvariable=scenario_var,
    values=list(SCENARIOS.keys()),
)
scenario_box.grid(row=2, column=0, sticky="ew", pady=(4, 10))
scenario_box.bind("<<ComboboxSelected>>", apply_scenario)

motion_var = tk.StringVar(value="No")
light_var = tk.StringVar(value="bright")
time_var = tk.StringVar(value="class")

ttk.Label(left_card, text="Motion Detected", style="CardText.TLabel").grid(row=3, column=0, sticky="w")
ttk.Combobox(left_card, state="readonly", textvariable=motion_var, values=["Yes", "No"]).grid(
    row=4, column=0, sticky="ew", pady=(4, 10)
)

ttk.Label(left_card, text="Light Level", style="CardText.TLabel").grid(row=5, column=0, sticky="w")
ttk.Combobox(left_card, state="readonly", textvariable=light_var, values=["bright", "dark"]).grid(
    row=6, column=0, sticky="ew", pady=(4, 10)
)

ttk.Label(left_card, text="Time Period", style="CardText.TLabel").grid(row=7, column=0, sticky="w")
ttk.Combobox(left_card, state="readonly", textvariable=time_var, values=["class", "free", "night"]).grid(
    row=8, column=0, sticky="ew", pady=(4, 12)
)

button_row = ttk.Frame(left_card, style="Card.TFrame")
button_row.grid(row=9, column=0, sticky="ew")
button_row.columnconfigure(0, weight=1)
button_row.columnconfigure(1, weight=1)

ttk.Button(button_row, text="Run Simulation", command=run_agent, style="Primary.TButton").grid(
    row=0, column=0, sticky="ew", padx=(0, 4)
)
ttk.Button(button_row, text="Apply Preset", command=apply_scenario, style="Secondary.TButton").grid(
    row=0, column=1, sticky="ew", padx=(4, 0)
)

status_text = tk.StringVar(value="Select a scenario and run simulation.")
ttk.Label(left_card, textvariable=status_text, style="CardText.TLabel", wraplength=320).grid(
    row=10, column=0, sticky="w", pady=(12, 0)
)

right_card = ttk.Frame(container, style="Card.TFrame", padding=14)
right_card.grid(row=1, column=1, sticky="nsew", padx=(8, 0))
right_card.columnconfigure(0, weight=1)

ttk.Label(right_card, text="Agent Decision", style="CardTitle.TLabel").grid(row=0, column=0, sticky="w", pady=(0, 10))

decision_action = tk.StringVar(value="-")
decision_rule = tk.StringVar(value="-")
decision_reason = tk.StringVar(value="-")
decision_impact = tk.StringVar(value="-")

ttk.Label(right_card, text="Action", style="CardText.TLabel").grid(row=1, column=0, sticky="w")
ttk.Label(right_card, textvariable=decision_action, style="CardTitle.TLabel").grid(row=2, column=0, sticky="w", pady=(2, 10))

ttk.Label(right_card, text="Rule Applied", style="CardText.TLabel").grid(row=3, column=0, sticky="w")
ttk.Label(right_card, textvariable=decision_rule, style="CardText.TLabel", wraplength=320).grid(
    row=4, column=0, sticky="w", pady=(2, 10)
)

ttk.Label(right_card, text="Why This Action", style="CardText.TLabel").grid(row=5, column=0, sticky="w")
ttk.Label(right_card, textvariable=decision_reason, style="CardText.TLabel", wraplength=320).grid(
    row=6, column=0, sticky="w", pady=(2, 10)
)

ttk.Label(right_card, text="Real-World Impact", style="CardText.TLabel").grid(row=7, column=0, sticky="w")
ttk.Label(right_card, textvariable=decision_impact, style="CardText.TLabel", wraplength=320).grid(
    row=8, column=0, sticky="w", pady=(2, 10)
)

problem_card = ttk.Frame(right_card, style="Card.TFrame", padding=10)
problem_card.grid(row=9, column=0, sticky="ew", pady=(6, 0))
problem_card.columnconfigure(0, weight=1)

ttk.Label(problem_card, text="Problem Context", style="CardTitle.TLabel").grid(row=0, column=0, sticky="w")
ttk.Label(
    problem_card,
    text=(
        "Dorm rooms waste electricity when devices remain on during class or sleep time. "
        "This simulator shows how a simple reflex agent applies IF-THEN rules to reduce waste "
        "without removing student comfort."
    ),
    style="CardText.TLabel",
    wraplength=320,
).grid(row=1, column=0, sticky="w", pady=(4, 0))

apply_scenario()
run_agent()

window.mainloop()