---
description: "Implementation tasks for Feature 003 research-to-publication workflow"
---

# Tasks: Deep Research and Final Reproducible Report

**Input**: Design documents from `specs/003-deep-research-final-report/`

**Prerequisites**: `plan.md`, `spec.md`, `research.md`, `data-model.md`, `contracts/`, `quickstart.md`

**Tests**: Required by the feature specification for evidence integrity, contract validation, and report readiness.

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Establish the research module and fixture/documentation paths.

- [x] T001 Create the research package structure in `src/synthsea/research/__init__.py` and `tests/research/__init__.py`
- [x] T002 [P] Create research artifact directories and README markers in `research/sources/.gitkeep`, `research/dossiers/.gitkeep`, `research/requirements/.gitkeep`, and `research/matrices/.gitkeep`
- [x] T003 [P] Add the Feature 003 contract fixtures in `tests/research/fixtures/research-dossier.json` and `tests/research/fixtures/evidence-matrix.json`
- [x] T004 [P] Add Feature 003 CLI and validation examples to `docs/research-report.md`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Implement shared typed states, serialization, and validation helpers before user stories.

- [x] T005 Add research evidence, source, dossier, and release status enums in `src/synthsea/research/models.py`
- [x] T006 [P] Add strict Pydantic models for SourceRecord, ResearchDossier, ResearchQuestion, and ExperimentRequirement in `src/synthsea/research/models.py`
- [x] T007 [P] Add strict Pydantic models for EvidenceRecord, ClaimEvidenceLink, and ReadinessReport in `src/synthsea/research/models.py`
- [x] T008 Implement JSON/YAML loading, writing, and schema validation helpers in `src/synthsea/research/io.py`
- [x] T009 Implement four-language slice constants and aggregate coverage validation in `src/synthsea/research/languages.py`
- [x] T010 [P] Add contract tests for dossier and evidence-matrix schemas in `tests/research/contract/test_research_contracts.py`
- [x] T011 [P] Add model validation tests for status transitions and required metadata in `tests/research/contract/test_research_models.py`

**Checkpoint**: Typed research artifacts and contracts validate independently.

---

## Phase 3: User Story 1 - Build an Evidence-Grounded Research Dossier (Priority: P1) 🎯 MVP

**Goal**: Register verifiable sources, create the literature matrix, capture novelty analysis, and preserve unresolved venue requirements.

**Independent Test**: Supply public, unavailable, duplicate, and unresolved source records and verify that the dossier identifies verification status, source provenance, novelty gaps, and venue blockers.

### Tests for User Story 1

- [x] T012 [P] [US1] Add source-record duplicate and verification tests in `tests/research/contract/test_sources.py`
- [x] T013 [P] [US1] Add dossier generation integration tests in `tests/research/integration/test_dossier.py`

### Implementation for User Story 1

- [x] T014 [P] [US1] Implement SourceRecord normalization, duplicate detection, and verification-state handling in `src/synthsea/research/sources.py`
- [x] T015 [US1] Implement literature matrix serialization and source provenance checks in `src/synthsea/research/sources.py`
- [x] T016 [US1] Implement ResearchDossier assembly with novelty, gap, venue, and unresolved-item summaries in `src/synthsea/research/dossier.py`
- [x] T017 [US1] Implement official-source and venue-approval checks without selecting an unverified template in `src/synthsea/research/venue_research.py`
- [x] T018 [US1] Add `research dossier` CLI command in `src/synthsea/cli.py`
- [x] T019 [US1] Add dossier and literature output writing under `research/dossiers/` and `research/sources/` in `src/synthsea/research/dossier.py`

**Checkpoint**: A researcher can generate an auditable dossier and see why venue approval remains blocked.

---

## Phase 4: User Story 2 - Define the Research and Experiment Readiness Plan (Priority: P1)

**Goal**: Convert research questions into explicit experiment, metric, language, human-review, ethics, and artifact requirements.

