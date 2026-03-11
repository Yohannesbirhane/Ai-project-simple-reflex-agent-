# ============================================================
# AI SIMPLE REFLEX AGENT
# Smart Dormitory Electricity Control System
# ============================================================

class DormitoryEnergyAgent:

    def __init__(self):
        print("==============================================")
        print(" SMART DORMITORY ELECTRICITY CONTROL AGENT ")
        print(" Type: Simple Reflex Agent")
        print("==============================================\n")

    # --------------------------------------------------------
    # PERCEPTION FUNCTION
    # --------------------------------------------------------
    def perceive(self, motion, light_level, time_period):
        """
        Receives current environmental state.
        This agent DOES NOT store history.
        """

        percept = {
            "motion": motion,
            "light_level": light_level,
            "time_period": time_period
        }

        return percept

    # --------------------------------------------------------
    # ACTION FUNCTION (Condition-Action Rules)
    # --------------------------------------------------------
    def act(self, percept):

        motion = percept["motion"]
        light = percept["light_level"]
        time = percept["time_period"]

        print("------------- CURRENT STATE -------------")
        print(f"Motion Detected   : {motion}")
        print(f"Light Level       : {light}")
        print(f"Time Period       : {time}")
        print("-----------------------------------------")

        # ===========================
        # RULE 1
        # ===========================
        if not motion and time == "class":
            print("\nRULE APPLIED: Rule 1")
            print("Condition: No Motion AND Class Time")
            print("WHY: Students should be in class, room is empty.")
            print("ACTION: TURN OFF LIGHT ")
            return "TURN OFF LIGHT"

        # ===========================
        # RULE 2
        # ===========================
        elif not motion and time == "night":
            print("\nRULE APPLIED: Rule 5")
            print("Condition: Night Time AND No Motion")
            print("WHY: Student is likely sleeping or room is empty.")
            print("ACTION: TURN OFF LIGHT")
            return "TURN OFF LIGHT"

        # ===========================
        # RULE 3
        # ===========================
        elif motion and light == "dark":
            print("\nRULE APPLIED: Rule 3")
            print("Condition: Motion Detected AND Dark Environment")
            print("WHY: Student is inside and needs light.")
            print("ACTION: TURN ON LIGHT")
            return "TURN ON LIGHT"

        # ===========================
        # RULE 4
        # ===========================
        elif light == "bright":
            print("\nRULE APPLIED: Rule 4")
            print("Condition: Bright Environment")
            print("WHY: Enough natural daylight available.")
            print("ACTION: TURN OFF LIGHT")
            return "TURN OFF LIGHT"

        # ===========================
        # RULE 5
        # ===========================
        elif not motion:
            print("\nRULE APPLIED: General Energy Saving Rule")
            print("Condition: No Motion Detected")
            print("WHY: Room appears empty.")
            print("ACTION: TURN OFF light")
            return "TURN OFF LIGHT"

        else:
            print("\nNo rule matched.")
            print("ACTION: NO CHANGE")
            return "NO ACTION"


# ============================================================
# SIMULATION SECTION
# ============================================================

agent = DormitoryEnergyAgent()

# ----------- TEST SCENARIOS ----------------

print("\n\n===== SCENARIO 1 =====")
state1 = agent.perceive(motion=False, light_level="bright", time_period="class")
agent.act(state1)

print("\n\n===== SCENARIO 2 =====")
state2 = agent.perceive(motion=True, light_level="dark", time_period="free")
agent.act(state2)

print("\n\n===== SCENARIO 3 =====")
state3 = agent.perceive(motion=False, light_level="dark", time_period="night")
agent.act(state3)

print("\n\n===== SCENARIO 4 =====")
state4 = agent.perceive(motion=True, light_level="bright", time_period="free")
agent.act(state4)