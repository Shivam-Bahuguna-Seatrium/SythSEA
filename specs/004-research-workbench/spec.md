# Feature Specification: Local Research Workbench

**Feature Branch**: `004-research-workbench`

**Created**: 2026-08-14

**Status**: Draft

**Input**: User description: "Create a frontend for the SynthSEA research workflow that supports ingestion, fine-tuning, and chat inference like a chatbot."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Review and Ingest Research Data (Priority: P1)

As a research engineer, I want to upload or register a dataset through a guided workspace so that I can validate its provenance, license, language profile, access class, and retention requirements before it enters any SynthSEA workflow.

**Why this priority**: Data governance is a prerequisite for every downstream generation, fine-tuning, evaluation, and reporting activity.

**Independent Test**: Submit one complete public dataset record and one record with a missing license; verify that the workspace registers the complete record, blocks the incomplete record, and displays a clear validation outcome.

**Acceptance Scenarios**:

1. **Given** a researcher provides source, provenance, license, access, retention, and language-profile information, **When** ingestion validation completes, **Then** the workspace shows whether the dataset is eligible and records an auditable outcome.
2. **Given** a dataset has unresolved license, provenance, privacy, or retention information, **When** the researcher attempts ingestion, **Then** the workspace blocks the action and identifies every missing requirement.
3. **Given** a restricted or private dataset, **When** the researcher views release information, **Then** the workspace clearly distinguishes it from publicly releasable data and prevents public export selection.
4. **Given** a language profile has not been approved, **When** a researcher associates it with a dataset, **Then** the workspace prevents the dataset from becoming eligible for generation or training.

---

### User Story 2 - Configure and Monitor Fine-Tuning Runs (Priority: P1)

As an experimental ML researcher, I want to create, review, start, and monitor a fine-tuning run from approved datasets so that I can compare reproducible training conditions without manually assembling hidden configuration files.

**Why this priority**: Fine-tuning is a primary downstream-utility experiment and must remain distinct from synthetic-data quality claims.

**Independent Test**: Select an approved dataset tier and language slice, create a training configuration with a named base model and seed, start a bounded fixture run, and verify that run status, inputs, outputs, warnings, and reproducibility details are visible.

**Acceptance Scenarios**:

1. **Given** an eligible dataset and an approved language profile, **When** a researcher creates a fine-tuning configuration, **Then** the workspace requires a base model, dataset version, split, seed, language scope, training objective, and output location.
2. **Given** a requested training run uses restricted data or a model that is unavailable locally, **When** the researcher starts it, **Then** the workspace blocks or queues the run with an actionable explanation and does not silently substitute a model or dataset.
3. **Given** a running or completed fine-tuning job, **When** the researcher opens its detail view, **Then** the workspace shows status, start and finish times, configuration version, dataset version, model version, logs, artifacts, failures, and resource limitations.
4. **Given** multiple training conditions, **When** the researcher compares them, **Then** the workspace preserves baseline, full-pipeline, ablation, and language-slice identifiers without implying a result before evaluation completes.

---

### User Story 3 - Chat with a Local Inference Model (Priority: P1)

As a researcher, I want a chat workspace connected to a selected local model so that I can inspect responses, test prompts, and record non-evaluative exploratory interactions without confusing them with approved experiment results.

**Why this priority**: Interactive inference helps researchers understand local model behavior and draft prompts while maintaining a clear boundary from reproducible evaluation runs.

**Independent Test**: Select an available local model, submit a chat message, receive a streamed or completed response, and verify that the conversation records model version, prompt settings, timestamp, and local-only status.

**Acceptance Scenarios**:

