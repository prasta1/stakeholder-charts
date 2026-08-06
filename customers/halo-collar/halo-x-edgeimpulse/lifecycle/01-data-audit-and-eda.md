# Stages 1–2: Data Audit & Exploratory Data Analysis

*The part of the plan that was thin. This is where the lab-to-field gap gets diagnosed before
anyone touches a model. Owner: Yvonne (SE) + Halo ML lead · Maps to WS2, WS3, WS6.*

The headline problem — 97.6% lab accuracy collapsing to ~60% in the field — is a **data
problem until proven otherwise.** The Python→C conversion is already validated (0.06% gap), so
the 37-point drop lives in the data and the labels, not the deployment math. EDA is how we find
*which* data problem. Skipping or rushing this stage is how teams waste Phase 2 optimizing a
model against a flawed target.

---

## Stage 1 — Data Audit & Inventory

**Goal:** know exactly what data exists, where it came from, and whether it's trustworthy —
before analyzing it. Register everything in `data/README.md` (the dataset registry).

### Checklist

- [ ] Inventory every dataset: source, size, date range, device/firmware version, sample rate
- [ ] Capture provenance: who collected each batch, how, under what protocol (links to C5)
- [ ] Confirm sensor config: IMU axes, units, 20 Hz rate, 3.2 s / 64-sample windows
- [ ] Map the label source: who labeled each batch, with what tool, to what definition
- [ ] Identify lab vs. field subsets — tag each record so the two can be compared in Stage 2
- [ ] Flag gaps: breeds, sizes, behaviors, collar orientations under- or un-represented
- [ ] Quarantine anything with unknown provenance — do not let it silently enter training

### Customer dependencies

Gated by **C3** (raw dataset + metadata), **C4** (firmware docs), **C5** (collection process).
If metadata is missing, that *is* a finding — record it; uncharacterized data is a root-cause candidate.

### Output

`data/README.md` populated · a one-page **Data Inventory & Provenance memo** · gaps logged as issues.

---

## Stage 2 — Exploratory Data Analysis

**Goal:** characterize the data and locate the source(s) of the lab-to-field gap. Every analysis
below should be run **split by lab vs. field** — the comparison is the whole point.

### 2.1 Distribution & quality profiling

- [ ] Per-axis accelerometer distributions (mean, variance, range) — lab vs. field
- [ ] Signal magnitude area / vector magnitude distributions per class
- [ ] Missing samples, dropouts, clipping, saturation, duplicate windows
- [ ] Sampling-rate stability — is 20 Hz actually 20 Hz in the field?
- [ ] Gravity/orientation component after the 0.3 Hz Butterworth low-pass — does separation hold in field data?

### 2.2 Class balance & separability

- [ ] Class frequency per subset — is the field set even covering the same behaviors?
- [ ] Per-class feature distributions; which classes overlap in feature space?
- [ ] Dimensionality reduction (PCA / t-SNE / UMAP) of the 50-feature vector — do lab and field clusters separate? (If lab and field form distinct clusters, that's the distribution shift, visualized.)
- [ ] Confusion-prone pairs (e.g. walk vs. run, active vs. play) — quantify overlap

### 2.3 Orientation diagnostics (the leading hypothesis — WS2)

- [ ] Distribution of inferred collar orientation across samples — lab vs. field
- [ ] Accuracy / feature stability as a function of orientation
- [ ] Is the field set simply seeing orientations the training set never did?
- [ ] Test rotation-invariance ideas (orientation normalization, augmentation) as EDA probes

### 2.4 Label-quality EDA (feeds Stage 3 — the highest-leverage analysis)

- [ ] Inter-annotator agreement where any clips were multiply labeled (Cohen's/Fleiss' κ) — gated by **C8**
- [ ] Per-labeler distributions — does one labeler's "play" = another's "active"?
- [ ] Suspicious-label detection: windows whose features are far from their class centroid
- [ ] Estimate the **label-noise ceiling**: realistic accuracy given current label consistency

### 2.5 Realistic-target framing

Peer-reviewed single-collar accelerometer behavior classification lands around **74% overall
across ~9 behaviors**, with wide per-behavior variance ([Kumpulainen et al., *Animals* 2021](https://www.mdpi.com/2076-2615/11/6/1549)).
Use EDA to place Halo's target inside that envelope: a simplified taxonomy + tight labels pushes
toward the top of the range; the current loose-label setup sits near the bottom. This reframes
"why not 97%?" with the customer using evidence, not opinion.

### Customer dependencies

Gated by **C3** (field-representative data) and **C8** (multiply-labeled clips for IAA). If no
field data exists yet, that is itself the finding — and it makes the case for the Stage 4 collection campaigns.

### Outputs

- **EDA findings report** — `docs/architecture/` or `experiments/` — the spine of the Phase 1 gate (G3) readout
- Root-cause ranking: orientation shift vs. label noise vs. coverage gaps vs. capture issues, with evidence weight each
- ADR in `docs/decisions/` recommending the fix path (taxonomy, collection, augmentation)
- Issues feeding Stage 3 (taxonomy/labeling) and Stage 4 (data strategy)

---

## How EDA gates the rest of the lifecycle

EDA is the fork in the road. Its findings decide what Phase 2 actually does:

| If EDA shows… | Then the priority becomes… | Stage |
|---|---|---|
| Lab/field clusters separate by orientation | Rotation-invariance + orientation-balanced collection | 4, 5 |
| Low inter-annotator agreement | Labeling standard first; everything else waits | 3 |
| Field set missing breeds/behaviors | Targeted collection campaigns | 4 |
| Capture-side issues (rate, dropouts) | Fix firmware/capture before more data | 1, 7 |
| Classes inherently overlap | Simplify taxonomy | 3 |

The discipline: **do not enter heavy model exploration (Stage 5) until EDA has ranked the root
causes.** Optimizing a model against noisy labels or a biased dataset is how you burn Phase 2 and
arrive at the renewal with nothing to show.
