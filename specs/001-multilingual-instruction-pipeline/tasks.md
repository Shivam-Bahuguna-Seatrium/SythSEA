---

description: "Task list for the SynthSEA multilingual synthetic instruction research pipeline"
---

# Tasks: Multilingual Synthetic Instruction Research Pipeline

**Input**: Design documents from `specs/001-multilingual-instruction-pipeline/`

**Prerequisites**: `plan.md`, `spec.md`, `research.md`, `data-model.md`, `contracts/`, and `quickstart.md`

**Tests**: Included because the specification requires deterministic tests, contract tests, integration tests, and smoke validation.

**Organization**: Tasks are grouped by user story. Every task has an exact path, a dependency note where applicable, and an observable acceptance check.

## Format

`- [ ] T### [P?] [US#?] [FR-###?] Description with exact file path and acceptance check`

- `[P]` means the task can run in parallel with other tasks in the same phase.
- `[US#]` maps a task to a user story from `spec.md`.
- `[FR-###]` maps a task to a functional requirement when applicable.

## Phase 1: Setup

**Purpose**: Create the CPU-first Python package and repository structure.

- [X] T001 Create `pyproject.toml` with Python 3.11+, runtime dependencies, optional development dependencies, CLI entry point, and package metadata; verify `python -m pip install -e ".[dev]"` is reproducible.
- [X] T002 [P] Create the planned directories under `src/synthsea/`, `tests/`, `configs/`, `data/`, `experiments/`, and `reports/`; verify every directory required by `plan.md` exists.
- [X] T003 [P] Add `src/synthsea/__init__.py`, `src/synthsea/cli.py`, and `tests/conftest.py`; verify the CLI exposes a version/help command without model or GPU access.
- [X] T004 [P] Add `configs/languages.yaml`, `configs/generation.yaml`, `configs/evaluation.yaml`, and `configs/models.yaml` with CPU-only fixture defaults; verify all files parse as YAML.
- [X] T005 [P] Configure Ruff, mypy, pytest, and coverage settings in `pyproject.toml`; verify the tools run against the empty package without configuration errors.

**Checkpoint**: The package installs locally and the CLI/test tooling runs without a GPU, paid API, or deployment service.

---

## Phase 2: Foundational Blocking Prerequisites

**Purpose**: Build shared schemas, storage, provenance, logging, and validation infrastructure before any user story implementation.

- [X] T006 [P] Define shared Pydantic base types, enums, timestamps, IDs, access classes, and reason codes in `src/synthsea/config/schemas.py`; verify invalid enum values are rejected.
- [X] T007 [P] Implement YAML loading, environment overrides, and configuration checks in `src/synthsea/config/loader.py`; verify missing required configuration produces an actionable error.
- [X] T008 [P] Implement structured logging and run-event records in `src/synthsea/tracking/events.py`; verify every event contains run ID, stage, timestamp, and severity.
- [X] T009 [P] Implement DuckDB catalog initialization and run/artifact registration in `src/synthsea/tracking/catalog.py`; verify a fresh catalog can create and query a run record.
- [X] T010 [P] Implement Parquet and JSON artifact read/write helpers in `src/synthsea/data/storage.py`; verify round-trip preservation of a fixture record and schema.
- [X] T011 [P] Implement SHA-256 checksums, artifact paths, and manifest generation in `src/synthsea/data/manifests.py`; verify changed content produces a changed checksum.
- [X] T012 [P] Implement provenance references and append-only version helpers in `src/synthsea/data/provenance.py`; verify a record retains its source and transformation chain.
- [X] T013 [P] Add contract validation utilities for the schemas in `contracts/artifact-manifest.schema.json` and `contracts/experiment-config.schema.json` under `src/synthsea/config/contracts.py`; verify valid fixtures pass and malformed fixtures fail.
- [X] T014 [P] Add foundational unit tests for schemas, YAML loading, catalog setup, artifact storage, checksums, provenance, and contract validation in `tests/unit/test_foundation.py`; verify tests pass without network access.

**Checkpoint**: Shared state, artifacts, contracts, logging, and deterministic fixtures are ready; all user stories may now proceed.

---

## Phase 3: User Story 1 - Define and Track Research Data (Priority: P1, MVP)

**Goal**: Register validated language profiles and source datasets with provenance, licensing, privacy, access, retention, and public/private release controls.

