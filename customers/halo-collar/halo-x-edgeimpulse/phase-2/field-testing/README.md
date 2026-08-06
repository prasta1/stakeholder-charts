# Field Testing & Validation

**Weeks 29–34 · Status: 🔲 Not started**

## Objective

Validate the deployed model against real dogs in real environments. This is the ultimate accuracy check — does the system actually work when a dog is wearing the collar at home, at the park, on a walk?

## Tasks

- [ ] Define field test protocol (breeds, environments, activities, duration)
- [ ] Recruit test cohort (target breed/size diversity)
- [ ] Deploy firmware to test devices
- [ ] Collect field data with ground-truth labels (video annotation)
- [ ] Evaluate field accuracy against per-class targets
- [ ] Identify and document failure modes
- [ ] Iterate on model/logic based on field findings

## Acceptance Criteria

- Field test covers minimum breed/size diversity targets
- Real-world accuracy meets 90%+ target on core classes
- Failure modes documented with remediation plan
- Results reproducible and traceable to specific firmware version

## Dependencies

- On-device integration complete (model running on STM32)
- Halo coordinates field test logistics (devices, dog owners)
- Evaluation framework from Phase 1 WS4

## Notes

_Detailed scope defined at Phase 1 → Phase 2 gate._
