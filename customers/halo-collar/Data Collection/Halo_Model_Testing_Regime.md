# Halo Collar — Structured Model Testing Regime

**Scope:** Two production models on the Halo Collar 5 platform — (A) **Activity Detection** (accelerometer/IMU-based canine behavior classification) and (B) **GPS Location / Indoor-Outdoor** (a classifier that infers whether the dog is **indoors vs. outdoors** from GNSS signal characteristics).
**Audience:** Cross-functional / QA (ML, hardware, QA, product).
**Phases covered:** Bench/offline evaluation → Field/in-the-wild → On-device/edge → Regression/ongoing.
**Status:** Draft outline for review. Thresholds marked *(TBD)* are placeholders to be ratified with the ML and hardware teams.

> Platform context (from public Halo materials): activity detection runs as on-collar AI signal processing over collar sensors; GPS uses L1+L5 dual-band, multi-constellation GNSS (GPS/GLONASS/Galileo) with Swift Navigation Skylark corrections (Precision+), analyzing location ~20×/sec with AlwaysOn tracking, AI obstacle/drift filtering, and ~48 hr battery. These constrain what "good" looks like and what must be tested on-device. See Sources at end.

---

## 1. Purpose & Guiding Principles

The regime exists to answer one question for each model, repeatably and defensibly: **is this model version safe and accurate enough to ship to a real dog on real hardware, and does it stay that way over time?**

Five principles govern every phase:

1. **Ground truth is the product.** No test is stronger than its labels. Every phase defines how truth is established (human annotation, reference-grade sensor, video, RTK base station) and its own error bar.
2. **Test the deployed artifact, not the notebook.** Offline accuracy is necessary but not sufficient; the quantized, on-collar model under real power/thermal/latency budgets is the object of record.
3. **Stratify by covariates, not just averages.** A single headline accuracy number hides failures on specific breeds, sizes, collar fit, environments, and satellite conditions. Acceptance is per-stratum, not just aggregate.
4. **Safety-weighted metrics.** For a containment/safety product, some errors cost more than others (a missed boundary breach ≫ a cosmetic activity misclassification). Metrics and gates are weighted accordingly.
5. **Everything is versioned and traceable.** Model version ↔ dataset version ↔ test run ↔ result ↔ sign-off. A shipped model can always be traced to the evidence that cleared it.

---

## 2. Shared Testing Framework (applies to both models)

### 2.1 Test phase model

| Phase | Question it answers | Environment | Gate |
|---|---|---|---|
| **Bench / offline** | Does the model generalize on held-out labeled data? | Cloud/dev, full-precision + quantized | Gate 1 |
| **On-device / edge** | Does the deployed artifact meet accuracy, latency, power, memory budgets on the collar? | Collar hardware / HIL rig | Gate 2 |
| **Field / in-the-wild** | Does it work on real dogs, in real environments, with real fit? | Controlled field trials | Gate 3 |
| **Regression / ongoing** | Does a new version regress vs. baseline; is the fleet drifting? | CI + production telemetry | Gate 4 (continuous) |

A model version must clear gates in order. A regression failure (Gate 4) can pull a version back to any prior gate.

### 2.2 Dataset governance

- **Splits:** Train / validation / **held-out test** (never touched during development) / **field-only test** (real-world, collected independently). Splits are **by dog and by session**, never by random window — windows from the same dog must not straddle splits (prevents leakage).
- **Versioning:** Each dataset is immutable and tagged (e.g., `activity-v3.2`, `gps-field-2026Q2`). Test results cite the exact dataset tag.
- **Representativeness matrix:** Every dataset is profiled against the covariate taxonomy (§2.3). Coverage gaps are documented as known limitations, not silently averaged over.
- **Ground-truth SLA:** Label source, annotator agreement (inter-rater κ for activity; reference-sensor error for GPS), and audit sampling rate are recorded per dataset.

### 2.3 Covariate / stratification taxonomy

Both models are evaluated *within* these strata, not just in aggregate:

