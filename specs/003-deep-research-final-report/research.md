# Feature 003 Research Decisions

## Decision: Use a source-record registry instead of embedded literature prose

**Rationale**: A final report must preserve title, authors, year, venue, DOI or URL,
retrieval date, verification status, contribution, limitation, and relevance for every
source. Structured records make missing identifiers and unverified citations visible and
allow the report to be regenerated without silently changing the bibliography.

**Alternatives considered**: Free-form Markdown references were rejected because they do
not support reliable duplicate detection, field validation, or claim-level provenance.

## Decision: Treat official RegiCON requirements as an input, not an assumption

**Rationale**: The project prompt names RegiCON 2026 but does not include an official CFP,
author guide, template URL, page limit, or submission system URL. The implementation must
accept a researcher-supplied official source record and leave venue status unresolved until
that record is verified. A generic Springer template cannot be treated as authoritative.

**Alternatives considered**: Selecting Springer LNCS by default was rejected because the
venue may use a different format and the constitution forbids unsupported claims.

## Decision: Make research readiness a claim-to-evidence graph represented as files

**Rationale**: Existing Feature 002 already models evidence manifests, claims, venue
profiles, and paper artifacts. Feature 003 should add research questions, experiment
requirements, source records, and readiness checks that reference those models. JSON/YAML
files are inspectable, diffable, and compatible with the existing CPU-first workflow.

**Alternatives considered**: A new database was rejected for the first release because it
would add operational complexity without improving reproducibility for local research
metadata.

## Decision: Use explicit evidence states and fail closed for release

**Rationale**: Verified, provisional, missing, unsupported, restricted, excluded, stale,
failed, and fixture evidence have different scientific meanings. Only verified evidence
may support a primary result; every other state remains visible in the readiness report.

**Alternatives considered**: Treating all present files as valid evidence was rejected
because presence does not establish checksum integrity, provenance, licensing, or
reproducibility.

## Decision: Keep the four language settings as first-class slices

**Rationale**: The constitution requires Singapore English/Singlish, Malay, Tamil, and
Singapore-context Mandarin to be evaluated separately. Research requirements and evidence
links therefore carry language-slice identifiers and aggregation is allowed only after
slice-level coverage is reported.

**Alternatives considered**: A single multilingual aggregate was rejected because it can
hide resource and quality differences between settings.

## Decision: Keep literature and venue retrieval human-approved

**Rationale**: Network availability, paywalls, changing conference pages, and ambiguous
identifiers make automatic citation acceptance unsafe. The workflow records candidates and
verification metadata, but a researcher must approve sources before they support final
claims.

**Alternatives considered**: Automatically importing search results was rejected because
search presence is not evidence of bibliographic correctness or scientific relevance.

## Decision: Reuse existing paper generation and validation boundaries

**Rationale**: `synthsea.paper` already provides venue profiles, evidence manifests,
checksum verification, claim validation, compliance checks, rendering, and package output.
Feature 003 should prepare and validate inputs for these APIs and extend the CLI, rather
than introduce duplicate manuscript logic.

**Alternatives considered**: Rewriting the paper package was rejected because it would
increase regression risk and weaken compatibility with Feature 002.

## Open Research Questions

- What is the official RegiCON 2026 author guide, page limit, template, anonymization rule,
  and reference style? This remains unresolved until an official source is added.
- Which datasets, models, and human reviewers are legally and practically available for
  each of the four language settings? This must be supplied through approved source and
  experiment records.
- Which quality and downstream metrics are valid for each language variety and task? The
  experiment requirements record must document the rationale and limitations instead of
  assuming one metric is equally valid everywhere.
- What sample size and statistical comparison is appropriate for each primary hypothesis?
  The final protocol requires researcher approval before execution.

## Web Research Status (2026-08-13)

Feature 003 includes a first web-research pass in
`research/sources/web-research-2026-08-13.json` and
`research/dossiers/web-research-findings-2026-08-13.md`. The pass used OpenAlex
metadata queries and followed DOI or ACL/arXiv landing pages for candidate
records. It found direct prior art for Self-Instruct, Southeast Asian code-mixed
generation, SeaLLMs, Singlish parsing, non-standard English robustness, and
cross-dialect evaluation.

The pass did not verify an official RegiCON 2026 CFP or author guide. This is a
blocking unresolved finding, not evidence that the venue has no requirements.
All candidate sources remain subject to researcher approval and full-paper
review before they can support final claims.

## Research Integrity Rules

- Do not invent papers, DOI values, venue rules, participants, results, or reviewer scores.
- Do not call a language setting low-resource without a source-backed characterization.
- Do not present CPU fixtures as publication evidence.
- Do not include restricted source content in public packages.
- Preserve negative, null, failed, stale, and contradictory evidence for auditability.