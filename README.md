# KnitWise AI: Reverse-Engineering Multi-Geometry Textile Architecture with Gemma 4

**Track Focus:** Digital Equity & Inclusivity / Ollama Special Technology Track
**Core Model:** `gemma-4-26b-a4b-it` (Local Deploy / Production Testing)

## Project Overview
KnitWise AI is a specialized, computer-vision-driven pattern parsing platform that translates visual textile designs into mathematically synchronized, structurally viable crochet notation. 

While general-purpose LLMs are excellent at standard textual tasks, they natively fail at maintaining spatial, multi-step geometric constraints over sequential lines of pattern generation. They frequently hallucinate impossible stitch increments, mix up stitch aspect ratios, or cause severe structural warping. KnitWise AI solves this by introducing robust geometric boundaries and prompt-driven shorthand parsing directly over the Gemma 4 26B model layer, unlocking flawless pattern replication for three distinct structural layouts:
1. **Granny Squares (Exponential Flat Grids):** Scaling corner increases perfectly without warping.
2. **Scarves (Static Linear Rows):** Handling shifting chevron angles and keeping edge margins straight.
3. **Beanies (Cylindrical Crowns & Fixed Bodies):** Transitioning smoothly from flat circles to straight vertical walls.

---

## 🛠️ System Architecture & Engineering Breakthroughs

KnitWise AI bypasses classic model reasoning limitations through specific logical guardrails defined in the parsing layer across all major textile shapes:

### 1. Mandatory Base Multiple Law (Universal Stitch Type Alignment)
Standard vision pipelines frequently misclassify stitch heights, pairing a tall stitch (like Double Crochet) with a low starting loop count (like 6 in a circular beanie crown), which forces the physical fabric to warp into a sharp cone. KnitWise implements cross-validation rules that bind visual loop aspect ratios to historical craft baselines (e.g., mandating a starting base of 11-12 stitches for a flat `dc` circle layout, vs 8-10 for `hdc`, vs 6-8 for `sc`).

### 2. Multi-Geometry Boundary & Cutoff Enforcements
When generating structural textile patterns, language models struggle with boundaries where mathematical formulas shift. KnitWise enforces explicit structural constraints based on targeted geometry profiles:
* **The Beanie Cutoff:** Instantly terminates the model’s permission to utilize increase keys once a calibrated crown diameter total is met, cleanly dropping the pattern matrix into un-warped vertical rows.
* **The Granny Square Progression:** Mandates a strict corner-contribution formula, forcing the stitches per side on Round(n) to always scale perfectly in proportion to the corner stitch cluster to keep the square completely flat.
* **The Scarf Margin Lock:** Sets strict flat-row linear logic that bans continuous rounds and forces a static, identical stitch count across every single subsequent row to maintain straight, un-warped fabric edges.

### 3. Consolidated Range Shorthand (Eliminating Multiplication Loop Failures)
Forcing a model to iterate long, repetitive arrays row-by-row introduces a massive surface area for cumulative arithmetic drift and text-instruction repetition errors. KnitWise solves this by directing the engine to leverage generalized shorthand ranges (e.g., batching uniform repeating segments inside tight, clean string matrices like "Rounds 3-10: Continue increasing uniformly..."). This completely prevents the model from scrambling its multiplication tables, keeping the output 100% mathematically accurate across expansive designs while producing clean, professional notation for human crafters.

---
