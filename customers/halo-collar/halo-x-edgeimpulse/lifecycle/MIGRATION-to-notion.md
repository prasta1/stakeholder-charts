# Taking this collaborative: Markdown → Notion

This overlay is markdown-first so it's fast to iterate and version-controlled. When the team is
ready to collaborate (Halo + Softeq included), the structure is built to lift into Notion with
no rework. You already have a Halo page in the EI Notion workspace
(`notion.so/edgeimpulse/Halo-31fb90f327a28007a23bef05a8b58ba8`).

## Recommended Notion structure

A single **Halo Engagement** page with these databases:

| This file | Becomes a Notion… | Key properties |
|---|---|---|
| `customer-accountability-tracker.md` | **Database** (table + board views) | Commitment, Stage (select), Owner (person), Due (date), Status (select), Blocks, Escalation |
| Lifecycle stages (`README.md` spine) | **Database** or linked pages | Stage #, Name, Workstreams (relation), Phase, Gate |
| Decision gates (`README.md`) | **Database** | Gate, Week, Question, Signers, Status |
| Escalation log | **Database** | Date, Commitment (relation), Impact, Action, Resolved |

## Why the tables already fit

Every table here is a flat record set: stable header row, one row per record, no merged cells,
single value per cell where a Notion property would be single-select. That means each markdown
table pastes into a Notion database and the columns map straight to properties.

## Two ways to move it

1. **Manual (fastest for one-time):** create the databases above, paste each markdown table —
   Notion auto-detects columns. ~30 minutes.
2. **Automated:** I can push these into the Halo Notion page directly via the connected Notion
   tools — create the databases and populate the accountability rows. Just ask.

## What to keep in markdown vs. Notion

- **Notion:** the accountability tracker, gate status, escalation log — the live, shared,
  customer-facing collaboration surface.
- **Markdown repo:** EDA findings, experiments, ADRs, firmware/pipeline detail — the engineering
  evidence trail that benefits from version control and lives with the work.

The split mirrors the operating model: Notion for shared accountability, the repo for technical truth.
