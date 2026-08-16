# Data Model: Springer Conference Paper Generation

## VenueProfile

Represents the official requirements for one conference package.

Required fields: `venue_id`, `venue_name`, `requirements_source`, `accessed_at`,
`format_family`, `template_reference`, `page_limit`, `author_mode`,
`required_sections`, `reference_style`, `anonymization_rule`, `version`, and
`status`.

Statuses: `draft`, `reviewed`, `approved`, `conflicted`, `superseded`.
A package cannot be submission-ready unless the profile is `approved`.

## EvidenceManifest

Represents immutable verified experiment inputs.

Required fields: `manifest_id`, `manifest_version`, `source_root`, `artifact_refs`,
`experiment_ids`, `language_profiles`, `conditions`, `checksums`,
`access_summary`, `limitations`, `created_at`, and `verification_status`.

Verification statuses: `verified`, `missing`, `inconsistent`, `restricted`,
`blocked`.

## PaperClaim

Represents a manuscript claim or numerical statement.

Required fields: `claim_id`, `claim_text`, `claim_type`, `status`, `evidence_refs`,
`citation_refs`, `language_scope`, `condition_scope`, `created_at`, and
`review_notes`.

Claim statuses: `verified`, `missing`, `unsupported`, `restricted`, `excluded`,
`blocked`.
A claim with status `unsupported`, `missing`, or `blocked` cannot be rendered as
an asserted result.

## PaperSection

Represents one generated manuscript section.

Required fields: `section_id`, `section_type`, `content`, `claim_refs`,
`evidence_refs`, `citation_refs`, `required`, `status`, and `version`.

## PaperTable and PaperFigure

Each visual artifact requires `artifact_id`, `title`, `caption`, `source_refs`,
`transformation`, `language_slices`, `condition_ids`, `version`, `access_class`,
`output_path`, and `validation_status`.

A visual with an unresolved source reference is blocked from the public package.

## BibliographyEntry

Required fields: `citation_key`, `title`, `authors`, `year`, `venue`,
`identifier`, `source_reference`, `in_text_use_count`, `duplicate_group`, and
`validation_status`.

Validation statuses: `verified`, `incomplete`, `duplicate`, `unused`,
`unsupported`, `manual_review`.

## ReproducibilityAppendix

Required fields: `appendix_id`, `experiment_ids`, `dataset_versions`,
`prompt_versions`, `model_versions`, `seeds`, `config_refs`, `commands`,
`environment`, `artifact_checksums`, `limitations`, and `validation_status`.

## ComplianceResult

Required fields: `result_id`, `venue_profile_id`, `checks`, `blocking_issues`,
`warnings`, `page_count`, `missing_assets`, `citation_status`,
`reproducibility_status`, `ethics_status`, `release_status`, and `created_at`.

## PaperPackage

Represents the complete generated output.

Required fields: `package_id`, `package_version`, `venue_profile_id`,
`evidence_manifest_id`, `manuscript_source`, `bibliography_source`, `sections`,
`tables`, `figures`, `appendix`, `compliance_result`, `build_result`,
`included_artifacts`, `excluded_artifacts`, `access_class`, `manifest_checksum`,
and `created_at`.

## Relationships and Lifecycle

`VenueProfile` governs `PaperPackage`; `EvidenceManifest` supplies
`PaperClaim`, `PaperTable`, and `PaperFigure` references; claims populate
`PaperSection`; `BibliographyEntry` supports claims; `ReproducibilityAppendix`
records experiment provenance; `ComplianceResult` gates release.

The lifecycle is append-only: source evidence is never changed, paper packages
are versioned, and a new venue or evidence version creates a new package rather
than mutating an earlier one.
