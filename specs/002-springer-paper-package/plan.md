# Implementation Plan: Springer Conference Paper Generation and Reproducible Research Package

**Branch**: `002-springer-paper-package` | **Date**: 2026-08-13 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `specs/002-springer-paper-package/spec.md`

## Summary

Add a read-only publication layer to SynthSEA. It will ingest a verified
experiment manifest, register official venue requirements, validate claims and
citations, generate an evidence-linked manuscript package, and optionally build
PDF output. The layer will never mutate source datasets, experiment results, or
original manifests. Missing evidence remains visible as a blocking or missing
status rather than becoming invented prose or numbers.

## Technical Context

**Language/Version**: Python 3.11+, reusing the existing SynthSEA package.

**Primary Dependencies**: Existing Pydantic, PyYAML, PyArrow, DuckDB,
jsonschema, Typer, pytest, Ruff, and mypy dependencies; Jinja2 for deterministic
text/template rendering; optional BibTeX parsing and LaTeX build adapters.

**Storage**: Versioned JSON/YAML venue profiles and paper configurations;
read-only Parquet/JSON/DuckDB evidence inputs; generated manuscript source,
`.bib`, tables, figures, appendix, manifests, compliance reports, and optional
PDF under a separate `reports/paper-packages/<package_id>/` output root.

**Testing**: pytest unit, contract, integration, golden-output, and smoke tests;
JSON Schema contract validation; Ruff; mypy; byte-for-byte source immutability
checks; fixture tests for unsupported claims, missing citations, restricted data,
and unavailable build tools.

**Target Platform**: Linux research workstation or CI runner. PDF compilation is
optional and only runs when the selected venue template and required document
utilities are available.

**Project Type**: Read-only research publication package generator and CLI layer.

**Performance Goals**: Venue, evidence, claim, and citation validation MUST
process a 10,000-item fixture package in under 60 seconds on the declared
4-vCPU, 8-GB-RAM CPU runner, excluding optional PDF compilation. Manuscript
rendering MUST be deterministic for fixed inputs, templates, and configuration.

**Constraints**: Official venue evidence is required before final compliance
status can pass. Public packages MUST exclude restricted and private artifacts.
Every claim, number, table, and figure MUST resolve to evidence or an explicit
source citation. PDF generation MUST report unavailable tools instead of a false
success. Generated outputs MUST be separate from source evidence.

**Scale/Scope**: One conference package per run, four language result slices,
Tier A/B/C/D comparisons when available, one selected venue profile, and
publication artifacts sized for a conference manuscript rather than a journal
production system.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **Scientific validity**: PASS. Claims and numerical values require evidence
  references and missing evidence is blocking or explicitly marked.
- **Reproducibility**: PASS. Paper packages retain evidence manifests, configs,
  source checksums, prompts, models, seeds, commands, and environment metadata.
- **Responsible data stewardship**: PASS. Public, restricted, and private access
  classes are enforced without mutating source artifacts.
- **Multilingual and cultural quality**: PASS. Paper results require separate
  slices for all four target language settings before aggregate reporting.
- **Evaluation rigor**: PASS. Baselines, translation comparisons, ablations,
  automated metrics, human evaluation, uncertainty, and error analysis are
  represented when available in verified evidence.
- **Engineering quality**: PASS. The design uses typed entities, JSON Schemas,
  deterministic templates, tests, and a read-only source boundary.
- **Transparent reporting**: PASS. Limitations, ethics, licensing, access,
  missing evidence, build warnings, and threat-to-validity findings are retained.

## Phase 0 Research Decisions

Research decisions are recorded in [research.md](research.md). The key choices
are a venue-profile-first workflow, manifest-based evidence ingestion, explicit
claim status, template-driven manuscript rendering, optional document builds,
and separate public/restricted/private outputs.

## Project Structure

### Documentation (this feature)

```text
specs/002-springer-paper-package/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
└── contracts/
    ├── venue-profile.schema.json
    ├── evidence-manifest.schema.json
    └── paper-package.schema.json
```

### Source Code (repository root)

```text
src/synthsea/paper/
├── __init__.py
├── venue.py
├── evidence.py
├── claims.py
├── sections.py
├── citations.py
├── tables.py
├── figures.py
├── reproducibility.py
├── compliance.py
├── renderer.py
├── builder.py
└── package.py

tests/paper/
├── unit/
├── contract/
├── integration/
├── fixtures/
└── smoke/

reports/paper-packages/
└── <package_id>/
    ├── manuscript.tex
    ├── references.bib
    ├── tables/
    ├── figures/
    ├── reproducibility/
    ├── compliance.json
    ├── manifest.json
    ├── README.md
    └── manuscript.pdf      # optional
```

**Structure Decision**: Use a separate `synthsea.paper` package and output root.
Existing experiment modules remain the source of truth. The publication layer
reads manifests and artifacts through immutable interfaces and writes only a
new paper package.

## Phase 1 Design Notes

- Entities and lifecycle rules are defined in [data-model.md](data-model.md).
- Venue, evidence, and package interfaces are defined under [contracts](contracts/).
- Fixture execution and expected blocking behavior are defined in [quickstart.md](quickstart.md).
- The selected venue template is an input decision; the package must not assume
  Springer LNCS when official venue evidence says otherwise.

## Post-Design Constitution Check

- All seven gates remain PASS after design.
- The paper layer does not weaken evidence, access, reproducibility, multilingual,
  or ethics requirements to satisfy formatting.
- Optional PDF compilation is isolated from source generation and cannot convert
  an unavailable build tool into a passing compliance result.

## Complexity Tracking

| Decision | Why Needed | Simpler Alternative Rejected Because |
|---|---|---|
| Venue profile and template resolver | Springer family and conference rules cannot be safely inferred | Hard-coding LNCS would risk non-compliant submissions |
| Claim-to-evidence graph | Every numerical claim and visual artifact needs scientific traceability | Prose-only generation would permit unsupported results |
| Separate paper package output root | Source datasets and results must remain immutable | In-place edits would damage reproducibility and release safety |
