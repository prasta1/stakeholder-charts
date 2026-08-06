# Halo Collar — Field Testing Rubric (Draft)

**For:** Model A (Activity Detection) + Model B (Indoor/Outdoor GPS Classifier)  
**Purpose:** Define go/no-go criteria for field trials before production deployment

---

## Quick Reference: Pass/Fail Gates

| Model | Metric | Phase Gate 3 (Field) | Requirement |
|-------|--------|-------------------|-------------|
| **Activity** | Real-world macro-F1 | ≥ 82% | Primary accuracy target |
| Activity | Worst-class recall | ≥ 72% | Safety floor for rare behaviors |
| Activity | Daily active-minutes error | ≤ 25% | User-facing accuracy |
| **GPS** | Balanced accuracy | ≥ 91% | Overall classification quality |
| GPS | **False-Indoor rate** | **≤ 4%** | **SAFETY** - missed escapes |
| GPS | Transition latency | ≤ 8 sec avg | Response time to boundary crossings |
| GPS | Flap/hysteresis rate | ≤ 1.8 /hr | Nuisance toggle suppression |

---

## Model A — Activity Detection

### Field Testing Protocol

**Test Design:**
- 20+ dogs across 3+ breeds (small, medium, large)
- 2-3 hour sessions combining scripted activities + free living
- Synchronized reference truth: time-aligned video + reference-grade IMU (not the collar)
- Collar orientation varied: loose fit, high rotation, toy breeds, heavy coat

**Ground Truth Sources (prioritized):**
1. **Primary:** Vetted video annotation (multiple reviewers, κ > 0.75 agreement)
2. **Secondary:** Reference IMU on harness (for motion validation)
3. **Fallback:** Human logbook with timestamped behaviors (only for obvious states)

**Metrics Collection:**
- Per-class precision/recall/F1 on 4-second windows
- **Macro-F1** (unweighted average - protects rare classes)
- **Daily aggregate error** (% deviation in daily active minutes vs. reference)
- **Bout detection rate** (did we catch the walk episode at all?)
- **Confidence calibration** (ECE - do 70% confident predictions land ~70% accurate?)

### Acceptance Criteria

| Category | Threshold | Rationale |
|----------|-----------|-----------|
| Overall accuracy | Macro-F1 ≥ 82% | Gap closure: 60% (current) → 85% target |
| Per-class floor | All classes ≥ 72% recall | Rare behaviors matter (scratching, distress) |
| Daily aggregates | ≤ 25% error | Users see daily summaries, not windows |
| Calibration | ECE ≤ 12% | Confidence drives UX filtering |
| Breed/Size | No stratum < 75% F1 | Toy breeds historically problematic |

### Red Flags (Stop the trial)
- Any class below 60% recall
- Macro-F1 dropping vs. lab baseline
- Confidence scores consistently overconfident
- Toy/small breeds systematically misclassified (>30% error)

---

## Model B — Indoor/Outdoor Classifier

### Field Testing Protocol

**Test Design:**
- Real houses with real dogs (not static testing)
- **Transition-heavy protocol:** 15+ in/out cycles per dog per session
- Cover confuser environments:
  - Urban canyon (downtown areas)
  - Dense canopy (heavily treed yards)
  - Garage/porch (transitional spaces)
  - Vehicles (dog in car or bed)
  - Near windows (dog on couch by window)

**Ground Truth Sources:**
1. **Door sensors** (magnetic/timed entry detection)
2. **Observer logs** with timestamped state changes
3. **Time-aligned video** for ambiguous transitions
4. **Reference GNSS** (RTK base station for signal quality validation)

**Metrics Collection:**
- Per-class precision/recall/F1 (Indoor/Outdoor)
- **Balanced accuracy** (equal weight to both directions)
- **False-Indoor rate** - *critical safety metric*
- **False-Outdoor rate** - drives nuisance alerts
- **Transition latency** (seconds from true crossing to correct classification)
- **Flap rate** (spurious toggles when stationary)
- **Per-confuser accuracy** (urban, canopy, vehicle, transitional)

