---
description: "Implementation tasks for the React and FastAPI SynthSEA research workbench"
---

# Tasks: Local Research Workbench

**Input**: Design documents from `specs/004-research-workbench/`

**Prerequisites**: `plan.md`, `spec.md`, `research.md`, `data-model.md`, `contracts/`, and `quickstart.md`

**Tests**: Required because the feature controls data governance, local model use, training state, and publication-readiness evidence.

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Create the FastAPI and React application shells, development tooling, and local-first configuration.

- [X] T001 Add FastAPI and Uvicorn runtime dependencies plus API test dependencies in `pyproject.toml`
- [X] T002 Create the backend API package entry points in `src/synthsea/api/__init__.py` and `src/synthsea/api/app.py`
- [X] T003 [P] Create the workspace service package in `src/synthsea/workspace/__init__.py`
- [X] T004 Create the Vite React TypeScript project configuration in `frontend/package.json`, `frontend/vite.config.ts`, `frontend/tsconfig.json`, and `frontend/index.html`
- [X] T005 [P] Configure frontend linting, formatting, Vitest, React Testing Library, and Playwright in `frontend/eslint.config.js`, `frontend/vitest.config.ts`, and `frontend/playwright.config.ts`
- [X] T006 [P] Add local API, MLX-LM training, and Ollama chat settings to `configs/workbench.yaml` and document non-secret environment variables in `.env.example`
- [X] T007 [P] Add generated frontend output and Playwright artifacts to `.gitignore`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Establish typed API, error, access-control, job-state, and frontend query foundations that all user stories depend on.

- [X] T008 Implement shared FastAPI dependency providers for catalog, artifact roots, and local configuration in `src/synthsea/api/dependencies.py`
- [X] T009 [P] Implement typed API request and response schemas from `workbench-api.openapi.yaml` in `src/synthsea/api/schemas/workbench.py`
- [X] T010 [P] Implement uniform API problem responses and exception handlers in `src/synthsea/api/errors.py`
- [X] T011 Implement server-side access-class authorization and public projection checks in `src/synthsea/workspace/access.py`
- [X] T012 [P] Implement persistent workspace job state models and state-transition validation in `src/synthsea/workspace/models.py`
- [X] T013 Implement job persistence over the existing catalog and artifact roots in `src/synthsea/workspace/jobs.py`
- [X] T014 Register API routes, CORS policy for the local frontend origin, and health endpoint in `src/synthsea/api/app.py`
- [X] T015 [P] Add API schema and error contract tests in `tests/api/test_api_contracts.py`
- [X] T016 [P] Add workspace job-state and access-control tests in `tests/workspace/test_foundation.py`
- [X] T017 Create typed API client, route definitions, and query provider in `frontend/src/api/client.ts`, `frontend/src/api/routes.ts`, and `frontend/src/app/providers.tsx`
- [X] T018 [P] Create the application shell, navigation, status badge, tooltip, and error boundary components in `frontend/src/components/` and `frontend/src/app/App.tsx`
- [X] T019 [P] Define global design tokens, responsive layout rules, typography, and state colors in `frontend/src/styles/tokens.css` and `frontend/src/styles/global.css`

**Checkpoint**: The local API health endpoint, typed frontend shell, access checks, and persistent job-state foundation work before story implementation begins.

---

## Phase 3: User Story 1 - Review and Ingest Research Data (Priority: P1) 🎯 MVP

**Goal**: Enable governed data intake with complete validation feedback and lineage links.

**Independent Test**: Submit one eligible public fixture and one fixture missing a license; the API and UI must display the correct eligible or blocked state, preserve all issues, and prevent public release of restricted content.

### Tests for User Story 1

- [X] T020 [P] [US1] Add dataset intake API contract tests for eligible, blocked, restricted, and invalid requests in `tests/api/test_dataset_intakes.py`
- [X] T021 [P] [US1] Add dataset intake service tests for provenance, license, retention, access class, and profile approval in `tests/workspace/test_intake.py`
- [X] T022 [P] [US1] Add intake form and validation-state component tests in `frontend/src/features/intake/DatasetIntakePage.test.tsx`

