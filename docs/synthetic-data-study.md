# Synthetic Data Study Protocol

## Scope

This workbench produces candidate multilingual instruction data. A generated batch, an
automatic audit, a completed fine-tuning job, or an agent trace is not evidence that a
model improved. A paper claim requires the controlled downstream experiments below.

## Research Questions

1. Does curated multi-agent synthetic data improve held-out task performance relative to
   the base model, seed-only SFT, and unfiltered synthetic SFT?
2. Do quality gates improve data efficiency for each language slice?

## Candidate Data Controls

- Generate a balanced allocation across task families: workplace pragmatics, cultural
  explanation, code-switching, and safety-aware clarification.
- Preserve generator version, seed, language slice, prompts, responses, failures, and
  the immutable dataset version.
- Run schema/completeness, exact-duplicate, response-length, and language-coverage
  audits. Add a semantic near-duplicate and benchmark-contamination check before a
  publishable study.
- Sample each language and task family for independent language-specialist and domain
  review; report disagreement and rejection reasons.

## Evaluation Design

- Freeze external or pre-generation held-out tests before generation.
- Compare base, seed-only, unfiltered-synthetic, and curated-synthetic conditions.
- Run ablations that remove the critic/judge, diversity policy, and language specialist.
- Use seeds `13`, `29`, and `47`; report per-language results, bootstrap confidence
  intervals, and a data-efficiency curve for the configured data sizes.
- Link every reported result to the dataset version, split, model version, training
  command, seed, and result artifact.

## Research Basis

- [Self-Instruct](https://arxiv.org/abs/2212.10560) motivates generation followed by
  invalid/similarity filtering and held-out instruction evaluation.
- [WizardLM / Evol-Instruct](https://arxiv.org/abs/2304.12244) motivates controlled
  instruction-complexity variation.
- [UltraFeedback](https://arxiv.org/abs/2310.01377) motivates diverse, multi-aspect
  feedback with bias mitigation rather than a single unexamined score.
- [Magpie](https://arxiv.org/abs/2406.08464) motivates selecting a smaller high-quality
  subset from a larger candidate pool and comparing the resulting fine-tunes.
- [DCLM / DataComp-LM](https://arxiv.org/abs/2406.11794) motivates treating curation as
  a controlled variable and measuring it with broad downstream evaluation.
- [LIMA](https://arxiv.org/abs/2305.11206) motivates testing whether quality can be more
  valuable than unfiltered volume.