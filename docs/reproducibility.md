# SynthSEA Reproducibility

Every experiment records its configuration, dataset versions, language profiles,
prompts, model versions, seeds, software environment, failures, exclusions,
checksums, and output manifest. Use the deterministic CPU fixture before any
GPU or remote-model run.

```bash
source .venv/bin/activate
pytest tests/unit tests/contract tests/integration tests/smoke
ruff check .
mypy src
```

Restricted artifacts remain outside public exports. Changes to research records
are append-only versions rather than in-place edits.