### Implementation for User Story 1

- [X] T023 [US1] Implement DatasetIntake creation, validation, and issue projection over `DatasetIngestor` in `src/synthsea/workspace/intake.py`
- [X] T024 [US1] Implement `POST /api/datasets/intakes` in `src/synthsea/api/routes/intakes.py`
- [X] T025 [US1] Register dataset intake routing in `src/synthsea/api/app.py`
- [X] T026 [P] [US1] Implement the governed intake form and client validation in `frontend/src/features/intake/DatasetIntakeForm.tsx`
- [X] T027 [P] [US1] Implement intake result, issue list, access-class, and lineage-link components in `frontend/src/features/intake/IntakeResult.tsx`
- [X] T028 [US1] Implement the Data Intake route and page composition in `frontend/src/features/intake/DatasetIntakePage.tsx` and `frontend/src/app/routes.tsx`
- [X] T029 [US1] Add visual and keyboard-accessible validation states for intake controls in `frontend/src/features/intake/intake.css`

**Checkpoint**: A researcher can complete or correct a governed dataset intake without using the CLI.

---

## Phase 4: User Story 2 - Configure and Monitor Fine-Tuning Runs (Priority: P1)

**Goal**: Submit, inspect, compare, and cancel reproducible fine-tuning jobs without equating job completion with a research result.

**Independent Test**: Create a fixture job using an approved dataset and language slice, observe status transitions and artifacts, then verify a missing model or ineligible dataset returns a blocked job with a reason.

### Tests for User Story 2

- [X] T030 [P] [US2] Add fine-tuning job request, status, and cancellation API tests in `tests/api/test_training_jobs.py`
- [X] T031 [P] [US2] Add job eligibility, state transition, failure, and cancellation tests in `tests/workspace/test_jobs.py`
- [X] T032 [P] [US2] Add fine-tuning form, job-list, and job-detail component tests in `frontend/src/features/training/TrainingPage.test.tsx`

### Implementation for User Story 2

- [X] T033 [US2] Implement MLX-LM FineTuningJob validation for dataset eligibility, MLX-compatible model, model license, split, seed, adapter configuration, and Apple Silicon execution location in `src/synthsea/workspace/jobs.py`
- [X] T034 [US2] Implement MLX-LM command construction, background job submission, progress recording, log references, checkpoint artifacts, unified-memory metadata, and cancellation in `src/synthsea/workspace/mlx_training.py`
- [X] T035 [US2] Implement `POST /api/training/jobs`, `GET /api/training/jobs/{jobId}`, and `DELETE /api/training/jobs/{jobId}` in `src/synthsea/api/routes/training.py`
- [X] T036 [US2] Register training routes in `src/synthsea/api/app.py`
- [X] T037 [P] [US2] Implement MLX-LM configuration form with dataset, split, slices, model, license, adapter settings, seed, objective, and unified-memory guidance in `frontend/src/features/training/TrainingForm.tsx`
- [X] T038 [P] [US2] Implement stable MLX-LM jobs table, status timeline, training command, log panel, checkpoint links, resource metadata, and cancel icon action in `frontend/src/features/training/TrainingJobs.tsx`
- [X] T039 [US2] Implement the Fine-Tuning route, polling behavior, and blocked-job messaging in `frontend/src/features/training/TrainingPage.tsx`
- [X] T040 [US2] Add visual job-state and resource-limitation styles in `frontend/src/features/training/training.css`

**Checkpoint**: A researcher can distinguish queued, running, blocked, failed, cancelled, and completed fine-tuning work from validated evaluation evidence.

---

## Phase 5: User Story 3 - Chat with a Local Inference Model (Priority: P1)

**Goal**: Offer an attractive local chat experience backed by the existing Ollama adapter while retaining model availability and exploratory provenance metadata.

**Independent Test**: With a mocked available local model, create a conversation and send a message; verify the UI shows model tag and settings, the backend records metadata, and unavailable Ollama produces an actionable state.

### Tests for User Story 3