**Independent Test**: Register one public and one restricted fixture per language profile, reject incomplete metadata, and verify a generated test record traces to an eligible source without leaking restricted content into a public manifest.

### Tests for User Story 1

- [X] T015 [P] [US1] [FR-003] Add language-profile validation fixtures for all four profiles in `tests/fixtures/language_profiles.yaml`; verify unvalidated profiles cannot enter generation.
- [X] T016 [P] [US1] [FR-001] Add dataset-ingestion fixtures covering public, restricted, missing-license, expired-retention, mixed-language, and ambiguous-variety records in `tests/fixtures/datasets/records.yaml`.
- [X] T017 [P] [US1] [FR-002] Add access-control and public-export contract tests in `tests/contract/test_data_governance.py`; verify restricted artifacts are excluded from public manifests.
- [X] T018 [P] [US1] [FR-001] Add provenance integration tests in `tests/integration/test_ingestion_provenance.py`; verify content hashes, source references, versions, and rejection reasons survive ingestion.

### Implementation for User Story 1

- [X] T019 [P] [US1] [FR-003] Implement `LanguageProfile` models and allowed-profile loading in `src/synthsea/profiles/models.py`; verify required inclusion, script, cultural, code-switching, and resource fields are enforced.
- [X] T020 [US1] [FR-003] Implement qualified reviewer validation and profile lifecycle in `src/synthsea/profiles/validation.py`; depends on T006 and T019; verify only approved profiles are generation-eligible.
- [X] T021 [P] [US1] [FR-001] Implement `SourceDataset` and `DataRecord` models in `src/synthsea/data/models.py`; verify access class, retention rule, license, profile, and provenance fields are required.
- [X] T022 [US1] [FR-001] Implement dataset ingestion and metadata validation in `src/synthsea/data/ingest.py`; depends on T007, T010, T012, T019, and T021; verify invalid datasets are rejected or marked ineligible.
- [X] T023 [US1] [FR-019] Implement public/restricted artifact filtering in `src/synthsea/export/public_private.py`; depends on T011 and T022; verify public export manifests contain only approved public artifacts and list exclusions.
- [X] T024 [US1] [FR-001] Add a `synthsea data register` CLI command in `src/synthsea/cli.py`; depends on T020 and T022; verify a fixture dataset can be registered and queried from DuckDB.

**Checkpoint**: User Story 1 is independently usable as the minimum viable research data catalog and provenance workflow.

---

## Phase 4: User Story 2 - Generate Language-Aware Instructions (Priority: P1)

**Goal**: Execute explicit generation stages with local/remote model adapters and controlled monolingual or English-mixing conditions.

**Independent Test**: Run a deterministic fixture through the stage graph for one language profile and one English-mixing condition; verify stage outputs, failures, prompts, model metadata, and code-switch labels.

### Tests for User Story 2

- [X] T025 [P] [US2] [FR-005] Add stage protocol tests in `tests/unit/test_stage_protocol.py`; verify each stage receives a typed input, emits a typed result, and records pass/fail/flag/retry decisions.
- [X] T026 [P] [US2] [FR-006] Add model-adapter tests using a deterministic fake adapter in `tests/unit/test_model_adapters.py`; verify prompt, model version, seed, request, response, and failure metadata are recorded.
- [X] T027 [P] [US2] [FR-004a] Add code-switching contract tests in `tests/contract/test_code_switching.py`; verify switch points, direction, proportion, intent, and condition are required when switching is enabled.
- [X] T028 [P] [US2] [FR-004] Add generation-run integration tests in `tests/integration/test_generation_pipeline.py`; verify resumable partial runs do not count failed outputs as valid examples.

### Implementation for User Story 2