- **Dog:** breed group, body mass/size, coat type, age, gait/mobility, neck circumference.
- **Fit:** collar tightness, vertical position/rotation on neck, hardware unit variance.
- **Environment:** open sky / suburban / dense urban / forest canopy / indoors / vehicle; weather; terrain.
- **Operating state:** battery level, temperature, firmware version, GNSS constellation availability, correction-service connectivity.

### 2.4 Roles, cadence & sign-off

- **Owners:** ML (metrics, offline), Hardware/Firmware (on-device), QA (field protocol, traceability), Product (acceptance gates).
- **Cadence:** Gate 1–2 on every candidate build; Gate 3 per release train; Gate 4 continuously (CI on every merge, fleet telemetry weekly).
- **Sign-off artifact:** A per-release **Model Test Report** with per-stratum results vs. thresholds, known limitations, and named approvers per gate.

### 2.5 Reporting & tooling

Standard outputs per run: metric tables (aggregate + per-stratum), confusion matrix, failure gallery (worst N cases with raw signal), and a pass/fail summary against the acceptance matrix. Results stored against the model+dataset version for longitudinal comparison.

### 2.6 Field-site selection

**Guiding rule:** test where the end users are. But that rule only reduces to a single location if the user base lives in a single location — and Halo's does not. Applied honestly to a geographically distributed install base, "test where the users are" *requires* multiple, deliberately contrasting field sites.

This matters most for the **indoor/outdoor model (Model B)**, which classifies environment from GNSS signal signatures. Those signatures are a direct function of the physical surroundings, so the same model behaves differently across regions:

- **Construction materials** — stucco over wire lath, concrete/masonry, and timber-frame homes attenuate and reflect GNSS very differently; a model calibrated on one can misread another.
- **Tree cover** — canopy density and species (evergreen vs. deciduous, seasonal leaf-off) change signal degradation, and heavy canopy can mimic an indoor signature outdoors.
- **Topography / built environment** — flat open suburb vs. hills vs. urban canyon changes satellite visibility and multipath.
- **Latitude / sky geometry** — affects satellite constellation visibility and typical fix quality.

**Selection procedure:**

1. **Start from the user distribution.** Pull install-base / telemetry location data and characterize where users actually are, by region and environment type — not by intuition.
2. **Map to the covariate matrix (§2.3).** Identify the distinct construction / canopy / terrain regimes that distribution spans.
3. **Choose a minimal covering set of sites** — the fewest field locations that together cover the important regimes, weighted toward where most users live. Coverage of signal conditions matters more than raw count of sites.
4. **Document coverage and gaps.** Any regime present in the user base but not in the test sites is logged in the known-limitations register (§5) with a risk rating.

**Failure mode this guards against:** single-geography validation cannot detect a model overfitting to that geography's signal profile. The error stays invisible until the model ships to a different region and starts throwing false-Indoor calls (the safety-critical error, §4.3) — i.e., the gap is in the *test*, not just the data. This subsection is why the field phases (A3, B3) are defined over a site matrix rather than a single location.

---

## 3. Model A — Activity Detection

### 3.1 Objective

Classify canine behavior from IMU/accelerometer windows into a defined activity taxonomy, accurately enough to drive health/wellness insights, walk logging, and activity trends — across breeds, sizes, and collar fit, on-device and in real time.

### 3.2 Activity taxonomy (to be ratified)

Working set: **rest/sleep, standing/idle, walking, running, playing, eating/drinking, scratching, and a "transition/other" reject class.** Barking/vocalization included only if a corroborating sensor supports it. The taxonomy, class definitions, and minimum bout durations must be frozen before dataset labeling — ambiguous boundaries (e.g., trotting vs. running) are the primary label-noise source.

### 3.3 Metrics

- **Primary:** per-class precision/recall/F1 and **macro-F1** (weights rare classes equally); confusion matrix.
- **Balanced accuracy** (guards against rest/sleep dominating the distribution).
- **Reject-class behavior:** false-accept rate into confident classes from "other."
- **Temporal/segment metrics:** bout-level detection (did we catch the walk?) and **daily aggregate error** (e.g., % error in daily active minutes) — the numbers users actually see.
- **Calibration:** reliability of confidence scores (ECE), since downstream logic may threshold on confidence.

### 3.4 Phase A1 — Bench / offline

