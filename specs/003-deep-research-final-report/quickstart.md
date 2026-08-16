# Feature 003 Quickstart

This guide validates the research-to-report workflow with CPU-safe fixtures. Fixture
outputs are not publication evidence.

## Prerequisites

```bash
cd /home/azureuser/shivam-dev/SynthSEA
.venv/bin/python --version
.venv/bin/pytest --version
```

## Validate the specification and plan

```bash
.venv/bin/python .specify/scripts/python/check_prerequisites.py --json
```

The command must resolve Feature 003 and report its `spec.md`, `plan.md`, and later
`tasks.md` paths.

## Create a research dossier

```bash
.venv/bin/python -m synthsea.cli research dossier \
  --sources research/sources \
  --output research/dossiers/synthsea-regicon-2026.json
```

The output must preserve source verification status and leave the venue unresolved until
an official CFP or author guide is registered.

## Build the requirements and evidence matrix

```bash
.venv/bin/python -m synthsea.cli research matrix \
  --dossier research/dossiers/synthsea-regicon-2026.json \
  --output research/matrices/synthsea-readiness.json
```

The matrix must include separate language slices, research questions, hypotheses, required
experiments, commands, metrics, artifact expectations, and missing-evidence statuses.

## Register and validate evidence

```bash
.venv/bin/python -m synthsea.cli research evidence-check \
  --manifest experiments/manifests/feature-003-fixture.json
```

The command must verify checksums, provenance, access classes, and fixture status without
modifying source artifacts.

## Generate and validate the report package

```bash
.venv/bin/python -m synthsea.cli research report \
  --dossier research/dossiers/synthsea-regicon-2026.json \
  --matrix research/matrices/synthsea-readiness.json \
  --output reports/research-packages

.venv/bin/python -m synthsea.cli research readiness \
  --package reports/research-packages/synthsea-regicon-2026 \
  --output reports/research-packages/readiness.json
```

The package must contain the dossier, literature matrix, novelty analysis, requirements
matrix, claim-evidence matrix, report source, references, reproducibility appendix, and
readiness report. It must be blocked while official venue approval or real evidence is
missing.

## Focused validation

```bash
.venv/bin/pytest tests/research tests/paper
.venv/bin/ruff check src tests
.venv/bin/mypy src
```

The final release check must distinguish `fixture` from `verified` evidence and must never
report a ready package from fixture-only inputs.