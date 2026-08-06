# WS2: Orientation Assumption Validation

**Weeks 1–5 · Est. 2–3 weeks effort · Status: 🔲 Not started**

## Objective

Quantify how much collar orientation variability contributes to the real-world accuracy gap. The technical response estimates orientation is a top contributor — this workstream validates that hypothesis and identifies which of the 50 features are most sensitive to rotation.

## Context

The current pipeline uses a Butterworth low-pass filter (0.3Hz cutoff) to separate gravity from dynamic motion. This approach assumes a relatively stable collar orientation. In practice, collars shift, rotate, and bounce — breaking gravity-based features that depend on consistent axis alignment.

## Key Questions

- Which of the 50 selected features degrade most under collar rotation?
- What is the distribution of real-world collar orientations across breeds and sizes?
- Can rotation-invariant alternatives (magnitude-based, quaternion-derived) maintain accuracy?
- What's the contribution of orientation vs. other factors (data diversity, class complexity)?

## Tasks

- [ ] Quantify collar orientation impact across all 50 features (sensitivity analysis)
- [ ] Design and run controlled rotation scenarios (field study or simulated)
- [ ] Rank features by orientation sensitivity — identify which break first
- [ ] Prototype rotation-invariant feature alternatives
- [ ] Produce findings report with recommendations for WS3 and WS6

## Acceptance Criteria

- Feature sensitivity ranking produced and reviewed
- Orientation impact quantified (estimated contribution to the 37-point gap)
- At least one rotation-invariant feature set prototyped and benchmarked
- Clear recommendations for feature engineering in WS6

## Dependencies

- WS1 pipeline mapping (partial — can start in parallel)
- Halo provides collar orientation metadata or raw IMU data with known orientations
- Access to multi-breed test data (or Halo arranges controlled data capture)

## Outputs

- `experiments/orientation-sensitivity-analysis.md`
- Feature sensitivity ranking table
- Rotation-invariant feature prototype results
- Recommendations for WS3 (data strategy) and WS6 (model exploration)
