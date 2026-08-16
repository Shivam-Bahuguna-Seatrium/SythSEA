# Implementation Plan: Multilingual Synthetic Instruction Research Pipeline

**Branch**: `001-multilingual-instruction-pipeline` | **Date**: 2026-08-13 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `specs/001-multilingual-instruction-pipeline/spec.md`

## Summary

Build a reproducible, local-first NLP research pipeline for creating and evaluating synthetic instruction data across four validated language profiles: Singapore English/Singlish, Malay, Tamil, and Singapore-context Mandarin. The pipeline will use explicit stage interfaces for language profiling, acquisition, generation, validation, review, deduplication, experiment execution, analysis, and publication export. Parquet artifacts plus a DuckDB experiment catalog keep datasets inspectable and portable, while model adapters allow local or remote teachers without changing experiment contracts.

## Technical Context

**Language/Version**: Python 3.11+

**Primary Dependencies**: MLX and MLX-LM for Apple Silicon fine-tuning, Pydantic v2, Typer, PyYAML, PyArrow, DuckDB, SciPy, statsmodels, SacreBLEU, pytest, Ruff, and mypy. PyTorch, Hugging Face Transformers/Datasets, PEFT, Accelerate, vLLM, and MLflow-compatible tracking remain optional adapters for non-Apple-Silicon or larger-scale runs.

**Storage**: Versioned Parquet files for datasets and evaluation tables; a DuckDB catalog for metadata, run state, provenance, and analytical queries; JSON/YAML manifests and configuration files; restricted artifacts stored in a separate access-controlled root from public exports.

**Testing**: pytest unit and integration tests, JSON Schema contract tests, golden fixtures for metadata and reports, Ruff linting, mypy type checking, and small deterministic end-to-end smoke runs.

**Target Platform**: Linux and macOS on Apple Silicon. Metadata and filtering are CPU-compatible; Apple Silicon fine-tuning uses MLX-LM and local interactive generation uses Ollama through a local HTTP adapter. CUDA remains optional for larger non-Apple-Silicon runs. The first release is a command-line research workflow.

**Project Type**: Research pipeline library and CLI with offline artifact processing plus adapters for local models, remote teacher APIs, and optional experiment tracking services.

**Performance Goals**: On a declared 4-vCPU, 8-GB-RAM CPU runner, metadata validation, filtering, and export MUST process a 10,000-record fixture in under 60 seconds, excluding filesystem setup. Generation MUST support batching, bounded concurrency, caching, retry/backoff, and resumable runs. A complete pilot report SHOULD be reproducible from one documented command sequence.

**Constraints**: No source dataset may be used without licensing, provenance, privacy, access-classification, and retention metadata. `public` means approved for external release, `restricted` means approved for project research but excluded from public exports, and `private` means researcher-only material. Restricted and private records MUST not cross into public exports. All primary runs MUST record prompts, model versions, seeds, configurations, failures, exclusions, and artifact checksums. The project MUST NOT assume equal resource availability across language profiles.

**Scale/Scope**: Initial experiments target 1K, 5K, 10K, 25K, and 50K synthetic examples as data-efficiency conditions, with separate slices for four language profiles, monolingual controls, and predefined English-mixing conditions.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **Scientific validity**: PASS. Experiment configurations, baselines, ablations, evaluation outputs, and statistical analyses are first-class artifacts with explicit condition identifiers.
- **Reproducibility**: PASS. Versioned configs, seeds, prompts, model adapters, dataset manifests, checksums, and runnable quickstart scenarios are required.
- **Responsible data stewardship**: PASS. Access classification, licensing, provenance, retention, privacy flags, and public/private export separation are enforced in the data model and contracts.
- **Multilingual and cultural quality**: PASS. Four validated language profiles are separate entities and all reports preserve language-specific slices.
- **Evaluation rigor**: PASS. Tier A human data, Tier B single-agent data, optional translation baseline, Tier C SynthSEA data, ablations, human review, automated metrics, and statistical analysis are represented.
- **Engineering quality**: PASS. The design uses typed stage interfaces, deterministic fixtures, contract tests, resumable execution, and focused integration checks.
- **Transparent reporting**: PASS. Reports include exclusions, failures, limitations, contamination checks, compute and model constraints, and provenance manifests.

## Phase 0 Research Decisions