- [X] T041 [P] [US3] Add local-model availability, conversation, message, and unavailable-service API tests in `tests/api/test_chat.py`
- [X] T042 [P] [US3] Add exploratory-message, access-class, and promotion-guard service tests in `tests/workspace/test_chat.py`
- [X] T043 [P] [US3] Add chat model selector, transcript, unavailable-state, and promotion-guard component tests in `frontend/src/features/chat/ChatPage.test.tsx`

### Implementation for User Story 3

- [X] T044 [US3] Implement local Ollama availability checks and model projection in `src/synthsea/workspace/chat.py`
- [X] T045 [US3] Implement conversation and exploratory message persistence with model, seed, temperature, token, and access metadata in `src/synthsea/workspace/chat.py`
- [X] T046 [US3] Implement promotion request validation requiring explicit provenance and access decisions in `src/synthsea/workspace/chat.py`
- [X] T047 [US3] Implement chat model, conversation, and message endpoints in `src/synthsea/api/routes/chat.py`
- [X] T048 [US3] Register chat routes in `src/synthsea/api/app.py`
- [X] T049 [P] [US3] Implement local model selector and unavailable-service recovery panel in `frontend/src/features/chat/ModelSelector.tsx`
- [X] T050 [P] [US3] Implement transcript, composer, model metadata strip, and exploratory badge in `frontend/src/features/chat/ChatPanel.tsx`
- [X] T051 [P] [US3] Implement explicit candidate-promotion dialog with provenance and access-class controls in `frontend/src/features/chat/PromotionDialog.tsx`
- [X] T052 [US3] Implement the Local Chat route and responsive workstation layout in `frontend/src/features/chat/ChatPage.tsx` and `frontend/src/features/chat/chat.css`

**Checkpoint**: Local chat is useful for model inspection while visibly separated from experiments and publication evidence.

---

## Phase 6: User Story 4 - Trace Research Evidence Across the Workspace (Priority: P2)

**Goal**: Connect artifact lineage, language-specific comparisons, and readiness blockers across existing research and paper artifacts.

**Independent Test**: Open a fixture artifact with sources and dependents, then verify lineage, access state, language slices, readiness blockers, and exclusion reasons appear without exposing restricted content.

### Tests for User Story 4

- [X] T053 [P] [US4] Add lineage projection and restricted-artifact API tests in `tests/api/test_lineage.py`
- [X] T054 [P] [US4] Add readiness projection and language-slice ordering tests in `tests/api/test_readiness.py`
- [X] T055 [P] [US4] Add evidence dashboard, lineage detail, and blocked-readiness component tests in `frontend/src/features/evidence/EvidencePage.test.tsx`

### Implementation for User Story 4

- [X] T056 [US4] Implement artifact lineage projection from existing manifests, catalog entries, and provenance references in `src/synthsea/workspace/lineage.py`
- [X] T057 [US4] Implement readiness-item projection from Feature 003 reports and evidence states in `src/synthsea/workspace/readiness.py`
- [X] T058 [US4] Implement `GET /api/artifacts/{artifactId}/lineage` and `GET /api/readiness` in `src/synthsea/api/routes/evidence.py`
- [X] T059 [US4] Register evidence routes in `src/synthsea/api/app.py`
- [X] T060 [P] [US4] Implement readiness blocker list, evidence-state summary, and language-slice comparison table in `frontend/src/features/evidence/ReadinessPanel.tsx`
- [X] T061 [P] [US4] Implement artifact lineage graph/detail and access-restriction presentation in `frontend/src/features/evidence/LineageDetail.tsx`
- [X] T062 [US4] Implement the Evidence route with separate language slices before aggregation in `frontend/src/features/evidence/EvidencePage.tsx`
- [X] T063 [US4] Add readable evidence, readiness, and lineage styles in `frontend/src/features/evidence/evidence.css`

**Checkpoint**: A researcher can trace a visible workspace item to its source artifacts and see exactly why it is or is not eligible for reporting.

---

## Phase 7: Polish and Cross-Cutting Concerns