- Evaluate on the held-out test set (dog- and session-disjoint), full-precision **and** quantized model.
- Report all §3.3 metrics **aggregate and per-stratum** (breed group, size, fit, activity intensity).
- **k-fold cross-validation by dog** to bound variance and expose small-cohort overfitting.
- **Robustness/ablation:** sensitivity to window length, sampling-rate reduction, sensor axis dropout, injected noise, and collar-rotation simulation.
- **Failure analysis:** worst-confused class pairs, per-stratum recall floors, mislabel audit of high-loss windows.
- **Gate 1 exit:** aggregate macro-F1 ≥ *(TBD)*, no single ratified class below recall *(TBD)*, no stratum below *(TBD)*, quantization degradation ≤ *(TBD)* absolute F1.

### 3.5 Phase A2 — On-device / edge

- Deploy the exact production artifact to the collar / HIL rig.
- **Parity check:** on-device inference matches offline predictions on an identical input corpus within *(TBD)* mismatch rate (catches quantization, preprocessing, and DSP-pipeline drift).
- **Budgets:** inference latency & throughput at required duty cycle, RAM/flash footprint, and **energy per inference / net battery impact** against the ~48 hr AlwaysOn target.
- **Real-time integrity:** no dropped windows under sustained sensor streaming; graceful behavior at low battery / thermal limits.
- **Gate 2 exit:** parity within tolerance; latency, memory, and power within budget on target hardware.

### 3.6 Phase A3 — Field / in-the-wild

- Controlled field trials: instrumented dogs across the covariate matrix, wearing collars normally, with **synchronized reference truth** — time-aligned video annotation and/or a reference-grade IMU/harness.
- Protocol specifies scripted activity circuits **plus** free-living capture to catch natural behavior distribution.
- Metrics: same as §3.3 computed against field truth; special attention to **daily aggregate error** and bout detection (the shipped experience).
- **Fit stress cases:** loose collar, high-rotation, small/toy breeds, heavy-coat dogs.
- **Gate 3 exit:** field macro-F1 and daily-active-minutes error within *(TBD)*; no safety-relevant misread pattern; per-stratum floors held.

### 3.7 Phase A4 — Regression / ongoing

- **CI regression suite:** every candidate re-scored on frozen golden set; **block merge** on any per-class or per-stratum regression beyond noise band *(TBD)*.
- **Fleet drift monitoring:** track prediction-distribution shifts and confidence-calibration drift from production telemetry; alert on divergence from release baseline.
- **Labeled-feedback loop:** sampled real-world misclassifications (user-flagged or audited) feed the next dataset version.
- **Re-test triggers:** firmware/DSP change, new hardware revision, taxonomy change, or drift alert re-enters the appropriate gate.

### 3.8 Activity Detection — acceptance matrix (skeleton)

| Metric | Gate 1 (offline) | Gate 2 (device) | Gate 3 (field) | Gate 4 (regression) |
|---|---|---|---|---|
| Macro-F1 | ≥ *(TBD)* | parity ± *(TBD)* | ≥ *(TBD)* | no drop > *(TBD)* |
| Worst-class recall | ≥ *(TBD)* | — | ≥ *(TBD)* | no drop > *(TBD)* |
| Worst-stratum F1 | ≥ *(TBD)* | — | ≥ *(TBD)* | stable |
| Daily active-minutes error | — | — | ≤ *(TBD)* % | stable |
| Latency / mem / power | — | ≤ budget | — | ≤ budget |

---

## 4. Model B — GPS Location (Indoor vs. Outdoor Classifier)

### 4.1 Objective

Classify the dog's environment as **indoors vs. outdoors** from GNSS signal characteristics (e.g., satellites tracked/used, carrier-to-noise C/N0 distribution, fix quality/HDOP, L1 vs. L5 signal presence, multipath indicators), accurately enough to inform containment logic, location-confidence, and GPS duty-cycle/power management — across building and environment types, on-device and in real time, with stable (non-flapping) transitions.

> **The task is classification, not positioning.** Ground truth is the true indoor/outdoor state, not a coordinate. The core difficulty is that **degraded outdoor conditions (urban canyon, dense canopy, under eaves, inside a vehicle) produce indoor-like GNSS signatures** — these confusers, not open-sky cases, decide whether the model is good.