1. **Given** a local model service is available, **When** a researcher selects a model and sends a message, **Then** the workspace displays the response and records the model version, settings, timestamp, and conversation identifier.
2. **Given** no local model service is available or a selected model is missing, **When** the researcher opens chat or sends a message, **Then** the workspace reports the unavailable status and a recovery action without exposing a misleading empty response.
3. **Given** a conversation contains sensitive, restricted, or private research material, **When** the researcher attempts to export or reuse it, **Then** the workspace enforces its access class and requires an explicit provenance decision before it can enter a dataset or experiment.
4. **Given** a chat response is exploratory, **When** the researcher views it alongside experiment artifacts, **Then** the workspace labels it as exploratory and prevents it from being treated as a measured result without a registered experiment.

---

### User Story 4 - Trace Research Evidence Across the Workspace (Priority: P2)

As a principal researcher, I want one workspace view that connects datasets, fine-tuning runs, chat sessions, evaluations, and report readiness so that I can identify missing evidence and reproduce any reported claim.

**Why this priority**: A unified traceability view reduces accidental use of unverified or restricted artifacts in research reporting.

**Independent Test**: Open a run with linked dataset, model, output, and evaluation records; verify that the workspace exposes its provenance chain, language slices, access class, reproducibility metadata, and unresolved blockers.

**Acceptance Scenarios**:

1. **Given** a registered artifact or run, **When** a researcher opens its provenance view, **Then** the workspace shows upstream sources, transformations, versions, checksums, access class, and downstream dependents.
2. **Given** four language-specific results exist, **When** the researcher opens a comparison view, **Then** the workspace shows each language slice separately before any aggregate result.
3. **Given** evidence is missing, stale, restricted, failed, or fixture-only, **When** the researcher opens report readiness, **Then** the workspace displays the status and blocking reason without allowing it to support a publication claim.

### Edge Cases

- A dataset upload may be interrupted, duplicated, malformed, too large, or have content that does not match its declared language profile; the workspace must preserve the failed state and avoid partial eligibility.
- A fine-tuning job may stop because of insufficient local memory, model-service failure, incompatible checkpoint, unavailable hardware, or user cancellation; partial artifacts must remain identifiable and cannot be marked complete.
- A local model may be replaced under the same display name; the workspace must retain the concrete model version or digest for each chat and run.
- A chat response may contain unsafe, culturally inappropriate, or unsupported content; the workspace must retain the interaction status and not promote it to a dataset or report automatically.
- A researcher may attempt to use an aggregate comparison with missing language slices; the workspace must display the incompleteness and block aggregate publication claims.
- A public export may be requested for a view containing restricted or private artifacts; the workspace must exclude those artifacts and record the exclusions.
- Multiple users may edit a draft configuration or review decision; the workspace must preserve prior versions and make conflicts visible.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The workspace MUST provide separate views for data ingestion, fine-tuning runs, local chat inference, artifact provenance, and research readiness.
- **FR-002**: The workspace MUST validate source, provenance, license, permitted use, access class, retention rule, and language-profile approval before marking a dataset eligible.
- **FR-003**: The workspace MUST distinguish public, restricted, and private datasets, artifacts, conversations, and exports, and MUST prevent restricted or private content from appearing in a public export.
- **FR-004**: The workspace MUST require a declared base model, model version, dataset version, split, seed, language scope, objective, and output location before a fine-tuning run starts.
- **FR-005**: The workspace MUST display fine-tuning run state, timestamps, configuration version, inputs, outputs, logs, warnings, failures, resource limitations, and reproducibility metadata.
- **FR-006**: The workspace MUST keep synthetic-data quality, fine-tuning progress, downstream evaluation, and publication claims as separate evidence categories.
- **FR-007**: The workspace MUST provide local chat inference using only a researcher-selected local model service and MUST display model availability, concrete model version, prompt settings, and local-only status.
- **FR-008**: The workspace MUST record each chat interaction with a conversation identifier, timestamp, model version, generation settings, access class, and exploratory status.
- **FR-009**: The workspace MUST require an explicit provenance and access decision before chat content can become a dataset record, prompt template, experiment input, or report evidence.
- **FR-010**: The workspace MUST display actionable errors when a local model, model variant, training dependency, dataset, or hardware resource is unavailable.
- **FR-011**: The workspace MUST preserve failed, cancelled, partial, stale, fixture, restricted, and missing states without representing them as completed results.
- **FR-012**: The workspace MUST provide provenance views that link datasets, configurations, model versions, prompts, seeds, runs, outputs, evaluations, checksums, and downstream artifacts.
- **FR-013**: The workspace MUST present Singapore English/Singlish, Malay, Tamil, and Singapore-context Mandarin as distinct language settings and MUST show them separately before aggregates.
- **FR-014**: The workspace MUST present baseline, full SynthSEA, ablation, translation baseline when available, and downstream conditions as distinct comparisons.
- **FR-015**: The workspace MUST surface report-readiness blockers for venue, evidence, citations, reproducibility, ethics, access restrictions, missing language slices, and incomplete required sections.
- **FR-016**: The workspace MUST support versioned, auditable changes to configurations, review decisions, and release selections.
- **FR-017**: The workspace MUST provide a CPU-safe fixture mode for local validation and MUST visibly label fixture outputs as non-publication evidence.
- **FR-018**: The workspace MUST not create, infer, or display fabricated results, citations, reviewer decisions, model availability, or completion statuses.

