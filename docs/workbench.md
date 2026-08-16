# SynthSEA Research Workbench

The local workbench is a React client backed by FastAPI. It exposes governed
data intake, MLX-LM fine-tuning jobs, local Ollama chat, artifact lineage, and
report readiness without creating another data or evidence system.

## Start Locally

```bash
source .venv/bin/activate
uvicorn synthsea.api.app:app --reload --port 8000

cd frontend
npm install
npm run dev
```

Open `http://127.0.0.1:5173`. API documentation is at
`http://127.0.0.1:8000/docs`.

## Execution Boundaries

- Dataset intake uses the existing SynthSEA provenance, license, access, and
  language-profile validation.
- Fine-tuning jobs use MLX-LM on Apple Silicon. The API records commands, model
  license, configuration, logs, checkpoints, and memory metadata. On an
  unsupported workstation, the job is visibly blocked.
- Local chat uses Ollama and is always exploratory. It cannot become a dataset,
  experiment input, or report claim until a provenance and access decision is
  explicitly recorded.
- The Evidence view reads readiness blockers from the Feature 003 report package.