# Halo × Edge Impulse — PM Operating Model (Lifecycle Overlay)

*Last updated: 2026-06-25 · Owner: Patrick Ruster (Head of CS, Account Lead)*

This folder adds a **machine-learning lifecycle spine** on top of the existing workstream
structure. The workstreams (WS1–WS6, Phase 2 tracks) describe *the work*. The lifecycle
describes *the sequence the work has to move through to ship a model* — from raw data audit
and EDA all the way to on-device deployment and field monitoring.

It exists for one reason: **to make customer accountability legible.** Halo is a fast-moving,
high-value, occasionally hard-to-steer customer (the CEO has a documented tendency to route
decisions around the account team). The single biggest risk to this engagement is not the ML —
it's customer-side dependencies slipping silently: data that doesn't arrive, labels with no
shared standard, a named ML lead who never materializes. This operating model turns every one
of those dependencies into a dated, owned, visible line item.

---

## How the pieces fit together

You already have a working operating system. This overlay does not replace it — it sequences it.

| Artifact | Role | Lives in |
|---|---|---|
| **Engagement OS** (`Halo_ML_Engagement_OS.xlsx`) | Live operational tool — WBS, RACI, risks, decisions, status dashboard | Spreadsheet |
| **This lifecycle overlay** (`lifecycle/`) | The ML stage spine + customer-accountability register | Markdown (→ Notion later) |
| **Workstream folders** (`phase-1/`, `phase-2/`) | Detailed scope, tasks, acceptance criteria per workstream | Markdown |
| **Central Reference / Company Brief** | Deal context, contacts, relationship history | Markdown |
| **Experiments / ADRs / meeting-notes** | Evidence trail — what was tried, what was decided, what was said | Markdown |

Rule of thumb: **the spreadsheet is where you operate day-to-day; this overlay is where you
prove the engagement is on track and where you hold the customer to their commitments.**

> **Collaboration note:** every table below is built as a flat record set (one row = one record,
> stable header columns, no merged cells) so it ports directly into a Notion database when the
> team is ready to collaborate on it. See `MIGRATION-to-notion.md`.

---

## The parties

| Party | Who | Owns |
|---|---|---|
| **Edge Impulse** | Patrick Ruster (Account/CS lead), Teague Gudemann (AE), Yvonne (SE) | ML methodology, platform, evaluation rigor, the lifecycle |
| **Halo Collar** | Ken (CEO), Michael (CTO), Heather Berhalt (role TBD), *named ML lead — still owed* | Data, labeling standard & labelers, domain truth, business decisions |
| **Softeq** | Halo's engineering partner | Firmware / on-device integration, STM32 build, field telemetry |

The tripartite structure is exactly why accountability needs to be explicit: when three
organizations share a pipeline, an unowned dependency falls between them by default.

---

## The lifecycle spine

Ten stages. Each maps onto existing workstreams, names the **customer dependency that gates it**,
and ends in a **decision gate**. Stages overlap in time (this is iterative, not waterfall) — the
ordering is one of logical dependency, not strict calendar.

| # | Stage | What it answers | Maps to | Phase |
|---|---|---|---|---|
| 0 | **Scoping & Access** | Who owns what, is everyone provisioned? | Kickoff, RACI | P1 W1–2 |
| 1 | **Data Audit & Inventory** | What data exists, where, how was it captured? | WS1, WS3 | P1 W1–4 |
| 2 | **Exploratory Data Analysis** | What does the data actually look like? Where's the lab-to-field gap coming from? | WS2, WS6 | P1 W2–8 |
| 3 | **Label Quality & Taxonomy** | Are labels consistent? Is the class set learnable? | WS3 | P1 W3–8 |
| 4 | **Data Strategy & Collection** | How do we close the gaps EDA exposed? | WS3, P2 data-strategy | P1 W6 → P2 |
| 5 | **Feature & Model Exploration** | What DSP + architecture works? | WS6, WS5, P2 model-opt | P1 W5 → P2 |
| 6 | **Evaluation Framework** | How do we measure real-world truth, not lab truth? | WS4 | P1 W5–8 |
| 7 | **On-Device Integration** | Does it run on the STM32 collar, identically to offline? | WS1, P2 on-device | P1 W1–3 → P2 |
| 8 | **Field Testing & Validation** | Does it hold up across breeds, orientations, real dogs? | P2 field-testing | P2 W22–36 |
| 9 | **Deployment & Release** | Ship it — license, rollout, production gate | P2, deployment | Post-W36 |
| 10 | **Monitoring & Lifecycle** | Keep it good — field retraining, MLOps, handoff | P2 knowledge-transfer | P2 W28+ |

