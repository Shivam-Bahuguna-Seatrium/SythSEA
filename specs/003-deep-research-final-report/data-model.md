# Feature 003 Data Model

## ResearchDossier

Represents one versioned research investigation.

- `dossier_id`, `version`, `title`, `target_venue`, `created_at`
- `source_refs`, `research_question_ids`, `novelty_summary`, `unresolved_items`
- `status`: `draft`, `reviewed`, `blocked`, or `approved`

## SourceRecord

Represents an academic, official, dataset, model, or technical source.

- `source_id`, `source_type`, `title`, `authors`, `year`, `venue`
- `doi_or_url`, `retrieved_at`, `contribution`, `limitation`, `relevance`
- `verification_status`: `candidate`, `verified`, `unavailable`, `conflicted`, or `rejected`
- `access_class`, `license_or_terms`

## ResearchQuestion

Represents a testable scientific question.

- `question_id`, `question`, `hypotheses`, `language_slices`, `claim_ids`
- `status`: planned, ready, tested, supported, unsupported, or unresolved

## ExperimentRequirement

Represents planned evidence needed for a question or claim.

- `requirement_id`, `question_id`, `claim_ids`, `condition_id`, `dataset_versions`
- `language_slices`, `metrics`, `sample_size`, `statistical_method`, `human_evaluation`
- `command`, `expected_artifacts`, `status`

## EvidenceRecord

Extends the existing evidence manifest concept with research status.

- `evidence_id`, `experiment_id`, `artifact_path`, `artifact_type`, `checksum`
- `language_slice`, `condition_id`, `access_class`, `status`, `provenance_refs`, `limitations`
- `status`: verified, provisional, missing, unsupported, restricted, excluded, stale, failed, or fixture

## ClaimEvidenceLink

Maps a claim to what supports it.

- `claim_id`, `claim_text`, `claim_type`, `evidence_ids`, `source_ids`
- `language_slices`, `transformation`, `status`, `review_notes`

## ReadinessReport

Represents the release decision.

- `package_id`, `blocking_issues`, `warnings`, `evidence_coverage`
- `citation_status`, `reproducibility_status`, `ethics_status`, `venue_status`
- `release_status`, `generated_at`

## Relationships and Invariants

- A dossier may not claim venue approval from an unresolved source.
- A research question must have at least one hypothesis and one language slice.
- An experiment requirement must define a command, expected artifact, metric, and status.
- Evidence is verified only when checksum, path, provenance, access decision, and required metadata validate.
- A primary claim is verified only when every supporting evidence record and source record is verified.
- Public packages cannot contain private or restricted artifact paths or content.
- Aggregate claims require slice-level evidence for every declared language slice, or must be marked incomplete.