### Acceptance Criteria

| Category | Threshold | Rationale |
|----------|-----------|-----------|
| Overall | Balanced accuracy ≥ 91% | High bar for safety product |
| **Safety** | **False-Indoor ≤ 4%** | **Critical: missed escapes = liability** |
| Nuisance | False-Outdoor ≤ 8% | Drives unnecessary alerts/power use |
| Transitions | Latency ≤ 8 sec avg | Dog crossing boundary needs timely catch |
| Stability | Flap rate ≤ 1.8/hr | Prevents alert spam during rest |
| Confusers | All strata ≥ 85% balanced accuracy | Edge cases define real-world quality |

### Red Flags (Stop the trial)
- False-Indoor rate > 6% (immediate safety concern)
- Flap rate > 3/hr (notification fatigue)
- Any confuser stratum below 75%
- Transition latency > 15 sec (missed boundary breaches)

---

## Shared Field Testing Infrastructure

### Hardware Setup
- **Reference IMU:** ±g triaxial accelerometer on separate harness
- **GNSS reference:** RTK base station for signal truth (if available)
- **Door sensors:** Magnetic reed switches on test home entry points
- **Video sync:** Time-stamped 1080p capture of dog + environment
- **Collar variants:** Halo Collar 5 (production) + logging-enabled test units

### Session Protocol
1. **Pre-test:** Sync all clocks to NTP, verify sensor alignment
2. **Baseline:** 15 min indoor resting (establish stable indoor signal)
3. **Transitions:** 3x in/out cycles (walking pace)
4. **Transitional:** 10 min on porch/garage threshold
5. **Vehicle:** 15 min with dog in car (stationary) / car moving
6. **Free living:** 30 min unfettered activity (natural distribution capture)
7. **Post-test:** Download and verify all logs

### Data Collection Requirements
- Minimum 4 hours per dog per environment type
- 3+ dogs per breed group (toy, medium, large)
- 2+ houses per confuser environment
- All sessions logged with environmental metadata (canopy cover %, building type, etc.)

---

## Reporting Template

**Per Trial Report Must Include:**
- Session metadata (date, dog, environment, collar sn)
- Confusion matrices (overall + per-stratum)
- Key metrics vs. thresholds (color-coded)
- Worst N failure cases with raw signal + video
- Any red-flag violations
- Sign-off from: ML lead, Hardware lead, Product lead

**Per-Stratum Requirements:**
- Minimum 50 transitions per confuser type (GPS)
- Minimum 100 samples per rare behavior (Activity)
- Statistical significance: 95% CI must not cross threshold

---

## Threshold Rationale (Why These Numbers?)

### Activity Detection
- **74% baseline from literature** (peer-reviewed canine accelerometer studies)
- **82% target** reflects achievable gap closure with tight labeling
- **72% per-class floor** protects rare but important behaviors (distress, scratching)
- **25% daily aggregate error** aligns with user-perceivable accuracy

### GPS Indoor/Outdoor
- **91% overall** matches safety-product standards (vs. 85% for general use)
- **4% false-Indoor** = 1 in 25 boundary crossings could be missed (absolute maximum)
- **8 sec transition latency** = dog moving at walking pace (0.5 mph) crosses ~12 ft in 8 sec
- **Flap rate 1.8/hr** = ~1 false alarm per 10-hour wear day (acceptable nuisance rate)

---

## Next Steps to Finalize

1. **Confirm with Halo:** Are these thresholds acceptable for their product quality bars?
2. **Lock confuser environments:** Which 4-5 site types represent their install base?
3. **Define transition threshold timing:** Exact criteria for "crossing" detection
4. **Set up golden set:** Freeze 1000-window reference corpus for regression testing
5. **Identify field trial sites:** Minimum 2 contrasting locations for GPS model

---

*Draft for Halo review — propose we discuss thresholds in next steering review*