# SynthSEA

SynthSEA is a reproducible research pipeline for multilingual synthetic
instruction generation and evaluation across Singapore English/Singlish, Malay,
Tamil, and Singapore-context Mandarin.

## CPU-first validation

```bash
uv pip install --python .venv/bin/python -e ".[dev]"
.venv/bin/pytest tests/unit tests/contract tests/integration tests/smoke
```

The deterministic fixture path does not require a GPU, paid model API, or
committed secrets. See [docs/reproducibility.md](docs/reproducibility.md) and
the [plan quickstart](specs/001-multilingual-instruction-pipeline/quickstart.md).

See the [SynthSEA architecture diagram](docs/architecture.md) for the complete
generation, evaluation, evidence, and report flow.

For a local Apple Silicon MacBook pilot with Ollama, see
[docs/macos-ollama.md](docs/macos-ollama.md).

The local workbench uses **MLX-LM** for Apple Silicon fine-tuning and uses
**Ollama** only for local chat and generation. Feature 004 adds a React client
and FastAPI service around those existing governed artifacts.

See [docs/workbench.md](docs/workbench.md) for local startup and operational
boundaries.

## Research-to-report workflow

Feature 003 creates an evidence-grounded research dossier and final report
package. It does not invent results or venue requirements.

```bash
.venv/bin/python -m synthsea.cli research dossier
.venv/bin/python -m synthsea.cli research matrix \
	--dossier research/dossiers/synthsea-regicon-2026.json
.venv/bin/python -m synthsea.cli research report \
	--dossier research/dossiers/synthsea-regicon-2026.json \
	--matrix research/matrices/synthsea-readiness.json
```

The generated readiness report remains `blocked` until official venue
requirements, verified experiment evidence, citations, and ethics review are
recorded. See [docs/research-report.md](docs/research-report.md).
