# WS3: Class Simplification & Data Strategy

**Weeks 3–8 · Est. 3–6 weeks effort · Status: 🔲 Not started**

## Objective

Simplify the activity class taxonomy from 8 classes to a core set and define the data collection strategy to address distribution gaps. The current dataset has severe class imbalance (28.8:1 ratio) and limited real-world diversity.

## Context

Current 8 classes: rest, walk, run, eat, play, on_shelf (847 samples), human_carry (1,789), unknown. The dataset has 92,800 samples total, but minority classes are dramatically underrepresented. The proposed simplification targets 4 core classes (rest, walk, run, eat) with remaining activities handled via application-level logic or merged.

## Key Questions

- Which classes can be merged vs. which need distinct treatment?
- What's the minimum viable class set that Halo's product requires?
- How much new data is needed to close the distribution gap?
- What labeling protocol will ensure quality for real-world data?

## Tasks

- [ ] Analyze confusion patterns between existing 8 classes
- [ ] Propose simplified taxonomy (target: 4 core classes)
- [ ] Evaluate what happens to minority classes (on_shelf, human_carry)
- [ ] Define real-world data collection protocol
- [ ] Update labeling guidelines and quality assurance process
- [ ] Begin collection campaigns for breed/size diversity
- [ ] Produce data strategy document with collection targets

## Acceptance Criteria

- Simplified taxonomy proposal reviewed and accepted by Halo
- Data collection protocol documented and actionable
- Labeling guidelines updated and shared
- Collection campaigns initiated with clear targets and timelines

## Dependencies

- WS1/WS2 findings inform which classes are most problematic
- Halo provides access to existing labeled data and labeling infrastructure
- Halo provides fleet access or coordinates field data collection

## Outputs

- `docs/decisions/XXX-class-taxonomy-simplification.md` (ADR)
- Data collection protocol document
- Updated labeling guidelines
- Collection campaign tracker