**Independent Test**: Generate a matrix from a dossier and verify that each question and claim has conditions, language slices, metrics, commands, expected artifacts, and a readiness status.

### Tests for User Story 2

- [x] T020 [P] [US2] Add experiment-requirement validation tests in `tests/research/contract/test_requirements.py`
- [x] T021 [P] [US2] Add language-slice and aggregate-coverage tests in `tests/research/integration/test_language_coverage.py`

### Implementation for User Story 2

- [x] T022 [P] [US2] Implement ResearchQuestion and ExperimentRequirement validation in `src/synthsea/research/requirements.py`
- [x] T023 [US2] Implement baseline, full-pipeline, ablation, control, human-evaluation, statistics, safety, and error-analysis requirement builders in `src/synthsea/research/requirements.py`
- [x] T024 [US2] Implement claim-to-requirement and four-language coverage matrix generation in `src/synthsea/research/matrix.py`
- [x] T025 [US2] Implement missing dependency, license, reviewer, compute, and venue blocker classification in `src/synthsea/research/readiness.py`
- [x] T026 [US2] Add `research matrix` CLI command in `src/synthsea/cli.py`
- [x] T027 [US2] Write requirements and evidence matrices under `research/requirements/` and `research/matrices/` in `src/synthsea/research/matrix.py`

**Checkpoint**: Every intended report claim has a declared, testable evidence requirement.

---

## Phase 5: User Story 3 - Run and Register Reproducible Research Evidence (Priority: P1)

**Goal**: Register immutable experiment artifacts with checksums, provenance, access class, language slice, command, environment, and fixture/real status.

**Independent Test**: Register a CPU fixture manifest, mutate an artifact, and verify that the second check reports stale evidence while public export excludes restricted content.

### Tests for User Story 3

- [x] T028 [P] [US3] Add checksum, stale-artifact, and source-immutability tests in `tests/research/integration/test_evidence_registry.py`
- [x] T029 [P] [US3] Add restricted-artifact exclusion tests in `tests/research/contract/test_public_evidence.py`

### Implementation for User Story 3

- [x] T030 [US3] Implement EvidenceRecord loading and manifest registration in `src/synthsea/research/evidence.py`
- [x] T031 [US3] Extend evidence verification to validate path existence, checksum, provenance, access class, language slice, condition, and fixture status in `src/synthsea/research/evidence.py`
- [x] T032 [US3] Implement reproducibility metadata validation for commands, inputs, outputs, models, prompts, seeds, environment, and dataset versions in `src/synthsea/research/reproducibility.py`
- [x] T033 [US3] Implement public evidence projection that excludes restricted/private content and records exclusions in `src/synthsea/research/evidence.py`
- [x] T034 [US3] Add `research evidence-check` CLI command in `src/synthsea/cli.py`
- [x] T035 [US3] Add fixture evidence manifest and source artifact under `tests/research/fixtures/feature-003-fixture/manifest.json` and `tests/research/fixtures/feature-003-fixture/result.json`

**Checkpoint**: Registered evidence is auditable, immutable, and visibly distinct from fixture-only evidence.

---

## Phase 6: User Story 4 - Generate and Validate the Final Research Report (Priority: P1)

**Goal**: Generate a complete report package from the dossier, matrix, approved venue, and verified evidence, then fail closed when release conditions are unmet.

**Independent Test**: Generate a fixture package and verify required sections, language slices, claim links, bibliography status, reproducibility appendix, excluded artifacts, and blocked release status.

### Tests for User Story 4

- [x] T036 [P] [US4] Add claim-evidence coverage and unsupported-claim tests in `tests/research/integration/test_claim_coverage.py`
- [x] T037 [P] [US4] Add report package generation tests in `tests/research/integration/test_report_package.py`
- [x] T038 [P] [US4] Add readiness blocker and release-status tests in `tests/research/integration/test_readiness.py`

### Implementation for User Story 4

