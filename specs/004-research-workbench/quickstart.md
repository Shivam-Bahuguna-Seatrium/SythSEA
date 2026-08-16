# Feature 004 Quickstart

This guide validates the local research workbench using CPU-safe fixtures. It
does not establish publication evidence.

## Prerequisites

- Python 3.11+
- Node.js 22+
- A local SynthSEA checkout with the existing virtual environment
- MLX-LM on Apple Silicon for fine-tuning jobs
- Optional local Ollama for interactive chat and model availability checks

## Backend setup

```bash
source .venv/bin/activate
python -m pip install -e ".[dev]" mlx-lm
uvicorn synthsea.api.app:app --reload --port 8000
```

The API should expose an interactive OpenAPI document at `http://127.0.0.1:8000/docs`.

## Frontend setup

```bash
cd frontend
npm install
npm run dev
```

Open the local Vite URL shown by the command. The first view must be the
operational workbench, not a landing page.

## Fixture validation

1. Submit a complete fixture dataset intake and confirm an eligible or restricted state.
2. Submit a fixture missing a license and confirm a blocked state with a reason.
3. Create an MLX-LM fixture fine-tuning job and verify it shows its model,
   model-license record, MLX-LM version, dataset version, split, seed, language
   slice, command, checkpoint, unified-memory record, and status.
4. With Ollama running, open Local Chat, choose an available local model, send a
   message, and confirm the response is marked exploratory.
5. Open the evidence view and confirm missing, fixture, stale, restricted, and
   blocked evidence are visible and cannot be promoted to a release claim.

## Validation commands

```bash
pytest tests/api tests/workspace tests/contract
ruff check src tests
mypy src
cd frontend && npm run lint && npm run test && npm run build
```

Run browser end-to-end checks against the local API before accepting the feature.

## Validation Record

Implemented validation uses the local FastAPI API, React/Vite production build,
Vitest component checks, and a Playwright Chromium smoke test. On a non-macOS
workstation, an MLX-LM training job must transition to `blocked` with an Apple
Silicon requirement rather than reporting false success.