- [X] T029 [P] [US2] [FR-005] Implement the typed stage protocol and stage result model in `src/synthsea/agents/base.py`; verify stage version and reason codes are persisted.
- [X] T030 [P] [US2] [FR-005] Implement stage role modules in `src/synthsea/agents/language_profile.py`, `resource_discovery.py`, `topic_context.py`, `instruction_generation.py`, `language_specialist.py`, `cultural_validation.py`, `semantic_validation.py`, `diversity_difficulty.py`, `critic.py`, `judge.py`, and `refinement.py`; verify each module can run as a no-op deterministic fixture stage.
- [X] T031 [P] [US2] [FR-006] Implement local and remote model adapter interfaces in `src/synthsea/generation/adapters.py`; verify local fake inference works without GPU and remote adapters expose provider/cost metadata without embedding credentials.
- [X] T032 [P] [US2] [FR-006] Implement batching, bounded concurrency, cache keys, retry/backoff, rate limits, and resumable checkpoints in `src/synthsea/generation/batching.py`, `cache.py`, and `retry.py`; verify retries and cache hits are logged.
- [X] T033 [US2] [FR-004] Implement generation configuration validation and stage-graph execution in `src/synthsea/generation/runner.py`; depends on T007, T012, T029, T030, T031, and T032; verify baseline stages can be disabled for ablations.
- [X] T034 [US2] [FR-004a] Implement predefined monolingual and English-mixing policies in `src/synthsea/agents/code_switching.py`; depends on T019 and T029; verify invalid switch proportions or missing labels fail validation.
- [X] T035 [US2] [FR-006] Add a `synthsea generate` CLI command in `src/synthsea/cli.py`; depends on T024 and T033; verify the CPU fixture produces a versioned artifact and run manifest.

**Checkpoint**: User Story 2 can generate a small, fully traced dataset with no GPU or paid model API.

---

## Phase 5: User Story 3 - Filter and Review Generated Data (Priority: P1)

**Goal**: Filter malformed, unsafe, culturally inappropriate, semantically invalid, duplicated, or low-quality examples and preserve review decisions.

**Independent Test**: Process a fixture batch containing valid, malformed, unsafe, duplicate, near-duplicate, culturally questionable, and reviewer-disagreement examples; verify every item has an auditable status and reason.

### Tests for User Story 3

- [X] T036 [P] [US3] [FR-007] Add quality, schema, safety, semantic, cultural, and factual validation fixtures in `tests/fixtures/filtering/records.yaml`; verify each deliberate failure maps to a distinct reason code.
- [X] T037 [P] [US3] [FR-008] Add exact and near-duplicate tests in `tests/unit/test_deduplication.py`; verify duplicate groups, comparison basis, selected record, and decision reason are deterministic.
- [X] T038 [P] [US3] [FR-009] Add annotation and disagreement tests in `tests/unit/test_review.py`; verify reviewer roles, rubric versions, abstentions, disagreements, and timestamps are retained.
- [X] T039 [P] [US3] [FR-010] Add filtering/review integration tests in `tests/integration/test_quality_gate.py`; verify rejected records are excluded from eligible datasets but remain queryable.

### Implementation for User Story 3

- [X] T040 [P] [US3] [FR-007] Implement quality, safety, semantic, cultural, and factual validators in `src/synthsea/filtering/quality.py`, `safety.py`, and `src/synthsea/agents/semantic_validation.py`; verify validators return versioned decisions and reasons.
- [X] T041 [P] [US3] [FR-008] Implement exact hashing and configurable near-duplicate detection in `src/synthsea/filtering/deduplication.py`; verify language/profile metadata is preserved while comparing normalized content.
- [X] T042 [P] [US3] [FR-009] Implement review record creation and rubric loading in `src/synthsea/review/annotation.py`; verify reviewer pseudonyms are stored instead of unnecessary personal information.
- [X] T043 [US3] [FR-010] Implement disagreement and adjudication workflows in `src/synthsea/review/adjudication.py`; depends on T042; verify original reviews remain append-only after adjudication.
- [X] T044 [US3] [FR-007] Implement the final quality-gate coordinator in `src/synthsea/filtering/pipeline.py`; depends on T040, T041, T042, and T043; verify only passed or explicitly approved records enter a release candidate.
- [X] T045 [US3] [FR-007] Add a `synthsea filter` CLI command in `src/synthsea/cli.py`; depends on T035 and T044; verify filtering produces a report of pass, fail, flag, abstain, and excluded counts.

**Checkpoint**: User Story 3 produces an auditable release candidate from noisy synthetic data.

---

## Phase 6: User Story 4 - Run Comparable Experiments (Priority: P1)

**Goal**: Run Tier A, Tier B, optional Tier D, and Tier C conditions with comparable splits, baselines, ablations, and reproducibility metadata.

**Independent Test**: Run one baseline, one full pipeline condition, and one ablation on the same CPU fixture and split manifest; verify condition IDs and artifacts are comparable.

### Tests for User Story 4

