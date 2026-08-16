# SynthSEA Plan Validation Quickstart

This guide defines the first runnable validation slice. It proves metadata
integrity, language-profile validation, controlled generation, filtering,
experiment recording, and report export before large-scale generation.

## Prerequisites

- Python 3.11 or newer
- `uv`
- A checked-out SynthSEA repository
- One legally usable small seed fixture per language profile, or synthetic test
  fixtures clearly marked as test-only
- No secrets committed to the repository

## Setup

```bash
uv venv
source .venv/bin/activate
uv pip install -e ".[dev]"
```

The implementation MUST provide a deterministic test mode that does not call a
remote model or require a GPU.

## Apple Silicon local-model pilot

On a MacBook, use MLX-LM for fine-tuning after the deterministic workflow
passes. Keep Ollama for interactive local generation and chat.

```bash
python -m pip install mlx-lm
mlx_lm.lora --help
```

Run only a documented, MLX-compatible model and record the MLX-LM version,
base-model or adapter identifier, dataset and split version, seed, macOS version,
and available unified memory. Start Ollama separately only when testing local
chat or generation. See [the Apple Silicon guide](../../docs/macos-ollama.md).

## Validation sequence

1. Validate the four language profiles and reject an unvalidated profile.
2. Register public and restricted source fixtures with provenance, license,
   access class, retention rule, and content checksum.
3. Run a small Tier B single-agent baseline and a Tier C multi-stage run using
   the same seed and split manifest.
4. Run one monolingual condition and one predefined English-mixing condition.
5. Insert deliberate malformed records, exact duplicates, near-duplicates, and
   unsafe-review fixtures; verify each receives a reasoned status.
6. Run a human-review fixture with two ratings and one disagreement; verify the
   adjudication record preserves both original ratings.
7. Run automated metrics, a statistical comparison, leakage checks, and error
   categorization for each available language profile.
8. Run a CPU-compatible downstream adaptation fixture using Tier B and Tier C
   records; verify the adaptation configuration, model version, checkpoint
   reference, and language-specific result rows are separate from
   generation-quality metrics.
9. Export a restricted package and a public package; verify restricted records
   and artifacts are absent from the public manifest.

## Expected checks

```bash
pytest tests/contract tests/integration tests/smoke
ruff check .
mypy src
```

The CPU benchmark MUST validate 10,000 metadata, filtering, and export records
in under 60 seconds on the declared 4-vCPU, 8-GB-RAM runner.

The smoke run MUST emit an experiment identifier, configuration checksum,
language-specific result rows, rejected-record reasons, and a valid artifact
manifest matching [artifact-manifest.schema.json](contracts/artifact-manifest.schema.json).

The experiment configuration MUST validate against
[experiment-config.schema.json](contracts/experiment-config.schema.json).

## Primary research validation

After the deterministic smoke run passes, repeat the same workflow with one
small open model adapter and one approved teacher adapter. Record model and
prompt versions, token/cost usage, retries, failures, seeds, and output hashes.
Do not increase to 1K, 5K, 10K, 25K, or 50K conditions until the pilot report
contains separate language slices and passes the public/restricted export check.