- [x] T039 [US4] Implement claim-evidence matrix validation and primary-result gating in `src/synthsea/research/claims.py`
- [x] T040 [US4] Implement report section planning and missing-evidence markers using existing paper section APIs in `src/synthsea/research/report.py`
- [x] T041 [US4] Implement evidence-backed table, figure, bibliography, and reproducibility appendix metadata in `src/synthsea/research/report.py`
- [x] T042 [US4] Implement research package manifest and public artifact projection in `src/synthsea/research/package.py`
- [x] T043 [US4] Add `research report` and `research readiness` CLI commands in `src/synthsea/cli.py`
- [x] T044 [US4] Connect report readiness to existing venue compliance and optional document build status in `src/synthsea/research/readiness.py`
- [x] T045 [US4] Preserve failed, null, negative, restricted, stale, and fixture evidence in generated readiness output in `src/synthsea/research/package.py`

**Checkpoint**: The report package is complete when evidence is complete and visibly blocked otherwise.

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Documentation, compatibility, full validation, and regression protection.

- [x] T046 [P] Update `README.md` with Feature 003 research-to-report workflow and blocked-release semantics
- [x] T047 [P] Update `specs/003-deep-research-final-report/quickstart.md` with final command names and expected statuses
- [x] T048 [P] Add CLI help and invalid-input error tests in `tests/research/integration/test_cli.py`
- [x] T049 Run the complete test suite and address Feature 003 regressions in `tests/`
- [x] T050 Run Ruff and mypy on the updated source tree and resolve relevant diagnostics in `src/`
- [x] T051 Run the quickstart end-to-end and record the fixture package and readiness report under `reports/research-packages/`
- [x] T052 Review Feature 003 against the constitution and update `specs/003-deep-research-final-report/checklists/requirements.md`
- [x] T053 Record web-research queries, candidate academic sources, DOI/ACL/arXiv URLs, retrieval date, limitations, and approval status in `research/sources/web-research-2026-08-13.json`
- [x] T054 Record web-research findings, novelty-gap hypothesis, and unresolved RegiCON 2026 venue search in `research/dossiers/web-research-findings-2026-08-13.md`

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies.
- **Foundational (Phase 2)**: Depends on Setup and blocks all user stories.
- **User Stories (Phases 3-6)**: Depend on Foundational; US1 and US2 can proceed in parallel, US3 depends on the artifact expectations from US2, and US4 depends on outputs from US1-3.
- **Polish (Phase 7)**: Depends on all desired user stories.

### User Story Dependencies

- **US1 (P1)**: Starts after Foundational; produces the dossier and source records.
- **US2 (P1)**: Starts after Foundational; consumes dossier concepts but is independently testable with a fixture dossier.
- **US3 (P1)**: Starts after Foundational and uses US2 artifact requirements; can validate independently with fixture requirements.
- **US4 (P1)**: Depends on the dossier, requirements matrix, and evidence registry from US1-3.

### Parallel Opportunities

- T002-T004 can run in parallel.
- T006-T007, T010-T011 can run in parallel.
- US1 and US2 can be developed in parallel after Phase 2.
- T012-T013, T020-T021, T028-T029, and T036-T038 can run in parallel.
- T046-T048 can run in parallel after report behavior stabilizes.

## Implementation Strategy

### MVP First

1. Complete Setup and Foundational phases.
2. Complete US1 to create an auditable dossier and prove venue uncertainty is preserved.
3. Complete US2 to produce a claim and experiment readiness matrix.
4. Validate the MVP with fixture dossier and matrix artifacts.

### Incremental Delivery

1. Add US3 to register real or fixture evidence with checksums and reproducibility metadata.
2. Add US4 to generate and validate the final report package.
3. Finish documentation, full regression tests, lint, type checking, and quickstart validation.

## Notes

- `[P]` tasks touch different files and have no dependency on incomplete work.
- Every task includes an exact file path and must be marked `[X]` when complete.
- A fixture-only package must remain blocked and must never be described as a final paper.