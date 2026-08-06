# Call Prep: Halo Collar — Adrian Lai

**Meeting:** Existing-customer check-in with the product owner driving data quality
**Your contact:** Adrian Lai — Principal Product Manager, Halo Collar
**Your goal (suggested):** Support and deepen the data-collection/labeling work Adrian is leading, and equip yourself to manage founder (Ken Ehrman) skepticism that "AI should just figure it out."

> Context: Halo is an **existing Edge Impulse customer**. Two live dynamics shape this call: (1) Adrian is focused on improving data-collection processes for clean, accurate, labeled training data — reinforce and equip that; (2) founder **Ken Ehrman** has been challenging to work with and believes AI should "just figure it out" — see the dedicated section below.

---

## Account Snapshot

| Field | Value |
|-------|-------|
| **Company** | Halo Collar (Halo Health / Halo Collar) |
| **Product** | GPS wireless dog fence + tracking + training collar, app-controlled |
| **Industry** | Pet tech / consumer wearables / IoT |
| **Scale** | ~$100M in sales; protects 200,000+ dogs/day in the US |
| **Notable founders** | Ken Ehrman (founder/managing partner, serial IoT entrepreneur); co-developed with dog behaviorist Cesar Millan |
| **Other leadership** | Jonathan Ragals (COO) |
| **Relationship** | Existing Edge Impulse customer |

---

## Who You're Meeting

### Adrian Lai — Principal Product Manager, Halo Collar (since Jan 2024)
- **Background:** Heavyweight product/ops operator. Prior: COO at Stochastic, Co-Founder & CTO at ClosingStack, Head of Ops & Chief of Staff at Wonderschool, Senior PM at Spin (e-scooters), Lead PM at Houzz, Lead Data Analyst at Facebook, strategy at McKinsey. MBA from INSEAD.
- **LinkedIn:** https://www.linkedin.com/in/adrlai/
- **Read on him:** Data-first PM with a startup-builder/CTO streak — he'll be comfortable going deep technically and will care about business case (cost, time-to-market, unit economics), not just the demo. He's owned ops and data at scale, so frame value in terms of dev velocity and measurable model performance.
- **Talking point:** His Facebook data + Spin/Houzz hardware-meets-product path is a natural bridge to "ML on real-world sensor data at the edge."

---

## Why Edge Impulse Is Relevant to Halo (your angle)