Detailed stage docs:

- [`01-data-audit-and-eda.md`](01-data-audit-and-eda.md) — Stages 1–2, the under-built part of the plan
- [`customer-accountability-tracker.md`](customer-accountability-tracker.md) — the wrangle tool
- [`MIGRATION-to-notion.md`](MIGRATION-to-notion.md) — how to lift this into a shared Notion workspace

---

## Where we are now (as of 2026-06-25)

Engagement started 2026-03-16, so this is roughly **Week 15** of a 16-week Phase 1. The
**Phase 1 → Phase 2 gate is ~Week 16 (target Jul 6)**. That makes the next two weeks the most
important accountability moment of the engagement: the gate readout to Ken and Michael is the
single biggest retention lever (per the Company Brief). Stages 1–3 should be substantially done;
Stage 6 (evaluation framework) and Stage 2 (EDA) findings are what the gate is judged on.

---

## Decision gates

Gates are where the engagement formally checks: *did the customer hold up their end, and is the
evidence good enough to proceed?* A gate that proceeds on missing customer inputs is how
engagements quietly fail.

| Gate | When | Question | Who signs |
|---|---|---|---|
| **G0 — Kickoff** | W1 | Access provisioned, named leads confirmed (incl. Halo ML lead) | Patrick + Michael |
| **G1 — Data ready** | W4 | Dataset + firmware docs delivered, inventoried, EDA started | Patrick + Michael + Softeq |
| **G2 — Phase 1 checkpoint** | W8 | Taxonomy proposed, eval framework drafted, EDA findings in | Patrick + Michael |
| **G3 — Phase 1 → 2 gate** | W16 | Exit criteria met, real-world accuracy 80–85% with path to 90% | Ken, Michael, Patrick, Teague |
| **G4 — First on-device candidate** | W20 | Model on test collar, parity validated | Patrick + Softeq + Michael |
| **G5 — Field validation** | W30 | Holds across breed categories | Patrick + Michael |
| **G6 — Deployment** | W36 | Production-ready, license terms agreed | Ken, Patrick, Teague |

Each gate has a one-line rule: **no required customer input = gate does not pass; slippage is
logged in the accountability tracker and surfaced at the next steering review.**

---

## Cadence

| Forum | Frequency | Attendees | Accountability function |
|---|---|---|---|
| **Technical sync** | Weekly | EI eng + Halo ML lead (+ Softeq as needed) | Review open customer dependencies; flag anything red |
| **Steering review** | Bi-weekly | Account leads + sponsors | Escalate slipped commitments; confirm gate readiness |
| **QBR** | Quarterly | Ken, Michael, Patrick, Teague | Strategic alignment, phase gates, renewal/expansion |
| **Ad-hoc escalation** | As needed | Patrick ↔ Michael (then Ken) | The defined channel — see escalation protocol below |

**Escalation protocol (the anti-"CEO-goes-around-the-team" mechanism):** technical and scope
decisions route Patrick ↔ Michael. If Ken raises something directly, it is acknowledged and
logged, then routed back through Michael + Patrick for a coordinated response before any
commitment is made. This is the lesson from the Albert episode, encoded as process. Document any
CEO-direct commitments in `docs/decisions/` immediately so nothing becomes an unrecorded promise.
