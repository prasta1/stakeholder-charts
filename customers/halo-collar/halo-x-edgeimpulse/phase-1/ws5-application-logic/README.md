# WS5: Application-Level Logic

**Weeks 8–16 · Est. 2–4 weeks effort · Status: 🔲 Not started**

## Objective

Design post-classification logic that smooths raw model outputs into reliable activity reports. Even a good model produces noisy frame-by-frame predictions — application logic handles transitions, confidence thresholds, and edge cases like head shaking that cause "classification explosions."

## Key Questions

- What temporal smoothing approach works best for 3.2-second classification windows?
- What confidence threshold balances accuracy vs. responsiveness?
- How should the state machine handle impossible transitions (e.g., rest → run in one window)?
- How do we handle the "unknown" or low-confidence case in the user experience?

## Tasks

- [ ] Design temporal smoothing (multi-window gating / majority voting)
- [ ] Implement confidence thresholding for uncertain predictions
- [ ] Build activity transition state machine
- [ ] Address "random classification explosions" (head shaking, collar adjustment)
- [ ] Test smoothing impact on evaluation metrics
- [ ] Document application logic design for Halo firmware team

## Acceptance Criteria

- Temporal smoothing demonstrably reduces false transitions
- Confidence thresholding eliminates low-quality predictions without excessive "unknown" rate
- State machine handles edge cases documented by Halo
- Net accuracy improvement quantified on real-world test set

## Dependencies

- WS4 evaluation framework (to measure impact)
- WS6 initial model outputs (to test against)
- Halo product input on acceptable UX tradeoffs (latency vs. accuracy)

## Outputs

- Application logic design document
- State machine specification
- Before/after evaluation comparison
- Implementation guide for Halo firmware integration
