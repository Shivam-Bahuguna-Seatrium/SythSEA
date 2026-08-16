# Research Workbench UI Contract

## Global Shell

- Left navigation: Overview, Data Intake, Fine-Tuning, Local Chat, Evidence.
- Header: current local-model state, active workspace, and non-dismissible
  release status.
- All views display access class and validation status as text plus color.
- No page may show a release-ready state when the backend readiness endpoint is blocked.

## Data Intake

- Intake form groups source, governance, language profile, and release fields.
- The submit action is unavailable until mandatory fields validate.
- Results show the complete blocking reason list and provide a link to lineage after registration.

## Fine-Tuning

- Configuration form identifies `MLX-LM` as the training engine and includes
  dataset, split, language slices, base model, version, license, adapter
  settings, seed, objective, execution location, and unified-memory guidance.
- Jobs list has stable status columns and links to logs, artifacts, and lineage.
- Job details display MLX-LM version, training command, checkpoint, macOS
  version, unified-memory record, and cancellation state.
- Cancel is an icon action with confirmation and only appears for queued or running jobs.

## Local Chat

- Model selector displays availability before a conversation can start.
- Conversation view shows model tag, seed, temperature, local-only status, and
  exploratory status beside the transcript.
- Promote action is disabled until an explicit access and provenance decision is supplied.

## Evidence

- Readiness view leads with blocking issues and shows evidence coverage by state.
- Comparison view renders language slices in the declared order before aggregate content.
- Artifact detail reveals source references, dependent references, checksum, and limitations.