- [X] T046 [P] [US4] [FR-012] Add experiment configuration contract fixtures and tests in `tests/contract/test_experiment_config.py`; verify required IDs, profiles, datasets, seeds, and metrics are enforced.
- [X] T047 [P] [US4] [FR-011] Add dataset-tier tests in `tests/unit/test_dataset_tiers.py`; verify Tier A human, Tier B single-agent, optional Tier D translation, and Tier C SynthSEA records remain distinguishable.
- [X] T048 [P] [US4] [FR-012] Add split and seed reproducibility tests in `tests/unit/test_experiment_registry.py`; verify identical manifests produce identical run fingerprints.
- [X] T049 [P] [US4] [FR-012] Add baseline/ablation integration tests in `tests/integration/test_experiment_runner.py`; verify disabled stages and changed conditions produce distinct run IDs and comparable outputs.

### Implementation for User Story 4

- [X] T050 [P] [US4] [FR-012] Implement experiment configuration models and validation in `src/synthsea/experiments/config.py`; depends on T013; verify configs validate against `contracts/experiment-config.schema.json`.
- [X] T051 [P] [US4] [FR-011] Implement Tier A, Tier B, Tier C, and optional Tier D dataset labeling in `src/synthsea/experiments/baselines.py`; verify each tier has a declared source and condition manifest.
- [X] T052 [US4] [FR-012] Implement run registry, split manifests, seed manifests, and run fingerprints in `src/synthsea/experiments/registry.py`; depends on T009, T011, T012, T048, and T050.
- [X] T053 [US4] [FR-012] Implement baseline and ablation condition builders in `src/synthsea/experiments/ablations.py`; depends on T033, T050, and T051; verify each condition declares changed variables.
- [X] T054 [US4] [FR-013] Implement the experiment runner in `src/synthsea/experiments/runner.py`; depends on T035, T045, T052, and T053; verify partial and failed runs remain recorded and are excluded from completed comparisons.
- [X] T055 [US4] [FR-006] Add a `synthsea experiment run` CLI command in `src/synthsea/cli.py`; depends on T054; verify a CPU fixture can execute Tier B and Tier C conditions from configuration files.

**Checkpoint**: User Story 4 creates comparable, reproducible experiment artifacts for the primary research comparison.

---

## Phase 7: User Story 5 - Evaluate, Analyze, and Report Findings (Priority: P1)

**Goal**: Produce language-specific automated and human evaluation, statistical analysis, leakage checks, error analysis, and publication-ready exports.

**Independent Test**: Evaluate a completed fixture run and export a report package containing four language slices, metrics, human-review summaries, statistical uncertainty, errors, limitations, and a valid manifest.

### Tests for User Story 5

- [X] T056 [P] [US5] [FR-014] Add automated metric fixtures and tests in `tests/unit/test_automatic_metrics.py`; verify metric definitions, denominators, exclusions, and language slices are recorded.
- [X] T057 [P] [US5] [FR-015] Add human-evaluation summary tests in `tests/unit/test_human_evaluation.py`; verify rubric, sample counts, reviewer limits, and agreement/disagreement summaries are retained.
- [X] T058 [P] [US5] [FR-017] Add statistical analysis tests in `tests/unit/test_statistics.py`; verify bootstrap/permutation uncertainty and declared comparison metadata are deterministic for fixed seeds.
- [X] T059 [P] [US5] [FR-018] Add leakage and contamination fixtures in `tests/unit/test_leakage.py`; verify prompt overlap, duplicate evaluation records, and exposed benchmark examples are flagged.
- [X] T060 [P] [US5] [FR-016] Add error-analysis tests in `tests/unit/test_error_analysis.py`; verify errors map to categories and retain auditable record references.
- [X] T061 [P] [US5] [FR-019] Add publication-manifest contract tests in `tests/contract/test_publication_export.py`; verify public packages exclude restricted artifacts and include checksums and exclusions.

### Implementation for User Story 5

