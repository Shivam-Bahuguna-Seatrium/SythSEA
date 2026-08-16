# SynthSEA Web Research Findings

**Research date**: 2026-08-13

**Discovery source**: OpenAlex Works API, using title and topic queries. The
returned records were checked for DOI or landing-page links to ACL Anthology,
arXiv, or publisher pages. These are research candidates and require researcher
approval before final citation status becomes verified.

## Confirmed Findings

1. **Synthetic instruction generation already has established baselines.**
   Self-Instruct describes a pipeline that generates instruction/input/output
   samples and filters invalid or similar examples. SynthSEA must compare against
   this kind of single-model self-generation baseline.

2. **Southeast Asian code-mixed generation is directly prior art.**
   The SEA code-mixed prompting study includes Indonesian, Malay, Chinese,
   Tagalog, Vietnamese, Tamil, and Singlish. Its reported inconsistent quality
   and recommendation for extensive human checks support SynthSEA's separate
   language slices and cultural-review requirements.

3. **Regional multilingual models already exist.**
   SeaLLMs is relevant model-level prior art. SynthSEA cannot claim novelty merely
   from targeting Southeast Asian languages; its claimed contribution must be
   narrower and experimentally demonstrated, such as a verified generation and
   evaluation protocol.

4. **Singlish has dedicated NLP resources and methods.**
   Universal Dependencies parsing for colloquial Singaporean English and later
   Singlish discourse-particle work show that Singlish should be treated as a
   distinct variety with its own linguistic and evaluation requirements.

5. **Dialect and non-standard English robustness is an established problem.**
   Mind Your Inflections and Multi-VALUE provide prior art for evaluating models
   across non-standard Englishes and dialects. SynthSEA should compare its
   language-aware quality claims against appropriate dialect-aware controls.

## Research Gap Hypothesis

The web evidence supports a **hypothesis**, not a proven novelty claim:

> Existing work covers self-instruction generation, Southeast Asian multilingual
> models, SEA code-mixed prompting, Singlish resources, and cross-dialect
> evaluation, but the retrieved sources do not by themselves establish a
> reproducible multi-agent pipeline that generates culturally reviewed synthetic
> instructions across the four SynthSEA settings and validates quality, safety,
> cultural fit, and downstream utility separately.

This hypothesis must be tested with a broader systematic review and the planned
baselines and ablations. It must not be written as a final novelty claim yet.

## Venue Finding

The search did not verify an official RegiCON 2026 CFP, author guide, page limit,
template, or submission system. The project prompt is not an authoritative venue
source. Venue status therefore remains unresolved and the report remains blocked.

## Required Human Review

- Approve or reject each candidate source in `web-research-2026-08-13.json`.
- Check the full papers, not only API metadata or abstracts.
- Add missing papers discovered through backward and forward citation chasing.
- Supply the official RegiCON 2026 URL or PDF.
- Confirm whether each source's data, code, and figures may be reused.