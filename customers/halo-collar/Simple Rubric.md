# Halo Collar — Simple Field Test Rubric

## Activity Detection - PASS if:
- **Macro-F1 ≥ 82%**
- **All behavior classes ≥ 72% recall**
- **Daily active minutes error ≤ 25%**

## GPS Indoor/Outdoor - PASS if:
- **False-Indoor rate ≤ 4%** (safety)
- **Balanced accuracy ≥ 91%**
- **Transition latency ≤ 8 sec avg**
- **Flap rate ≤ 1.8/hr**

## FAIL immediately if:
- False-Indoor > 6%
- Any class < 60% recall
- Time sync > 500ms

---

## Data Collector Behavior Guide

### Before Collection
✅ **Confirm dog comfort** - collar should fit snug but not tight  
✅ **Sync all devices** - phone, IMU, collar to same time source  
✅ **Set up reference** - door sensors on entry points, video ready  
✅ **Log environment** - canopy %, building type, weather  

### During Collection

**Pace Yourself - Let the Dog Lead**
- Don't direct or force behaviors
- Follow at normal walking distance (3-5 feet)
- Keep voice neutral (no commands that change behavior)

**Watch for Dangerous Transitions**
- When going indoors: pause at threshold, wait for recognition
- When going outdoors: ensure collar has clear sky view
- If door sensor missed a crossing: log it manually with timestamp

**Log Key Moments**
- "Rest start" when dog lies down
- "Walk start"/"Walk end" for walks > 30 seconds
- "Eat start" for any food/water activity
- "Carry start" if picked up (rare but important)
- "Collar loose" if it shifts/rotates significantly
- "Dog stressed" if barking, excessive panting, or trying to remove collar

**Handle Edge Cases**
- Head shaking = pause collection (causes "classification explosions")
- Loose collar = stop session, reposition
- Battery low = end session, swap if mid-transition
- Weather changes = note in logs (affects GNSS)

### After Collection
✅ **Stop all logs within 2 minutes of each other**  
✅ **Verify file sizes** - any file < 1KB is suspect  
✅ **Upload immediately** to shared folder  
✅ **Sign off:** Handler + Equipment Monitor initials  

---

**Stop test • Escalate • Do not proceed if any FAIL condition met**