# Halo Collar — Field Testing Process

**Audience:** 
- **Testers** (field staff, dog handlers, data collectors)
- **Evaluators** (ML engineers, QA analysts, product team)

**Scope:** Model A (Activity Detection) + Model B (Indoor/Outdoor GPS Classifier)  
**Goal:** Reproducible field testing with clear evaluation outcomes

---

## Part 1: Tester Actions — How to Run Field Tests

### Pre-Test Setup

**1. Equipment Check**
- [ ] Reference IMU mounted on separate harness (not the Halo collar)
- [ ] Video camera with time stamp (enable NTP sync on phone/computer)
- [ ] Door sensors installed on all entry points (magnetic reed switches)
- [ ] Collar fully charged, firmware version logged
- [ ] Environmental logging: note canopy cover %, building construction type, nearby structures

**2. Session Preparation**
- [ ] Sync all device clocks via NTP (phone, IMU logger, collar if possible)
- [ ] Verify time stamp alignment test: 10-second shake test with all devices
- [ ] Load test protocol into shared checklist (Google Sheet or paper form)
- [ ] Confirm dog is comfortable with collar placement and harness

**3. Test Subject Assignment**
- Assign one person as **Primary Handler** (dog control)
- Assign one person as **Equipment Monitor** (logs, timestamps, sensors)
- Both sign off on session start in the checklist

---

### Test Execution

**Phase 1: Indoor Baseline (15 minutes)**
- Dog rests indoors, collar and harness both recording
- Handler sits quietly, no interaction
- Equipment Monitor logs: "Indoor steady" at minute 5, 10, 15
- Purpose: Establish baseline GNSS signature, validate reference signals