- [X] T062 [P] [US5] [FR-014] Implement automated metric adapters and language-slice aggregation in `src/synthsea/evaluation/automatic.py`; verify unsupported metrics are reported with exclusion reasons.
- [X] T063 [P] [US5] [FR-015] Implement human-evaluation aggregation and agreement summaries in `src/synthsea/evaluation/human.py`; depends on T043; verify disagreements are not silently collapsed.
- [X] T064 [P] [US5] [FR-017] Implement bootstrap/permutation uncertainty, comparison metadata, and multiplicity notes in `src/synthsea/evaluation/statistics.py`; verify fixed seeds reproduce results.
- [X] T065 [P] [US5] [FR-018] Implement prompt overlap, content-hash, benchmark exposure, and contamination reporting in `src/synthsea/evaluation/leakage.py`; depends on T011 and T012.
- [X] T066 [P] [US5] [FR-016] Implement error taxonomy, sampled examples, and category summaries in `src/synthsea/evaluation/errors.py`; verify every error references a source record and stage decision.
- [X] T067 [US5] [FR-019] Implement report assembly and publication export in `src/synthsea/export/reports.py`; depends on T062, T063, T064, T065, and T066; verify methods, configurations, results, limitations, and provenance are included.
- [X] T068 [US5] [FR-019] Add a `synthsea evaluate` and `synthsea export` CLI command in `src/synthsea/cli.py`; depends on T067; verify a completed fixture run produces public and restricted packages.

**Checkpoint**: User Story 5 produces reviewable, language-specific, publication-oriented evidence from a completed experiment.

---

## Phase 8: Polish and Cross-Cutting Concerns

**Purpose**: Complete reproducibility, documentation, cost reporting, and end-to-end validation without adding deployment infrastructure.

- [X] T069 [P] [FR-006] Implement token, request, retry, cache-hit, and estimated-cost accounting in `src/synthsea/tracking/costs.py`; verify each run reports examples, tokens, calls, failures, and estimated cost.
- [X] T070 [P] [FR-021] Implement complete reproducibility manifests in `src/synthsea/tracking/catalog.py` and `src/synthsea/data/manifests.py`; verify inputs, configs, seeds, prompts, models, environment, outputs, and validation status are linked.
- [X] T071 [P] [FR-022] Add ethical, cultural, privacy, licensing, representation-gap, compute, and model-access reporting templates in `reports/templates/publication-sections.md`; verify every publication package includes these sections.
- [X] T072 [P] Add the CPU-only end-to-end smoke workflow from `quickstart.md` in `tests/smoke/test_quickstart.py`; verify it runs without a GPU, remote model, or paid API.
- [X] T073 [P] Add package/API usage and reproducibility documentation in `README.md` and `docs/reproducibility.md`; verify commands match the validated quickstart.
- [X] T074 Run the complete quality gate from `pyproject.toml` using `pytest`, `ruff check .`, and `mypy src`; fix only task-related failures and verify all checks pass.
- [X] T075 Run `/speckit-analyze` against `spec.md`, `plan.md`, `tasks.md`, and generated contracts; review its read-only report and do not write an `analysis.md` file from this task.

- [X] T076 [P] [US4] [FR-013] Add downstream adaptation contract tests in `tests/contract/test_downstream_evaluation.py`; verify dataset tier, model version, adaptation configuration, checkpoint reference, and language profile are required.
- [X] T077 [US4] [FR-013] Implement downstream adaptation and evaluation records in `src/synthsea/training/downstream.py`; verify downstream utility is reported separately from synthetic-data quality.
- [X] T078 [P] [US5] [FR-014] Add the 10,000-record CPU benchmark in `tests/smoke/test_performance.py`; verify metadata, filtering, and export complete in under 60 seconds on the declared runner.
- [X] T079 [P] [FR-019] Add public/restricted/private access-class contract tests in `tests/contract/test_access_classes.py`; verify restricted and private artifacts are excluded from public manifests.
- [X] T080 [P] [FR-003a] Add explicit language-profile approval task coverage in `tests/contract/test_language_profile_approval.py`; verify profile inclusion, cultural, script, resource, and reviewer-validation fields are required.
- [X] T081 [P] [US2] [FR-006] Implement the local Ollama generation adapter with model tag, seed, temperature, timeout, token metadata, and actionable connection failures in `src/synthsea/generation/adapters.py` and `tests/unit/test_model_adapters.py`.
- [X] T082 [US2] [FR-006] Add CLI adapter selection and an Apple Silicon Ollama model profile in `src/synthsea/cli.py` and `configs/models.yaml`; verify fixture and Ollama paths use the same generation-run contract.
- [X] T083 [P] [FR-021] Document the Apple Silicon pilot, local Ollama setup, reproducibility metadata, research limitations, and architecture path in `docs/macos-ollama.md`, `docs/architecture.md`, `README.md`, and `specs/001-multilingual-instruction-pipeline/`.
- [X] T084 [P] [US4] [FR-013] Define MLX-LM as the Apple Silicon fine-tuning engine, including model-license, command, seed, checkpoint, environment, unified-memory, and checksum metadata requirements in `specs/001-multilingual-instruction-pipeline/plan.md`, `research.md`, and `quickstart.md`.
- [X] T085 [P] [FR-021] Update the local Apple Silicon architecture and run guide so MLX-LM owns fine-tuning while Ollama remains limited to chat and local generation in `docs/architecture.md` and `docs/macos-ollama.md`.

