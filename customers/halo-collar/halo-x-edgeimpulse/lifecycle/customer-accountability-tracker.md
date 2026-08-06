# Customer Accountability Tracker — Halo (and Softeq)

*The "wrangle" tool. Last updated: 2026-06-25 · Owner: Patrick Ruster*

## Why this exists

This engagement's success is gated less by Edge Impulse's ML work than by **customer-side
inputs arriving, on time, to a usable standard.** The model cannot be better than the labels;
the pipeline cannot be validated without firmware docs; field testing cannot happen without
collars and dogs. Every one of those is owned by Halo or Softeq, not by EI.

This register makes each customer obligation a **dated, named, visible line item tied to the
lifecycle stage it gates.** When something slips, the downstream gate flips to blocked and the
slip is on the record — surfaced at the next steering review, not discovered at the QBR.

**How to run it:**
1. Review before every weekly technical sync. Anything `At risk` / `Blocked` / `Overdue` is the agenda.
2. Each line has a single **named** owner on the customer side — not "Halo," a person.
3. When a line slips, fill **Slipped on** and **Escalation** and raise it Patrick → Michael.
4. A gate (see `README.md`) does **not** pass while any of its required inputs are open.

**Status key:** 🔲 Not started · 🔄 In progress · ✅ Done · ⚠️ At risk · ⛔ Blocked/Overdue

---

## A. Foundational commitments (Stages 0–1)

| ID | Commitment (what Halo/Softeq owes) | Stage | Owner | Due | Status | Blocks if missing | Escalation |
|---|---|---|---|---|---|---|---|
| C1 | Name a dedicated Halo ML / embedded lead (single technical point of contact) | 0 | Ken / Michael | W1 | ⚠️ | Everything — no counterpart = no decisions, no data context | Raise at steering; this is the #1 open structural risk |
| C2 | Provision EI Studio access; confirm Albert removed and access stuck | 0 | Michael | W1 | 🔄 | Account hygiene; relationship landmine | Patrick → Michael |
| C3 | Deliver raw accelerometer/IMU dataset with capture metadata (device, firmware ver, sample rate, orientation) | 1 | Michael | W2 | 🔄 | Stages 1–6; no data = no audit, no EDA, no model | Patrick → Michael, log slip |
| C4 | Deliver firmware source **or** detailed firmware docs (windowing, buffering, filter, feature compute) | 1/7 | Softeq | W2 | 🔄 | WS1 pipeline parity; can't rule out deployment bug | Patrick → Michael → Softeq |
| C5 | Document the current data-collection process (who captures, how, where stored) | 1 | Michael | W3 | 🔲 | Stage 4 data strategy; root-cause of capture issues | Surface at sync |

## B. The labeling commitments — the highest-leverage lines (Stages 2–3)

> Per the "Wrangling Halo" messaging: **model quality is capped by label quality.** Labels
> currently come from a loose, uncoordinated group with no shared standard. These five lines are
> the difference between a 60%-ceiling and a credible path to 90%. Treat as critical.

| ID | Commitment | Stage | Owner | Due | Status | Blocks if missing | Escalation |
|---|---|---|---|---|---|---|---|
| C6 | Agree one written definition per behavior class (rest/walk/run/eat/play…) | 3 | Halo ML lead | W4 | 🔲 | Taxonomy (WS3); all label work | Critical — Patrick → Michael |
| C7 | Publish written labeling guidelines all labelers follow | 3 | Halo ML lead | W5 | 🔲 | Consistent labels; eval validity | Critical |
| C8 | Run inter-annotator agreement spot-checks (2 labelers, same clips, compare) | 3 | Halo ML lead | W6 | 🔲 | Quantifies the label-noise ceiling | Critical — feeds G2 |
| C9 | Consolidate labeling to the shared standard (retrain/realign the labeler group) | 3/4 | Halo ML lead | W8 | 🔲 | Quality of all future training data | Critical |
| C10 | Sign off on the simplified class taxonomy proposal | 3 | Michael | W6 | 🔲 | Gate G2; model scope | Patrick → Michael |

## C. Data strategy & collection (Stage 4, Phase 2)

| ID | Commitment | Stage | Owner | Due | Status | Blocks if missing | Escalation |
|---|---|---|---|---|---|---|---|
| C11 | Approve & resource targeted data-collection campaigns (breed/orientation/behavior gaps) | 4 | Michael / Ken | W12 | 🔲 | Closing the EDA-exposed gaps in Phase 2 | Steering / QBR #1 |
| C12 | Provide access to representative dogs/collars for new capture | 4/8 | Halo ops | P2 | 🔲 | Field-relevant training data | Steering |
| C13 | Decide data-retention / field-telemetry approach for continuous retraining | 4/10 | Michael | P2 | 🔲 | MLOps / expansion thesis | QBR |

## D. On-device & field (Stages 7–8)

| ID | Commitment | Stage | Owner | Due | Status | Blocks if missing | Escalation |
|---|---|---|---|---|---|---|---|
| C14 | Provide STM32 dev environment or representative test harness | 7 | Softeq | W3 | 🔲 | WS1 parity test; on-device integration | Patrick → Michael → Softeq |
| C15 | Integrate candidate model into firmware build for on-device test | 7 | Softeq | W20 | 🔲 | Gate G4 | Steering |
| C16 | Run field-test protocol across breed categories, return labeled field telemetry | 8 | Halo ops + Softeq | W22–30 | 🔲 | Gate G5; real-world validation | Steering |

## E. Business & gate decisions (all stages)

| ID | Decision / sign-off owed | Stage | Decider | Due | Status | Blocks if missing | Escalation |
|---|---|---|---|---|---|---|---|
| C17 | Sign off Gate G1 (data ready) | 1 | Michael | W4 | 🔲 | Phase 1 proceed | Steering |
| C18 | Sign off Gate G2 (Phase 1 checkpoint) | 3/6 | Michael | W8 | 🔲 | Phase 1 proceed | Steering |
| C19 | Sign off Gate G3 (Phase 1 → 2 gate) — **the retention moment** | all | Ken + Michael | W16 (~Jul 6) | ⚠️ | Phase 2 start, renewal anchor | Patrick owns the readout |
| C20 | Agree Phase 2 scope & device-volume deployment pricing | 9 | Ken | W16+ | 🔲 | Expansion / renewal | Teague + Patrick |
| C21 | Finalize deployment license terms (device-volume tier) | 9 | Ken | W36 | 🔲 | Production rollout | Teague + Patrick |

---

## Live escalation log

Record here when a commitment slips, the impact, and the response. This is the evidence trail
that protects EI and keeps the engagement honest.

| Date | Commitment | What happened | Downstream impact | Action / who | Resolved |
|---|---|---|---|---|---|
| | | | | | |

---

## Standing risks this tracker manages

These come straight from the Central Reference / Company Brief — the tracker is how you keep them from materializing:

1. **No named Halo ML lead (C1).** Without a technical counterpart, every other line stalls. This is the top structural risk; do not let G1 pass without it.
2. **Loose labeling group (C6–C9).** The accuracy ceiling. Cheap to fix, fatal to ignore.
3. **CEO routes around the account team.** Decisions C19–C21 sit with Ken — keep them on the record and routed through the escalation protocol so nothing becomes an unrecorded promise (the Albert lesson).
4. **Three-party hand-offs (Halo ↔ EI ↔ Softeq).** C4/C14/C15/C16 cross org boundaries — the most likely place for an unowned dependency to fall through.
