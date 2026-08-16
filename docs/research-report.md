# Research-to-Report Workflow

Feature 003 turns SynthSEA research requirements into an auditable report package.
It records literature and official venue sources, maps claims to experiments,
checks evidence integrity, and generates report source from verified artifacts.

The local workbench keeps MLX-LM fine-tuning jobs separate from Ollama chat
sessions. Neither a completed job nor exploratory chat output becomes report
evidence until the existing experiment, evaluation, and claim checks are met.

## Workflow

```bash
.venv/bin/python -m synthsea.cli research dossier \
  --sources research/sources \
  --output research/dossiers/synthsea-regicon-2026.json

.venv/bin/python -m synthsea.cli research matrix \
  --dossier research/dossiers/synthsea-regicon-2026.json \
  --output research/matrices/synthsea-readiness.json

.venv/bin/python -m synthsea.cli research evidence-check \
  --manifest tests/research/fixtures/feature-003-fixture/manifest.json \
  --source-root tests/research/fixtures/feature-003-fixture

.venv/bin/python -m synthsea.cli research report \
  --dossier research/dossiers/synthsea-regicon-2026.json \
  --matrix research/matrices/synthsea-readiness.json \
  --output reports/research-packages
```

## Evidence policy

Only evidence with valid checksums, provenance, access decisions, and complete
reproducibility metadata can support a primary result. CPU fixtures are retained
for tests but remain visibly labeled `fixture`. Missing, restricted, stale,
failed, null, and negative evidence is preserved in readiness output.

## Venue policy

RegiCON 2026 requirements must be entered as a verified official source record.
The workflow does not infer a Springer template, page limit, citation style, or
submission rule from the conference name alone.

## Release policy

The report package is blocked until the venue is approved, evidence is verified,
claims and citations resolve, reproducibility metadata is complete, and ethics
review is recorded. Missing PDF tooling affects build availability but cannot be
reported as a successful PDF build.