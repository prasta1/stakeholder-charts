# WS1: Pipeline & Inference Review

**Weeks 1–3 · Est. 1–2 weeks effort · Status: 🔲 Not started**

## Objective

Map the end-to-end inference pipeline and verify that the firmware implementation matches the offline (Python) pipeline exactly. The Python-to-C conversion shows only a 0.06% gap, so we don't expect a deployment bug — but we need to rule out any windowing, buffering, or preprocessing discrepancies that could explain the real-world accuracy drop.

## Key Questions

- Does the firmware's continuous-buffer approach match the offline sliding-window implementation?
- Are there timing or sampling rate inconsistencies between the 20Hz IMU stream and the 3.2-second (64-sample) windows?
- Is the Butterworth low-pass filter (0.3Hz cutoff) for gravity separation identical in both paths?
- Are all 50 features computed identically on-device vs. offline?

## Tasks

- [ ] Map end-to-end windowing & inference flow (Python → ONNX → STM32Cube.AI → firmware)
- [ ] Validate firmware vs. offline pipeline consistency on identical input data
- [ ] Run continuous-buffer test to isolate firmware vs. model contribution to accuracy gap
- [ ] Document all limits, assumptions, and handoff points
- [ ] Produce pipeline architecture diagram for `docs/architecture/`

## Acceptance Criteria

- Pipeline diagram reviewed and accepted by both teams
- Firmware vs. offline parity quantified (pass/fail with numerical delta)
- Any discrepancies documented as issues with severity rating
- Clear handoff to WS2 for orientation-specific analysis

## Dependencies

- Halo provides firmware source or detailed firmware documentation (Week 1)
- Halo provides raw IMU data samples for cross-validation
- Access to STM32 development environment or representative test harness

## Outputs

- `docs/architecture/pipeline-diagram.md`
- `docs/decisions/001-pipeline-parity-findings.md` (ADR if discrepancies found)
- Issues created for any identified gaps
