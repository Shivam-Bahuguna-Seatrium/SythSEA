# Implementation Plan: Deep Research and Final Reproducible Report

**Branch**: `003-deep-research-final-report` | **Date**: 2026-08-13 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `/specs/003-deep-research-final-report/spec.md`

**Note**: This template is filled in by the `/speckit-plan` command; its definition describes the execution workflow.

## Summary

Add a local-first research-readiness layer that records verifiable literature and venue
sources, maps research questions and claims to executable evidence requirements, registers
immutable experiment artifacts, and drives the existing paper package generator from
verified evidence only. Official venue requirements remain unresolved until an
authoritative RegiCON source is supplied.

## Technical Context

<!--
  ACTION REQUIRED: Replace the content in this section with the technical details
  for the project. The structure here is presented in advisory capacity to guide
  the iteration process.
-->

**Language/Version**: Python 3.11+

**Primary Dependencies**: Existing Pydantic, Typer, JSON Schema, PyYAML, Jinja2, and paper package modules

**Storage**: Versioned JSON/YAML/Markdown files under `research/`, `experiments/`, and `reports/`; no new database

**Testing**: pytest contract and integration tests, Ruff, mypy, and CLI smoke tests

**Target Platform**: Linux and local CPU-first development environment

**Project Type**: Python research library and Typer CLI

**Performance Goals**: Validate a dossier and evidence manifest for at least 10,000 records without unnecessary full-file duplication

**Constraints**: No fabricated content; read-only source evidence; restricted artifacts excluded from public packages; missing venue information blocks release; fixtures are labeled separately from real evidence

**Scale/Scope**: One approved venue per package; four language slices; file-based research metadata; real model execution remains owned by Feature 001

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

Pass. The design preserves scientific validity through claim-to-evidence links and explicit
evidence states; reproducibility through immutable manifests, checksums, commands, seeds,
and environment metadata; responsible data stewardship through licenses, access classes,
privacy, consent, and cultural limitations; multilingual quality through separate slices;
evaluation rigor through baselines, ablations, metrics, sample sizes, uncertainty, human
evaluation, and error analysis; engineering quality through typed models, contracts, and
tests; and transparent reporting through retained negative, null, failed, restricted, and
missing states.

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
│   ├── research/
│   │   ├── models.py
│   │   ├── sources.py
│   │   ├── requirements.py
│   │   ├── evidence.py
│   │   ├── readiness.py
│   │   └── package.py
│   ├── paper/
│   └── cli.py

tests/
├── contract/
├── integration/
├── paper/
└── research/

research/
├── sources/
├── dossiers/
├── requirements/
└── matrices/

reports/
└── research-packages/
```

**Structure Decision**: Extend the existing single Python package with one `research`
domain module. Keep research inputs and generated dossiers in a versioned `research/`
tree, while final report packages remain under `reports/`. Reuse `synthsea.paper` models,
checksum verification, venue compliance, and package writing rather than creating a second
paper abstraction.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| None | N/A | The design uses the existing project and adds one cohesive research module. |
