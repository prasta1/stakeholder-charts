# Wrangling Halo — Messaging for [PAWS Contact Name]

Purpose: introduce the project tracker / responsibilities doc, set the right expectations about how the model gets built, and give them resources to understand the work. Three versions below — use whichever fits the moment. Replace anything in [brackets] before sending.

The single most important point to land, in every version: **model quality is capped by label quality.** Right now labels come from a loose, uncoordinated group of labelers. Until that group works to one shared standard, no amount of model tuning will fix the ceiling. The tracker is how we close that gap — clear owners, clear definitions, visible status.

---

## 1. Follow-up email

**Subject:** Wrangling Halo — how we'll run this, and why labeling is the lever

Hi [Name],

Good talking today. Quick recap of what we put in place and the one thing I want to make sure lands.

**The tracker.** I've set up a lightweight doc that shows who owns what and where each piece stands: [link]. It's deliberately simple — a responsibilities list plus a status column we update as we go. Two asks: (1) confirm the names against each line so ownership is right, and (2) glance at it before our syncs so we're working from the same picture. Anything red or stalled is where I'll want your help unblocking.

**How the model actually gets built.** Edge Impulse takes you through one loop: collect sensor data, label it, train a model, test it, then repeat. It's iterative by design — the first model is a starting point, not the finish line, and it gets better each cycle as the data improves. The short "[What is Edge Impulse]" and beginner overview in the resources below cover this in a few minutes.

**The part that matters most: labeling.** A behavior model is only as good as the labels it learns from. Our labels currently come from a loose group of labelers, and when different people interpret "playing" vs. "active" vs. "walking" differently, that inconsistency goes straight into the model as noise — and it sets a ceiling we can't tune our way past. This is well documented; the industry term is inter-annotator agreement, and "garbage in, garbage out" is the blunt version. The fix isn't more labelers, it's a shared standard: one agreed definition per behavior, written guidelines everyone uses, and occasional spot-checks where two people label the same clip to see if they agree.

For context on what's realistic: peer-reviewed studies classifying dog behavior from a single collar accelerometer land around 74% overall accuracy across ~9 behaviors, with some behaviors much easier than others. That's the neighborhood we should be planning around — and tight labeling is what moves us toward the top of that range rather than the bottom.

A few resources worth 20 minutes, linked at the end of this email.

Happy to walk through any of it. The near-term priority I'd suggest: lock the behavior definitions and labeling guidelines, since everything downstream depends on it.

Best,
[Your name]

**Resources**
- What is Edge Impulse (3-min overview): https://docs.edgeimpulse.com/docs/concepts/edge-ai-fundamentals/what-is-edge-impulse
- Edge Impulse for beginners: https://docs.edgeimpulse.com/docs/readme/for-beginners
- Labeling time-series sensor data in Edge Impulse: https://docs.edgeimpulse.com/docs/edge-impulse-studio/data-acquisition/multi-label
- The ML project lifecycle, plain-language: https://developers.google.com/machine-learning/managing-ml-projects/phases
- Why labeler agreement matters (short explainer): https://labelstud.io/videos/in-the-loop-what-is-agreement/
- Dog behavior from a collar accelerometer — what accuracy is realistic (peer-reviewed): https://www.mdpi.com/2076-2615/11/6/1549

---

## 2. Live call talking points

Use these to drive the conversation. Order matters: process first, then the labeling message, then expectations.

**Open — the tracker (2 min)**
- "I've set up a light tracker so we both see who owns what and where things stand. Not heavy process — a responsibilities list and a status column."
- Ask them to confirm names against each line.
- Agree on a cadence: glance before each sync; I'll flag anything blocked.

**How Edge Impulse works (2 min)**
- One loop: collect data → label it → train → test → repeat.
- First model is a baseline, not the answer. It improves each cycle as data quality improves.
- No heavy coding on their side — the platform guides the steps.

**The labeling message — the one to land (4 min)**
- "The model is only as good as the labels it learns from."
- Right now labels come from a loose group with no shared standard. When people interpret the same behavior differently, that disagreement becomes noise the model can't overcome — it's a ceiling, not a tuning problem.
- The fix is cheap and high-leverage: one agreed definition per behavior, written guidelines everyone follows, and spot-checks where two labelers tag the same clip and we compare.
- This is a known, named problem (inter-annotator agreement) — not us being picky.

**Set expectations (2 min)**
- Published studies on dog behavior from a collar accelerometer hit ~74% accuracy across ~9 behaviors; some behaviors are much easier than others.
- Tight labeling is what gets us toward the high end of that range.
- Frame the first deliverable: lock behavior definitions + labeling guidelines.

**Close**
- "I'll send the tracker link and a few short resources. The one near-term priority is the labeling standard — can we name an owner for that today?"

---

## 3. Real-time chat message

> Hey [Name] — just shared the project tracker [link]. It shows who owns what + a status column; can you confirm the names against each line?
>
> One thing I want to flag while it's fresh: the model is only as good as the labels behind it, and right now they're coming from a loose group with no shared standard. Different people labeling the same behavior differently = noise the model can't tune past. Easiest high-leverage fix is one agreed definition per behavior + simple written guidelines everyone uses.
>
> Sent a couple of short reads too — incl. a study showing ~74% accuracy is realistic for dog-behavior-from-collar work, so tight labeling is what pushes us toward the top of that range. Happy to walk through any of it. 🐾

---

## Notes for you (not for the contact)

- Everything in [brackets] is a placeholder — the tracker link, the contact's name, your name.
- I wrote this without seeing the actual tracker (the Wrangling Halo folder was empty). Drop the doc in and I'll tailor the wording to its real structure, owners, and current red/yellow items.
- The "~74% accuracy" figure is from peer-reviewed canine-accelerometer studies (see Sources). It's a defensible anchor for expectation-setting; adjust if your target behavior set is narrower/easier.

## Sources
- [What is Edge Impulse? — Edge Impulse Documentation](https://docs.edgeimpulse.com/docs/concepts/edge-ai-fundamentals/what-is-edge-impulse)
- [For beginners — Edge Impulse Documentation](https://docs.edgeimpulse.com/docs/readme/for-beginners)
- [Multi-label (time-series) — Edge Impulse Documentation](https://docs.edgeimpulse.com/docs/edge-impulse-studio/data-acquisition/multi-label)
- [ML development phases — Google for Developers](https://developers.google.com/machine-learning/managing-ml-projects/phases)
- [In the Loop: What is Annotator Agreement? — Label Studio](https://labelstud.io/videos/in-the-loop-what-is-agreement/)
- ["Garbage In, Garbage Out" Revisited (on human-labeled training data) — arXiv](https://arxiv.org/pdf/2107.02278)
- [Deep Learning Classification of Canine Behavior Using a Single Collar-Mounted Accelerometer — Animals (MDPI), 2021](https://www.mdpi.com/2076-2615/11/6/1549)
- [Triaxial Accelerometers and ML for Behavioural Identification in Domestic Dogs — Sensors (MDPI), 2024](https://doi.org/10.3390/s24185955)