### 4.2 Class definition

Working set: **Outdoor / Indoor**, plus a decision on how to handle the ambiguous middle — **Vehicle** and **Sheltered/transitional** (porch, garage, dense canopy) either as explicit classes or as documented members of one side of the binary. The class boundary (e.g., is an open garage "indoor"?) must be frozen before labeling, since it defines what "correct" even means and is the dominant source of label disagreement.

### 4.3 Metrics

- **Primary:** per-class precision/recall/F1, **balanced accuracy**, and the confusion matrix (the Indoor↔Outdoor confusion cells are the whole story).
- **Safety-weighted errors** — the two directions are not equal:
  - **False-Indoor (misses that the dog is outside):** highest cost — could suppress a boundary/escape alert while the dog is actually out. Treated as the safety-critical error.
  - **False-Outdoor (thinks outside while indoors):** lower cost but drives nuisance alerts and wasted power/duty-cycle.
- **Transition behavior:** detection **latency** on genuine in→out / out→in crossings, and **flap/hysteresis rate** (spurious state toggles while stationary). A model can be accurate per-window yet unusable if it chatters at thresholds.
- **Confidence calibration** (ECE), since downstream logic may gate on classifier confidence.
- **Per-confuser recall:** accuracy specifically within urban-canyon, canopy, vehicle, and near-window/eaves cases.

### 4.4 Phase B1 — Bench / offline

- Evaluate on a held-out set of labeled GNSS-feature windows, **split by dog and by site/building** (no window from the same location in both train and test — prevents memorizing a specific house).
- Full-precision **and** quantized model; report §4.3 metrics **aggregate and per-stratum** (building/construction type, environment, vehicle, transition vs. steady-state).
- **Confuser-focused evaluation:** dedicated slices for urban canyon, dense canopy, garage/porch, and in-vehicle — the cases that manufacture false-Indoor errors.
- **Robustness/ablation:** sensitivity to window length, reduced satellite visibility, C/N0 degradation, and L5 dropout (L1-only fallback).
- **Gate 1 exit:** balanced accuracy ≥ *(TBD)*; **false-Indoor rate ≤ *(TBD)* (safety)**; no confuser-stratum recall below *(TBD)*; quantization degradation ≤ *(TBD)*.

### 4.5 Phase B2 — On-device / edge

- Run the exact production classifier on the collar / HIL rig against a fixed feature corpus.
- **Parity check:** on-device predictions match offline within *(TBD)* mismatch rate (catches quantization + feature-extraction drift).
- **Budgets:** inference latency at required cadence, RAM/flash footprint, and **energy per classification / net battery impact** — note the classifier's *output* may itself drive GNSS duty-cycle, so measure its effect on the ~48 hr AlwaysOn budget.
- **Real-time transition integrity:** verify hysteresis/debounce logic behaves on-device; no state chatter under sustained input.
- **Gate 2 exit:** parity within tolerance; latency, memory, power within budget; transition-smoothing verified on hardware.

### 4.6 Phase B3 — Field / in-the-wild

- Real dogs moving **in and out of real homes/buildings**, with independent ground truth — synchronized observer logs, **door/threshold sensors**, and/or time-aligned video marking true indoor/outdoor state and crossing timestamps.
- Protocol is **transition-heavy by design:** repeated entries/exits, dwell indoors near windows, time on porches/garages, and time in vehicles — plus free-living capture for natural distribution.
- Environment coverage spans the confuser matrix (urban canyon, canopy, construction types).
- Metrics: §4.3 against field truth, with **false-Indoor rate and transition latency** as the headline numbers.
- **Gate 3 exit:** field balanced accuracy ≥ *(TBD)*; **false-Indoor rate ≤ safety threshold *(TBD)***; transition latency ≤ *(TBD)* with flap rate ≤ *(TBD)*; per-confuser floors held.

### 4.7 Phase B4 — Regression / ongoing

