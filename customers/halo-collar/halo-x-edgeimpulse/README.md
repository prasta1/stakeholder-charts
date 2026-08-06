# Halo Collar × Edge Impulse

**Pet Activity Detection — 12-Month Engagement**

> Real-world accuracy from ~60% to 90%+ on STM32 smart collar

---

## The Problem

Halo's dog activity classification model achieves 97.6% accuracy in controlled lab conditions but drops to ~60% in the real world — a 37-point gap. The Python-to-C conversion pipeline has been verified correct (0.06% gap). This is a **train-test distribution mismatch**, primarily driven by collar orientation variability, limited behavioral diversity in training data, and class taxonomy complexity.

## Engagement Structure

| | Weeks | Investment | Focus |
|---|---|---|---|
| **Phase 1** | 1–16 | $66,500 | Understand, restructure, build foundations |
| **Phase 2** | 17–36 | $66,500 | Optimize, validate, deploy |
| **Deployment** | Post-36 | $8K–$30K | One-time license, scaled to device volume |

## Success Criteria

| Metric | Current | Phase 1 Target | Phase 2 Target |
|---|---|---|---|
| Real-world accuracy | ~60% | 80–85% | 90%+ |
| Collar orientation | Brittle | Measurably improved | Rotation-invariant |
| Cloud-to-device parity | Unvalidated | Validated | Production-ready |
| Model footprint | 51KB / 1.1KB | Within STM32 budget | Optimized |

---

## Repo Structure

```
halo-x-edgeimpulse/
├── README.md                  ← You are here
├── docs/
│   ├── architecture/          ← System diagrams, pipeline docs
│   └── decisions/             ← ADRs (Architecture Decision Records)
├── phase-1/
│   ├── ws1-pipeline-review/
│   ├── ws2-orientation-validation/
│   ├── ws3-class-simplification/
│   ├── ws4-evaluation-framework/
│   ├── ws5-application-logic/
│   └── ws6-model-exploration/
├── phase-2/
│   ├── data-strategy/
│   ├── model-optimization/
│   ├── on-device-integration/
│   ├── field-testing/
│   └── knowledge-transfer/
├── milestones/                ← Milestone reports and review artifacts
├── meeting-notes/
│   ├── weekly-syncs/
│   ├── steering-reviews/
│   └── qbrs/
├── data/                      ← Data dictionaries, schemas (not raw data)
├── experiments/               ← Experiment logs and results
└── .github/
    └── ISSUE_TEMPLATE/        ← Standardized issue templates
```

## Phase 1 Workstreams (Weeks 1–16)

These run in parallel. Findings from each feed into the others through experiment-evaluate-refine cycles.

| WS | Name | Weeks | Est. Effort | Status |
|---|---|---|---|---|
| WS1 | [Pipeline & Inference Review](phase-1/ws1-pipeline-review/) | 1–3 | 1–2 wk | 🔲 Not started |
| WS2 | [Orientation Assumption Validation](phase-1/ws2-orientation-validation/) | 1–5 | 2–3 wk | 🔲 Not started |
| WS3 | [Class Simplification & Data Strategy](phase-1/ws3-class-simplification/) | 3–8 | 3–6 wk | 🔲 Not started |
| WS4 | [Evaluation Framework Redesign](phase-1/ws4-evaluation-framework/) | 5–8 | 2–3 wk | 🔲 Not started |
| WS5 | [Application-Level Logic](phase-1/ws5-application-logic/) | 8–16 | 2–4 wk | 🔲 Not started |
| WS6 | [Model & Feature Exploration](phase-1/ws6-model-exploration/) | 5–16 | 4–8 wk | 🔲 Not started |

### Phase 1 Exit Criteria

- Real-world accuracy at 80–85% with clear path to 90%+
- Orientation robustness measurably improved
- Cloud-to-device parity validated
- Simplified class taxonomy proven
- Evaluation framework in place with real-world test harness

## Phase 2 Workstreams (Weeks 17–36)

| Name | Weeks | Status |
|---|---|---|
| [Expanded Data Strategy](phase-2/data-strategy/) | 17–28 | 🔲 Not started |
| [Model Optimization](phase-2/model-optimization/) | 17–30 | 🔲 Not started |
| [On-Device Integration](phase-2/on-device-integration/) | 20–32 | 🔲 Not started |
| [Field Testing & Validation](phase-2/field-testing/) | 22–36 | 🔲 Not started |
| [Knowledge Transfer](phase-2/knowledge-transfer/) | 28–36 | 🔲 Not started |

### Phase 2 Exit Criteria

- Real-world accuracy at 90%+
- Production-ready model deployed on STM32 collar
- Cloud-to-device parity fully validated
- Halo team self-sufficient on Edge Impulse platform
- Deployment license terms finalized

---

## Key Milestones

| Week | Date (est.) | Milestone | Deliverable |
|---|---|---|---|
| W1 | Mar 16, 2026 | Kickoff | Signed SOW, access provisioned |
| W2 | Mar 23 | Data handoff | Halo delivers raw dataset + firmware docs |
| W4 | Apr 13 | Early indicators | WS1/WS2 initial findings report |
| W8 | May 11 | Phase 1 checkpoint | Class taxonomy proposal, eval framework draft |
| W12 | Jun 8 | QBR #1 | Phase 1 progress review with leadership |
| W16 | Jul 6 | Phase 1 → Phase 2 gate | Phase 1 exit criteria reviewed |
| W20 | Aug 3 | First on-device candidate | Model deployed to test collar |
| W26 | Sep 14 | QBR #2 | Phase 2 mid-point review |
| W30 | Oct 12 | Field testing complete | Validation results across breed categories |
| W34 | Nov 9 | Knowledge transfer done | Halo team independently operating |
| W36 | Nov 23 | Engagement close | Final report, deployment license finalized |

## Collaboration Cadence

| Meeting | Frequency | Attendees | Purpose |
|---|---|---|---|
| Technical sync | Weekly | EI engineering + Halo ML lead | Hands-on progress, blockers, decisions |
| Steering review | Bi-weekly | Account leads + project sponsors | Progress vs. plan, risk escalation |
| QBR | Quarterly | Leadership (Ken, Michael, Patrick, Teague) | Strategic alignment, phase gates |
| Ad-hoc | As needed | Varies | Escalation path for blockers |

## Team

### Edge Impulse
- **Patrick Ruster** — Head of CS, Account Lead
- **Teague Gudemann** — Account Executive
- **Yvonne** — Solutions Engineer

### Halo Collar
- **Ken** — CEO
- **Michael Ehrman** — CTO
- **Heather Berhalt** — TBD role
- ⚠️ Named ML/embedded lead needed by Week 1

---

## How to Use This Repo

1. **Track work** — Each workstream folder has a README with scope, tasks, and acceptance criteria. Create issues using the templates in `.github/ISSUE_TEMPLATE/`.
2. **Document decisions** — Use `docs/decisions/` for ADRs. Number them sequentially (e.g., `001-class-taxonomy-simplification.md`).
3. **Log experiments** — Use `experiments/` to track what was tried, what worked, what didn't.
4. **Capture meetings** — Drop notes in `meeting-notes/` by type. Use the template.
5. **Update status** — Update workstream READMEs and the main table above as work progresses.
