# Smart Dormitory Electricity Control
## Simple Reflex Agent (AI Project Presentation)

---

## 1) Problem Description

### Environment
University dormitory room

### Problem
Students often leave lights and electrical devices ON when:
- They go to class
- They are outside
- They are sleeping
- There is enough daylight

### Effects
- Energy waste
- High electricity cost
- Negative environmental impact

---

## 2) Type of Agent

### ✅ Simple Reflex Agent

### Definition
A **Simple Reflex Agent** acts only based on:
- Current percept (sensor input)
- Condition-action rules

It does **not**:
- Store past history
- Learn from experience
- Predict future states

Decision logic:
**IF condition → THEN action**

---

## 3) Environment Description (PEAS)

### P — Performance Measure
- Minimize electricity waste
- Maximize energy efficiency
- Avoid disturbing students unnecessarily

### E — Environment
- Dormitory room
- Students
- Day / Night
- Class time / Free time

### A — Actuators
- Turn light ON/OFF
- Turn fan ON/OFF
- Cut main power (optional extension)

### S — Sensors
- Motion sensor
- Light sensor
- Time sensor
- 

---

## 4) Possible Environment States

State variables:
- `M` = Motion detected (Yes/No)
- `T` = Time (Class/Night/Free)
- `L` = Light level (Bright/Dark)

### Important States and Actions

1. **M=Yes, T=Free, L=Dark**  
   Student inside + dark room → **Light ON**

2. **M=No, T=Class, L=Any**  
   No motion during class time → **Turn OFF everything**

3. **M=No, T=Night, L=Dark**  
   No motion at night → **Turn OFF light**

4. **M=Yes, T=Night, L=Dark**  
   Student awake at night → **Light ON**

5. **M=No, T=Free, L=Bright**  
   Room empty + daylight available → **Turn OFF**

6. **M=Yes, T=Day, L=Bright**  
   Student inside but enough sunlight → **Light OFF**

---

## 5) Condition–Action Rules

### Rule 1
IF (No Motion) AND (Class Time)  
THEN Turn OFF light and fan

### Rule 2
IF (No Motion) AND (No Motion for 20 minutes)  
THEN Turn OFF light

### Rule 3
IF (Motion Detected) AND (Dark)  
THEN Turn ON light

### Rule 4
IF (Bright Environment)  
THEN Turn OFF light

### Rule 5
IF (Night Time) AND (No Motion)  
THEN Turn OFF light

> Note: In the current Python script, the 20-minute timeout from Rule 2 is simplified into the no-motion behavior.

---

## 6) Python Implementation Summary

File: `simple.py`

Main parts:
- `DormitoryEnergyAgent` class
- `perceive(motion, light_level, time_period)` to read current state
- `act(percept)` to apply condition-action rules
- 4 simulation scenarios to demonstrate behavior

---

## 7) How to Run

In terminal:

```bash
py simple.py
```

Expected result:
- The program prints each scenario
- Displays current state (motion, light, time)
- Shows matched rule and selected action

---

## 8) Example Presentation Script (Short)

“This project uses a Simple Reflex Agent to reduce electricity waste in dormitory rooms.  
The agent observes only the current environment using motion, light, and time sensors.  
Then it applies fixed IF-THEN rules, for example: if motion is detected in a dark room, it turns the light ON; if it is bright or no one is present, it turns the light OFF.  
This approach is simple, fast, and suitable for basic smart energy control.”

---

## 9) Future Improvements

- Add real 20-minute inactivity timer
- Control fan and sockets separately
- Integrate with IoT devices (ESP32/Arduino)
- Add a Learning Agent version for smarter adaptation
