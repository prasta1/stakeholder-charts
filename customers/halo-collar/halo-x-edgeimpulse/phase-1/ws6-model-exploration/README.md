# WS6: Model & Feature Exploration

**Weeks 5–16 · Est. 4–8 weeks effort · Status: 🔲 Not started**

## Objective

Explore model architectures and feature engineering strategies that improve real-world accuracy. The current ResNet-MLP with FocalLoss uses 50 features selected from 420+ candidates. This workstream tests whether better architectures, better features, or better augmentation can close the gap.

## Context

Current approach: 6-axis IMU → Butterworth gravity separation → 420+ feature candidates → Random Forest importance selection → 50 features → ResNet-MLP with FocalLoss → 5-fold CV → ONNX → STM32Cube.AI. Deployed on STM32 with 51KB model / 1.1KB RAM budget.

## Key Questions

- Do end-to-end architectures (1D CNN, TCN) outperform the hand-crafted feature pipeline?
- What's the best augmentation strategy for orientation robustness?
- Can EON Tuner find architectures that fit the STM32 constraints and improve accuracy?
- Which features from WS2 findings should be replaced with rotation-invariant alternatives?

## Tasks

- [ ] Implement spatial rotation augmentation strategies
- [ ] Benchmark architectures: 1D CNN, TCN, Transformer (within STM32 budget)
- [ ] Run EON Tuner for hardware-aware architecture search
- [ ] Review and revise current two-level augmentation approach
- [ ] Integrate rotation-invariant features from WS2 findings
- [ ] Per-class accuracy refinement for weak classes
- [ ] Document all experiments with configs and results

## Acceptance Criteria

- At least 3 architectures benchmarked against current baseline
- Best-performing approach identified with reproducible results
- Model fits within STM32 memory constraints (51KB flash, 1.1KB RAM)
- Measurable accuracy improvement on real-world test set (from WS4)

## Dependencies

- WS2 orientation findings (inform feature engineering direction)
- WS3 simplified class taxonomy (defines model output space)
- WS4 evaluation framework (standardized benchmarking)
- Halo provides STM32 memory/latency constraints documentation

## Outputs

- `experiments/` — logged results for every architecture and feature set tried
- Architecture comparison report
- Recommended model for Phase 2 optimization
- `docs/decisions/XXX-model-architecture-selection.md` (ADR)
