# Data Model: SynthSEA Research Pipeline

## Core Entities

### LanguageProfile

Represents one validated evaluation setting.

Required fields: `profile_id`, `display_name`, `language_or_variety`, `region`;
`script_or_orthography`, `inclusion_rules`, `cultural_context`,
`code_switching_notes`, `resource_limitations`, `validation_status`,
`validated_by_role`, `validated_at`, and `profile_version`.

Allowed initial profiles: Singapore English/Singlish, Malay, Tamil, and
Singapore-context Mandarin. A profile is not eligible for generation or
evaluation until validation status is approved.

### SourceDataset

Represents a source collection or seed dataset.

Required fields: `dataset_id`, `dataset_version`, `source_uri_or_reference`,
`provenance`, `license`, `permitted_use`, `access_class`, `retention_rule`,
`language_profile_id`, `acquisition_method`, `content_hash`, `record_count`,
`created_at`, and `status`.

Statuses: `pending_review`, `eligible`, `restricted`, `rejected`, `expired`.

Records with unresolved license, provenance, privacy, access, or retention
requirements cannot become `eligible`.

Access classes have these meanings:

- `public`: approved for external release.
- `restricted`: approved for project research but excluded from public exports.
- `private`: researcher-only material excluded from public exports.

### DataRecord

Represents a source, generated, reviewed, or evaluation example.

Required fields: `record_id`, `dataset_id`, `record_version`, `instruction`,
`response`, `language_profile_id`, `task_category`, `source_type`,
`access_class`, `provenance_ref`, `quality_status`, `created_at`, and
`content_hash`.

Optional code-switch fields: `switch_condition`, `switch_points`,
`switch_direction`, `language_proportion`, and `communicative_intent`.

### GenerationConfiguration

Defines one reproducible generation condition.

Required fields: `config_id`, `config_version`, `stage_graph_version`,
`language_profile_id`, `condition_id`, `prompt_versions`, `model_versions`,
`parameters`, `random_seeds`, `sampling_policy`, `code_switch_policy`,
`source_dataset_versions`, and `created_at`.

### StageResult

Captures the output of one pipeline stage.

Required fields: `stage_result_id`, `run_id`, `stage_name`, `stage_version`,
`input_record_ids`, `output_record_ids`, `decision`, `reason_codes`,
`checker_metadata`, `created_at`, and `artifact_ref`.

Decisions include `pass`, `fail`, `flag`, `abstain`, `retry`, and `skipped`.

### ReviewRecord

Represents a human or automated review.

Required fields: `review_id`, `record_id`, `review_type`, `rubric_version`,
`reviewer_role`, `decision`, `ratings`, `rationale`, `reviewer_pseudonym`,
`created_at`, and `access_class`.

Disagreement and adjudication are additional records linked to the original
reviews; earlier decisions are never overwritten.

### ExperimentRun

Represents one baseline, full-pipeline, ablation, transfer, or downstream run.

Required fields: `run_id`, `experiment_id`, `condition_id`, `config_id`,
`dataset_versions`, `split_manifest`, `seed_manifest`, `model_manifest`,
`prompt_manifest`, `software_environment`, `status`, `started_at`, `ended_at`,
`failure_summary`, and `artifact_manifest_ref`.

Statuses: `planned`, `running`, `partial`, `completed`, `failed`, `cancelled`.

### EvaluationResult

Represents a metric, human summary, statistical comparison, leakage result, or
error analysis.

Required fields: `evaluation_id`, `run_id`, `evaluation_type`, `language_profile_id`,
`metric_name`, `metric_version`, `sample_definition`, `denominator`,
`exclusions`, `value`, `uncertainty`, `comparison_ref`, `created_at`, and
`artifact_ref`.

### DownstreamEvaluation

Represents model adaptation and downstream utility evaluation separately from
synthetic-data quality.

Required fields: `evaluation_id`, `run_id`, `dataset_tier`, `model_version`,
`adaptation_config`, `checkpoint_ref`, `language_profile_id`, `metric_name`,
`value`, `uncertainty`, `sample_definition`, and `artifact_ref`.

### PublicationPackage

Represents a versioned export for review or release.

Required fields: `package_id`, `package_version`, `run_ids`, `included_artifacts`,
`excluded_artifacts`, `provenance_summary`, `limitations`, `license_summary`,
`access_class`, `manifest_checksum`, and `created_at`.

Public packages MUST contain only public-approved records and artifacts.

## Relationships and Lifecycle

`LanguageProfile` validates `SourceDataset`; a `SourceDataset` contains
`DataRecord` values; a `GenerationConfiguration` selects profiles and dataset
versions; an `ExperimentRun` executes the configuration; each stage creates
`StageResult` records; `ReviewRecord` values assess records or profiles;
`EvaluationResult` values summarize runs; `PublicationPackage` references only
approved artifacts.

The lifecycle is append-only for scientific records: corrections create a new
version, failures remain visible, and public export is a derived view rather
than a mutation of restricted data.