- **CI regression:** re-score the frozen golden set (incl. the confuser slices) on every model/feature change; **block** on false-Indoor or per-stratum regression beyond noise band *(TBD)*.
- **Fleet drift monitoring:** track indoor/outdoor prediction ratios, confidence calibration, and flap frequency vs. release baseline; alert on divergence (e.g., a firmware change quietly shifting the C/N0 distribution).
- **Labeled-feedback loop:** sampled field disagreements (user-flagged escapes, contradictory location context) feed the next dataset version.
- **Re-test triggers:** GNSS firmware/feature change, antenna/hardware revision, class-definition change, or a fleet drift/flap alert re-enters the appropriate gate.

### 4.8 Indoor/Outdoor Classifier — acceptance matrix (skeleton)

| Metric | Gate 1 (offline) | Gate 2 (device) | Gate 3 (field) | Gate 4 (regression) |
|---|---|---|---|---|
| Balanced accuracy | ≥ *(TBD)* | parity ± *(TBD)* | ≥ *(TBD)* | no drop > *(TBD)* |
| **False-Indoor rate** | **≤ *(TBD)* (safety)** | — | **≤ *(TBD)* (safety)** | **no worsen** |
| False-Outdoor rate | ≤ *(TBD)* | — | ≤ *(TBD)* | stable |
| Worst-confuser recall | ≥ *(TBD)* | — | ≥ *(TBD)* | stable |
| Transition latency | — | — | ≤ *(TBD)* | stable |
| Flap / hysteresis rate | — | ≤ *(TBD)* | ≤ *(TBD)* | stable |
| Latency / mem / power | — | ≤ budget | — | ≤ budget |

---

## 5. Cross-Cutting Concerns

- **Traceability spine:** model version ↔ dataset tag ↔ test run ID ↔ result set ↔ gate sign-off, queryable end-to-end.
- **Golden sets:** frozen, versioned offline + replay corpora that define "no regression"; expanded (never quietly edited) as blind spots are found.
- **Combined-system checks:** the two models interact — the indoor/outdoor state may gate GNSS duty cycle, and activity/motion may inform the environment classifier. Add integration tests so their combined behavior (and any feedback loop between them) is validated together, not only in isolation.
- **Known-limitations register:** every uncovered stratum or scenario is logged as an explicit limitation with risk rating — the honest boundary of what's been validated.

## 6. Open Questions / Assumptions to Confirm

1. **Final activity taxonomy** (Model A) and per-class minimum bout durations.
2. **Indoor/outdoor class definition** (Model B) — how Vehicle and Sheltered/transitional (porch, garage, canopy, open eaves) are handled: explicit classes or assigned to one side of the binary.
3. **Input feature set** for the indoor/outdoor model — which GNSS-derived signals (C/N0 stats, satellite counts, HDOP, L1/L5 presence, multipath indicators) are used, since the test data schema follows from this.
4. **Ground-truth method** per model (video vs. reference IMU for activity; observer logs / door sensors / video for indoor-outdoor) and their assumed error bars.
5. **Numeric thresholds** for every *(TBD)* — the quantitative heart of the regime; needs ML + hardware + product ratification.
6. **Safety weighting** — the explicit cost ratio of false-Indoor vs. false-Outdoor, and of safety-relevant activity misreads.
7. **Field trial scale** — how many dogs/sessions/buildings per stratum for statistical power.
8. **Edge deployment target** — exact hardware/firmware and Edge Impulse pipeline the on-device gate runs against.

---

*Sources for platform grounding:*
- [How Halo Collar Works & Product Features](https://www.halocollar.com/features/)
- [Halo Collar 5 debuts Precision+ (L1+L5, Swift Skylark)](https://www.prnewswire.com/news-releases/halo-collar-5-debuts-precision-bringing-autonomous-vehiclegrade-gps-accuracy-to-dog-safety-302743805.html)
- [Halo Collar Launches Collar 5 with AlwaysOn GPS](https://www.petage.com/halo-health-launches-collar-5-app-alwayson-gps-tracking-capabilities/)
- [Enhanced Location Accuracy for Pet GPS Trackers](https://www.halocollar.com/blog/dog-safety/why-precision-matters-enhanced-location-accuracy-that-cuts-false-alerts-and-builds-trust/)
