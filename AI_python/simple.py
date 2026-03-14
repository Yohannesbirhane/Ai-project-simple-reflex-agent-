"""
============================================================
AI SIMPLE REFLEX AGENT
Smart Dormitory Electricity Control System
============================================================
"""
from typing import Dict, Union

class DormitoryEnergyAgent:
    """A Simple Reflex Agent that controls dormitory electricity based on current percepts."""

    def __init__(self) -> None:
        print("==============================================")
        print(" SMART DORMITORY ELECTRICITY CONTROL AGENT ")
        print(" Type: Simple Reflex Agent")
        print("==============================================\n")

    def perceive(self, motion: bool, light_level: str, time_period: str) -> Dict[str, Union[bool, str]]:
        """
        Receives current environmental state.
        This agent DOES NOT store history.
        """
        return {
            "motion": motion,
            "light_level": light_level,
            "time_period": time_period
        }

    def act(self, percept: Dict[str, Union[bool, str]]) -> str:
        """
        Applies condition-action rules based on the current percept.
        """
        motion = percept.get("motion", False)
        light = percept.get("light_level", "dark")
        time = percept.get("time_period", "free")

        print("------------- CURRENT STATE -------------")
        print(f"Motion Detected   : {motion}")
        print(f"Light Level       : {light}")
        print(f"Time Period       : {time}")
        print("-----------------------------------------")

        # RULE 1: Class time and empty room
        if not motion and time == "class":
            print("\nRULE APPLIED: Rule 1")
            print("Condition: No Motion AND Class Time")
            print("WHY: Students should be in class, room is empty.")
            print("ACTION: TURN OFF LIGHT ")
            return "TURN OFF LIGHT"

        # RULE 2: Night time and empty room (or sleeping)
        elif not motion and time == "night":
            print("\nRULE APPLIED: Rule 5 (from README)")
            print("Condition: Night Time AND No Motion")
            print("WHY: Student is likely sleeping or room is empty.")
            print("ACTION: TURN OFF LIGHT")
            return "TURN OFF LIGHT"

        # RULE 3: Motion detected and it's dark
        elif motion and light == "dark":
            print("\nRULE APPLIED: Rule 3")
            print("Condition: Motion Detected AND Dark Environment")
            print("WHY: Student is inside and needs light.")
            print("ACTION: TURN ON LIGHT")
            return "TURN ON LIGHT"

        # RULE 4: Bright environment (daylight available)
        elif light == "bright":
            print("\nRULE APPLIED: Rule 4")
            print("Condition: Bright Environment")
            print("WHY: Enough natural daylight available.")
            print("ACTION: TURN OFF LIGHT")
            return "TURN OFF LIGHT"

        # RULE 5: General no motion rule
        elif not motion:
            print("\nRULE APPLIED: General Energy Saving Rule")
            print("Condition: No Motion Detected")
            print("WHY: Room appears empty.")
            print("ACTION: TURN OFF LIGHT")
            return "TURN OFF LIGHT"

        # Default action when no specific rule matches
        else:
            print("\nRULE APPLIED: Default / No Rule Matched")
            print("Condition: Unhandled State")
            print("WHY: Environment is safe, letting status quo remain.")
            print("ACTION: NO CHANGE")
            return "NO ACTION"


def main() -> None:
    # ============================================================
    # SIMULATION SECTION
    # ============================================================
    agent = DormitoryEnergyAgent()

    # ----------- TEST SCENARIOS ----------------
    scenarios = [
        (1, False, "bright", "class"),
        (2, True,  "dark",   "free"),
        (3, False, "dark",   "night"),
        (4, True,  "bright", "free")
    ]

    for num, motion, light_level, time_period in scenarios:
        print(f"\n\n===== SCENARIO {num} =====")
        state = agent.perceive(motion=motion, light_level=light_level, time_period=time_period)
        agent.act(state)

if __name__ == "__main__":
    main()