Research decisions are recorded in [research.md](research.md). The main choices are Python with explicit pipeline stages rather than a heavy multi-agent framework, Parquet plus DuckDB rather than a hosted database, adapter-based model access, and a local-first experiment catalog with optional remote tracking.

## Project Structure

### Documentation (this feature)

```text
specs/001-multilingual-instruction-pipeline/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
│   ├── artifact-manifest.schema.json
│   └── experiment-config.schema.json
└── tasks.md                 # Created by /speckit-tasks
```

### Source Code (repository root)

```text
pyproject.toml
src/synthsea/
├── cli.py
├── config/
│   ├── loader.py
│   └── schemas.py
├── data/
│   ├── ingest.py
│   ├── provenance.py
│   ├── manifests.py
│   └── storage.py
├── profiles/
│   ├── models.py
│   └── validation.py
├── agents/
│   ├── base.py
│   ├── language_profile.py
│   ├── resource_discovery.py
│   ├── topic_context.py
│   ├── instruction_generation.py
│   ├── language_specialist.py
│   ├── code_switching.py
│   ├── cultural_validation.py
│   ├── semantic_validation.py
│   ├── diversity_difficulty.py
│   ├── critic.py
│   ├── judge.py
│   └── refinement.py
├── generation/
│   ├── runner.py
│   ├── adapters.py
│   ├── batching.py
│   ├── cache.py
│   └── retry.py
├── filtering/
│   ├── quality.py
│   ├── safety.py
│   └── deduplication.py
├── review/
│   ├── annotation.py
│   └── adjudication.py
├── experiments/
│   ├── registry.py
│   ├── baselines.py
│   ├── ablations.py
│   └── runner.py
├── evaluation/
│   ├── automatic.py
│   ├── human.py
│   ├── statistics.py
│   ├── leakage.py
│   └── errors.py
├── training/
│   ├── adapters.py
│   ├── datasets.py
│   └── downstream.py
├── export/
│   ├── datasets.py
│   ├── reports.py
│   └── public_private.py
└── tracking/
    ├── catalog.py
    ├── events.py
    └── costs.py

tests/
├── unit/
├── integration/
├── contract/
├── fixtures/
└── smoke/
configs/
├── languages.yaml
├── generation.yaml
├── evaluation.yaml
└── models.yaml
data/
├── raw/
├── processed/
├── synthetic/
├── evaluation/
├── restricted/
└── public/
experiments/
reports/
```

**Structure Decision**: Use one Python package with explicit domain modules and one CLI. Stage interfaces remain independently testable and can run locally or through adapters. Data and reports are artifacts, not application database records, so researchers can inspect, checksum, archive, and publish them without recreating a service environment.

## Phase 1 Design Notes

- The canonical entities, relationships, lifecycle states, and validation rules are defined in [data-model.md](data-model.md).
- The artifact and experiment configuration contracts are defined under [contracts](contracts/).
- Runnable validation scenarios and expected outputs are defined in [quickstart.md](quickstart.md).
- Downstream adaptation and evaluation are explicit in `src/synthsea/training/` and MUST be evaluated separately from direct synthetic-data quality.
- No public web API is required for the first release. The CLI and versioned artifact schemas are the external contracts.
- Apple Silicon pilots use MLX-LM for fine-tuning and the local Ollama adapter for chat or generation. Both record concrete model identifiers, configuration, seed, local environment, and output artifacts without credentials.

## Post-Design Constitution Check

- All seven gates remain PASS after design.
- The only deliberate complexity is the multi-stage agent pipeline; each stage has an explicit contract and can be disabled for baseline or ablation runs.
- No hosted service is required to reproduce the pilot, reducing operational and access risk while preserving adapters for larger experiments.

## Complexity Tracking

| Decision | Why Needed | Simpler Alternative Rejected Because |
|---|---|---|
| Explicit stage graph with 10+ roles | The research question tests whether coordinated validation improves data quality | A single prompt would not support role ablations or stage-level auditability |
| DuckDB catalog plus Parquet artifacts | Researchers need both structured run metadata and portable large tables | JSON-only storage is difficult to query and SQLite-only storage is less convenient for large dataset interchange |
| Local and remote model adapters | Reproducibility requires open/local options while experiments may compare teacher families | Hard-coding one provider would reduce replication and introduce access dependence |