Halo's collar is essentially an edge-AI device, which is squarely your wheelhouse:
- **On-device AI today:** Halo already markets proprietary AI/ML that filters false GPS signals (multipath off buildings/trees), runs dual-frequency GPS with ~20 location updates/sec, plus activity and health tracking — all on a battery-constrained wearable (they tout ~48 hrs per charge).
- **Recent moves:** Halo Collar 5 launched with "AlwaysOn" GPS and a more robust health/activity system; in April 2026 they announced **Precision+** (L1+L5 dual-band GPS + Swift Navigation's Skylark correction service) claiming 3x accuracy. Momentum + heavy sensor/ML investment = appetite for better ML tooling.
- **Edge Impulse fit:** You provide the embedded-ML pipeline — data collection from IMU/sensors, model training, on-device optimization (quantization, latency/power profiling), and deployment to constrained MCUs. Directly applicable to activity/behavior classification, anomaly/health detection, and sensor-fusion to cut GPS power draw.
- **Proof point to drop:** Edge Impulse has a published tinyML **pet activity tracker** reference (Seeed XIAO nRF52840 Sense, 6-axis IMU, dog activity classification). Concrete, on-topic, shows you've already built in their domain.

---

## Talking Points 1 — With Adrian: reinforce and equip the data-quality work

**Anchor principle:** Model accuracy on a collar is bounded by **label quality, not model cleverness.** In data-centric ML, most real-world accuracy gains come from fixing labels and coverage rather than tuning architecture — and that's doubly true at the edge, where the model has to stay tiny.

- **Validate his instinct.** Investing in clean labeled data is the highest-leverage thing he can do. Say it plainly — it also gives him internal air cover (useful against Ken).
- **Ground truth is the hard part in their domain.** IMU/activity labels are ambiguous — what was the dog *actually* doing? Ask how they establish ground truth (video-synced capture? trainer annotation?) and whether they measure **inter-labeler agreement**. If two humans disagree on a label, the model can't beat that noise floor.
- **Coverage and domain shift.** Collar placement, breed, size, coat, and motion artifacts all shift the sensor signal. Ask how diverse the training set is across real deployment conditions — clean labels on a narrow dataset still fail in the field.
- **Class balance.** The events that matter most (boundary crossings, rare behaviors, escapes) are usually rarest in the data. Ask how they sample/augment for those.
- **Point him at the EI tooling that fits this:** Data Explorer / feature explorer to surface mislabeled or outlier samples visually, dataset versioning for reproducibility, and active-learning–style prioritization so labelers spend time on the samples that actually move accuracy. Offer a working session on his labeling pipeline as a concrete next step.
- **Discovery hook:** "Where in your data-to-deployment loop are you losing the most time today — collecting, labeling, or validating?"

---

## Talking Points 2 — With Ken Ehrman: reframe "AI should just figure it out"

**Approach:** Don't fight it head-on. Agree with the *goal* (AI that just works) and position data quality as the only way to get there.

- **Agree, then redirect:** "The goal absolutely is AI that just figures it out — and the way you get that is by showing it the right examples. Even frontier models are trained on heavily curated data; 'figuring it out' is learned from what you feed it, not in spite of it."
- **The new-hire analogy.** The model is like a brilliant employee who's never seen a dog — it learns entirely from the examples you show it. Hand it mislabeled examples and it confidently learns the wrong rule. The intelligence is real; it's only ever as good as the textbook.
- **The edge constraint is the kicker.** On a battery-constrained collar you can't brute-force ambiguity with a giant model — you don't have the compute or power. Clean labels are what let a *small, efficient* model hit accuracy targets inside the power envelope. Data quality is how you get the "magic" to run on a collar at all.
- **Translate to his scoreboard.** Ken cares about a $100M brand and dog safety. Bad labels → false boundary alerts and missed escapes → refunds, support load, and reputation hits. Tie label quality directly to false-positive / false-negative rates customers actually feel.
- **Cost/velocity angle.** Dirty data makes the team iterate forever; clean data ships features faster. It's a margin and time-to-market lever, not an engineering luxury.
- **Win with proof, not argument.** The most durable way to convert a "just figure it out" exec is a before/after: take one feature, show the accuracy delta from a labeling cleanup. One chart beats the philosophical debate.

> **Line that does double duty in the room:** *"AI can absolutely figure it out — clean labeled data is just how we tell it what 'it' is. On a collar with this little compute, that's the difference between a feature that ships and one that drains the battery chasing noise."*

---

## Suggested Agenda (≈30 min discovery)

1. **Open** — Reference their momentum: Collar 5 / Precision+ launch and the health-and-activity expansion. Congratulate, then get curious.
2. **Their world** — How the product/ML org is structured; where on-device ML sits today vs. cloud; what's roadmap for behavior/health features.
3. **Pain discovery** — Where the current edge-ML workflow hurts (data pipeline, model iteration speed, power/latency, firmware handoff).
4. **Value framing** — Briefly map Edge Impulse to 1-2 of their stated pains; reference the pet activity-tracker example.
5. **Next steps** — Propose a technical deep-dive with their firmware/ML lead, or a scoped pilot on one feature (e.g., activity classification).

---

## Discovery Questions

1. How is on-device intelligence split between the collar and the cloud today, and where do you *want* more to run on-device?
2. What's the biggest constraint on shipping new sensor-driven features — model accuracy, power budget, or engineering time to iterate?
3. How does your team currently go from collected sensor data to a deployed model on the collar? Who owns that pipeline?
4. With Collar 5 and the health/activity push, what new ML capabilities are on the 6–12 month roadmap?
5. How do you measure success for an on-device feature — battery impact, accuracy, false-positive rate, time-to-market?
6. Build vs. buy: how do you think about internal ML tooling versus a platform like Edge Impulse?
7. Who else would need to be in the room for a technical or commercial evaluation?

---

## Potential Objections

| Objection | Suggested Response |
|-----------|-------------------|
| "We already have proprietary AI / built it in-house." | Great — Edge Impulse isn't a rip-and-replace; it accelerates *iteration* and deployment so your team ships sensor features faster and frees them for the hard differentiated work (your GPS IP). Offer to benchmark against one existing model. |
| "Our edge stack is locked to specific silicon/firmware." | Edge Impulse is hardware-agnostic and exports optimized C++/libraries; we integrate into existing firmware rather than dictate it. Confirm their MCU/SoC and show the path. |
| "We don't have bandwidth to evaluate new tooling." | Propose a tightly scoped pilot on one feature (e.g., activity classification) with a clear success metric, minimal eng lift. |
| "Why would a product PM care about a dev tool?" | Frame in his language: faster model iteration = faster feature releases and better unit economics on power/connectivity — a product and margin lever, not just an eng tool. |

---

## Quick Facts to Have Ready
- Halo: ~$100M sales, 200k+ dogs protected/day, Cesar Millan association, Ken Ehrman founder.
- Latest: Collar 5 (AlwaysOn GPS), Precision+ with Swift Navigation Skylark (announced ~April 2026).
- Your proof point: Edge Impulse tinyML pet activity tracker (IMU-based dog activity classification).

---

## Sources
- [Adrian Lai — LinkedIn](https://www.linkedin.com/in/adrlai/)
- [Adrian Lai profile — ContactOut](https://contactout.com/Adrian-Lai-3349690)
- [Halo Collar 5 debuts Precision+ — PR Newswire](https://www.prnewswire.com/news-releases/halo-collar-5-debuts-precision-bringing-autonomous-vehiclegrade-gps-accuracy-to-dog-safety-302743805.html)
- [Halo Collar 5 AlwaysOn GPS — Petage](https://www.petage.com/halo-health-launches-collar-5-app-alwayson-gps-tracking-capabilities/)
- [How Halo Collar scaled to $100M — US Chamber of Commerce](https://www.uschamber.com/co/good-company/the-leap/halo-collar-pet-safety-technology)
- [Halo Collar 3 AI-driven launch — PR Newswire](https://www.prnewswire.com/news-releases/halo-collar-introduces-new-ai-driven-halo-3-301915338.html)
- [Edge Impulse — tinyML pet activity tracker](https://www.edgeimpulse.com/blog/activity-trackers-unleashed-a-tinyml-wearable-device-for-pets/)