**Phase 2: Transition Circuit (20 minutes)**
- **Sequence:** Walk → Out → Walk 20ft → In → Walk → Repeat 3x
- Dog moves at normal walking pace (handler follows, doesn't lead)
- Equipment Monitor marks: "Transition start" when crossing threshold
- Purpose: Measure transition detection, false-indoor/false-outdoor rates

**Phase 3: Transitional Spaces (10 minutes each)**
- **Porch/Garage:** Dog stays on threshold edge
- **Near Window:** Dog on couch or bed next to window
- **Vehicle:** Dog in stationary car (or car drives slowly in parking)
- Log: "Transitional state: [type]" at entry, exit, midpoint

**Phase 4: Free Living Capture (30 minutes)**
- Dog roams freely in yard/home
- Handler observes but doesn't direct
- Log major activities: "Play start", "Eat start", "Rest start"
- Purpose: Natural distribution capture

**Phase 5: Size/Breed Variation (if applicable)**
- Run same protocol with different dog subject
- Log: breed, weight, neck circumference, coat type

---

### Post-Test Actions

**1. Immediate**
- [ ] Stop all recordings within 2 minutes of each other
- [ ] Note any equipment issues (battery died, signal dropout)
- [ ] Snapshot: "Session complete - [dog name] - [site type]"

**2. Data Handling**
- [ ] Transfer all logs immediately (don't leave on device)
- [ ] Verify file integrity: all files > 1KB and time-stamped
- [ ] Name files: `[YYYY-MM-DD]_[dog-name]_[session-type]_[device-type].[ext]`
- [ ] Upload to shared folder within 2 hours

**3. Session Notes**
- [ ] Log collar position issues (slipped, rotated, loose)
- [ ] Note weather/environmental anomalies
- [ ] Record any behaviors that were hard to classify even for humans
- [ ] Sign off: "Handler: ___ Equipment: ___ Files: ___"

---

## Part 2: Evaluator Actions — How to Analyze Results

### Step 1: Data Alignment (0-2 hours)

**Actions:**
1. **Time sync verification** - Plot all timestamps, confirm alignment within 100ms
2. **Missing data check** - Flag any file gaps > 5 seconds
3. **Extract reference labels** - Pull from video annotations + door sensors
4. **Segment creation** - Create 4-second windows aligned across all sources

**Gate:** If time sync error > 500ms, escalate to hardware team. Do not analyze.

---

### Step 2: Offline Evaluation (2-4 hours)

**Actions:**
1. **Run inference** on full-precision model against captured windows
2. **Generate metrics:**
   - Confusion matrix (overall)
   - Per-class precision/recall/F1
   - Macro-F1 and balanced accuracy
   - Confidence histogram + ECE calculation

**For GPS Model Specifically:**
- Tag each window by environment type (indoor/outdoor/transitional)
- Isolate confuser environments: urban canyon, canopy, vehicle, porch
- Calculate false-Indoor and false-Outdoor rates

**For Activity Model Specifically:**
- Stratify by breed/size if multiple dogs tested
- Identify bout-level detection (did we catch the walk?)
- Measure daily aggregates (if full day of data)

---

### Step 3: On-Device Parity Check (4-6 hours)

**Actions:**
1. **Deploy same model** to test collar via Edge Impulse
2. **Run identical data** through on-device inference
3. **Compare predictions** - Calculate mismatch rate
4. **Log power/latency** if available from firmware

**Gate:** Mismatch rate ≤ 2% required. If higher, investigate quantization or preprocessing.

---

### Step 4: Field Trial Analysis (6-12 hours)

#### For Activity Detection:

**Primary Analysis:**
```
Metrics to compute:
- Macro-F1 = average of all class F1 scores
- Worst-class recall = min(recall for each class)
- Daily active minutes error = |predicted - reference| / reference
- Confidence ECE = |confidence bins - accuracy bins| averaged
```

**Evaluation Flow:**
1. **Check overall accuracy** - Does macro-F1 hit 82%?
2. **Check per-class floor** - Any class < 72% recall?
3. **Check strata** - Any breed/size stratum < 75% F1?
4. **Check confidence** - ECE ≤ 12%?

**If any red flag:** Stop. Create failure report with worst N cases (N=20).

#### For GPS Indoor/Outdoor:

**Primary Analysis:**
```
Metrics to compute:
- False-Indoor rate = FalseIndoors / (TrueOutdoors + FalseIndoors) × 100
- False-Outdoor rate = FalseOutdoors / (TrueIndoors + FalseOutdoors) × 100
- Transition latency = avg(time between true crossing and correct classification)
- Flap rate = number of state toggles while motionless / session hours
- Per-confuser accuracy = balanced accuracy within each environment type
```

**Evaluation Flow:**
1. **Check safety metric first** - Is false-Indoor rate ≤ 4%?
2. **Check overall accuracy** - Balanced accuracy ≥ 91%?
3. **Check transitions** - Average latency ≤ 8 seconds?
4. **Check stability** - Flap rate ≤ 1.8/hr?
5. **Check confusers** - Any environment type < 85% balanced accuracy?

**If any red flag:** Stop. Document immediately to product team.

---

### Step 5: Reporting (12-24 hours)

**Template Sections:**

**1. Executive Summary**
- Pass/Fail verdict for each model
- Headline numbers vs. thresholds
- Any red flags triggered

**2. Test Conditions**
- Dog subjects (breed, weight, age)
- Environment types tested
- Session duration and conditions

**3. Detailed Metrics**
- Confusion matrices (overall + per-stratum)
- All primary metrics with confidence intervals
- Comparison to lab baseline

**4. Failure Analysis (if any)**
- Worst N failure cases (N=10 for activity, N=5 for GPS)
- Root cause hypothesis per failure
- Recommendation for next step

**5. Recommendations**
- Proceed to next phase
- Retest with modified protocol
- Escalate specific issue
- No regression risk (if passing)

**6. Sign-off**
- ML Lead: _______ Date: _______
- Hardware Lead: _______ Date: _______
- Product Lead: _______ Date: _______

---

## Escalation Triggers

| Condition | Action |
|-----------|--------|
| False-Indoor > 6% | **Immediate** email to Ken + Patrick + Teague |
| Macro-F1 < 70% | Flag for steering review in 24 hours |
| Time sync > 500ms | Re-run session, do not analyze |
| Missing reference data | Re-run session, do not analyze |
| Confidence ECE > 15% | Escalate before proceeding |

---

## File Naming Convention

**Data Files:**
```
[YYYY-MM-DD]_[dog-name-code]_[location-code]_[device-type].[ext]
Example: 2026-07-15_max-golden_retriever_porch_imu.csv
```

**Reports:**
```
Field-Test-Report_[model]_[YYYY-MM-DD]_[verdict].md
Example: Field-Test-Report_GPS_2026-07-15_PASS.md
```

---

## Tools Required

**Tester Side:**
- Mobile device with time sync app (GPS status & toolbox)
- Reference IMU logger (or custom firmware with timestamped output)
- Video camera (iPhone default OK if NTP synced)
- Door sensors (magnetic reed + simple logger)

**Evaluator Side:**
- Python with sklearn, numpy, pandas
- Edge Impulse CLI or Studio API access
- Jupyter notebook for metrics computation (template provided)
- Shared drive for data + reports

---

*Process v1.0 - subject to iteration after first trial run*