### Key Entities

- **Workspace Session**: A researcher interaction with an ingestion, training, chat, or evidence view, including access context and timestamps.
- **Dataset Intake**: A proposed dataset version with source, provenance, license, permitted use, retention, access class, language profile, validation status, and issues.
- **Fine-Tuning Run**: A versioned training request or execution with base model, dataset and split, seed, objective, resource settings, logs, artifacts, status, and limitations.
- **Chat Conversation**: An exploratory local-inference session with selected model, message history, generation settings, access class, provenance decision, and export status.
- **Artifact Lineage**: Links between sources, datasets, prompts, configurations, model versions, runs, evaluations, checksums, and report artifacts.
- **Readiness Item**: A blocking issue, warning, or verified condition for release or report generation.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A researcher can submit a dataset intake and see a complete eligible or blocked decision, including every missing governance field, without leaving the workspace.
- **SC-002**: 100% of started fine-tuning runs display their dataset version, base-model version, split, seed, language scope, status, and output or failure location.
- **SC-003**: 100% of chat messages display the selected local model version and are labeled exploratory until linked to a registered experiment.
- **SC-004**: A local-model availability failure produces a clear unavailable state and recovery action within the same workspace view.
- **SC-005**: Public-export views expose zero restricted or private artifact contents while reporting every excluded artifact identifier.
- **SC-006**: A researcher can navigate from any result, chat-derived candidate, or report-readiness item to its recorded provenance chain and current validation status.
- **SC-007**: Comparison views show all available target language slices separately before displaying any aggregate metric.
- **SC-008**: Fixture mode can demonstrate ingestion, fine-tuning status, chat status, and provenance workflows without a remote service or paid model API.
- **SC-009**: The workspace identifies every fixture missing-evidence, stale-artifact, unapproved-venue, missing-citation, and incomplete-reproducibility condition as non-release-ready.

## Assumptions

- The first release is a local-first research workspace for authorized researchers, not a public multi-tenant product.
- Existing SynthSEA data, experiment, paper, and research artifact contracts remain the source of truth; the workspace does not create a parallel evidence system.
- A locally installed model service is available for interactive chat and small pilot generation when the researcher chooses a local model.
- Fine-tuning may run locally or through a configured worker, but the workspace must disclose the actual execution location and available resource limits.
- User authentication, collaboration permissions, and remote deployment are deferred unless needed to protect restricted data in a later release.
- Human review, ethical review, and publication approval remain researcher responsibilities; the workspace records their status but does not replace them.

## Out of Scope

- Automatic publication submission or automatic claim approval.
- Treating chat output or a fine-tuning completion indicator as scientific evidence without registered evaluation.
- Uploading restricted or private source material to an unapproved external model service.
- Full production hosting, multi-organization tenancy, billing, or cloud resource provisioning.
- Automatic model downloading, model-license acceptance, or silent model substitution.