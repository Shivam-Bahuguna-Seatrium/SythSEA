# Springer Paper Package

The paper package consumes verified SynthSEA evidence and writes outputs under
`reports/paper-packages/`. It does not modify source datasets, experiment
results, or original manifests.

## CPU-first commands

```bash
source .venv/bin/activate
synthsea paper venue-profile configs/paper/venue.yaml
synthsea paper evidence-check tests/paper/fixtures/evidence/manifest.json
synthsea paper generate
synthsea paper validate
synthsea paper build
```

`paper build` reports `unavailable` when PDF tools are missing. That is an honest
status, not a successful submission build.

Before a real submission, replace fixture venue and evidence inputs with the
official conference author guide and verified experiment manifests. Review
claims, references, author details, ethics, and access decisions manually.