**Purpose**: Complete dashboard entry behavior, accessibility, documentation, end-to-end coverage, and production-quality local operation.

- [X] T064 [P] Implement the operational overview page with active jobs, local model status, intake summary, and readiness blockers in `frontend/src/features/overview/OverviewPage.tsx`
- [X] T065 [P] Add empty, loading, error, keyboard-navigation, focus, and responsive mobile states across `frontend/src/components/` and `frontend/src/styles/global.css`
- [X] T066 [P] Add API OpenAPI route coverage and local CORS integration tests in `tests/api/test_app.py`
- [X] T067 [P] Add browser end-to-end coverage for intake, fixture training, local chat unavailable state, and readiness blockers in `frontend/tests/e2e/workbench.spec.ts`
- [X] T068 [P] Add React client build, lint, unit-test, and Playwright commands to `frontend/package.json`
- [X] T069 Update workspace setup and Apple Silicon MLX-LM fine-tuning plus Ollama chat workflow documentation in `README.md`, `docs/macos-ollama.md`, and `docs/research-report.md`
- [X] T070 Update `.gitignore` with frontend dependency, build, test, and local workspace artifact patterns
- [X] T071 Run backend tests, frontend tests, lint, type checks, browser tests, and `quickstart.md` end-to-end validation; record outcomes in `specs/004-research-workbench/quickstart.md`
- [X] T072 Review Feature 004 against the constitution and update `specs/004-research-workbench/checklists/requirements.md`

---

## Dependencies and Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: Starts immediately.
- **Foundational (Phase 2)**: Depends on setup and blocks all user stories.
- **US1 (Phase 3)**: Depends on the foundational API and frontend shell; this is the recommended MVP.
- **US2 (Phase 4)**: Depends on foundational job persistence and the dataset eligibility projection from US1.
- **US3 (Phase 5)**: Depends on the foundational API and existing Ollama adapter; it can run in parallel with US2 after Phase 2.
- **US4 (Phase 6)**: Depends on foundational artifact access controls and may consume completed interfaces from US1-US3.
- **Polish (Phase 7)**: Depends on the desired user stories.

### User Story Dependencies

- **US1 (P1)**: Independent after Phase 2 and delivers governed dataset intake.
- **US2 (P1)**: Uses US1 eligibility semantics but can be verified with fixture datasets.
- **US3 (P1)**: Independent after Phase 2; uses the existing local Ollama adapter.
- **US4 (P2)**: Integrates the shared lineage and readiness contracts from all stories.

### Parallel Opportunities

- T003, T005-T007 can run in parallel after T001-T002.
- T009-T012 and T015-T019 can run in parallel after API package setup.
- T020-T022, T030-T032, T041-T043, and T053-T055 can run in parallel within their user stories.
- Frontend components marked `[P]` work in separate feature files after their API contracts stabilize.
- US2 and US3 can be developed in parallel after Phase 2.

## Parallel Execution Examples

### User Story 1

```text
T020 Dataset intake API tests
T021 Dataset intake service tests
T022 Intake form component tests
```

### User Story 3

```text
T041 Chat API tests
T042 Chat service tests
T043 Chat component tests
```

### User Story 4

```text
T053 Lineage API tests
T054 Readiness API tests
T055 Evidence UI tests
```

## Implementation Strategy

### MVP First

1. Complete Setup and Foundational phases.
2. Complete US1 for controlled dataset intake.
3. Validate API and React intake workflows with eligible and blocked fixtures.
4. Demonstrate the operational workspace before adding training and chat.

### Incremental Delivery

1. Add US2 to submit and monitor fixture fine-tuning jobs.
2. Add US3 to connect local Ollama chat with explicit exploratory metadata.
3. Add US4 to unify provenance and readiness.
4. Complete browser validation, accessibility, documentation, and constitution review.

## Notes

- All tasks follow the required checkbox, task-ID, story-label, and file-path format.
- UI work must preserve a dense operational research-workbench experience, not a marketing landing page.
- No task may permit chat output, job completion, or fixture data to become a publication claim without registered evidence.