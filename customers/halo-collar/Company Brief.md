# Company Brief: Protect Animals With Satellites, LLC (dba Halo Collar)

*Edge Impulse Customer Success — retention & expansion | Prepared 2026-06-23*

## Snapshot
| Field | Value |
|---|---|
| Industry | Consumer Pet Tech / GPS Wearables |
| HQ | Jacksonville, Florida, USA |
| CARR | $133,000 (per CRM; central reference cites $130K platform + premium support, billed in 4 staggered installments) |
| Renewal | 2027-03-16 |
| Health | Healthy (70) |
| Risk level | 0 - Not Assessed |
| Stage / Maturity | — (engagement began 2026-03-16; Phase 1 diagnostic) |
| CSM / Account owner | Patrick Ruster (CSM) / Teague Gudemann (account owner) |
| Solutions | Yvonne (assigned SE) |

## Company background
Halo Collar makes a premium GPS smart dog collar combining wireless containment ("fence"), real-time location tracking, and activity/behavior features. The business has scaled fast — roughly $3M revenue in 2020 to ~$75M in 2024, projected past $100M in 2025 — and reports keeping 200,000+ dogs safe across 350 breeds ([US Chamber of Commerce, 2025](https://www.uschamber.com/co/good-company/the-leap/halo-collar-pet-safety-technology)). Product momentum is strong: Halo Collar 5 launched September 2025 with AlwaysOn GPS and 20 location updates/sec ([PR Newswire](https://www.prnewswire.com/news-releases/halo-collar-5-debuts-precision-bringing-autonomous-vehiclegrade-gps-accuracy-to-dog-safety-302743805.html)), and in April 2026 the company introduced Precision+ (dual-band L1+L5 GPS with Swift Navigation's Skylark service) plus expanded retail distribution.

## Edge Impulse relationship
New, high-value engagement that started 16 March 2026, structured as a paid diagnostic project rather than open-ended advisory. The core problem: Halo's **dog activity classification** models underperform. Suspected root causes are multifaceted — poor dataset collection practices at capture, imprecise data handling/labeling, a lab-to-field performance gap, and hardware constraints (collar positioning affecting accelerometer readings). Phase 1 uses a "fail fast" methodology to identify what is actually broken before proposing fixes. CTO Michael K. Vang provided the initial accelerometer dataset; Teague built a diagnostic spreadsheet to structure troubleshooting. Halo's org sits in Edge Impulse Studio (org 62443).

## Retention assessment
Health is good (70) and the renewal is far out (March 2027), but risk is **unassessed** and the account is early and fragile in two ways. First, this is a "prove it" diagnostic engagement — if Phase 1 doesn't produce a credible improvement path on activity classification, there is no installed production dependency yet to anchor renewal. Second, there is a documented relationship landmine: EI's Albert previously made commitments to CEO Ken without full technical understanding and nearly derailed the deal; he has been removed from account access, but the CEO's tendency to go around the account team is a known dynamic to manage. Mitigants: strong executive attention (Patrick as Head of CS leads directly), staggered payments already underway, and a customer whose commercial success makes on-device intelligence strategically valuable.

## Expansion opportunities
The expansion thesis is strong because Halo is growing fast and their differentiation is increasingly on-device. Concrete angles: (1) **land the activity-classification win**, then extend the same pipeline to additional behavior/health signals (rest vs. activity, anomaly/distress detection, scratching/itching, bark or vocalization detection) — each a net-new model use case; (2) **device-volume scaling** — 200K+ active collars and accelerating retail distribution mean per-device or fleet-tier deployment economics as models ship in Collar 5 and successors; (3) **model lifecycle / MLOps** as Halo moves from diagnostics to continuous field-data retraining; (4) position EI's on-device ML as complementary to the Precision+ GPS investment — accelerometer/edge inference is the layer GPS can't cover (behavior, not just location).

## Recommended next actions
1. **Close out Phase 1 with a crisp diagnostic readout** to Ken and Michael — root-cause findings on the dataset + lab-to-field gap, with a recommended fix path. This is the single biggest retention lever.
2. **Formally assess account risk** in CRM (currently "Not Assessed") and set a stage/maturity now that the engagement is live.
3. **Lock the relationship cadence around Patrick + Teague** to keep the CEO from routing decisions outside the account team; confirm Albert's access removal stuck.
4. **Scope Phase 2** as a written proposal tying improved activity classification to a multi-use-case on-device roadmap, with device-volume-based pricing.
5. **Capture a reference/case study** opportunity early — Halo is a marquee, fast-growing consumer brand and a strong logo to showcase.

## Sources
- [How Halo Collar Scaled to $100 Million — US Chamber of Commerce](https://www.uschamber.com/co/good-company/the-leap/halo-collar-pet-safety-technology)
- [Halo Collar 5 / Precision+ — PR Newswire](https://www.prnewswire.com/news-releases/halo-collar-5-debuts-precision-bringing-autonomous-vehiclegrade-gps-accuracy-to-dog-safety-302743805.html)
- [Halo Collar introduces new escape-proof collar — PR Newswire](https://www.prnewswire.com/news-releases/halo-collar-introduces-new-escape-proof-collar-302556459.html)
- Internal: Halo — Central Reference.md (deal overview, contacts, technical problem, deal history)
