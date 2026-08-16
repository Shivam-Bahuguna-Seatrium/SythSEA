# Research Workbench

## Local Data Generation

The Data Generation view is the entry point for the SynthSEA research pipeline.
It uses the local Ollama `gpt-oss:20b` model to create candidate instruction
data and records the full agent methodology: resource discovery, topic context,
language profile, instruction generation, language-specialist review,
code-switch control, cultural and semantic validation, diversity checks,
critic, judge, and refinement.

Before starting the workbench on the Mac, ensure the local model is available:

```bash
ollama pull gpt-oss:20b
ollama serve
```

Each run is saved under `reports/workspace/generation/`. Its candidate records
must be reviewed and filtered before governed dataset intake. The subsequent
fine-tuning, baseline and ablation experiments, per-language evaluation, and
evidence checks supply the inputs for the research dossier and paper package;
generated candidate text itself is never a research claim.

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