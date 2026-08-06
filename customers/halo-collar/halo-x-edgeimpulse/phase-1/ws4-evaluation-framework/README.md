# WS4: Evaluation Framework Redesign

**Weeks 5–8 · Est. 2–3 weeks effort · Status: 🔲 Not started**

## Objective

Build an evaluation framework that measures real-world performance, not just lab accuracy. The current 97.6% lab number is misleading because the test set doesn't represent deployment conditions. We need metrics that reflect what users actually experience.

## Key Questions

- What KPIs matter to Halo's product experience (not just classification accuracy)?
- How do we construct a representative real-world test set?
- What per-class precision/recall targets are acceptable?
- How do we track regression as models evolve?

## Tasks

- [ ] Define real-world KPIs (accuracy, latency, transition smoothness, etc.)
- [ ] Build evaluation harness with automated confusion matrix tracking
- [ ] Set per-class precision/recall targets (agreed with Halo)
- [ ] Construct real-world test set (held out from training)
- [ ] Establish baseline measurements on real-world test set
- [ ] Document evaluation methodology for reproducibility

## Acceptance Criteria

- Evaluation harness running and producing automated reports
- Real-world test set constructed and baselined
- Per-class targets agreed with Halo product team
- Baseline results documented (this becomes the Phase 1 starting line)

## Dependencies

- WS3 class taxonomy finalized (at least draft)
- Real-world data available from Halo or collection campaigns
- WS1 pipeline understanding (to ensure eval matches deployment conditions)

## Outputs

- Evaluation harness (code + config)
- Baseline performance report
- Per-class target agreement document
- `docs/decisions/XXX-evaluation-methodology.md` (ADR)
