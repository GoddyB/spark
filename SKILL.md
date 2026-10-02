---
name: spark
description: >-
  use this whenever framing work or emitting agent context — SPARK is a general
  meta-framework (Stack, Productization, Art/taste, Risks and Rumblings, Knowledge)
  for coding work, org work, and any other turn or task, not just issues or PRs.
  When invoked, consider all SPARK points for that turn/task and apply each
  that is relevant; do not invent irrelevant material or work. Shapes output,
  response, or work pattern only, never changes the task;
  default when it fits. Also when the caller says "make a Spark pin to do X"
  (or close variants): create a GitHub issue labeled pin whose body uses one
  SPARK heading per letter
---
SPARK is compatible with other skills, does not trample them, and only adds context.

**Rule:** SPARK never changes the task at hand — it only shapes the output, response, or work pattern.

**Org default:** Across coding work, org work, and other turns or tasks, consider SPARK by default even when the caller does not invoke this skill by name; apply only the points that fit, without inventing unrelated material or work.

SPARK is a meta-framework, not a framework. Sections in order:

## S — Stack
The stack elements.

## P — Productization
The wrapper or shape to the outside world: who sees it, who works with it, who it is for, and how it moves GoddyB up in the world. Packaging is the intuition.

## A — Art / direction / taste
Front-end: art direction. Coding: performant, elegant, small extensions to working code, deep black-box modules with predictable behavior and low demand on their surroundings, modularity.

## R — Risks and Rumblings
**Risks:** For relevant tasks, sketch risk pictures along the axes appropriate to the task, such as likelihood, impact, time horizon, and reversibility, across technical, product, and organizational concerns. Include the risks exposed to us by relevant frontier developments. Give special importance to **bitter lesson risk**: bespoke techniques and hand-engineered expertise may be overtaken by general methods that scale with compute. Call out the riskier sides of rumblings so we remain wary of them.

**Rumblings:** When relevant to the task, record actual beneficial frontier software-engineering developments that are encroaching or already upon us. Include an explicit as-of date and, where current sources are available, draw from X and the latest arXiv — one line or link plus a short synopsis each. If no relevant, verifiable rumbling is available, omit this part rather than inventing one. Awareness only: never argue against the SPARK, and never send agents chasing alternatives from rumblings.

## K — Knowledge sources
A short index: repos, docs, APIs, chat artifacts, scholarly articles (for example arXiv and the Apple ML research page as first-class). Subheadings are fine. Loose structure — images, videos, posts, screenshots, links, paths, PR numbers, and prose are all allowed.

## Trigger — make a Spark pin

When the caller says **"make a Spark pin to do X"** (or close variants such as "spark pin to X", "make a SPARK pin for X", "pin this with Spark: X"):

1. Create a GitHub issue on the **repo the pin targets** (if the target repo is ambiguous, ask once before filing).
2. Ensure label `pin` exists; apply it.
3. Title: `(pin) <intent>` — short intent distilled from X.
4. Body: populate using the SPARK meta-framework — **one heading for each letter** of SPARK — and distribute the X content under those headings as appropriate:

```markdown
## S — Stack
…

## P — Productization
…

## A — Art / direction / taste
…

## R — Risks and Rumblings
…

## K — Knowledge sources
…
```

5. In the live conversation, hold **pin names only**; full SPARK context lives in the issue (same as pin-and-spelunk).

This trigger **adds** pin-filing behavior; it does not replace or weaken the framing/default SPARK behavior above. For pin workflow details (LIFO, blocked commits), pair with [pin-and-spelunk](sand-workflow:pin-and-spelunk) after shaping the body here.
