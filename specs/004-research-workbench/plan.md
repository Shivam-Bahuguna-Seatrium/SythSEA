# Implementation Plan: Local Research Workbench

**Branch**: `004-research-workbench` | **Date**: 2026-08-14 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `/specs/004-research-workbench/spec.md`

**Note**: This template is filled in by the `/speckit-plan` command; its definition describes the execution workflow.

## Summary

Create a local-first research workspace with a React frontend and FastAPI backend.
The frontend provides dense researcher-facing views for governed dataset intake,
MLX-LM fine-tuning configuration and monitoring, local Ollama chat, provenance, and
readiness. The backend wraps existing SynthSEA modules and artifact contracts;
it does not create a parallel data or evidence model. Long-running fine-tuning
is submitted as a persistent job and polled through a status endpoint. Chat is
local-only and exploratory until an explicit provenance decision registers it.

## Technical Context

<!--
  ACTION REQUIRED: Replace the content in this section with the technical details
  for the project. The structure here is presented in advisory capacity to guide
  the iteration process.
-->

**Language/Version**: Python 3.11+; TypeScript 5+ and React 19+

**Primary Dependencies**: Existing Pydantic, DuckDB, PyArrow, Typer, MLX-LM training adapter, and Ollama chat adapter; FastAPI, Uvicorn, React, Vite, React Router, and Lucide icons

**Storage**: Existing DuckDB catalog plus versioned JSON/Parquet artifacts; local browser state only for non-sensitive workspace preferences

**Testing**: pytest API and service tests; Vitest and React Testing Library component tests; Playwright end-to-end tests; Ruff, mypy, ESLint, and TypeScript checks

**Target Platform**: Local Linux and Apple Silicon macOS research workstations, with MLX-LM fine-tuning on Apple Silicon and local Ollama inference for chat

**Project Type**: Local web application with a React client and FastAPI backend over the existing research pipeline

**Performance Goals**: Interactive local views load their first page of metadata within 2 seconds for 10,000 records; UI actions acknowledge submitted ingestion, chat, and training requests within 1 second; no operation blocks the browser while a job runs

**Constraints**: Local-first; no credentials stored in the browser; public/restricted/private boundaries enforced by the backend; chat is exploratory and cannot become evidence without explicit registration; all four language slices remain visible before aggregates; unavailable local models or hardware produce actionable status rather than fallback behavior

**Scale/Scope**: One authorized research team on one local workspace; five primary views: overview, dataset intake, fine-tuning, chat, and evidence/readiness; deployment, multi-tenant identity, and billing are out of scope

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

Pass. The workspace makes evidence status explicit and does not convert chat or
training completion into scientific claims. It reuses versioned datasets,
configs, prompts, models, seeds, and manifests from the existing pipeline. It
enforces access classes server-side, preserves separate language slices, exposes
baselines and ablations, and displays ethics, citation, venue, and evidence
blockers. All mutation endpoints create auditable records rather than modifying
source artifacts in place.

## Project Structure

### Documentation (this feature)

```text
specs/[###-feature]/
├── plan.md              # This file (/speckit-plan command output)
├── research.md          # Phase 0 output (/speckit-plan command)
├── data-model.md        # Phase 1 output (/speckit-plan command)
├── quickstart.md        # Phase 1 output (/speckit-plan command)
├── contracts/           # Phase 1 output (/speckit-plan command)
└── tasks.md             # Phase 2 output (/speckit-tasks command - NOT created by /speckit-plan)
```

### Source Code (repository root)
<!--
  ACTION REQUIRED: Replace the placeholder tree below with the concrete layout
  for this feature. Delete unused options and expand the chosen structure with
  real paths (e.g., apps/admin, packages/something). The delivered plan must
  not include Option labels.
-->

```text
src/
├── synthsea/
│   ├── api/
│   │   ├── app.py
│   │   ├── dependencies.py
│   │   ├── routes/
│   │   └── schemas/
│   ├── workspace/
│   │   ├── intake.py
│   │   ├── jobs.py
│   │   ├── chat.py
│   │   ├── mlx_training.py
│   │   └── lineage.py
│   ├── data/
│   ├── generation/
│   ├── research/
│   └── training/

tests/
├── contract/
├── integration/
├── api/
├── workspace/
└── unit/

frontend/
├── src/
│   ├── components/
│   ├── features/
│   ├── pages/
│   ├── api/
│   └── styles/
├── tests/
└── package.json
```

**Structure Decision**: Keep the established Python package as the source of
truth and add `synthsea.api` and `synthsea.workspace` as a narrow HTTP and
orchestration layer. Add a standalone Vite React client under `frontend/` so
the UI can evolve independently while consuming typed backend contracts. The
FastAPI service submits and monitors MLX-LM jobs; it does not run training in a
request handler. Do not duplicate dataset, experiment, evidence, or
access-control rules in TypeScript.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| React client plus FastAPI service | A browser workspace requires a responsive UI and controlled backend access to local artifacts, jobs, and Ollama | Extending the CLI alone would not provide the requested visual workflows or prevent browser clients from bypassing governance rules |