## Dependencies and Execution Order

### Phase Dependencies

- **Phase 1 Setup**: No dependencies; T002-T005 can run in parallel after T001 where needed.
- **Phase 2 Foundational**: Depends on T001 and T002; T006-T014 are mostly parallel and block all user stories.
- **Phase 3 User Story 1**: Depends on Phase 2; establishes the MVP data and provenance boundary.
- **Phase 4 User Story 2**: Depends on Phase 2 and the approved profiles/artifact helpers from US1; generation remains independently testable with fixtures.
- **Phase 5 User Story 3**: Depends on Phase 2 and generated-record contracts from US2; filtering can be tested independently with fixture records.
- **Phase 6 User Story 4**: Depends on Phases 2-5 because experiments consume eligible generated and reviewed artifacts.
- **Phase 7 User Story 5**: Depends on Phase 6 completed run records and evaluation inputs.
- **Phase 8 Polish**: Depends on the desired user stories being complete.

### User Story Order

1. **US1 (P1)**: Can start after foundational work; recommended MVP.
2. **US2 (P1)**: Depends on validated profiles and artifact contracts from US1.
3. **US3 (P1)**: Depends on generated-record shape from US2 but uses independent fixtures for testing.
4. **US4 (P1)**: Depends on eligible records and filtering decisions from US1-US3.
5. **US5 (P1)**: Depends on experiment artifacts from US4.

### Parallel Opportunities

- T002-T005 can run in parallel after the package metadata in T001 exists.
- T006-T014 can run in parallel once the package structure exists.
- US1 fixture tests T015-T018 can run in parallel; model/validation/ingestion work can then proceed by file.
- US2 stage protocol, adapter, code-switch, and integration tests T025-T028 can run in parallel.
- US3 validators, deduplication, review, and integration tests T036-T039 can run in parallel.
- US4 contract, tier, registry, and runner tests T046-T049 can run in parallel.
- US5 metric, human, statistics, leakage, error, and export contract tests T056-T061 can run in parallel.
- T069-T073 can run in parallel after the core stories are complete.

## Parallel Execution Examples

### User Story 1

```text
T015 language profile fixtures
T016 dataset ingestion fixtures
T017 access-control contract tests
T018 provenance integration tests
```

### User Story 2

```text
T025 stage protocol tests
T026 model adapter tests
T027 code-switching contract tests
T028 generation integration tests
```

### User Story 5

```text
T056 automated metric tests
T057 human-evaluation tests
T058 statistics tests
T059 leakage tests
T060 error-analysis tests
T061 publication-export tests
```

## Implementation Strategy

### MVP First

1. Complete Phase 1 and Phase 2.
2. Complete User Story 1.
3. Validate public/restricted ingestion and provenance independently.
4. Stop for review before enabling model-backed generation.

### Incremental Research Delivery

1. Add US2 with the deterministic CPU adapter first, then optional local/remote adapters.
2. Add US3 and establish the quality-gated release candidate.
3. Add US4 with Tier A/B/C and optional Tier D comparisons.
4. Add US5 and generate language-specific pilot reports.
5. Increase data-efficiency conditions only after the CPU smoke path and pilot report pass.

### Constraints for Every Implementation Task

- Do not add deployment or production infrastructure in this feature.
- Keep the first milestone runnable without a GPU, secret, or paid model API.
- Preserve failed, rejected, incomplete, and restricted records with reasons.
- Use append-only versions for research artifacts and include exact file paths in changes.
- Validate tests and contracts before expanding experiment scale.

## Completion Criteria

- Every task above has a checkbox, sequential ID, required labels, and an exact file path.
- Every user story has an independent test and checkpoint.
- Every functional requirement in the specification maps to one or more tasks.
- The first milestone can run with deterministic CPU fixtures.
- `tasks.md` is ready for `/speckit-analyze` and then `/speckit-implement`.