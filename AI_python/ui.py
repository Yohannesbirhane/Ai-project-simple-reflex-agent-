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
    run_agent()

def draw_room(motion_input, light_input, time_input, action_decision):
    room_canvas.delete("all")
    w = room_canvas.winfo_width()
    h = room_canvas.winfo_height()
    if w <= 1 or h <= 1:
        w = room_canvas.winfo_reqwidth()
        h = room_canvas.winfo_reqheight()

    motion = motion_input == "Yes"
    light_on = action_decision == "TURN ON LIGHT"

    # Background Colors based on light and time
    if light_on:
        wall_color, floor_color = "#FEF3C7", "#FDE68A"
        desk_color, screen_color = "#92400E", "#E2E8F0"
        person_head, person_body, person_legs = "#FCA5A5", "#60A5FA", "#3B82F6"
    else:
        if time_input == "night" or light_input == "dark":
            wall_color, floor_color = "#1E293B", "#0F172A"
            desk_color, screen_color = "#451A03", "#64748B"
            person_head, person_body, person_legs = "#991B1B", "#1E3A8A", "#1E40AF"
        else:
            wall_color, floor_color = "#94A3B8", "#475569"
            desk_color, screen_color = "#78350F", "#94A3B8"
            person_head, person_body, person_legs = "#F87171", "#3B82F6", "#1D4ED8"

    room_canvas.create_rectangle(0, 0, w, h, fill=wall_color, outline="")
    room_canvas.create_polygon(0, h-70, w, h-70, w, h, 0, h, fill=floor_color, outline="")

    # Window
    win_w, win_h = 80, 100
    win_x, win_y = w // 2, h // 2 - 30
    window_color = "#38BDF8"
    if time_input == "night":
        window_color = "#020617"
    elif light_input == "dark" and time_input != "night":
        window_color = "#1E1B4B"

    room_canvas.create_rectangle(win_x - win_w//2, win_y - win_h//2, win_x + win_w//2, win_y + win_h//2, fill=window_color, outline="#475569", width=4)
    room_canvas.create_line(win_x, win_y - win_h//2, win_x, win_y + win_h//2, fill="#475569", width=4)
    room_canvas.create_line(win_x - win_w//2, win_y, win_x + win_w//2, win_y, fill="#475569", width=4)

    # Person
    if motion:
        px, py = w // 4, h - 70
        room_canvas.create_oval(px - 15, py - 90, px + 15, py - 60, fill=person_head, outline="")
        room_canvas.create_rectangle(px - 20, py - 60, px + 20, py - 10, fill=person_body, outline="")
        room_canvas.create_rectangle(px - 15, py - 10, px - 5, py + 30, fill=person_legs, outline="")
        room_canvas.create_rectangle(px + 5, py - 10, px + 15, py + 30, fill=person_legs, outline="")

    # Desk
    dx, dy = w * 3 // 4, h - 70
    room_canvas.create_rectangle(dx - 35, dy - 40, dx + 35, dy, fill=desk_color, outline="")
    room_canvas.create_rectangle(dx - 30, dy, dx - 15, dy + 45, fill="#78350F", outline="")
    room_canvas.create_rectangle(dx + 15, dy, dx + 30, dy + 45, fill="#78350F", outline="")
    # Laptop
    room_canvas.create_polygon(dx - 20, dy - 40, dx + 20, dy - 40, dx + 25, dy - 30, dx - 25, dy - 30, fill=screen_color, outline="")

    # Lightbulb
    bulb_color = "#FBBF24" if light_on else "#64748B"
    room_canvas.create_line(w//2, 0, w//2, 30, fill="#475569", width=3)
    if light_on:
        room_canvas.create_oval(w//2 - 25, 15, w//2 + 25, 65, fill="#FEF08A", outline="")
    room_canvas.create_oval(w//2 - 15, 30, w//2 + 15, 60, fill=bulb_color, outline="")

def update_visualizer(*_):
    window.after(50, lambda: draw_room(motion_var.get(), light_var.get(), time_var.get(), decision_action.get()))

def run_agent(*_):
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
        action_label.configure(foreground="#F87171")
    elif decision["action"] == "TURN ON LIGHT":
        status_text.set("Comfort/safety action selected.")
        action_label.configure(foreground="#4ADE80")
    else:
        status_text.set("No switching required.")
        action_label.configure(foreground="#FDE68A")
        
    update_visualizer()

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
window.geometry("1120x620")
window.configure(bg="#0F172A")

background_canvas = tk.Canvas(window, highlightthickness=0, bd=0)
background_canvas.pack(fill="both", expand=True)

style = ttk.Style()
style.theme_use("clam")
style.configure("TFrame", background="#1E1B4B")
style.configure("Card.TFrame", background="#1E1B4B")
style.configure("TLabel", background="#1E1B4B", foreground="#E2E8F0", font=("Segoe UI", 11))
style.configure("Title.TLabel", background="#1E1B4B", foreground="#F8FAFC", font=("Segoe UI", 20, "bold"))
style.configure("Subtitle.TLabel", background="#1E1B4B", foreground="#C4B5FD", font=("Segoe UI", 11))
style.configure("CardTitle.TLabel", background="#1E1B4B", foreground="#FDE68A", font=("Segoe UI", 13, "bold"))
style.configure("CardText.TLabel", background="#1E1B4B", foreground="#DBEAFE", font=("Segoe UI", 11))
style.configure("Action.TLabel", background="#1E1B4B", foreground="#F8FAFC", font=("Segoe UI", 16, "bold"))
style.configure("TButton", font=("Segoe UI", 11, "bold"))
style.configure("Primary.TButton", background="#7C3AED", foreground="#FFFFFF", borderwidth=0)
style.map("Primary.TButton", background=[("active", "#8B5CF6")])
style.configure("Secondary.TButton", background="#0891B2", foreground="#FFFFFF", borderwidth=0)
style.map("Secondary.TButton", background=[("active", "#06B6D4")])
style.configure("TCombobox", font=("Segoe UI", 11))

container = ttk.Frame(background_canvas, padding=16)
container.columnconfigure(0, weight=1)
container.columnconfigure(1, weight=1)
container.columnconfigure(2, weight=1)
container.rowconfigure(1, weight=1)

container_window = background_canvas.create_window(18, 18, window=container, anchor="nw")

def on_resize(event):
    draw_background()
    width = max(event.width - 36, 1080)
    height = max(event.height - 36, 580)
    background_canvas.itemconfigure(container_window, width=width, height=height)
    update_visualizer()

background_canvas.bind("<Configure>", on_resize)

header = ttk.Frame(container)
header.grid(row=0, column=0, columnspan=3, sticky="ew", pady=(0, 15))

ttk.Label(header, text="Smart Dormitory Electricity Control", style="Title.TLabel").pack(anchor="w")
ttk.Label(
    header,
    text="Real-world problem: lights are often left on when rooms are empty, increasing cost and waste.",
    style="Subtitle.TLabel",
).pack(anchor="w", pady=(2, 0))

# --- LEFT CARD: INPUTS ---
left_card = ttk.Frame(container, style="Card.TFrame", padding=16)
left_card.grid(row=1, column=0, sticky="nsew", padx=(0, 10))
left_card.columnconfigure(0, weight=1)

ttk.Label(left_card, text="Simulation Inputs", style="CardTitle.TLabel").grid(row=0, column=0, sticky="w", pady=(0, 15))

scenario_var = tk.StringVar(value="Class Time (Room Empty)")
ttk.Label(left_card, text="Scenario Preset", style="CardText.TLabel").grid(row=1, column=0, sticky="w")
scenario_box = ttk.Combobox(left_card, state="readonly", textvariable=scenario_var, values=list(SCENARIOS.keys()))
scenario_box.grid(row=2, column=0, sticky="ew", pady=(4, 15))
scenario_box.bind("<<ComboboxSelected>>", apply_scenario)

motion_var = tk.StringVar(value="No")
light_var = tk.StringVar(value="bright")
time_var = tk.StringVar(value="class")

# Bind manual changes to auto-run
def on_input_change(*_): run_agent()

motion_var.trace_add("write", on_input_change)
light_var.trace_add("write", on_input_change)
time_var.trace_add("write", on_input_change)

ttk.Label(left_card, text="Motion Detected", style="CardText.TLabel").grid(row=3, column=0, sticky="w")
ttk.Combobox(left_card, state="readonly", textvariable=motion_var, values=["Yes", "No"]).grid(
    row=4, column=0, sticky="ew", pady=(4, 15)
)

ttk.Label(left_card, text="Light Level", style="CardText.TLabel").grid(row=5, column=0, sticky="w")
ttk.Combobox(left_card, state="readonly", textvariable=light_var, values=["bright", "dark"]).grid(
    row=6, column=0, sticky="ew", pady=(4, 15)
)

ttk.Label(left_card, text="Time Period", style="CardText.TLabel").grid(row=7, column=0, sticky="w")
ttk.Combobox(left_card, state="readonly", textvariable=time_var, values=["class", "free", "night"]).grid(
    row=8, column=0, sticky="ew", pady=(4, 20)
)

status_text = tk.StringVar(value="Select a scenario and run simulation.")
ttk.Label(left_card, textvariable=status_text, style="CardText.TLabel", wraplength=300).grid(
    row=9, column=0, sticky="w", pady=(10, 0)
)

# --- MIDDLE CARD: VISUALIZATION ---
middle_card = ttk.Frame(container, style="Card.TFrame", padding=16)
middle_card.grid(row=1, column=1, sticky="nsew", padx=(10, 10))
middle_card.rowconfigure(1, weight=1)
middle_card.columnconfigure(0, weight=1)

ttk.Label(middle_card, text="Dormitory View", style="CardTitle.TLabel").grid(row=0, column=0, sticky="w", pady=(0, 15))

room_canvas = tk.Canvas(middle_card, width=280, height=360, bg="#0F172A", highlightthickness=0)
room_canvas.grid(row=1, column=0, sticky="nsew")
room_canvas.bind("<Configure>", update_visualizer)

# --- RIGHT CARD: DECISION ---
right_card = ttk.Frame(container, style="Card.TFrame", padding=16)
right_card.grid(row=1, column=2, sticky="nsew", padx=(10, 0))
right_card.columnconfigure(0, weight=1)

ttk.Label(right_card, text="Agent Decision", style="CardTitle.TLabel").grid(row=0, column=0, sticky="w", pady=(0, 15))

decision_action = tk.StringVar(value="-")
decision_rule = tk.StringVar(value="-")
decision_reason = tk.StringVar(value="-")
decision_impact = tk.StringVar(value="-")

ttk.Label(right_card, text="Action", style="CardText.TLabel").grid(row=1, column=0, sticky="w")
action_label = ttk.Label(right_card, textvariable=decision_action, style="Action.TLabel")
action_label.grid(row=2, column=0, sticky="w", pady=(2, 15))

ttk.Label(right_card, text="Rule Applied", style="CardText.TLabel").grid(row=3, column=0, sticky="w")
ttk.Label(right_card, textvariable=decision_rule, style="CardText.TLabel", wraplength=280).grid(
    row=4, column=0, sticky="w", pady=(2, 15)
)

ttk.Label(right_card, text="Why This Action?", style="CardText.TLabel").grid(row=5, column=0, sticky="w")
ttk.Label(right_card, textvariable=decision_reason, style="CardText.TLabel", wraplength=280).grid(
    row=6, column=0, sticky="w", pady=(2, 15)
)

ttk.Label(right_card, text="Real-World Impact", style="CardText.TLabel").grid(row=7, column=0, sticky="w")
ttk.Label(right_card, textvariable=decision_impact, style="CardText.TLabel", wraplength=280).grid(
    row=8, column=0, sticky="w", pady=(2, 15)
)

problem_card = ttk.Frame(right_card, style="Card.TFrame", padding=12)
problem_card.grid(row=9, column=0, sticky="ew", pady=(15, 0))
problem_card.columnconfigure(0, weight=1)

ttk.Label(problem_card, text="Problem Context", style="CardTitle.TLabel").grid(row=0, column=0, sticky="w")
ttk.Label(
    problem_card,
    text=(
        "Dorm rooms waste electricity. This simulator applies "
        "IF-THEN rules to reduce waste."
    ),
    style="CardText.TLabel",
    wraplength=260,
).grid(row=1, column=0, sticky="w", pady=(4, 0))

apply_scenario()

window.mainloop()
