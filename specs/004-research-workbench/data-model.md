# Feature 004 Data Model

## DatasetIntake

Represents a proposed dataset registration from the workspace.

- `intake_id`: stable identifier
- `dataset`: existing source-dataset metadata
- `record_source`: local path or approved reference
- `validation_status`: draft, eligible, blocked, restricted, or failed
- `issues`: validation findings with field and message
- `requested_by`, `created_at`, `version`

**Rules**: An intake may create an eligible dataset only after provenance,
license, retention, access class, and approved language profile validate.

## FineTuningJob

Represents an asynchronous training request and execution.

- `job_id`, `run_id`, `created_at`, `started_at`, `completed_at`
- `dataset_version`, `dataset_tier`, `split_version`, `language_slices`
- `training_engine`: `mlx_lm`, `base_model`, `model_version`, `adapter_config`
- `seed`, `objective`, `execution_location`, `mlx_lm_version`, `training_command`
- `macos_version`, `unified_memory_mb`, `model_license`
- `status`: draft, queued, running, succeeded, failed, cancelled, blocked
- `configuration_ref`, `logs_ref`, `artifact_refs`, `failure_reason`, `limitations`

**Rules**: A job cannot start with an ineligible dataset, missing MLX-compatible
base-model version, missing license record, missing split, missing seed, or
unavailable Apple Silicon execution resource.

## ChatConversation

Represents an exploratory local-model conversation.

- `conversation_id`, `model_version`, `generation_settings`, `access_class`
- `status`: active, unavailable, blocked, archived
- `created_at`, `updated_at`, `provenance_decision`

## ChatMessage

Represents one user or assistant turn.

- `message_id`, `conversation_id`, `role`, `content`, `created_at`
- `model_version`, `input_tokens`, `output_tokens`, `seed`, `status`
- `exploratory`: always true on creation
- `promotion_status`: unreviewed, approved, rejected, or excluded

**Rules**: A chat message cannot be promoted to a dataset or experiment input
without an explicit access class and provenance decision.

## WorkspaceArtifactView

Represents a backend-projected lineage record for UI display.

- `artifact_id`, `artifact_type`, `access_class`, `validation_status`
- `source_refs`, `dependent_refs`, `checksum`, `language_slices`
- `created_at`, `limitations`, `public_export_eligible`

## ReadinessItem

Represents an evidence, venue, citation, ethics, reproducibility, or
language-coverage state surfaced to the workspace.

- `item_id`, `category`, `severity`, `status`, `message`
- `artifact_refs`, `language_slices`, `resolution_action`

## Relationships

- A `DatasetIntake` may create one `SourceDataset` and many data records.
- A `FineTuningJob` consumes one or more approved dataset versions and creates
  output artifacts and downstream evaluations.
- A `ChatConversation` contains messages and may create candidate artifacts only
  after explicit promotion.
- `WorkspaceArtifactView` links all entities through existing provenance and
  manifest records.
- `ReadinessItem` references the underlying evidence or compliance artifacts;
  it does not replace them.